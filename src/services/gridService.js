export const getGridStats = async (region) => {
  // Simulated API call to fetch grid stats
  return {
    totalProduction: 15842,
    solarProduction: 8427,
    windProduction: 5321,
    hydroProduction: 2094,
    gridLoad: 14320,
    gridCapacity: 22000,
    storageLevel: 68,
    carbonSaved: 12450
  };
};

export const getPowerGenerationData = async (region) => {
  // Simulated API call to fetch power generation data
  return {
    current: [
      { time: '00:00', solar: 0, wind: 3200, hydro: 1800, conventional: 9000, demand: 13500 },
      { time: '03:00', solar: 0, wind: 3800, hydro: 1750, conventional: 8900, demand: 13200 },
      { time: '06:00', solar: 1200, wind: 3600, hydro: 1800, conventional: 8500, demand: 13800 },
      { time: '09:00', solar: 5800, wind: 2800, hydro: 1900, conventional: 5500, demand: 14500 },
      { time: '12:00', solar: 8200, wind: 2200, hydro: 2000, conventional: 3000, demand: 14800 },
      { time: '15:00', solar: 7500, wind: 2400, hydro: 2100, conventional: 3200, demand: 15000 },
      { time: '18:00', solar: 4200, wind: 3200, hydro: 2000, conventional: 5800, demand: 15200 },
      { time: '21:00', solar: 500, wind: 3500, hydro: 1900, conventional: 8200, demand: 14000 },
    ],
    forecast: [
      { time: '00:00', forecast: 12500 },
      { time: '04:00', forecast: 11800 },
      { time: '08:00', forecast: 13200 }
    ]
  };
};

export const getGridAlerts = async (region) => {
  // Simulated API call to fetch grid alerts
  return [
    { id: 1, type: 'warning', message: 'Wind farm output dropping in Western grid section', time: '15 mins ago' },
    { id: 2, type: 'success', message: 'Battery storage optimized in Northern region', time: '32 mins ago' },
    { id: 3, type: 'info', message: 'Solar generation exceeding forecast by 15% in Southern region', time: '1 hour ago' },
    { id: 4, type: 'danger', message: 'Grid congestion detected in Delhi-NCR transmission line', time: '2 hours ago' },
  ];
};
