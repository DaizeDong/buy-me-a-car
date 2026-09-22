async (page) => {
  // Read-only extraction. Store the returned records only in verified private DATA.
  return await page.evaluate(() => {
    const records = [];
    const errors = [];
    const text = value => ['string', 'number'].includes(typeof value) ? String(value).trim() || null : null;
    const url = value => {
      if (!value) return null;
      try {
        const parsed = new URL(value, location.href);
        return ['https:', 'http:'].includes(parsed.protocol) ? parsed.href : null;
      } catch { return null; }
    };
    const number = value => {
      if (!['number', 'string'].includes(typeof value) || String(value).trim() === '') return null;
      const numeric = Number(String(value).replaceAll(',', ''));
      return Number.isFinite(numeric) && numeric >= 0 ? numeric : null;
    };
    const vin = value => /^[A-HJ-NPR-Z0-9]{17}$/.test(String(value).toUpperCase()) ? String(value).toUpperCase() : null;
    const add = record => {
      record.missing = ['vin', 'vehicle', 'asking_price', 'mileage', 'dealer', 'url'].filter(key => record[key] === null || record[key] === '' || (key === 'asking_price' && record[key] === 0));
      if (record.currency !== 'USD') record.missing.push('usd_currency');
      records.push(record);
    };
    // Values come from one connected card, never parallel global VIN/price arrays.
    for (const card of document.querySelectorAll('fuse-card[data-vehicle-details]')) {
      let item;
      try { item = JSON.parse(card.getAttribute('data-vehicle-details')); }
      catch { errors.push('malformed_vehicle_card'); continue; }
      if (!item || typeof item !== 'object') { errors.push('invalid_vehicle_card'); continue; }
      const link = card.querySelector('a[href*="/vehicledetail/"]');
      const seller = item.seller;
      add({
        source_format: 'cars_vehicle_card', vin: vin(item.vin),
        vehicle: [item.year, item.make, item.model, item.trim].filter(Boolean).join(' '),
        asking_price: number(item.price), mileage: number(item.mileage),
        dealer: text(typeof seller === 'string' ? seller : seller?.dealerName || seller?.name),
        stock_type: text(item.stockType), url: link ? url(link.href) : null,
        currency: location.hostname === 'www.cars.com' || location.hostname === 'cars.com' ? 'USD' : null,
        source_record: item,
      });
    }
    if (!records.length) {
      const visit = node => {
        if (!node || typeof node !== 'object') return;
        if (Array.isArray(node)) { node.forEach(visit); return; }
        const types = Array.isArray(node['@type']) ? node['@type'] : [node['@type']];
        if (types.some(type => ['Car', 'Vehicle'].includes(type))) {
          const offer = Array.isArray(node.offers) ? node.offers[0] : node.offers;
          const seller = offer?.seller || node.seller;
          const distance = node.mileageFromOdometer;
          const unit = distance?.unitCode || distance?.unitText;
          add({
            source_format: 'json_ld', vin: vin(node.vehicleIdentificationNumber),
            vehicle: text(node.name), asking_price: number(offer?.price),
            mileage: ['SMI', 'MI', 'MILE', 'MILES'].includes(String(unit).toUpperCase()) ? number(distance?.value) : null,
            dealer: text(typeof seller === 'string' ? seller : seller?.name),
            stock_type: text(node.itemCondition), url: url(node.url || offer?.url),
            currency: text(offer?.priceCurrency)?.trim().toUpperCase() || null, source_record: node,
          });
        } else Object.values(node).forEach(visit);
      };
      for (const script of document.querySelectorAll('script[type="application/ld+json"]')) {
        try { visit(JSON.parse(script.textContent)); }
        catch { errors.push('malformed_json_ld'); }
      }
    }
    return {
      schema_version: 1, observed_at: new Date().toISOString(),
      source_url: location.href, title: document.title,
      status: records.length ? 'partial' : 'no_records',
      coverage: 'one rendered page; pagination and current seller availability not verified',
      complete_records: records.filter(record => !record.missing.length).length,
      unique_vins: new Set(records.map(record => record.vin).filter(Boolean)).size,
      errors, records,
    };
  });
}
