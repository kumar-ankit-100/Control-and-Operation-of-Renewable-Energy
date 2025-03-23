import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FaSolarPanel, FaWind, FaChartLine, FaUserShield, FaGlobe, FaBolt, FaCog, FaInfoCircle, FaSun } from 'react-icons/fa';
import EnergyDashboard from '../components/EnergyDashboard';

const EnergyLandingPage = () => {
  const [activeTab, setActiveTab] = useState('solar');
  const [energyData, setEnergyData] = useState({
    solar: { current: 65, max: 100, unit: 'kW' },
    wind: { current: 42, max: 75, unit: 'kW' },
    battery: { current: 85, max: 100, unit: '%' },
    grid: { current: 72, max: 100, unit: '%' }
  });
  
  // Animation effect for counters
  const [animatedValues, setAnimatedValues] = useState({
    solar: 0,
    wind: 0,
    battery: 0,
    grid: 0
  });
  
  useEffect(() => {
    const interval = setInterval(() => {
      setAnimatedValues(prev => {
        const newValues = {...prev};
        
        Object.keys(energyData).forEach(key => {
          if (newValues[key] < energyData[key].current) {
            newValues[key] += 1;
          }
        });
        
        return newValues;
      });
    }, 30);
    
    return () => clearInterval(interval);
  }, [energyData]);

  // Stats data
  const stats = [
    { id: 1, number: '175 GW', label: 'Renewable Capacity Target', icon: <FaChartLine className="text-blue-500" /> },
    { id: 2, number: '40%', label: 'Share of Renewables Goal', icon: <FaSolarPanel className="text-yellow-500" /> },
    { id: 3, number: '₹250,000 Cr', label: 'Clean Energy Investment', icon: <FaGlobe className="text-green-500" /> },
    { id: 4, number: '1M+', label: 'Renewable Sector Jobs', icon: <FaUserShield className="text-purple-500" /> },
  ];

  // Features data
  const features = [
    {
      id: 1,
      title: 'AI-Powered Energy Forecasting',
      description: 'Real-time prediction of solar & wind power generation using advanced ML models and weather APIs',
      icon: <FaChartLine className="text-green-600 text-4xl mb-4" />,
      link: 'http://192.168.231.246:8501/',
    },
    {
      id: 2,
      title: 'Battery Health Management',
      description: 'Monitor battery health and capacity in real-time with predictive maintenance recommendations',
      icon: <FaBolt className="text-yellow-500 text-4xl mb-4" />,
      link: 'http://192.168.231.246:8501/',
    },
    {
      id: 3,
      title: 'Grid Monitoring & Control',
      description: 'Real-time monitoring and dynamic power allocation to prevent overloads and ensure grid stability',
      icon: <FaGlobe className="text-blue-500 text-4xl mb-4" />,
      link: 'http://192.168.231.246:8501/',
    },
    {
      id: 4,
      title: 'Smart Energy Utilization',
      description: 'Intelligent scheduling of energy usage during peak renewable generation with personalized recommendations',
      icon: <FaUserShield className="text-purple-500 text-4xl mb-4" />,
      link: 'http://192.168.231.246:8501/',
    },
    {
      id: 5,
      title: 'Advanced India Solar Power Calculator',
      description: 'Estimate solar power generation potential based on location, panel efficiency, and real-time weather data',
      icon: <FaSun className="text-orange-500 text-4xl mb-4" />,
      link: 'http://localhost:8501',
    }
    ,
    {
      id: 6,
      title: 'Advanced Wind Energy Forecasting',
      description: 'Predict wind energy generation using real-time weather data, turbine specifications, and AI-based modeling.',
      icon: <FaWind className="text-blue-500 text-4xl mb-4" />,
      link: 'http://localhost:8501', // Change this to the actual URL where your wind forecasting app runs
    }
  ];

  // Energy sources tabs
  const energySources = [
    { id: 'solar', label: 'Solar', icon: <FaSolarPanel className="mr-2" />, color: 'yellow' },
    { id: 'wind', label: 'Wind', icon: <FaWind className="mr-2" />, color: 'blue' },
    { id: 'battery', label: 'Battery', icon: <FaBolt className="mr-2" />, color: 'green' },
    { id: 'grid', label: 'Grid', icon: <FaGlobe className="mr-2" />, color: 'purple' },
  ];

  // Mock data for energy source visualization
  const getSourceContent = (source) => {
    const data = energyData[source];
    const colorClass = source === 'solar' ? 'bg-yellow-500' : 
                       source === 'wind' ? 'bg-blue-500' : 
                       source === 'battery' ? 'bg-green-500' : 'bg-purple-500';
                       
    return (
      <div className="flex flex-col items-center">
        <div className="relative w-64 h-64 mb-8">
          <div className="absolute inset-0 rounded-full border-8 border-gray-200"></div>
          <div 
            className={`absolute top-0 left-0 bottom-0 right-0 rounded-full border-8 ${colorClass} transition-all duration-1000`}
            style={{ 
              clipPath: `polygon(50% 50%, 0 0, ${animatedValues[source] * 3.6}deg 0)`,
              transform: 'rotate(-90deg)'
            }}
          ></div>
          <div className="absolute inset-0 flex items-center justify-center flex-col">
            <span className="text-4xl font-bold">{animatedValues[source]}{data.unit}</span>
            <span className="text-gray-500">of {data.max}{data.unit}</span>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4 w-full">
          <div className="bg-white p-4 rounded-lg shadow-md">
            <h4 className="text-lg font-semibold mb-2">Efficiency</h4>
            <p className="text-2xl font-bold text-green-600">{Math.floor((animatedValues[source] / data.max) * 100)}%</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-md">
            <h4 className="text-lg font-semibold mb-2">Status</h4>
            <p className="text-2xl font-bold text-green-600">Active</p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-r from-green-600 to-blue-700 text-white">
        <div className="container mx-auto px-6 pt-32 pb-24">
          <div className="flex flex-col md:flex-row items-center">
            <div className="md:w-1/2 mb-12 md:mb-0">
              <h1 className="text-5xl md:text-6xl font-bold leading-tight mb-6">
                Smart Renewable
                <span className="block text-yellow-300">Energy Management</span>
              </h1>
              <p className="text-xl mb-10 max-w-lg">
                Empowering India's green energy transition with AI-driven forecasting, 
                smart grid management, and integrated energy solutions.
              </p>
              <div className="flex flex-wrap gap-4">
                <Link to="/register" className="bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-bold py-4 px-8 rounded-full transition duration-300 transform hover:scale-105">
                  Get Started
                </Link>
                <Link to="/about" className="bg-transparent border-2 border-white hover:bg-white hover:text-blue-600 text-white font-bold py-4 px-8 rounded-full transition duration-300 transform hover:scale-105">
                  Learn More
                </Link>
                
              </div>
            </div>
            <div className="md:w-1/2">
              {/* Interactive Energy Monitor Section */}
              <div className="bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg p-6 rounded-xl shadow-xl">
                <h3 className="text-2xl font-bold mb-6 text-center">Live Energy Monitor</h3>
                
                {/* Tabs for different energy sources */}
                <div className="flex mb-8 bg-gray-800 bg-opacity-30 rounded-lg p-1">
                  {energySources.map(source => (
                    <button
                      key={source.id}
                      onClick={() => setActiveTab(source.id)}
                      className={`flex items-center justify-center py-2 px-4 rounded-lg flex-1 transition-all duration-300 ${
                        activeTab === source.id 
                          ? `bg-${source.color}-500 text-white font-medium` 
                          : 'text-white hover:bg-white hover:bg-opacity-10'
                      }`}
                    >
                      {source.icon}
                      {source.label}
                    </button>
                  ))}
                </div>
                
                {/* Content for selected energy source */}
                <div className="p-4">
                  {getSourceContent(activeTab)}
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Wave separator */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 160">
            <path fill="#f9fafb" fillOpacity="1" d="M0,128L48,117.3C96,107,192,85,288,90.7C384,96,480,128,576,138.7C672,149,768,139,864,122.7C960,107,1056,85,1152,80C1248,75,1344,85,1392,90.7L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
          </svg>
        </div>
      </div>

      {/* Features Section */}
      <div className="container mx-auto px-6 py-24">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">Our Renewable Energy Solutions</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Cutting-edge technologies to optimize energy production, storage, and consumption
            for a sustainable future.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature) => (
            <div 
              key={feature.id} 
              className="bg-white rounded-xl shadow-lg p-8 transition-all duration-300 hover:shadow-xl hover:transform hover:-translate-y-2"
            >
              <div className="flex justify-center mb-4">
                {feature.icon}
              </div>
              <h3 className="text-2xl font-bold mb-3 text-center text-gray-800">{feature.title}</h3>
              <p className="text-gray-600 mb-6 text-center">{feature.description}</p>
              <div className="text-center">
                <Link to={feature.link} className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition-all duration-300">
                  Explore
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* Stats Section */}
      <div className="bg-gray-900 text-white py-24">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">India's Renewable Energy Targets</h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Ambitious goals to reduce carbon footprint and create a sustainable energy future
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat) => (
              <div 
                key={stat.id} 
                className="bg-gray-800 rounded-xl p-8 text-center transform transition-all duration-500 hover:bg-gray-700"
              >
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-600 mb-6">
                  {stat.icon}
                </div>
                <h3 className="text-3xl font-bold mb-2">{stat.number}</h3>
                <p className="text-gray-400">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      {/* Interactive Dashboard Preview */}
      <div className="container mx-auto px-6 py-24">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">Interactive Dashboards</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Real-time monitoring and control interfaces for different stakeholders
          </p>
        </div>
        
        <div className="bg-white rounded-xl shadow-xl overflow-hidden mb-16">
          <div className="flex border-b border-gray-200">
            <div className="px-6 py-4 border-r border-gray-200 bg-gray-50">
              <h3 className="text-lg font-semibold text-gray-800">User Dashboard</h3>
            </div>
            <div className="px-6 py-4 border-r border-gray-200">
              <h3 className="text-lg font-semibold text-gray-500">Producer Dashboard</h3>
            </div>
            <div className="px-6 py-4 border-r border-gray-200">
              <h3 className="text-lg font-semibold text-gray-500">Grid Dashboard</h3>
            </div>
            <div className="px-6 py-4">
              <h3 className="text-lg font-semibold text-gray-500">Government Dashboard</h3>
            </div>
          </div>
          
          <div className="p-8">
            <EnergyDashboard />
          </div>
        </div>
      </div>
      
      {/* Call to Action */}
      <div className="bg-gradient-to-r from-green-600 to-blue-700 text-white py-16">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold mb-6">Join India's Renewable Energy Revolution</h2>
          <p className="text-xl mb-10 max-w-3xl mx-auto">
            Whether you're a consumer, producer, or government entity, our platform helps you contribute 
            to India's sustainable future.
          </p>
          <div className="flex flex-wrap justify-center gap-6">
            <Link to="/register" className="bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-bold py-4 px-10 rounded-full transition duration-300 transform hover:scale-105">
              Sign Up Now
            </Link>
            <Link to="/contact" className="bg-transparent border-2 border-white hover:bg-white hover:text-blue-600 text-white font-bold py-4 px-10 rounded-full transition duration-300 transform hover:scale-105">
              Contact Us
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnergyLandingPage;