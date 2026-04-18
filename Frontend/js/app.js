// OffGrid Platform - Core App Logic

// ── TOAST NOTIFICATIONS ──────────────────────────────────────────────
function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<span>${icons[type] || '✅'}</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// ── ACTIVE NAV LINK ──────────────────────────────────────────────────
function setActiveNavLink() {
  const currentPage = window.location.pathname.split('/').pop();
  document.querySelectorAll('.navbar-links a, .dash-nav-item').forEach(link => {
    const href = link.getAttribute('href');
    if (href && href.split('?')[0] === currentPage) {
      link.classList.add('active');
    }
  });
}

// ── NOTIFICATION BADGE ───────────────────────────────────────────────
function initNotifBadge() {
  const badge = document.getElementById('notif-badge');
  if (badge && window.OffGridData) {
    const unread = OffGridData.notifications.filter(n => !n.read).length;
    if (unread > 0) {
      badge.textContent = unread;
      badge.style.display = 'flex';
    }
  }
}

// ── SMOOTH SCROLL TO TOP ON LOAD ─────────────────────────────────────
window.scrollTo({ top: 0 });

// ── INTERSECTION OBSERVER FOR FADE-IN ───────────────────────────────
function initFadeIn() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
}

// ── URL PARAMS ───────────────────────────────────────────────────────
function getParam(key) {
  return new URLSearchParams(window.location.search).get(key);
}

// ── FORMAT DATE ──────────────────────────────────────────────────────
function formatDate(dateStr) {
  if (!dateStr || dateStr === 'TBD') return dateStr;
  try {
    return new Date(dateStr).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
  } catch { return dateStr; }
}

// ── INIT ─────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  setActiveNavLink();
  initNotifBadge();
  initFadeIn();
});

// Expose
window.showToast = showToast;
window.getParam = getParam;
