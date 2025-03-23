  import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const PrivateRoute = ({ userType }) => {
  const { user } = useAuth();

  if (!user || user.type !== userType) {
    return <Navigate to="/login" />;
  }

  return <Outlet />;
};

export default PrivateRoute;
