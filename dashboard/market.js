async function loadMarkets() {
  const res = await fetch('../data/markets.json');
  const data = await res.json();

  const selector = document.getElementById('zipSelector');

  data.markets.forEach(market => {
    if (!market.enabled) return;

    const option = document.createElement('option');
    option.value = market.zip;
    option.textContent = `${market.zip} – ${market.city}`;
    selector.appendChild(option);
  });

  selector.addEventListener('change', () => {
    loadMarketData(selector.value);
  });

  loadMarketData(data.markets[0].zip);
}

async function loadMarketData(zip) {
  const path = `../data/houston-county-ga/${zip}/processed/market.json`;
  const res = await fetch(path);
  const data = await res.json();

  document.getElementById('marketSummary').textContent =
    `${data.city} (${data.zip}) · Updated ${data.updated}`;

  renderCards(data);
  renderTalkingPoints(data);
}

function renderCards(data) {
  document.getElementById('inventoryCard').innerHTML = `
    <h3>Inventory</h3>
    <p>Active: ${data.inventory.active}</p>
    <p>Change: ${data.inventory.change_pct}%</p>
  `;

  document.getElementById('pricingCard').innerHTML = `
    <h3>Pricing</h3>
    <p>Median List: $${data.pricing.median_list.toLocaleString()}</p>
    <p>Trend: ${data.pricing.trend}</p>
  `;

  document.getElementById('velocityCard').innerHTML = `
    <h3>Market Velocity</h3>
    <p>Avg DOM: ${data.velocity.avg_dom}</p>
    <p>Absorption: ${data.velocity.absorption_rate}</p>
  `;
}

function renderTalkingPoints(data) {
  const points = [];

  if (data.inventory.change_pct > 0)
    points.push(`Inventory increased ${data.inventory.change_pct}% this week.`);

  if (data.velocity.dom_change > 0)
    points.push(`Homes are taking ${data.velocity.dom_change} days longer to sell.`);

  if (data.pricing.trend === 'cooling')
    points.push(`Pricing momentum is cooling in this ZIP code.`);

  const ul = document.getElementById('talkingPoints');
  ul.innerHTML = '';
  points.forEach(p => {
    const li = document.createElement('li');
    li.textContent = p;
    ul.appendChild(li);
  });
}

loadMarkets();
