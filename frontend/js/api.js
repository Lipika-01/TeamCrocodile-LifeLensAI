const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
  ? 'http://localhost:8000/api' 
  : '/api'; // Uses relative path since frontend and backend are served together on Render

function getAuthHeaders() {
  const token = localStorage.getItem('token');
  if (!token) {
    window.location.href = 'login.html';
    return {};
  }
  return {
    'Authorization': `Bearer ${token}`
  };
}

async function extractPDFData(file) {
  const formData = new FormData();
  formData.append('file', file);
  try {
    const res = await fetch(`${API_URL}/extract`, {
      method: 'POST',
      body: formData,
      headers: getAuthHeaders()
    });
    return await res.json();
  } catch (err) {
    console.error(err);
    return null;
  }
}

async function fetchPreviousRecords() {
  try {
    const res = await fetch(`${API_URL}/user/records`, {
      headers: getAuthHeaders()
    });
    return await res.json();
  } catch (err) {
    console.error(err);
    return null;
  }
}

async function predictDisease(module, data) {
  // Show loading state on submit button
  const btn = document.querySelector('#health-form button[type="submit"]');
  const originalText = btn ? btn.textContent : '';
  if (btn) { btn.textContent = 'Analysing...'; btn.disabled = true; }

  try {
    const res = await fetch(`${API_URL}/predict/${module}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      },
      body: JSON.stringify(data)
    });

    const parsed = await res.json();

    if (res.status === 401) {
      window.location.href = 'login.html';
      return null;
    }

    if (parsed.status === 'error' || parsed.detail) {
      const msg = parsed.message || parsed.detail || 'Prediction failed. Please check inputs.';
      showError(msg);
      return null;
    }

    return parsed;
  } catch (err) {
    console.error('Predict error:', err);
    showError('Unable to reach the AI server. Make sure the backend is running on port 8000.');
    return null;
  } finally {
    if (btn) { btn.textContent = originalText; btn.disabled = false; }
  }
}

function showError(message) {
  // Remove existing toast
  const existing = document.getElementById('error-toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.id = 'error-toast';
  toast.innerHTML = `
    <div style="
      position: fixed; bottom: 2rem; right: 2rem; z-index: 9999;
      background: rgba(239,68,68,0.95); color: white;
      padding: 1rem 1.5rem; border-radius: 12px;
      box-shadow: 0 8px 32px rgba(239,68,68,0.3);
      font-size: 0.9rem; font-weight: 500; max-width: 400px;
      display: flex; align-items: center; gap: 0.75rem;
      animation: slideUp 0.3s ease;
    ">
      <span style="font-size:1.2rem;">⚠️</span>
      <span>${message}</span>
      <button onclick="this.closest('#error-toast').remove()" style="background:none;border:none;color:white;cursor:pointer;font-size:1.1rem;margin-left:auto;">✕</button>
    </div>
  `;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 8000);
}
