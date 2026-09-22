"""Generate fictional vehicle cards for extraction pairing and missing-data tests."""
import json


def build():
    cards = []
    for index, (price, miles) in enumerate(((12000, 10000), (18000, 2000)), 1):
        cards.append({'vin': f'1HGCM82633A{index:06d}', 'year': 2024,
                      'make': 'Acme', 'model': 'Example SUV', 'trim': 'Test',
                      'price': price, 'mileage': miles, 'seller': {'dealerName': f'Acme Motors {index}'},
                      'stockType': 'used', 'url': f'https://example.com/vehicledetail/{index}'})
    data = {'synthetic': True, 'cards': cards,
            'json_ld': {'@type': 'Car', 'name': 'Acme Example SUV',
                        'vehicleIdentificationNumber': '1HGCM82633A000003',
                        'mileageFromOdometer': {'value': 1000, 'unitCode': 'KMT'},
                        'offers': {'price': 15000, 'priceCurrency': 'USD',
                                   'seller': {'name': 'Acme Motors'},
                                   'url': 'https://example.com/vehicle/3'}}}
    return {'eval/fixtures/inventory.json': (json.dumps(data, indent=2) + '\n').encode('utf-8')}
