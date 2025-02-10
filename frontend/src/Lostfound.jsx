import React, { useState } from "react";

const LostFoundApp = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    name: "",
    description: "",
    location: "",
    dateLost: "",
    contactInfo: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    const response = await fetch("http://localhost:5000/users/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: formData.username,
        password: formData.password,
      }),
    });
    const data = await response.json();
    console.log(data);
  };

  const handleLostItem = async (e) => {
    e.preventDefault();
    const response = await fetch("http://localhost:5000/lost-items/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: formData.name,
        description: formData.description,
        location: formData.location,
        date_lost: formData.dateLost,
        contact_info: formData.contactInfo,
      }),
    });
    const data = await response.json();
    console.log(data);
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold text-center mb-6">Lost & Found</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white shadow-lg rounded-lg p-6">
          <h2 className="text-2xl font-semibold mb-4">Register</h2>
          <form onSubmit={handleRegister} className="space-y-4">
            <input
              type="text"
              name="username"
              placeholder="Username"
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            />
            <button
              type="submit"
              className="bg-blue-500 text-white px-4 py-2 rounded"
            >
              Register
            </button>
          </form>
        </div>
        <div className="bg-white shadow-lg rounded-lg p-6">
          <h2 className="text-2xl font-semibold mb-4">Report Lost Item</h2>
          <form onSubmit={handleLostItem} className="space-y-4">
            <input
              type="text"
              name="name"
              placeholder="Item Name"
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            />
            <textarea
              name="description"
              placeholder="Description"
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            ></textarea>
            <input
              type="text"
              name="location"
              placeholder="Location"
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            />
            <input
              type="date"
              name="dateLost"
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            />
            <input
              type="text"
              name="contactInfo"
              placeholder="Contact Info"
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            />
            <button
              type="submit"
              className="bg-red-500 text-white px-4 py-2 rounded"
            >
              Report Lost Item
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LostFoundApp;
