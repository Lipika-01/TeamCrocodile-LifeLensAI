/**
 * LifeLensAI Shared Components
 * Handles Header, Footer, and Theme Toggle logic.
 */

const UI = {
  icons: {
    moon: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`,
    sun: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>`,
    dashboard: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>`,
    history: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>`
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

    const currentPath = window.location.pathname;
    const isDashboard = currentPath.includes('dashboard');
    const username = localStorage.getItem('username') || 'Member';
    const initial = username.charAt(0).toUpperCase();

    header.innerHTML = `
      <div class="header-inner animate-slide-up">
        <div class="logo-container flex items-center gap-2" style="cursor:pointer;" onclick="window.location.href='dashboard.html'">
          <div style="background: var(--primary-crimson); color: white; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 700;">L</div>
          <h1 class="text-gradient" style="font-size: 1.3rem; letter-spacing: -0.5px;">LifeLens<span style="color: var(--text-main); font-weight: 400;">AI</span></h1>
        </div>
        
        <nav class="nav-links">
          <a href="dashboard.html" class="nav-link ${isDashboard ? 'active' : ''}">
            ${this.icons.dashboard} Dashboard
          </a>
          <a href="history.html" class="nav-link ${currentPath.includes('history') ? 'active' : ''}">
            ${this.icons.history} Intelligence History
          </a>
          
          <button id="theme-btn" class="theme-toggle">
            ${localStorage.getItem('theme') === 'dark' ? this.icons.sun : this.icons.moon}
          </button>

          <div class="user-identity">
            <div class="user-avatar">${initial}</div>
            <div style="display: flex; flex-direction: column;">
              <span style="font-size: 0.8rem; font-weight: 600;">${username}</span>
              <button onclick="localStorage.removeItem('token'); window.location.href='index.html'" 
                      style="background: none; border: none; color: var(--primary-crimson); font-size: 0.7rem; cursor: pointer; padding: 0; text-align: left; font-weight: 700;">
                  Sign Out
              </button>
            </div>
          </div>
        </nav>
      </div>
    `;

    document.getElementById('theme-btn').addEventListener('click', () => this.toggleTheme());
  },

  renderFooter() {
    const footer = document.createElement('footer');
    footer.className = 'main-footer';
    footer.innerHTML = `
      <div class="container overflow-hidden">
        <div class="footer-grid">
          <div class="footer-column">
            <h2 class="text-gradient mb-4" style="font-size: 1.5rem;">LifeLensAI</h2>
            <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 2rem;">
              Empowering proactive healthcare through high-accuracy predictive intelligence and clinical data synthesis.
            </p>
            <div class="flex gap-4">
              <span style="width: 32px; height: 32px; background: var(--border-subtle); border-radius: 50%;" title="X"></span>
              <span style="width: 32px; height: 32px; background: var(--border-subtle); border-radius: 50%;" title="LinkedIn"></span>
            </div>
          </div>
          
          <div class="footer-column">
            <h4>Diagnostic Hub</h4>
            <ul class="footer-links">
              <li><a href="diabetes.html" class="footer-link">Diabetes Intelligence</a></li>
              <li><a href="hypertension.html" class="footer-link">Cardiovascular Panel</a></li>
              <li><a href="heart.html" class="footer-link">Arterial Analysis</a></li>
              <li><a href="#" class="footer-link">Oncology (Coming Soon)</a></li>
            </ul>
          </div>
          
          <div class="footer-column">
            <h4>Resources</h4>
            <ul class="footer-links">
              <li><a href="#" class="footer-link">Clinical Methodology</a></li>
              <li><a href="#" class="footer-link">API Documentation</a></li>
              <li><a href="#" class="footer-link">Help Center</a></li>
              <li><a href="#" class="footer-link">Privacy Guardian</a></li>
            </ul>
          </div>
          
          <div class="footer-column">
            <h4>Contact Support</h4>
            <ul class="footer-links">
              <li><a href="mailto:support@lifelens.ai" class="footer-link">support@lifelens.ai</a></li>
              <li><a href="#" class="footer-link">System Status</a></li>
              <li><a href="#" class="footer-link">Clinical Partnership</a></li>
            </ul>
          </div>
        </div>

        <div class="footer-disclaimer">
          <strong>Medical Intelligence Disclaimer:</strong> LifeLensAI is an artificial intelligence-driven assistant. The insights generated are strictly informational and are NOT a substitute for professional medical advice, clinical diagnosis, or therapeutic treatment. No data provided here constitutes a doctor-patient relationship. Always consult a licensed physician immediately if you suspect any clinical anomaly.
        </div>

        <div class="footer-bottom">
          <div>&copy; 2026 LifeLensAI Platform. Redefining Preventive Care.</div>
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
