/**
 * LifeLensAI Shared Components
 * Handles Header, Footer, and Theme Toggle logic.
 */

const UI = {
  icons: {
    moon: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`,
    sun: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>`,
    dashboard: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>`,
    lens: `<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="4"></circle><line x1="4.93" y1="4.93" x2="9.17" y2="9.17"></line><line x1="14.83" y1="14.83" x2="19.07" y2="19.07"></line><line x1="14.83" y1="9.17" x2="19.07" y2="4.93"></line><line x1="4.93" y1="19.07" x2="9.17" y2="14.83"></line></svg>`,
    twitter: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"/></svg>`,
    linkedin: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>`,
    github: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>`,
    heart: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l8.89-8.89 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>`
  },

  init() {
    this.injectBackground();
    this.renderHeader();
    this.renderFooter();
    this.setupTheme();
  },

  injectBackground() {
    const blobs = document.createElement('div');
    blobs.className = 'bg-blobs';
    blobs.innerHTML = '<div class="blob blob-1"></div><div class="blob blob-2"></div>';
    document.body.prepend(blobs);
  },

  renderHeader() {
    const header = document.querySelector('header.main-header');
    if (!header) return;

    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username') || 'Member';
    const initial = username.charAt(0).toUpperCase();

    let navContent = '';
    
    if (token) {
      navContent = `
        <a href="dashboard.html" class="nav-link" style="font-size: 1rem; gap: 8px; font-weight: 600;">
          ${this.icons.dashboard} Dashboard
        </a>
        <button id="theme-btn" class="theme-toggle" style="width: 42px; height: 42px; background: var(--glass-bg); border: 1px solid var(--border-subtle);">
          ${localStorage.getItem('theme') === 'dark' ? this.icons.sun : this.icons.moon}
        </button>
        <div class="user-identity" style="padding-left: 20px; border-left: 1px solid var(--border-subtle); margin-left: 10px;">
          <div class="user-avatar" style="width: 38px; height: 38px; background: var(--primary-crimson); color: white; font-weight: 700;">${initial}</div>
          <div style="display: flex; flex-direction: column; gap: 1px;">
            <span style="font-size: 0.95rem; font-weight: 800; letter-spacing: -0.3px; text-transform: capitalize;">${username}</span>
            <button id="logout-btn" style="background: none; border: none; color: var(--primary-crimson); font-size: 0.7rem; cursor: pointer; padding: 0; font-weight: 700; text-align: left; opacity: 0.7; text-transform: uppercase;">Sign Out</button>
          </div>
        </div>
      `;
    } else {
      navContent = `
        <a href="login.html" class="nav-link" style="font-weight: 600;">Sign In</a>
        <a href="register.html" class="btn btn-primary" style="padding: 0.6rem 1.4rem; font-size: 0.9rem; border-radius: 10px; font-weight: 600;">Get Started</a>
        <button id="theme-btn" class="theme-toggle" style="width: 42px; height: 42px; background: var(--glass-bg); border: 1px solid var(--border-subtle);">
          ${localStorage.getItem('theme') === 'dark' ? this.icons.sun : this.icons.moon}
        </button>
      `;
    }

    header.innerHTML = `
      <div class="header-inner animate-slide-up" style="height: 72px; padding: 0 5%; border-bottom: 1px solid var(--border-subtle); backdrop-filter: blur(20px); background: rgba(var(--bg-rgb), 0.7); position: fixed; top: 0; left: 0; right: 0; z-index: 1000;">
        <div class="logo-container flex items-center gap-3" style="cursor:pointer;" onclick="window.location.href='index.html'">
          <div style="color: var(--primary-crimson); display: flex; align-items: center; justify-content: center;">
            ${this.icons.lens}
          </div>
          <h1 class="text-gradient" style="font-size: 1.5rem; letter-spacing: -1px; font-weight: 800;">LifeLens<span style="color: var(--text-main); font-weight: 400;">AI</span></h1>
        </div>
        <nav class="nav-links" style="gap: 2rem; align-items: center;">
          ${navContent}
        </nav>
      </div>
      <div style="height: 72px;"></div> <!-- Spacer -->
    `;

    document.getElementById('theme-btn').addEventListener('click', () => this.toggleTheme());
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) logoutBtn.addEventListener('click', () => { localStorage.clear(); window.location.href = 'index.html'; });
  },

  renderFooter() {
    const footer = document.createElement('footer');
    footer.className = 'main-footer';
    footer.style.borderTop = '1px solid var(--border-subtle)';
    footer.innerHTML = `
      <div class="container" style="padding: 5rem 2rem 2rem 2rem;">
        <div class="footer-grid" style="display: grid; grid-template-columns: 1.5fr 1fr 1fr 1fr; gap: 4rem; margin-bottom: 4rem;">
          <div class="footer-column">
            <div class="flex items-center gap-2 mb-6" style="color: var(--primary-crimson);">
              ${this.icons.lens}
              <h2 class="text-gradient" style="font-size: 1.4rem; font-weight: 800;">LifeLensAI</h2>
            </div>
            <p style="font-size: 0.9rem; line-height: 1.7; color: var(--text-muted); margin-bottom: 2rem;">
              Redefining preventive medicine through high-fidelity predictive intelligence and clinical data synthesis.
            </p>
            <div class="flex gap-3">
              <a href="#" class="social-icon">${this.icons.twitter}</a>
              <a href="#" class="social-icon">${this.icons.linkedin}</a>
              <a href="#" class="social-icon">${this.icons.github}</a>
            </div>
          </div>
          
          <div class="footer-column">
            <h4 style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.6; margin-bottom: 2rem;">Diagnostic Hub</h4>
            <ul class="footer-links" style="list-style: none; display: flex; flex-direction: column; gap: 1rem;">
              <li><a href="diabetes.html" class="footer-link flex items-center gap-2">${this.icons.heart} Diabetes Suite</a></li>
              <li><a href="hypertension.html" class="footer-link flex items-center gap-2">${this.icons.heart} Arterial Panel</a></li>
              <li><a href="breast_cancer_imaging.html" class="footer-link flex items-center gap-2">${this.icons.heart} Oncology AI</a></li>
              <li><a href="dashboard.html" class="footer-link flex items-center gap-2">${this.icons.heart} Clinical Hub</a></li>
            </ul>
          </div>
          
          <div class="footer-column">
            <h4 style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.6; margin-bottom: 2rem;">Architecture</h4>
            <ul class="footer-links" style="list-style: none; display: flex; flex-direction: column; gap: 1rem;">
              <li><a href="#" class="footer-link">Methodology</a></li>
              <li><a href="#" class="footer-link">Privacy Guard</a></li>
              <li><a href="#" class="footer-link">Data Ethics</a></li>
              <li><a href="#" class="footer-link">API Gateway</a></li>
            </ul>
          </div>
          
          <div class="footer-column">
            <h4 style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.6; margin-bottom: 2rem;">Support</h4>
            <ul class="footer-links" style="list-style: none; display: flex; flex-direction: column; gap: 1rem;">
              <li><a href="mailto:support@lifelens.ai" class="footer-link">support@lifelens.ai</a></li>
              <li class="flex items-center gap-2" style="font-size: 0.85rem; font-weight: 600;">
                <span class="status-pulse"></span> Platform Operational
              </li>
              <li><a href="#" class="footer-link">Clinical Partner</a></li>
            </ul>
          </div>
        </div>

        <div class="footer-disclaimer" style="padding: 2.5rem; background: rgba(var(--bg-rgb), 0.3); border-radius: 20px; border: 1px solid var(--border-subtle); margin-bottom: 3rem; font-size: 0.85rem; line-height: 1.8; text-align: center;">
          <strong style="color: var(--primary-crimson); display: block; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">Medical Intelligence Disclaimer</strong>
          LifeLensAI is an artificial intelligence diagnostic assistant. Insights are purely informational and do NOT constitute professional medical advice, clinical diagnosis, or therapeutic treatment. No data provided here establishes a doctor-patient relationship. Consult a licensed physician immediately for any clinical anomaly.
        </div>

        <div class="footer-bottom" style="padding-top: 2rem; border-top: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: var(--text-muted); font-weight: 500;">
          <div>&copy; 2026 LifeLensAI Platform. Professional Diagnostic Intelligence.</div>
          <div class="flex gap-8">
            <a href="#" class="footer-link">Terms of Service</a>
            <a href="#" class="footer-link">Data Ethics Policy</a>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(footer);
  },

  setupTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
  },

  toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const target = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', target);
    localStorage.setItem('theme', target);
    const btn = document.getElementById('theme-btn');
    btn.innerHTML = target === 'dark' ? this.icons.sun : this.icons.moon;
  }
};

document.addEventListener('DOMContentLoaded', () => UI.init());
