import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  const [location, setLocation] = useState('Imphal,Manipur  ');
  const [greeting, setGreeting] = useState('');

  // useEffect(() => {
  //   if (navigator.geolocation) {
  //     navigator.geolocation.getCurrentPosition((position) => {
  //       const { latitude, longitude } = position.coords;
  //       fetch(`https://geocode.xyz/${latitude},${longitude}?geoit=json`)
  //         .then(response => response.json())
  //         .then(data => {
  //           setLocation(`${Imphal}, ${India}`);
  //           if (data.city === 'Imphal' && data.country === 'India') {
  //             setGreeting('Welcome to Renewable Energy Management, Imphal!');
  //           }
  //         })
  //         .catch(error => console.error('Error fetching location:', error));
  //     });
  //   }
  // }, []);

  return (
    <nav className="bg-gray-800 text-white py-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold">Renewable Energy Management</Link>
        <div className="space-x-4">
          <Link to="/" className="hover:text-gray-400">Home</Link>
          <Link to="/about" className="hover:text-gray-400">About</Link>
          <Link to="/contact" className="hover:text-gray-400">Contact</Link>
          <Link to="/login" className="hover:text-gray-400">Login</Link>
          <Link to="/register" className="hover:text-gray-400">Register</Link>
        </div>
        <div className="text-sm text-gray-400">
          {location ? `Current Location: ${location}` : 'Fetching location...'}
        </div>
      </div>
      {greeting && <div className="text-center text-yellow-500 mt-2">{greeting}</div>}
    </nav>
  );
};

export default Navbar;
