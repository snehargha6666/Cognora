import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const searchQuery = async (query) => {
  const res = await API.post("/search", { query });
  return res.data;
};