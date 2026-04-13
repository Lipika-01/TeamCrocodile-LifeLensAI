const API_URL = 'http://localhost:8000/api';

async function extractPDFData(file) {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch(`${API_URL}/extract`, {
      method: 'POST',
      body: formData
    });
    return await res.json();
  } catch (error) {
    console.error('Extraction Error:', error);
    return null;
  }
}

async function predictAll(data) {
  try {
    const res = await fetch(`${API_URL}/predict/all`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    return await res.json();
  } catch (error) {
    console.error('Prediction Error:', error);
    return null;
  }
}
