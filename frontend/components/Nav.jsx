"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function Nav() {
  const router = useRouter();
  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") : null;
  console.log("tokennn", token);
  return (
    <div className="container mx-auto p-4">
      <nav className="flex justify-between items-center mb-8">
        <button onClick={() => router.push("/")} className="text-2xl font-bold">
          Lost & Found
        </button>
        <div>
          {!token ? (
            <>
              <button href="/login" className="mr-4 text-blue-500">
                Login
              </button>
              <button href="/register" className="text-blue-500">
                Register
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => router.push("/report")}
                className="mr-4 text-blue-500"
              >
                Report Item
              </button>
              <button
                onClick={() => router.push("/my-items")}
                className="mr-4 text-blue-500"
              >
                My Items
              </button>
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
    </div>
  );
}
