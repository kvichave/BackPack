// pages/report.js
"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import Nav from "@/components/Nav";

export default function Report() {
  const [itemData, setItemData] = useState({
    name: "",
    description: "",
    location: "",
    date_lost: "",
    date_found: "",
    contact_info: "",
  });
  const [type, setType] = useState("lost");
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState("");
  const router = useRouter();

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const endpoint = type === "lost" ? "lost-items" : "found-items";

    const formData = new FormData();
    Object.keys(itemData).forEach((key) => {
      if (itemData[key]) formData.append(key, itemData[key]);
    });
    if (image) formData.append("image", image);

    try {
      const res = await fetch(`http://localhost:5000/${endpoint}/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!res.ok) {
        const error = await res.json();
        alert(error.message || "Error submitting item");
        return;
      }

      router.push("/");
    } catch (error) {
      alert("Error submitting item");
    }
  };

  return (
    <>
      <Nav></Nav>
      <div className="min-h-screen flex items-center justify-center p-4">
        <form
          onSubmit={handleSubmit}
          className="bg-white p-8 rounded shadow-md w-full max-w-md"
        >
          <h2 className="text-2xl text-black font-bold mb-6">
            Report {type === "lost" ? "Lost" : "Found"} Item
          </h2>

          <div className="mb-4">
            <select
              className="w-full p-2 text-black border rounded"
              value={type}
              onChange={(e) => setType(e.target.value)}
            >
              <option value="lost">Lost Item</option>
              <option value="found">Found Item</option>
            </select>
          </div>

          <div className="mb-4">
            <input
              required
              type="text"
              placeholder="Item Name"
              className="w-full text-black p-2 border rounded"
              onChange={(e) =>
                setItemData({ ...itemData, name: e.target.value })
              }
            />
          </div>

          <div className="mb-4">
            <textarea
              required
              placeholder="Description"
              className="w-full text-black p-2 border rounded"
              onChange={(e) =>
                setItemData({ ...itemData, description: e.target.value })
              }
            />
          </div>

          <div className="mb-4">
            <input
              required
              type="text"
              placeholder="Location"
              className="w-full text-black p-2 border rounded"
              onChange={(e) =>
                setItemData({ ...itemData, location: e.target.value })
              }
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-400 mb-1">
              Date {type === "lost" ? "Lost" : "Found"}
            </label>
            <input
              required
              type="date"
              className="w-full text-black p-2 border rounded"
              onChange={(e) =>
                setItemData({
                  ...itemData,
                  [type === "lost" ? "date_lost" : "date_found"]:
                    e.target.value,
                })
              }
            />
          </div>

          <div className="mb-4">
            <input
              required
              type="text"
              placeholder="Contact Information"
              className="w-full text-black p-2 border rounded"
              onChange={(e) =>
                setItemData({ ...itemData, contact_info: e.target.value })
              }
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-400 mb-2">Upload Image</label>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              className="w-full p-2 border rounded"
            />
            {preview && (
              <div className="mt-2 relative h-48 w-full">
                <Image
                  src={preview}
                  alt="Preview"
                  fill
                  className="object-contain"
                />
              </div>
            )}
          </div>

          <button
            type="submit"
            className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
          >
            Submit Report
          </button>
        </form>
      </div>
    </>
  );
}
