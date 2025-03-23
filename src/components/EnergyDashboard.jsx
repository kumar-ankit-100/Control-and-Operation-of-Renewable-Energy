import React, { useState, useEffect } from 'react';
import { FaSolarPanel, FaWind, FaBatteryThreeQuarters, FaBolt, FaChartLine, FaBell, FaCog, FaMapMarkedAlt, FaCheck, FaExclamationTriangle, FaInfoCircle, FaRobot } from 'react-icons/fa';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const EnergyDashboard = () => {
  // Selected state tracking
  const [selectedState, setSelectedState] = useState('Manipur');
  const [selectedRegion, setSelectedRegion] = useState('Northeast');
  
  const handleChatbotClick = () => {
    window.open("http://127.0.0.1:5000/", "_blank"); // Opens the chatbot in a new tab
  };




  // State for energy metrics
  const [energyMetrics, setEnergyMetrics] = useState({
    solar: { current: 28, max: 40, unit: 'kW', efficiency: 70 },
    wind: { current: 15, max: 25, unit: 'kW', efficiency: 60 },
    hydro: { current: 42, max: 50, unit: 'kW', efficiency: 84 },
    battery: { current: 85, max: 100, unit: '%', status: 'Charging' },
    consumption: { current: 34, average: 38, unit: 'kW' },
    grid: { status: 'Connected', load: 75 }
  });

  // State for alerts
  const [alerts, setAlerts] = useState([
    { id: 1, type: 'warning', message: 'Monsoon affecting solar generation in Manipur', time: '10:25 AM' },
    { id: 2, type: 'info', message: 'New hydropower plant operational in Meghalaya', time: '09:45 AM' },
    { id: 3, type: 'success', message: 'Manipur reduces peak consumption by 15%', time: 'Yesterday' }
  ]);

  // Indian states data with focus on Northeast
  const indiaStates = {
    Northeast: ['Manipur', 'Assam', 'Meghalaya', 'Nagaland', 'Tripura', 'Arunachal Pradesh', 'Mizoram', 'Sikkim'],
    North: ['Delhi', 'Haryana', 'Punjab', 'Uttar Pradesh', 'Uttarakhand', 'Himachal Pradesh', 'Jammu & Kashmir'],
    South: ['Tamil Nadu', 'Kerala', 'Karnataka', 'Andhra Pradesh', 'Telangana'],
    West: ['Gujarat', 'Maharashtra', 'Rajasthan', 'Goa'],
    East: ['West Bengal', 'Bihar', 'Jharkhand', 'Odisha'],
    Central: ['Madhya Pradesh', 'Chhattisgarh']
  };

  // Northeast states renewable energy data
  const northeastEnergyData = {
    'Manipur': {
      solar: { current: 28, max: 40, efficiency: 70, potential: 'Medium' },
      wind: { current: 15, max: 25, efficiency: 60, potential: 'Low' },
      hydro: { current: 42, max: 50, efficiency: 84, potential: 'High' },
      biomass: { current: 18, max: 30, efficiency: 60, potential: 'Medium' },
      battery: { current: 85, max: 100, status: 'Charging' },
      initiatives: [
        'Loktak Floating Solar Project - 50MW',
        'Mini-Hydro Projects in Hill Districts',
        'Biomass Power from Rice Husk - Imphal Valley',
        'Solar Rooftop Scheme for Government Buildings'
      ]
    },
    'Assam': {
      solar: { current: 35, max: 45, efficiency: 78, potential: 'Medium' },
      wind: { current: 20, max: 30, efficiency: 67, potential: 'Medium' },
      hydro: { current: 38, max: 60, efficiency: 63, potential: 'High' },
      biomass: { current: 25, max: 35, efficiency: 71, potential: 'High' },
      battery: { current: 75, max: 100, status: 'Discharging' },
      initiatives: [
        'Brahmaputra Floating Solar Project',
        'Tea Garden Solar Integration Program',
        'Biomass Cogeneration in Sugar Mills',
        'Namrup Thermal Power Station Modernization'
      ]
    },
    'Meghalaya': {
      solar: { current: 22, max: 35, efficiency: 63, potential: 'Medium' },
      wind: { current: 10, max: 20, efficiency: 50, potential: 'Low' },
      hydro: { current: 56, max: 65, efficiency: 86, potential: 'Very High' },
      biomass: { current: 15, max: 25, efficiency: 60, potential: 'Medium' },
      battery: { current: 90, max: 100, status: 'Charging' },
      initiatives: [
        'Umiam Hydroelectric Upgrade Project',
        'East Khasi Hills Solar Farm',
        'Community Micro-Hydro Network',
        'Energy Conservation in Limestone Industries'
      ]
    },
    'Nagaland': {
      solar: { current: 18, max: 30, efficiency: 60, potential: 'Medium' },
      wind: { current: 8, max: 15, efficiency: 53, potential: 'Low' },
      hydro: { current: 45, max: 55, efficiency: 82, potential: 'High' },
      biomass: { current: 20, max: 30, efficiency: 67, potential: 'Medium' },
      battery: { current: 80, max: 100, status: 'Charging' },
      initiatives: [
        'Doyang Hydroelectric Power Station Expansion',
        'Kohima Solar City Initiative',
        'Bamboo Biomass Research Project',
        'Rural Electrification through Micro-Hydro'
      ]
    },
    'Tripura': {
      solar: { current: 32, max: 45, efficiency: 71, potential: 'High' },
      wind: { current: 12, max: 20, efficiency: 60, potential: 'Low' },
      hydro: { current: 30, max: 40, efficiency: 75, potential: 'Medium' },
      biomass: { current: 28, max: 35, efficiency: 80, potential: 'High' },
      battery: { current: 65, max: 100, status: 'Charging' },
      initiatives: [
        'Gomati Basin Solar Park',
        'Natural Gas to Power Integration',
        'Dumbur Lake Hydro Renovation',
        'Agartala Smart Grid Project'
      ]
    }
  };

  // Animation effect for energy values
  const [animatedValues, setAnimatedValues] = useState({
    solar: 0,
    wind: 0,
    hydro: 0,
    battery: 0,
    consumption: 0,
    grid: 0
  });

  // Time intervals for updates
  const [timeInterval, setTimeInterval] = useState('day');

  // Language selection
  const [language, setLanguage] = useState('English');
  
  // Weather and local conditions
  const [weather, setWeather] = useState({
    temperature: 28,
    condition: 'Partly Cloudy',
    windSpeed: 12,
    humidity: 65,
    rainfall: 'Light'
  });

  // User interaction mode
  const [interactionMode, setInteractionMode] = useState('Basic'); // Basic, Advanced, Expert

  // State for chatbot popup visibility and language
  const [showChatbotPopup, setShowChatbotPopup] = useState(true);
  const [popupLanguage, setPopupLanguage] = useState('English');

  useEffect(() => {
    // Update energy metrics based on selected state
    if (northeastEnergyData[selectedState]) {
      setEnergyMetrics({
        solar: northeastEnergyData[selectedState].solar,
        wind: northeastEnergyData[selectedState].wind,
        hydro: northeastEnergyData[selectedState].hydro,
        battery: northeastEnergyData[selectedState].battery,
        consumption: { current: 34, average: 38, unit: 'kW' },
        grid: { status: 'Connected', load: 75 }
      });
      
      // Reset animations
      setAnimatedValues({
        solar: 0,
        wind: 0,
        hydro: 0,
        battery: 0,
        consumption: 0,
        grid: 0
      });
    }
  }, [selectedState]);

  useEffect(() => {
    const interval = setInterval(() => {
      setAnimatedValues(prev => {
        const newValues = { ...prev };
        const currentMetrics = northeastEnergyData[selectedState] || energyMetrics;

        if (newValues.solar < currentMetrics.solar.current) newValues.solar += 1;
        if (newValues.wind < currentMetrics.wind.current) newValues.wind += 1;
        if (newValues.hydro < currentMetrics.hydro.current) newValues.hydro += 1;
        if (newValues.battery < currentMetrics.battery.current) newValues.battery += 1;
        if (newValues.consumption < energyMetrics.consumption.current) newValues.consumption += 1;
        if (newValues.grid < energyMetrics.grid.load) newValues.grid += 1;

        return newValues;
      });
    }, 30);

    return () => clearInterval(interval);
  }, [energyMetrics, selectedState]);

  useEffect(() => {
    // Show chatbot popup every 5 minutes
    const interval = setInterval(() => {
      setShowChatbotPopup(true);
    }, 300000); // 300000 ms = 5 minutes

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // Toggle popup language every 30 seconds
    const languageInterval = setInterval(() => {
      setPopupLanguage(prevLanguage => (prevLanguage === 'English' ? 'Hindi' : 'English'));
    }, 30000); // 30000 ms = 30 seconds

    return () => clearInterval(languageInterval);
  }, []);

  const handleClosePopup = () => {
    setShowChatbotPopup(false);
  };

  const getPopupMessage = () => {
    if (popupLanguage === 'Hindi') {
      return '💬 मदद चाहिए? हमारे एआई सहायक से चैट करें!';
    }
    return '💬 Need help? Chat with our AI assistant!';
  };

  // Mock data for energy production graph - adjusted for selected state
  const getEnergyProductionData = () => {
    const baseData = {
      day: [
        { time: '06:00', solar: 5, wind: 8, hydro: 30 },
        { time: '08:00', solar: 15, wind: 10, hydro: 35 },
        { time: '10:00', solar: 25, wind: 12, hydro: 38 },
        { time: '12:00', solar: 32, wind: 15, hydro: 40 },
        { time: '14:00', solar: 28, wind: 18, hydro: 42 },
        { time: '16:00', solar: 20, wind: 15, hydro: 41 },
        { time: '18:00', solar: 10, wind: 12, hydro: 40 },
        { time: '20:00', solar: 2, wind: 8, hydro: 38 }
      ],
      week: [
        { time: 'Mon', solar: 120, wind: 80, hydro: 250 },
        { time: 'Tue', solar: 150, wind: 100, hydro: 260 },
        { time: 'Wed', solar: 200, wind: 120, hydro: 255 },
        { time: 'Thu', solar: 250, wind: 150, hydro: 270 },
        { time: 'Fri', solar: 300, wind: 180, hydro: 280 },
        { time: 'Sat', solar: 350, wind: 200, hydro: 275 },
        { time: 'Sun', solar: 400, wind: 220, hydro: 265 }
      ],
      month: [
        { time: 'Week 1', solar: 500, wind: 400, hydro: 1050 },
        { time: 'Week 2', solar: 600, wind: 450, hydro: 1100 },
        { time: 'Week 3', solar: 700, wind: 500, hydro: 1080 },
        { time: 'Week 4', solar: 800, wind: 550, hydro: 1120 }
      ]
    };

    // Adjust data based on selected state's energy profile
    const stateData = northeastEnergyData[selectedState];
    if (stateData) {
      const solarFactor = stateData.solar.efficiency / 70;
      const windFactor = stateData.wind.efficiency / 60;
      const hydroFactor = stateData.hydro.efficiency / 80;
      
      return {
        day: baseData.day.map(item => ({
          ...item,
          solar: Math.round(item.solar * solarFactor),
          wind: Math.round(item.wind * windFactor),
          hydro: Math.round(item.hydro * hydroFactor)
        })),
        week: baseData.week.map(item => ({
          ...item,
          solar: Math.round(item.solar * solarFactor),
          wind: Math.round(item.wind * windFactor),
          hydro: Math.round(item.hydro * hydroFactor)
        })),
        month: baseData.month.map(item => ({
          ...item,
          solar: Math.round(item.solar * solarFactor),
          wind: Math.round(item.wind * windFactor),
          hydro: Math.round(item.hydro * hydroFactor)
        }))
      };
    }
    
    return baseData;
  };

  // Energy Mix data for pie chart
  const getEnergyMixData = () => {
    const stateData = northeastEnergyData[selectedState];
    if (stateData) {
      return [
        { name: 'Solar', value: stateData.solar.current, color: '#FF9800' },
        { name: 'Wind', value: stateData.wind.current, color: '#03A9F4' },
        { name: 'Hydro', value: stateData.hydro.current, color: '#4CAF50' },
        { name: 'Biomass', value: stateData.biomass.current, color: '#8D6E63' },
        { name: 'Thermal', value: 15, color: '#F44336' } // Fixed thermal value as it's not in original data
      ];
    }
    
    return [
      { name: 'Solar', value: 28, color: '#FF9800' },
      { name: 'Wind', value: 15, color: '#03A9F4' },
      { name: 'Hydro', value: 42, color: '#4CAF50' },
      { name: 'Biomass', value: 18, color: '#8D6E63' },
      { name: 'Thermal', value: 15, color: '#F44336' }
    ];
  };

  // Date formatter
  const formatDate = () => {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return new Date().toLocaleDateString('en-IN', options);
  };

  // Transliterate content based on selected language - simplified implementation
  const translate = (text) => {
    if (language === 'Hindi') {
      const translations = {
        'Energy Dashboard': 'ऊर्जा डैशबोर्ड',
        'Solar Energy': 'सौर ऊर्जा',
        'Wind Energy': 'पवन ऊर्जा',
        'Hydro Energy': 'जल ऊर्जा',
        'Battery Storage': 'बैटरी भंडारण',
        'Energy Consumption': 'ऊर्जा खपत',
        'Energy Production': 'ऊर्जा उत्पादन',
        'Alerts': 'सूचनाएँ',
        'Day': 'दिन',
        'Week': 'सप्ताह',
        'Month': 'महीना',
        'Efficiency': 'दक्षता',
        'Status': 'स्थिति',
        'Charging': 'चार्जिंग',
        'Grid Status': 'ग्रिड स्थिति',
        'Connected': 'जुड़ा हुआ',
        'Energy Mix': 'ऊर्जा मिश्रण',
        'Initiatives': 'पहल',
        'Max': 'अधिकतम',
        'Live': 'लाइव',
        'Temperature': 'तापमान',
        'Wind Speed': 'हवा की गति',
        'Basic': 'बुनियादी',
        'Advanced': 'उन्नत',
        'Expert': 'विशेषज्ञ'
      };
      
      return translations[text] || text;
    }
    
    return text;
  };

  // Get initiative recommendations based on selected state
  const getInitiatives = () => {
    return northeastEnergyData[selectedState]?.initiatives || [];
  };

  return (
    <div className="bg-gradient-to-b from-gray-50 to-gray-100 min-h-screen p-4 md:p-6">
      <div className="container mx-auto">
        {/* Header with State Selection */}
        <div className="bg-white rounded-xl shadow-md p-4 md:p-6 mb-6">
          <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-4">
            <div>
              <h1 className="text-2xl md:text-3xl font-bold text-gray-800 mb-1">{translate('Energy Dashboard')} - {selectedState}</h1>
              <p className="text-gray-600">{formatDate()}</p>
              <div className="flex flex-wrap items-center mt-2">
                <div className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded flex items-center mr-2 mb-2">
                  <span>{translate('Temperature')}: {weather.temperature}°C</span>
                </div>
                <div className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded flex items-center mr-2 mb-2">
                  <span>{translate('Wind Speed')}: {weather.windSpeed} km/h</span>
                </div>
                <div className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded flex items-center mr-2 mb-2">
                  <span>Monsoon Status: {weather.rainfall}</span>
                </div>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row mt-4 lg:mt-0 gap-4">
              {/* Region selector */}
              <div className="relative">
                <select 
                  className="bg-white border border-gray-300 text-gray-700 py-2 px-4 pr-8 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={selectedRegion}
                  onChange={e => setSelectedRegion(e.target.value)}
                >
                  {Object.keys(indiaStates).map(region => (
                    <option key={region} value={region}>{region} India</option>
                  ))}
                </select>
              </div>
              
              {/* State selector */}
              <div className="relative">
                <select 
                  className="bg-white border border-gray-300 text-gray-700 py-2 px-4 pr-8 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={selectedState}
                  onChange={e => setSelectedState(e.target.value)}
                >
                  {indiaStates[selectedRegion].map(state => (
                    <option key={state} value={state}>{state}</option>
                  ))}
                </select>
              </div>
              
              {/* Language selector */}
              <div className="relative">
                <select 
                  className="bg-white border border-gray-300 text-gray-700 py-2 px-4 pr-8 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={language}
                  onChange={e => setLanguage(e.target.value)}
                >
                  <option value="English">English</option>
                  <option value="Hindi">हिंदी</option>
                  <option value="Manipuri">মৈতৈলোন্</option>
                </select>
              </div>
              
              {/* Interaction mode selector */}
              <div className="relative">
                <select 
                  className="bg-blue-600 text-white py-2 px-4 pr-8 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-700"
                  value={interactionMode}
                  onChange={e => setInteractionMode(e.target.value)}
                >
                  <option value="Basic">{translate('Basic')}</option>
                  <option value="Advanced">{translate('Advanced')}</option>
                  <option value="Expert">{translate('Expert')}</option>
                </select>
              </div>
            </div>
          </div>
          
          {/* Interactive India Map with Northeast Focus - Simplified Representation */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mt-4">
            <div className="bg-blue-50 p-4 rounded-lg lg:col-span-1">
              <h3 className="text-lg font-semibold mb-3 text-blue-800">Northeast India Renewable Energy Focus</h3>
              <div className="flex flex-wrap gap-2">
                {indiaStates['Northeast'].map(state => (
                  <button
                    key={state}
                    onClick={() => setSelectedState(state)}
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      selectedState === state 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-white text-gray-700 hover:bg-blue-100'
                    }`}
                  >
                    {state}
                  </button>
                ))}
              </div>
              <div className="mt-4">
                <h4 className="font-medium text-gray-700 mb-2">Renewable Energy Potential</h4>
                <div className="space-y-2">
                  {northeastEnergyData[selectedState] && (
                    <>
                      <div className="flex justify-between items-center">
                        <span className="text-sm">Solar</span>
                        <span className={`text-sm font-medium px-2 py-1 rounded ${
                          northeastEnergyData[selectedState].solar.potential === 'High' 
                            ? 'bg-green-100 text-green-800' 
                            : northeastEnergyData[selectedState].solar.potential === 'Medium'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {northeastEnergyData[selectedState].solar.potential}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm">Wind</span>
                        <span className={`text-sm font-medium px-2 py-1 rounded ${
                          northeastEnergyData[selectedState].wind.potential === 'High' 
                            ? 'bg-green-100 text-green-800' 
                            : northeastEnergyData[selectedState].wind.potential === 'Medium'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {northeastEnergyData[selectedState].wind.potential}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm">Hydro</span>
                        <span className={`text-sm font-medium px-2 py-1 rounded ${
                          northeastEnergyData[selectedState].hydro.potential === 'High' || 
                          northeastEnergyData[selectedState].hydro.potential === 'Very High'
                            ? 'bg-green-100 text-green-800' 
                            : northeastEnergyData[selectedState].hydro.potential === 'Medium'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {northeastEnergyData[selectedState].hydro.potential}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm">Biomass</span>
                        <span className={`text-sm font-medium px-2 py-1 rounded ${
                          northeastEnergyData[selectedState].biomass.potential === 'High' 
                            ? 'bg-green-100 text-green-800' 
                            : northeastEnergyData[selectedState].biomass.potential === 'Medium'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {northeastEnergyData[selectedState].biomass.potential}
                        </span>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
            
            <div className="lg:col-span-2">
              <div className="bg-white rounded-lg p-4 h-full">
                <h3 className="text-lg font-semibold mb-3 text-gray-800">Regional Energy Mix</h3>
                <div className="flex items-center justify-center h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={getEnergyMixData()}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={80}
                        paddingAngle={5}
                        dataKey="value"
                        label={({name, percent}) => `${name} ${(percent * 100).toFixed(0)}%`}
                      >
                        {getEnergyMixData().map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Energy Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6">
          {/* Solar Energy Card */}
          <div className="bg-white rounded-xl shadow-md overflow-hidden transform transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
            <div className="p-4 md:p-6">
              <div className="flex justify-between items-center mb-4">
                <div className="flex items-center">
                  <div className="bg-yellow-100 p-3 rounded-lg">
                    <FaSolarPanel className="text-yellow-500 text-xl" />
                  </div>
                  <h3 className="ml-3 font-semibold text-gray-800">{translate('Solar Energy')}</h3>
                </div>
                <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">{translate('Live')}</span>
              </div>

              <div className="flex items-end mb-2">
                <span className="text-3xl font-bold text-gray-800">{animatedValues.solar}</span>
                <span className="ml-1 text-lg text-gray-600">{energyMetrics.solar.unit}</span>
                <span className="ml-auto text-sm text-green-600">+2.5%</span>
              </div>

              <div className="w-full bg-gray-200 rounded-full h-2.5 mb-1">
                <div
                  className="bg-yellow-500 h-2.5 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${(animatedValues.solar / energyMetrics.solar.max) * 100}%` }}
                ></div>
              </div>

              <div className="flex justify-between mt-2 text-xs text-gray-500">
                <span>0 {energyMetrics.solar.unit}</span>
                <span>{translate('Max')}: {energyMetrics.solar.max} {energyMetrics.solar.unit}</span>
              </div>
            </div>

            <div className="px-6 py-3 bg-gray-50 border-t">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">{translate('Efficiency')}</span>
                <span className="text-sm font-medium text-green-600">{energyMetrics.solar.efficiency}%</span>
              </div>
            </div>
          </div>

          {/* Wind Energy Card */}
          <div className="bg-white rounded-xl shadow-md overflow-hidden transform transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
            <div className="p-4 md:p-6">
              <div className="flex justify-between items-center mb-4">
                <div className="flex items-center">
                  <div className="bg-blue-100 p-3 rounded-lg">
                    <FaWind className="text-blue-500 text-xl" />
                  </div>
                  <h3 className="ml-3 font-semibold text-gray-800">{translate('Wind Energy')}</h3>
                </div>
                <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">{translate('Live')}</span>
              </div>

              <div className="flex items-end mb-2">
                <span className="text-3xl font-bold text-gray-800">{animatedValues.wind}</span>
                <span className="ml-1 text-lg text-gray-600">{energyMetrics.wind.unit}</span>
                <span className="ml-auto text-sm text-green-600">+1.8%</span>
              </div>

              <div className="w-full bg-gray-200 rounded-full h-2.5 mb-1">
                <div
                  className="bg-blue-500 h-2.5 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${(animatedValues.wind / energyMetrics.wind.max) * 100}%` }}
                ></div>
              </div>

              <div className="flex justify-between mt-2 text-xs text-gray-500">
                <span>0 {energyMetrics.wind.unit}</span>
                <span>{translate('Max')}: {energyMetrics.wind.max} {energyMetrics.wind.unit}</span>
              </div>
            </div>

            <div className="px-6 py-3 bg-gray-50 border-t">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">{translate('Efficiency')}</span>
                <span className="text-sm font-medium text-green-600">{energyMetrics.wind.efficiency}%</span>
              </div>
            </div>
          </div>

          {/* Hydro Energy Card */}
          <div className="bg-white rounded-xl shadow-md overflow-hidden transform transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
            <div className="p-4 md:p-6">
              <div className="flex justify-between items-center mb-4">
                <div className="flex items-center">
                  <div className="bg-green-100 p-3 rounded-lg">
                    <FaChartLine className="text-green-500 text-xl" />
                  </div>
                  <h3 className="ml-3 font-semibold text-gray-800">{translate('Hydro Energy')}</h3>
                </div>
                <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">{translate('Live')}</span>
              </div>

              <div className="flex items-end mb-2">
                <span className="text-3xl font-bold text-gray-800">{animatedValues.hydro}</span>
                <span className="ml-1 text-lg text-gray-600">{energyMetrics.hydro.unit}</span>
                <span className="ml-auto text-sm text-green-600">+3.2%</span>
              </div>

              <div className="w-full bg-gray-200 rounded-full h-2.5 mb-1">
                <div
                  className="bg-green-500 h-2.5 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${(animatedValues.hydro / energyMetrics.hydro.max) * 100}%` }}
                ></div>
              </div>

              <div className="flex justify-between mt-2 text-xs text-gray-500">
                <span>0 {energyMetrics.hydro.unit}</span>
                <span>{translate('Max')}: {energyMetrics.hydro.max} {energyMetrics.hydro.unit}</span>
              </div>
            </div>

            <div className="px-6 py-3 bg-gray-50 border-t">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">{translate('Efficiency')}</span>
                <span className="text-sm font-medium text-green-600">{energyMetrics.hydro.efficiency}%</span>
              </div>
            </div>
          </div>

          {/* Battery Storage Card */}
          <div className="bg-white rounded-xl shadow-md overflow-hidden transform transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
            <div className="p-4 md:p-6">
              <div className="flex justify-between items-center mb-4">
                <div className="flex items-center">
                  <div className="bg-green-100 p-3 rounded-lg">
                    <FaBatteryThreeQuarters className="text-green-500 text-xl" />
                  </div>
                  <h3 className="ml-3 font-semibold text-gray-800">{translate('Battery Storage')}</h3>
                </div>
                <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">{translate('Live')}</span>
              </div>

              <div className="flex items-end mb-2">
                <span className="text-3xl font-bold text-gray-800">{animatedValues.battery}</span>
                <span className="ml-1 text-lg text-gray-600">{energyMetrics.battery.unit}</span>
                <span className="ml-auto text-sm text-green-600">{translate('Charging')}</span>
              </div>

              <div className="w-full bg-gray-200 rounded-full h-2.5 mb-1">
                <div
                  className="bg-green-500 h-2.5 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${animatedValues.battery}%` }}
                ></div>
              </div>

              <div className="flex justify-between mt-2 text-xs text-gray-500">
                <span>0 {energyMetrics.battery.unit}</span>
                <span>{translate('Max')}: {energyMetrics.battery.max} {energyMetrics.battery.unit}</span>
              </div>
            </div>

            <div className="px-6 py-3 bg-gray-50 border-t">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">{translate('Status')}</span>
                <span className="text-sm font-medium text-green-600">{energyMetrics.battery.status}</span>
              </div>
            </div>
          </div>

          {/* Energy Consumption Card */}
          <div className="bg-white rounded-xl shadow-md overflow-hidden transform transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
            <div className="p-4 md:p-6">
              <div className="flex justify-between items-center mb-4">
                <div className="flex items-center">
                  <div className="bg-red-100 p-3 rounded-lg">
                    <FaBolt className="text-red-500 text-xl" />
                  </div>
                  <h3 className="ml-3 font-semibold text-gray-800">{translate('Energy Consumption')}</h3>
                </div>
                <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">{translate('Live')}</span>
              </div>

              <div className="flex items-end mb-2">
                <span className="text-3xl font-bold text-gray-800">{animatedValues.consumption}</span>
                <span className="ml-1 text-lg text-gray-600">{energyMetrics.consumption.unit}</span>
                <span className="ml-auto text-sm text-green-600">-1.2%</span>
              </div>

              <div className="w-full bg-gray-200 rounded-full h-2.5 mb-1">
                <div
                  className="bg-red-500 h-2.5 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${(animatedValues.consumption / energyMetrics.consumption.average) * 100}%` }}
                ></div>
              </div>

              <div className="flex justify-between mt-2 text-xs text-gray-500">
                <span>0 {energyMetrics.consumption.unit}</span>
                <span>{translate('Avg')}: {energyMetrics.consumption.average} {energyMetrics.consumption.unit}</span>
              </div>
            </div>

            <div className="px-6 py-3 bg-gray-50 border-t">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">{translate('Grid Status')}</span>
                <span className="text-sm font-medium text-green-600">{energyMetrics.grid.status}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Alerts Section */}
        <div className="bg-white rounded-xl shadow-md p-4 md:p-6 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-semibold text-gray-800">{translate('Alerts')}</h3>
            <button className="text-gray-600 hover:text-gray-800">
              <FaBell />
            </button>
          </div>

          <div className="space-y-4">
            {alerts.map(alert => (
              <div key={alert.id} className={`p-4 rounded-lg shadow-md flex items-center ${alert.type === 'warning' ? 'bg-yellow-100' : alert.type === 'info' ? 'bg-blue-100' : 'bg-green-100'}`}>
                <div className={`p-2 rounded-lg ${alert.type === 'warning' ? 'bg-yellow-500' : alert.type === 'info' ? 'bg-blue-500' : 'bg-green-500'}`}>
                  {alert.type === 'warning' ? <FaExclamationTriangle className="text-white" /> : alert.type === 'info' ? <FaInfoCircle className="text-white" /> : <FaCheck className="text-white" />}
                </div>
                <div className="ml-4">
                  <p className="font-semibold text-gray-800">{alert.message}</p>
                  <p className="text-xs text-gray-600">{alert.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Energy Production Graph */}
        <div className="bg-white rounded-xl shadow-md p-4 md:p-6">
          <h3 className="font-semibold text-gray-800 mb-4">{translate('Energy Production')}</h3>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={getEnergyProductionData()[timeInterval]}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="solar" stroke="#FFBB28" activeDot={{ r: 8 }} />
              <Line type="monotone" dataKey="wind" stroke="#00C49F" />
              <Line type="monotone" dataKey="hydro" stroke="#4CAF50" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Chatbot Helper */}
        <div className="fixed bottom-4 right-4">
        <button
          onClick={handleChatbotClick}
          className="bg-blue-600 text-white p-6 rounded-full shadow-lg hover:bg-blue-700 focus:outline-none transition-transform transform hover:scale-110"
        >
          <FaRobot className="text-3xl" />
        </button>
      </div>


        {/* Chatbot Popup */}
        {showChatbotPopup && (
          <div className="fixed bottom-20 right-4 bg-blue-600 text-white p-4 rounded-lg shadow-lg border border-blue-700 animate-bounce">
            <div className="flex justify-between items-center">
              <p className="text-lg font-semibold">{getPopupMessage()}</p>
              <button onClick={handleClosePopup} className="text-white hover:text-gray-300">
                &times;
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EnergyDashboard;