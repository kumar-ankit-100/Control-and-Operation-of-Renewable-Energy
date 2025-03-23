import React from 'react';
import PropTypes from 'prop-types';

const DashboardCard = ({ title, value, icon, color, subtitle }) => {
  return (
    <div className={`bg-${color}-50 p-6 rounded-lg shadow-md`}>
      <div className="flex items-center justify-between mb-4">
        <div className={`text-${color}-600 text-3xl`}>
          {icon}
        </div>
        <div className="text-right">
          <h3 className="text-xl font-bold text-gray-800">{title}</h3>
          <p className="text-2xl font-bold text-gray-800">{value}</p>
          <p className="text-sm text-gray-600">{subtitle}</p>
        </div>
      </div>
    </div>
  );
};

DashboardCard.propTypes = {
  title: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
  icon: PropTypes.element.isRequired,
  color: PropTypes.string.isRequired,
  subtitle: PropTypes.string,
};

export default DashboardCard;
