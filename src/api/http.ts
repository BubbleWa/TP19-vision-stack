// src/api/http.ts
import axios from "axios";

const http = axios.create({
  baseURL: "https://cybermate.onrender.com", 
  timeout: 10000, 
});

export default http;
