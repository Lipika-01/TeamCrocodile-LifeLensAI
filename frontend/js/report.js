/**
 * LifeLensAI Premium Report Engine
 * Renders structured medical insights into glassmorphism cards.
 */

const ReportUI = {
  icons: {
    summary: `<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>`,
    routine: `<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>`,
    monitoring: `<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>`,
    exercise: `<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8h1a4 4 0 0 1 0 8h-1"></path><path d="M2 8h16v8H2V8z"></path><line x1="6" y1="12" x2="14" y2="12"></line></svg>`,
    diet: `<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10"></path><path d="M12 20V4"></path><path d="M6 20v-6"></path></svg>`,
    supplements: `<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"></path><path d="m8.5 8.5 7 7"></path></svg>`,
    medicine: `<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M4.8 2.8C3.5 1.5 1.5 3.5 2.8 4.8L12 14l9.2-9.2c1.3-1.3-0.7-3.3-2-2L12 10 4.8 2.8z"></path><path d="m12 14 9.2 9.2c1.3 1.3 3.3-0.7 2-2L14 12l-2 2z"></path><path d="M12 14 2.8 23.2c-1.3 1.3-3.3-0.7-2-2L10 12l2 2z"></path></svg>`
  },

  render(reportData) {
    document.getElementById('empty-state').classList.add('hidden');
    const dashboard = document.getElementById('full-dashboard');
    dashboard.classList.remove('hidden');
    dashboard.classList.add('animate-slide-up');

    const report = reportData.report || reportData;
    const predictions = report.predictions || {};
    const analysis = report.analysis || [];
    const warnings = report.combined_warnings || [];
    const docReport = report.doctor_report || {};

    // 1. Predictions Summary Card
    const summaryText = docReport.medical_summary || 'AI analysis complete. Review the detailed report below.';
    this.renderSummary(predictions, summaryText);

    // 2. Metrics Analysis
    this.renderMetrics(analysis);

    // 3. Detailed Insight Cards
    this.renderInsightCards(docReport);

    // 4. Alerts
    this.renderAlerts(warnings, predictions);
  },

  renderSummary(predictions, summaryText) {
    const grid = document.getElementById('predictions-grid');
    grid.innerHTML = '';
    
    for(const [key, result] of Object.entries(predictions)) {
      // Support both old `probability_percent` and new `probability` field
      const prob = result.probability_percent ?? result.probability ?? 50;
      let status = 'safe';
      if(result.risk_level === 'Medium') status = 'warning';
      if(result.risk_level === 'High') status = 'danger';

      const offset = 251.2 - (251.2 * prob) / 100;
      const label = result.prediction || result.risk_level || 'Analysed';

      grid.innerHTML += `
        <div class="glass-card card-border-none" style="padding: 2.5rem; flex: 1; border-left: 6px solid var(--${status}); margin-bottom: 2rem;">
          <div class="flex justify-between items-start mb-6">
            <div>
              <p class="input-label" style="margin-bottom: 4px;">Diagnostic Result</p>
              <h2 style="font-size: 1.8rem;">${key.replace(/_/g,' ').toUpperCase()}</h2>
              <p style="font-size: 0.95rem; font-weight: 600; margin-top: 4px; color: var(--${status});">${label}</p>
            </div>
            <div class="prob-circle-container">
              <svg class="prob-ring" width="80" height="80" viewBox="0 0 100 100" style="transform: rotate(-90deg);">
                <circle cx="50" cy="50" r="40" fill="none" stroke="var(--border-subtle)" stroke-width="8" />
                <circle cx="50" cy="50" r="40" fill="none" stroke="var(--${status})" stroke-width="8" 
                  stroke-dasharray="251.2" style="stroke-dashoffset: ${offset}; transition: stroke-dashoffset 1s ease-out;" />
              </svg>
              <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-weight: 700;">
                ${Number(prob).toFixed(0)}%
              </div>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: var(--${status});"></span>
            <span style="font-weight: 600; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px; color: var(--${status});">
              ${result.risk_level} Risk Level
            </span>
          </div>
          ${result.model_accuracy ? `<p class="mt-2" style="font-size: 0.8rem; color: var(--text-muted);">Model Accuracy: ${result.model_accuracy}</p>` : ''}
          <p class="mt-4" style="font-size: 0.95rem; color: var(--text-muted);">${summaryText || result.explanation || ''}</p>
        </div>
      `;
    }
  },

  renderMetrics(analysis) {
    const container = document.getElementById('metrics-analysis');
    if (!container) return;
    container.innerHTML = analysis.map(m => `
      <div class="flex justify-between items-center p-4" style="border-bottom: 1px solid var(--border-subtle);">
        <div>
          <p style="font-weight: 500;">${m.name}</p>
          <p style="font-size: 0.8rem; color: var(--text-muted);">${m.value}</p>
        </div>
        <span style="font-size: 0.85rem; font-weight: 600; color: ${m.warning ? 'var(--danger)' : 'var(--safe)'};">
          ${m.status}
        </span>
      </div>
    `).join('');
  },

  renderInsightCards(docReport) {
    const grid = document.getElementById('recommendations-grid');
    grid.innerHTML = '';

    const sections = [
      { id: 'daily_routine', title: 'Daily Routine Plan', icon: this.icons.routine },
      { id: 'monitoring_plan', title: 'Monitoring Strategy', icon: this.icons.monitoring },
      { id: 'diet_configuration', title: 'Dietary Intelligence', icon: this.icons.diet },
      { id: 'physical_activity', title: 'Physical Activity', icon: this.icons.exercise },
      { id: 'supplements', title: 'Clinical Supplements', icon: this.icons.supplements },
      { id: 'medicinal_guidance', title: 'Medicinal Guidance', icon: this.icons.medicine }
    ];

    sections.forEach(s => {
      const data = docReport[s.id] || ["Content currently unavailable due to AI parsing failure. Check clinical parameters."];
      const items = Array.isArray(data) ? data : [data];

      grid.innerHTML += `
        <div class="glass-card card-border-none animate-slide-up" style="padding: 1.5rem; height: 100%;">
          <div class="flex items-center gap-3 mb-6" style="color: var(--primary-crimson);">
            <div style="padding: 10px; background: var(--secondary-pink); border-radius: 12px; color: var(--primary-crimson);">
              ${s.icon}
            </div>
            <h4 style="font-size: 1.1rem; font-weight: 600;">${s.title}</h4>
          </div>
          <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.8rem;">
            ${items.map(i => `
              <li style="display: flex; gap: 10px; font-size: 0.9rem; line-height: 1.5;">
                <span style="color: var(--primary-crimson); margin-top: 2px;">•</span>
                <span>${i}</span>
              </li>
            `).join('')}
          </ul>
        </div>
      `;
    });
  },

  renderAlerts(warnings, predictions) {
    const container = document.getElementById('risk-alerts');
    container.innerHTML = '';
    
    // Global Danger Alert if any High Risk
    let hasHigh = Object.values(predictions).some(p => p.risk_level === 'High');
    
    if (hasHigh) {
      container.innerHTML += `
        <div class="glass-card" style="background: rgba(239, 68, 68, 0.1); border-color: var(--danger); padding: 1.5rem; margin-bottom: 2rem;">
          <div class="flex items-center gap-4">
            <div style="font-size: 2rem;">⚠️</div>
            <div>
              <h4 style="color: var(--danger); margin-bottom: 4px;">Urgent Health Advisory</h4>
              <p style="font-size: 0.9rem;">Clinical benchmarks indicate high-severity anomalies. Immediate medical consultation is advised to prevent systemic complications.</p>
            </div>
          </div>
        </div>
      `;
    }

    warnings.forEach(w => {
      container.innerHTML += `
        <div class="glass-card" style="background: rgba(245, 158, 11, 0.1); border-color: var(--warning); padding: 1rem; margin-bottom: 1rem; font-size: 0.9rem;">
          ${w}
        </div>
      `;
    });
  }
};

window.renderDoctorReport = (data) => ReportUI.render(data);
