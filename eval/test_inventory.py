"""Exercise the shipped browser extractor against generated DOM-shaped records."""
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/orchestrator/scripts/extract_inventory.js'
DRIVER = r'''
const fs = require('node:fs');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
global.location = {href: 'https://www.cars.com/inventory', hostname: 'www.cars.com'};
global.document = {title: 'Synthetic inventory', querySelectorAll: selector => {
  if (selector.startsWith('fuse-card')) return (input.cards || []).map(item => ({
    getAttribute: () => typeof item === 'string' ? item : JSON.stringify(item),
    querySelector: () => item.url ? {href: item.url} : null,
  }));
  return (input.scripts || []).map(textContent => ({textContent}));
}};
const extractor = eval('(' + fs.readFileSync(process.argv[1], 'utf8') + ')');
extractor({evaluate: async fn => fn()}).then(result => process.stdout.write(JSON.stringify(result)));
'''


@unittest.skipUnless(shutil.which('node'), 'Node is needed for the JavaScript extractor test')
class InventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads((ROOT / 'eval/fixtures/inventory.json').read_text(encoding='utf-8'))

    def extract(self, payload):
        result = subprocess.run(['node', '-e', DRIVER, str(SCRIPT)], input=json.dumps(payload),
                                capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    def test_connected_cards_preserve_price_identity_and_partial_coverage(self):
        result = self.extract({'cards': self.fixture['cards']})
        self.assertEqual(result['complete_records'], 2)
        self.assertEqual(result['status'], 'partial')
        self.assertEqual([(x['vin'], x['asking_price']) for x in result['records']],
                         [(x['vin'], x['price']) for x in self.fixture['cards']])

    def test_unknown_units_and_missing_dealer_are_not_invented(self):
        result = self.extract({'scripts': [json.dumps(self.fixture['json_ld'])]})
        self.assertIsNone(result['records'][0]['mileage'])
        self.assertIn('mileage', result['records'][0]['missing'])
        payload = json.loads(json.dumps(self.fixture['cards']))
        payload[0]['seller'] = None
        payload[0]['price'] = 0
        result = self.extract({'cards': payload})
        self.assertIn('dealer', result['records'][0]['missing'])
        self.assertIn('asking_price', result['records'][0]['missing'])

    def test_malformed_and_empty_pages_do_not_pass(self):
        result = self.extract({'cards': ['{bad'], 'scripts': ['{bad']})
        self.assertEqual(result['status'], 'no_records')
        self.assertEqual(result['errors'], ['malformed_vehicle_card', 'malformed_json_ld'])

    def test_blank_mileage_and_unconfirmed_currency_are_incomplete(self):
        payload = json.loads(json.dumps(self.fixture['cards']))
        payload[0]['mileage'] = '  '
        payload[0]['seller'] = {'dealerName': '  '}
        result = self.extract({'cards': payload})
        self.assertIsNone(result['records'][0]['mileage'])
        self.assertIsNone(result['records'][0]['dealer'])
        for currency in ('EUR', None):
            item = json.loads(json.dumps(self.fixture['json_ld']))
            item['mileageFromOdometer'] = {'value': 1000, 'unitCode': 'SMI'}
            item['offers']['priceCurrency'] = currency
            result = self.extract({'scripts': [json.dumps(item)]})
            self.assertEqual(result['complete_records'], 0)
            self.assertIn('usd_currency', result['records'][0]['missing'])


if __name__ == '__main__':
    unittest.main()
