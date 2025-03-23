import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';

const data = [
  { name: 'Jan', load: 4000, capacity: 2400 },
  { name: 'Feb', load: 3000, capacity: 1398 },
  { name: 'Mar', load: 2000, capacity: 9800 },
  { name: 'Apr', load: 2780, capacity: 3908 },
  { name: 'May', load: 1890, capacity: 4800 },
  { name: 'Jun', load: 2390, capacity: 3800 },
  { name: 'Jul', load: 3490, capacity: 4300 },
];

const OperatorDashboard = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">Operator Dashboard</h1>
      <p className="text-gray-700 mb-8">
        Welcome to your dashboard. Here you can monitor grid load, manage energy distribution, and ensure grid stability.
      </p>
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-bold mb-4">Grid Load vs Capacity</h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="load" fill="#8884d8" />
            <Bar dataKey="capacity" fill="#82ca9d" />
          </BarChart>
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

export default OperatorDashboard;
