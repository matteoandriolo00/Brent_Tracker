const API_URL = "http://127.0.0.1:8000";

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let detail = "Errore nella richiesta";
    try {
      const data = await response.json();
      detail = Array.isArray(data.detail)
        ? data.detail.map((item) => item.msg).join(", ")
        : data.detail || detail;
    } catch {
      // Ignore invalid JSON errors
    }
    throw new Error(detail);
  }

  if (response.status === 204) return null;
  return response.json();
}

export const api = {
  register: (data) =>
    request("/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  login: (data) =>
    request("/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  getCurrentPrice: () => request("/prices/current"),

  getHistory: () => request("/prices/history"),

  getAlerts: (userId) => request(`/alerts/${userId}`),

  createAlert: (data) =>
    request("/alerts/", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  updateAlertStatus: (alertId, status) =>
    request(`/alerts/${alertId}/status`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    }),

  deleteAlert: (alertId) =>
    request(`/alerts/${alertId}`, {
      method: "DELETE",
    }),

  deleteUser: (username) =>
    request(`/delete_user?username=${encodeURIComponent(username)}`, {
      method: "DELETE",
    }),
};