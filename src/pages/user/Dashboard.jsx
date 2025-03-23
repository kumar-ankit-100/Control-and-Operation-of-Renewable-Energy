import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';

const data = [
  { name: 'Jan', consumption: 4000, production: 2400 },
  { name: 'Feb', consumption: 3000, production: 1398 },
  { name: 'Mar', consumption: 2000, production: 9800 },
  { name: 'Apr', consumption: 2780, production: 3908 },
  { name: 'May', consumption: 1890, production: 4800 },
  { name: 'Jun', consumption: 2390, production: 3800 },
  { name: 'Jul', consumption: 3490, production: 4300 },
];

const UserDashboard = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">User Dashboard</h1>
      <p className="text-gray-700 mb-8">
        Welcome to your dashboard. Here you can monitor your energy consumption, manage your smart devices, and get tips on how to optimize your energy usage.
      </p>
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-bold mb-4">Energy Consumption vs Production</h2>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="consumption" stroke="#8884d8" activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="production" stroke="#82ca9d" />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className="relative h-96">
        <Canvas>
          <OrbitControls />
          <Stars />
          <ambientLight intensity={0.5} />
          <directionalLight position={[10, 10, 5]} intensity={1} />
          <mesh>
            <boxGeometry args={[3, 3, 3]} />
            <meshStandardMaterial color="orange" />
          </mesh>
        </Canvas>
      </div>
    </div>
  );
};

export default UserDashboard;
