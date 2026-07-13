// ============================================================
// layout.js — renders the sidebar + mobile topbar shell.
// Call renderAppShell(activePage) at the top of each protected page.
// ============================================================
const NAV_ITEMS = [
  { href: "/dashboard", icon: "🏠", label: "Dashboard", key: "dashboard" },
  { href: "/profile", icon: "👤", label: "My Profile", key: "profile" },
  { href: "/resume", icon: "📄", label: "Resume & Docs", key: "resume" },
  { href: "/projects", icon: "🛠️", label: "My Projects", key: "projects" },
  { href: "/chatbot", icon: "🤖", label: "Chat with AI", key: "chatbot" },
  { href: "/analytics", icon: "📊", label: "Analytics", key: "analytics" },
  { href: "/voice-bot", icon: "🎙️", label: "Voice AI Bot", key: "voice-bot" },
  { href: "/chat-history", icon: "🕐", label: "Chat History", key: "chat-history" },
];

function computeCompletion(user, profile, projects) {
  const skills = (profile && profile.skills) || [];
  const checks = [
    user && user.name,
    profile && profile.role,
    user && user.email,
    profile && profile.photo_path,
    profile && (profile.resume_text || profile.resume_path),
    skills.length > 0,
    (projects || []).length > 0,
    profile && profile.summary,
  ];
  const done = checks.filter(Boolean).length;
  return Math.round((done / checks.length) * 100);
}

async function renderAppShell(activePage) {
  const user = await Auth.requireAuth();
  if (!user) return null; // already redirected

  let profile = null;
  let projects = [];
  try {
    const [profileRes, projectsRes] = await Promise.all([
      api.get("/profile"),
      api.get("/projects"),
    ]);
    profile = profileRes.profile;
    projects = projectsRes.projects;
  } catch (e) {
    console.error("Failed to load profile/projects for shell:", e);
  }

  const completion = computeCompletion(user, profile, projects);
  const photoUrl = profile && profile.photo_path ? profile.photo_path : null;
  const progColor = completion === 100 ? "#34D399" : "#6366F1";

  const navHtml = NAV_ITEMS.map(
    (n) => `
    <a href="${n.href}" class="nav-item ${n.key === activePage ? "active" : ""}">
      <span class="nav-icon">${n.icon}</span>${n.label}
    </a>`
  ).join("");

  const shellHtml = `
    <div class="sidebar-overlay" id="sidebarOverlay"></div>
    <div class="sidebar" id="sidebar">
      <div class="sb-logo">
        <div class="sb-logo-icon">🎯</div>
        <div class="sb-logo-name">Interview<span class="sb-logo-sub">IQ</span></div>
      </div>
      <div class="sb-profile">
        <div class="sb-av-wrap">
          <div class="sb-av">${photoUrl ? `<img src="${photoUrl}" alt="" />` : "👤"}</div>
        </div>
        <div class="sb-name">${escapeHtml(user.name || "Your Name")}</div>
        <div class="sb-role">${escapeHtml(profile && profile.role ? profile.role : "Add your role →")}</div>
        <div class="sb-online"><div class="online-dot"></div><div class="online-txt">Ready to prep</div></div>
      </div>
      <div class="sb-nav">
        <div class="nav-section">Navigation</div>
        ${navHtml}
      </div>
      <div class="sb-footer">
        <div class="prog-row"><span>Profile complete</span><span style="color:${progColor}">${completion}%</span></div>
        <div class="prog-bar"><div class="prog-fill" style="width:${completion}%;background:${progColor}"></div></div>
        <button class="btn btn-g sb-logout" id="logoutBtn">Log out</button>
      </div>
    </div>
    <div class="main-area">
      <div class="mobile-topbar">
        <button class="hamburger" id="hamburgerBtn">☰</button>
        <div class="mobile-topbar-title">Interview<span style="color:#818CF8">IQ</span></div>
      </div>
      <div id="pageContent"></div>
    </div>
  `;

  document.getElementById("appRoot").innerHTML = shellHtml;

  document.getElementById("logoutBtn").addEventListener("click", () => {
    Auth.logout();
    window.location.href = "/login";
  });

  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("sidebarOverlay");
  document.getElementById("hamburgerBtn").addEventListener("click", () => {
    sidebar.classList.add("open");
    overlay.classList.add("show");
  });
  overlay.addEventListener("click", () => {
    sidebar.classList.remove("open");
    overlay.classList.remove("show");
  });

  return { user, profile, projects };
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str == null ? "" : String(str);
  return div.innerHTML;
}
