import React from 'react';
import PropTypes from 'prop-types';
import { FaExclamationTriangle, FaCheck, FaInfoCircle, FaTimes } from 'react-icons/fa';

const AlertBox = ({ type, message, time }) => {
  const getIcon = () => {
    switch (type) {
      case 'warning':
        return <FaExclamationTriangle className="text-yellow-500" />;
      case 'success':
        return <FaCheck className="text-green-500" />;
      case 'info':
        return <FaInfoCircle className="text-blue-500" />;
      case 'danger':
        return <FaTimes className="text-red-500" />;
      default:
        return null;
    }
  };

  return (
    <div className={`alert-box alert-${type} p-4 rounded-lg shadow-md flex items-center`}>
      <div className="icon mr-4">
        {getIcon()}
      </div>
      <div className="message flex-1">
        <p className="font-bold">{message}</p>
        <p className="text-sm text-gray-600">{time}</p>
      </div>
    </div>
  );
};

AlertBox.propTypes = {
  type: PropTypes.string.isRequired,
  message: PropTypes.string.isRequired,
  time: PropTypes.string.isRequired,
};

export default AlertBox;
