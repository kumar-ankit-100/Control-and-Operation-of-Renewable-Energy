import React from 'react';

// URL for the contact image
const ContactImage = 'https://example.com/path-to-your-contact-image.jpg';

const Contact = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">Contact Us</h1>
      <div className="flex items-center mb-8">
        <img src={ContactImage} alt="Contact Us" className="w-24 h-24 rounded-full mr-4" />
        <div>
          <h2 className="text-xl font-bold">Get in Touch</h2>
          <p className="text-gray-700">We'd love to hear from you!</p>
        </div>
      </div>
      <form className="space-y-4">
        <div>
          <label className="block text-gray-700">Name</label>
          <input type="text" className="w-full px-4 py-2 border rounded-md" />
        </div>
        <div>
          <label className="block text-gray-700">Email</label>
          <input type="email" className="w-full px-4 py-2 border rounded-md" />
        </div>
        <div>
          <label className="block text-gray-700">Message</label>
          <textarea className="w-full px-4 py-2 border rounded-md"></textarea>
        </div>
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">Send</button>
      </form>
    </div>
  );
};

export default Contact;
