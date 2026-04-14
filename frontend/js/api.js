const API_URL = 'http://localhost:8000/api';

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
    if(res.status === 401) {
       window.location.href = 'login.html';
    }
    return parsed;
  } catch (err) {
    console.error(err);
    return null;
  }
}
