function renderDashboard(data) {
  // Hide empty state and show full dashboard
  document.getElementById('empty-state').classList.add('hidden');
  document.getElementById('full-dashboard').classList.remove('hidden');

  // Render combined alerts
  const combinedContainer = document.getElementById('combined-alerts-container');
  combinedContainer.innerHTML = '';
  if (data.combined_warnings && data.combined_warnings.length > 0) {
    data.combined_warnings.forEach(warn => {
      combinedContainer.innerHTML += `
        <div class="combined-alert">
          <span class="combined-icon">🚨</span>
          <div>
            ${warn.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}
          </div>
        </div>
      `;
    });
  }

  // Render Predictions
  const grid = document.getElementById('predictions-grid');
  grid.innerHTML = '';
  
  const models = [
    { title: 'Diabetes', key: 'diabetes' },
    { title: 'Hypertension', key: 'hypertension' },
    { title: 'Heart Disease', key: 'heart' }
  ];

  models.forEach(model => {
    const result = data.predictions[model.key];
    const reasoning = data.reasoning ? data.reasoning[model.key] : "";
    if(!result) return;
    
    let stateClass = 'safe';
    if(result.risk_level === 'Medium') stateClass = 'warning';
    if(result.risk_level === 'High') stateClass = 'danger';

    // SVG Math: 251.2 is full circle outline length
    const offset = 251.2 - (251.2 * result.probability_percent) / 100;

    grid.innerHTML += `
      <div class="prediction-card glass-card ${stateClass}">
        <div class="disease-title">${model.title}</div>
        <div class="prob-circle-container">
          <svg class="prob-ring" width="100" height="100" viewBox="0 0 100 100">
            <circle class="prob-ring-bg" cx="50" cy="50" r="40" />
            <circle class="prob-ring-fill" cx="50" cy="50" r="40" style="stroke-dashoffset: ${offset};" />
          </svg>
          <div class="prob-text">${result.probability_percent.toFixed(0)}%</div>
        </div>
        <div class="risk-level">${result.risk_level} Risk</div>
        <div class="reasoning-text">${reasoning}</div>
      </div>
    `;
  });

  // Render Metrics Analysis
  const vGrid = document.getElementById('value-grid');
  vGrid.innerHTML = '';
  if (data.analysis) {
    data.analysis.forEach(v => {
      const cls = v.warning ? 'alert' : 'safe';
      const statCls = v.warning ? 'warn' : 'ok';
      vGrid.innerHTML += `
        <div class="value-box ${cls}">
          <div class="v-name">${v.name}</div>
          <div class="v-val">${v.value}</div>
          <div class="v-stat ${statCls}">${v.status}</div>
        </div>
      `;
    });
  }

  // Render Insights
  const insList = document.getElementById('insights-list');
  insList.innerHTML = '';
  if (data.insights) {
    data.insights.forEach(ins => {
      insList.innerHTML += `<li>${ins}</li>`;
    });
  }

  // Render Recommendations Lists
  const r = data.recommendations;
  if(r) {
    populateList('rec-diet', r.diet);
    populateList('rec-exercise', r.exercise);
    populateList('rec-med', r.medicine);
    populateList('rec-prev', r.preventive);
    populateList('rec-vitamins', r.vitamins);
  }

  setupAccordions();
}

function setupAccordions() {
  const titles = document.querySelectorAll('.rec-title');
  titles.forEach(title => {
    // Only attach once
    if (title.getAttribute('data-listener') !== 'true') {
      title.setAttribute('data-listener', 'true');
      
      const list = title.nextElementSibling;
      const icon = title.querySelector('.expand-icon');
      
      // Default to expanded for immediate visibility
      list.classList.add('expanded');
      if (icon) icon.style.transform = 'rotate(180deg)';
      
      title.addEventListener('click', () => {
        list.classList.toggle('expanded');
        if (list.classList.contains('expanded')) {
          if(icon) icon.style.transform = 'rotate(180deg)';
        } else {
          if(icon) icon.style.transform = 'rotate(0deg)';
        }
      });
    }
  });
}

function populateList(id, array) {
  const ul = document.getElementById(id);
  ul.innerHTML = '';
  if (array) {
    array.forEach(item => {
      ul.innerHTML += `<li>${item}</li>`;
    });
  }
}
