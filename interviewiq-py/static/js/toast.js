// ============================================================
// toast.js — small popup notification
// ============================================================
function showToast(message, type = "success") {
  const existing = document.querySelector(".toast");
  if (existing) existing.remove();

  const el = document.createElement("div");
  el.className = `toast ${type === "error" ? "error" : ""}`;
  el.textContent = message;
  document.body.appendChild(el);

  setTimeout(() => el.remove(), 2800);
}
