// pages/index.js
"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function Home() {
  const [lostItems, setLostItems] = useState([]);
  const [foundItems, setFoundItems] = useState([]);
  const [location, setLocation] = useState("");
  const router = useRouter();
  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") : null;

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async (locationFilter = "") => {
    const lostUrl = locationFilter
      ? `http://localhost:5000/nearby-lost-items?location=${encodeURIComponent(
          locationFilter
        )}`
      : "http://localhost:5000/lost-items/";

    const [lostRes, foundRes] = await Promise.all([
      fetch(lostUrl),
      fetch("http://localhost:5000/found-items/"),
    ]);

    const [lostData, foundData] = await Promise.all([
      lostRes.json(),
      foundRes.json(),
    ]);

    setLostItems(lostData);
    setFoundItems(foundData);
  };

  const handleLocationFilter = async (e) => {
    e.preventDefault();
    await fetchItems(location);
  };

  return (
    <div className="container mx-auto p-4">
      <nav className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold">Lost & Found</h1>
        <div>
          {!token ? (
            <>
              <Link href="/login" className="mr-4 text-blue-500">
                Login
              </Link>
              <Link href="/register" className="text-blue-500">
                Register
              </Link>
            </>
          ) : (
            <>
              <Link href="/report" className="mr-4 text-blue-500">
                Report Item
              </Link>
              <button
                onClick={() => {
                  localStorage.removeItem("token");
                  router.push("/login");
                }}
                className="text-red-500"
              >
                Logout
              </button>
            </>
          )}
        </div>
      </nav>

      <form onSubmit={handleLocationFilter} className="mb-8">
        <div className="flex gap-4">
          <input
            type="text"
            placeholder="Enter city or address..."
            className="flex-1 p-2 border rounded"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded"
          >
            Filter
          </button>
          <button
            type="button"
            onClick={() => {
              setLocation("");
              fetchItems();
            }}
            className="bg-gray-500 text-white px-4 py-2 rounded"
          >
            Show All
          </button>
        </div>
      </form>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <h2 className="text-xl font-semibold mb-4">Lost Items</h2>
          <div className="space-y-4">
            {lostItems.map((item) => (
              <div key={item.id} className="border p-4 rounded">
                <h3 className="font-bold">{item.name}</h3>
                <p>{item.description}</p>
                <p>Location: {item.location}</p>
                <p>Date Lost: {item.date_lost}</p>
                <p>Contact: {item.contact_info}</p>
                <img src={item.image}></img>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-4">Found Items</h2>
          <div className="space-y-4">
            {foundItems.map((item) => (
              <div key={item.id} className="border p-4 rounded">
                <h3 className="font-bold">{item.name}</h3>
                <p>{item.description}</p>
                <p>Location: {item.location}</p>
                <p>Date Found: {item.date_found}</p>
                <p>Contact: {item.contact_info}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// pages/report.js - Location input section update
const LocationInput = ({ value, onChange }) => (
  <div className="mb-4">
    <input
      required
      type="text"
      placeholder="Enter address or city"
      className="w-full p-2 border rounded"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    />
    <p className="text-sm text-gray-500 mt-1">
      Enter a city, street address, or landmark
    </p>
  </div>
);
