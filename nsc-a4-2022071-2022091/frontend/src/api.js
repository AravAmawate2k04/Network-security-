// src/api.js
import axios from "axios";

export const client = axios.create({
  baseURL: "http://localhost:4000/api",  // <-- full URL
  withCredentials: true
});

export const signup   = data => client.post("/signup", data);
export const login    = data => client.post("/login", data);
export const download = type => client.get(`/download/${type}`, { responseType: "blob" });
