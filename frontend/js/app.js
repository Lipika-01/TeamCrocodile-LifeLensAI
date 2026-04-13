document.addEventListener('DOMContentLoaded', () => {
  setupPDFUpload();
  setupFormSubmit();
});

function setupPDFUpload() {
  const dropZone = document.getElementById('drop-zone');
  const fileInput = document.getElementById('pdf-upload');

  dropZone.addEventListener('click', () => fileInput.click());

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
  });

  dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
  });

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
      handleFile(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
      handleFile(e.target.files[0]);
    }
  });
}

async function handleFile(file) {
  if (file.type !== 'application/pdf') {
    alert('Please upload a valid PDF medical report.');
    return;
  }
  
  showLoader();
  const res = await extractPDFData(file);
  hideLoader();

  if (res && res.status === 'success') {
    autoFillForm(res.data);
    alert('Metrics auto-filled from PDF successfully!');
  } else {
    alert('Failed to extract data from PDF. Please enter manually.');
  }
}

function autoFillForm(data) {
  if(data.age) document.getElementById('age').value = data.age;
  if(data.bmi) document.getElementById('bmi').value = data.bmi;
  if(data.glucose) document.getElementById('glucose').value = data.glucose;
  if(data.ap_hi) document.getElementById('ap_hi').value = data.ap_hi;
  if(data.ap_lo) document.getElementById('ap_lo').value = data.ap_lo;
}

function setupFormSubmit() {
  const form = document.getElementById('health-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const payload = {
      age: parseInt(document.getElementById('age').value),
      bmi: parseFloat(document.getElementById('bmi').value),
      glucose: parseFloat(document.getElementById('glucose').value),
      insulin: parseFloat(document.getElementById('insulin').value),
      ap_hi: parseFloat(document.getElementById('ap_hi').value),
      ap_lo: parseFloat(document.getElementById('ap_lo').value),
      cholesterol: parseFloat(document.getElementById('cholesterol').value),
      thalach: parseFloat(document.getElementById('thalach').value),
      cp: parseInt(document.getElementById('cp').value),
      oldpeak: parseFloat(document.getElementById('oldpeak').value),
      exang: parseInt(document.getElementById('exang').value)
    };

    showLoader();
    const res = await predictAll(payload);
    hideLoader();

    if(res && res.status === 'success') {
      renderDashboard(res);
    } else {
      alert('Error fetching predictions from the backend.');
    }
  });
}

function showLoader() {
  document.getElementById('sidebar-loader').classList.remove('hidden');
}

function hideLoader() {
  document.getElementById('sidebar-loader').classList.add('hidden');
}
