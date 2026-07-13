// ============================================================
// api.js — fetch wrapper that auto-attaches JWT, handles 401s
// ============================================================
const API_BASE = "/api";

async function apiRequest(path, { method = "GET", body, isFormData = false } = {}) {
  const token = localStorage.getItem("iq_token");
  const headers = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (!isFormData && body !== undefined) headers["Content-Type"] = "application/json";

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: isFormData ? body : body !== undefined ? JSON.stringify(body) : undefined,
  });

  let data = null;
  try {
    data = await res.json();
  } catch {
    data = null;
  }

  if (res.status === 401) {
    localStorage.removeItem("iq_token");
    localStorage.removeItem("iq_user");
    if (!window.location.pathname.startsWith("/login")) {
      window.location.href = "/login";
    }
  }

  if (!res.ok) {
    const err = new Error((data && data.message) || `Request failed with status ${res.status}`);
    err.status = res.status;
    err.data = data;
    throw err;
  }

  return data;
}

const api = {
  get: (path) => apiRequest(path, { method: "GET" }),
  post: (path, body, opts = {}) => apiRequest(path, { method: "POST", body, ...opts }),
  put: (path, body) => apiRequest(path, { method: "PUT", body }),
  del: (path) => apiRequest(path, { method: "DELETE" }),
};
