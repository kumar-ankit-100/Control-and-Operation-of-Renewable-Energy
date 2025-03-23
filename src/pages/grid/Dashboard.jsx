import React, { useState, useEffect } from 'react';
import { FaExclamationTriangle, FaCheck, FaInfoCircle, FaChartLine, FaSun, FaWind, FaBolt, FaDatabase } from 'react-icons/fa';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';

import DashboardCard from '../../components/DashboardCard';
import AlertBox from '../../components/AlertBox';
import LoadingSpinner from '../../components/LoadingSpinner';
import { getGridStats, getPowerGenerationData, getGridAlerts } from '../../services/gridService';

const GridDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [generationData, setGenerationData] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [forecastData, setForecastData] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState('all');

  // Fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // In a real app, these would be API calls to your backend
        const statsData = await getGridStats(selectedRegion);
        const powerData = await getPowerGenerationData(selectedRegion);
        const alertsData = await getGridAlerts(selectedRegion);
        
        setStats(statsData);
        setGenerationData(powerData.current);
        setForecastData(powerData.forecast);
        setAlerts(alertsData);
      } catch (error) {
        console.error('Error fetching grid data:', error);
        // Show error notification
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
    
    // Set up an interval to refresh data every 5 minutes
    const interval = setInterval(fetchData, 300000);
    
    return () => clearInterval(interval);
  }, [selectedRegion]);

  // Simulated data for demo purposes
  const simulatedStats = {
    totalProduction: 15842,
    solarProduction: 8427,
    windProduction: 5321,
    hydroProduction: 2094,
    gridLoad: 14320,
    gridCapacity: 22000,
    storageLevel: 68,
    carbonSaved: 12450
  };

  const simulatedGenerationData = [
    { time: '00:00', solar: 0, wind: 3200, hydro: 1800, conventional: 9000, demand: 13500 },
    { time: '03:00', solar: 0, wind: 3800, hydro: 1750, conventional: 8900, demand: 13200 },
    { time: '06:00', solar: 1200, wind: 3600, hydro: 1800, conventional: 8500, demand: 13800 },
    { time: '09:00', solar: 5800, wind: 2800, hydro: 1900, conventional: 5500, demand: 14500 },
    { time: '12:00', solar: 8200, wind: 2200, hydro: 2000, conventional: 3000, demand: 14800 },
    { time: '15:00', solar: 7500, wind: 2400, hydro: 2100, conventional: 3200, demand: 15000 },
    { time: '18:00', solar: 4200, wind: 3200, hydro: 2000, conventional: 5800, demand: 15200 },
    { time: '21:00', solar: 500, wind: 3500, hydro: 1900, conventional: 8200, demand: 14000 },
  ];

  const simulatedAlerts = [
    { id: 1, type: 'warning', message: 'Wind farm output dropping in Western grid section', time: '15 mins ago' },
    { id: 2, type: 'success', message: 'Battery storage optimized in Northern region', time: '32 mins ago' },
    { id: 3, type: 'info', message: 'Solar generation exceeding forecast by 15% in Southern region', time: '1 hour ago' },
    { id: 4, type: 'danger', message: 'Grid congestion detected in Delhi-NCR transmission line', time: '2 hours ago' },
  ];

  const regions = [
    { id: 'all', name: 'All India' },
    { id: 'north', name: 'Northern Region' },
    { id: 'west', name: 'Western Region' },
    { id: 'south', name: 'Southern Region' },
    { id: 'east', name: 'Eastern Region' },
    { id: 'northeast', name: 'North-Eastern Region' },
  ];

  // For demo purposes, we'll use the simulated data
  const displayStats = stats || simulatedStats;
  const displayGenerationData = generationData.length ? generationData : simulatedGenerationData;
  const displayAlerts = alerts.length ? alerts : simulatedAlerts;

  const handleRegionChange = (e) => {
    setSelectedRegion(e.target.value);
  };

  if (loading && !displayStats) {
    return <LoadingSpinner />;
  }

  return (
    <div className="grid-dashboard">
      <div className="mb-8 flex flex-col md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Grid Control Dashboard</h1>
          <p className="text-gray-600">Real-time monitoring and control of renewable energy grid operations</p>
        </div>
        <div className="mt-4 md:mt-0">
          <select 
            value={selectedRegion}
            onChange={handleRegionChange}
            className="bg-white border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {regions.map(region => (
              <option key={region.id} value={region.id}>{region.name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Key Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <DashboardCard 
          title="Total Generation" 
          value={`${displayStats.totalProduction.toLocaleString()} MW`} 
          icon={<FaBolt />} 
          color="blue"
          subtitle="Current power output"
        />
        <DashboardCard 
          title="Grid Load" 
          value={`${displayStats.gridLoad.toLocaleString()} MW`} 
          icon={<FaChartLine />} 
          color="purple"
          subtitle={`${Math.round((displayStats.gridLoad/displayStats.gridCapacity)*100)}% of capacity`}
        />
        <DashboardCard 
          title="Storage Level" 
          value={`${displayStats.storageLevel}%`} 
          icon={<FaDatabase />} 
          color="green"
          subtitle="Available energy storage"
        />
        <DashboardCard 
          title="Carbon Saved" 
          value={`${displayStats.carbonSaved.toLocaleString()} tons`} 
          icon={<FaCheck />} 
          color="teal"
          subtitle="Compared to conventional"
        />
      </div>

      {/* Energy Mix */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6 col-span-2">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Energy Generation Mix</h2>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={displayGenerationData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis label={{ value: 'Power (MW)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Area type="monotone" dataKey="solar" stackId="1" stroke="#FFB800" fill="#FFB800" />
              <Area type="monotone" dataKey="wind" stackId="1" stroke="#00C6FF" fill="#00C6FF" />
              <Area type="monotone" dataKey="hydro" stackId="1" stroke="#0072FF" fill="#0072FF" />
              <Area type="monotone" dataKey="conventional" stackId="1" stroke="#777777" fill="#777777" />
              <Line type="monotone" dataKey="demand" stroke="#FF0000" dot={false} strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Current Energy Sources</h2>
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center">
                <div className="w-4 h-4 rounded-full bg-yellow-500 mr-2"></div>
                <span>Solar</span>
              </div>
              <span className="font-bold">{displayStats.solarProduction.toLocaleString()} MW</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-yellow-500 h-2 rounded-full" style={{ width: `${Math.round((displayStats.solarProduction/displayStats.totalProduction)*100)}%` }}></div>
            </div>
          </div>
          
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center">
                <div className="w-4 h-4 rounded-full bg-blue-400 mr-2"></div>
                <span>Wind</span>
              </div>
              <span className="font-bold">{displayStats.windProduction.toLocaleString()} MW</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-blue-400 h-2 rounded-full" style={{ width: `${Math.round((displayStats.windProduction/displayStats.totalProduction)*100)}%` }}></div>
            </div>
          </div>
          
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center">
                <div className="w-4 h-4 rounded-full bg-blue-600 mr-2"></div>
                <span>Hydro</span>
              </div>
              <span className="font-bold">{displayStats.hydroProduction.toLocaleString()} MW</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${Math.round((displayStats.hydroProduction/displayStats.totalProduction)*100)}%` }}></div>
            </div>
          </div>
          
          <div className="text-center mt-6">
            <button className="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition duration-300">
              View Detailed Breakdown
            </button>
          </div>
        </div>
      </div>

      {/* Alerts and Forecasting */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Recent Alerts</h2>
          <div className="space-y-4">
            {displayAlerts.map(alert => (
              <AlertBox
                key={alert.id}
                type={alert.type}
                message={alert.message}
                time={alert.time}
              />
            ))}
          </div>
          <div className="text-center mt-6">
            <button className="bg-gray-100 text-gray-800 py-2 px-4 rounded-md hover:bg-gray-200 transition duration-300">
              View All Alerts
            </button>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold mb-4 text-gray-800">24-Hour Forecast</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div className="bg-blue-50 rounded-lg p-4 flex flex-col items-center">
              <FaSun className="text-yellow-500 text-3xl mb-2" />
              <h3 className="font-bold text-lg">Solar Forecast</h3>
              <p className="text-2xl font-bold text-blue-600">8.2 GW</p>
              <p className="text-sm text-gray-600">Peak at 12:30 PM</p>
            </div>
            
            <div className="bg-blue-50 rounded-lg p-4 flex flex-col items-center">
              <FaWind className="text-blue-500 text-3xl mb-2" />
              <h3 className="font-bold text-lg">Wind Forecast</h3>
              <p className="text-2xl font-bold text-blue-600">4.7 GW</p>
              <p className="text-sm text-gray-600">Peak at 7:00 PM</p>
            </div>
          </div>
          
          <ResponsiveContainer width="100%" height={200}>
            <LineChart
              data={[
                { time: '00:00', forecast: 12500 },
                { time: '04:00', forecast: 11800 },
                { time: '08:00', forecast: 13200 }
              ]}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="forecast" stroke="#8884d8" activeDot={{ r: 8 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default GridDashboard;