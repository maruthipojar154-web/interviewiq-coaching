// ============================================================
// auth.js — login state stored in localStorage, shared helpers
// ============================================================
const Auth = {
  getToken() {
    return localStorage.getItem("iq_token");
  },
  getUser() {
    const raw = localStorage.getItem("iq_user");
    return raw ? JSON.parse(raw) : null;
  },
  login(token, user) {
    localStorage.setItem("iq_token", token);
    localStorage.setItem("iq_user", JSON.stringify(user));
  },
  logout() {
    localStorage.removeItem("iq_token");
    localStorage.removeItem("iq_user");
    // Clear any cached app data (profile/projects/sessions) tied to the old account.
    sessionStorage.removeItem("iq_chat_history");
    sessionStorage.removeItem("iq_chat_messages");
  },
  isLoggedIn() {
    return Boolean(this.getToken());
  },
  /** Call at the top of any protected page. Redirects to /login if not authenticated. */
  async requireAuth() {
    if (!this.isLoggedIn()) {
      window.location.href = "/login";
      return null;
    }
    try {
      const res = await api.get("/auth/me");
      localStorage.setItem("iq_user", JSON.stringify(res.user));
      return res.user;
    } catch {
      this.logout();
      window.location.href = "/login";
      return null;
    }
  },
  /** Call at the top of login/register pages. Redirects to /dashboard if already logged in. */
  redirectIfLoggedIn() {
    if (this.isLoggedIn()) {
      window.location.href = "/dashboard";
    }
  },
};
