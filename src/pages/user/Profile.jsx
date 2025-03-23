import React from 'react';

// URL for the profile image
const ProfileImage = 'https://example.com/path-to-your-profile-image.jpg';

const UserProfile = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">User Profile</h1>
      <div className="flex items-center mb-8">
        <img src={ProfileImage} alt="User Profile" className="w-24 h-24 rounded-full mr-4" />
        <div>
          <h2 className="text-xl font-bold">John Doe</h2>
          <p className="text-gray-700">john.doe@example.com</p>
        </div>
      </div>
      <p className="text-gray-700">
        Manage your profile information and settings here.
      </p>
    </div>
  );
};

export default UserProfile;
