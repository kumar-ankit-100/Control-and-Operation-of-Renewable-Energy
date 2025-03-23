import React from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

// URL for the government dashboard image
const GovDashboardImage = 'https://example.com/path-to-your-gov-dashboard-image.jpg';

const data = [
  { name: 'Solar', value: 400 },
  { name: 'Wind', value: 300 },
  { name: 'Hydro', value: 300 },
  { name: 'Conventional', value: 200 },
];

const COLORS = ['#FFBB28', '#FF8042', '#00C49F', '#0088FE'];

const GovDashboard = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">Government Dashboard</h1>
      <p className="text-gray-700 mb-8">
        Welcome to the government dashboard. Here you can manage policies, incentives, and view regional analytics.
      </p>
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <img src={GovDashboardImage} alt="Government Dashboard" className="w-full h-auto rounded mb-4" />
        <h2 className="text-xl font-bold mb-4">Energy Source Distribution</h2>
        <ResponsiveContainer width="100%" height={400}>
          <PieChart>
            <Pie data={data} cx="50%" cy="50%" outerRadius={150} fill="#8884d8" dataKey="value" label>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default GovDashboard;
