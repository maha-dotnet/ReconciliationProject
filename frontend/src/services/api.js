import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const uploadCSV = async (system, file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post(
    `/upload/${system}/`,
    formData
  );

  return response.data;
};

export const reconcileRecords = async () => {
  const response = await api.post("/reconcile/");
  return response.data;
};

export const getResults = async () => {
  const response = await api.get("/results/");
  return response.data;
};

export const getDashboard = async () => {
  const response = await api.get("/dashboard/");
  return response.data;
};

export default api;