// pages/my-items.js
"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

export default function MyItems() {
  const [lostItems, setLostItems] = useState([]);
  const [foundItems, setFoundItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }

    const fetchItems = async () => {
      try {
        const config = {
          headers: {
            Authorization: `Bearer ${token}`, // Make sure "Bearer" prefix is included
            "Content-Type": "application/json",
          },
        };

        const [lostResponse, foundResponse] = await Promise.all([
          axios.get("http://localhost:5000/my-lost-items/", config),
          axios.get("http://localhost:5000/my-found-items/", config),
        ]);

        setLostItems(lostResponse.data);
        setFoundItems(foundResponse.data);
        setLoading(false);
      } catch (err) {
        setError(err.response?.data?.error || "An error occurred");
        setLoading(false);
        if (err.response?.status === 401) {
          localStorage.removeItem("token");
          router.push("/login");
        }
      }
    };

    fetchItems();
  }, [router]);

  const handleDelete = async (id, type) => {
    try {
      const token = localStorage.getItem("token");
      await axios.delete(`http://localhost:5000/${type}-items/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (type === "lost") {
        setLostItems((items) => items.filter((item) => item.id !== id));
      } else {
        setFoundItems((items) => items.filter((item) => item.id !== id));
      }
    } catch (err) {
      alert("Error deleting item");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 p-8">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-2xl font-bold mb-4">Loading...</h1>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 p-8">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-2xl font-bold mb-4 text-red-600">{error}</h1>
        </div>
      </div>
    );
  }

  const ItemCard = ({ item, type }) => (
    <div className="bg-white rounded-lg shadow-md p-6 mb-4">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-xl font-semibold mb-2">{item.name}</h3>
          <p className="text-gray-600 mb-2">{item.description}</p>
          <p className="text-sm text-gray-500">Location: {item.location}</p>
          <p className="text-sm text-gray-500">
            Date: {type === "lost" ? item.date_lost : item.date_found}
          </p>
          <p className="text-sm text-gray-500">Contact: {item.contact_info}</p>
        </div>
        {item.image && (
          <img
            src={item.image}
            alt={item.name}
            className="w-32 h-32 object-cover rounded-lg ml-4"
          />
        )}
      </div>
      <button
        onClick={() => handleDelete(item.id, type)}
        className="mt-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
      >
        Delete
      </button>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">My Items</h1>

        <div className="grid md:grid-cols-2 gap-8">
          <div>
            <h2 className="text-2xl font-semibold mb-4">Lost Items</h2>
            {lostItems.length === 0 ? (
              <p className="text-gray-500">No lost items reported</p>
            ) : (
              lostItems.map((item) => (
                <ItemCard key={item.id} item={item} type="lost" />
              ))
            )}
          </div>

          <div>
            <h2 className="text-2xl font-semibold mb-4">Found Items</h2>
            {foundItems.length === 0 ? (
              <p className="text-gray-500">No found items reported</p>
            ) : (
              foundItems.map((item) => (
                <ItemCard key={item.id} item={item} type="found" />
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
