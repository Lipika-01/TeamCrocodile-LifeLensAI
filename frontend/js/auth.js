const API_URL = '/api';

// Auth Guard Logic
const protectedRoutes = [
  'dashboard.html', 
  'diabetes.html', 
  'hypertension.html', 
  'heart.html', 
  'lung_cancer.html', 
  'breast_cancer.html',
  'breast_cancer_imaging.html',
  'brain_tumor_imaging.html'
];
const publicOnlyRoutes = ['login.html', 'register.html'];

function checkAuth() {
  const token = localStorage.getItem('token');
  const currentPath = window.location.pathname.split('/').pop();

  if (protectedRoutes.includes(currentPath) && !token) {
    window.location.href = 'login.html';
    return;
  }

  if (publicOnlyRoutes.includes(currentPath) && token) {
    window.location.href = 'dashboard.html';
    return;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  checkAuth();
  
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const params = new URLSearchParams();
      params.append('username', document.getElementById('username').value);
      params.append('password', document.getElementById('password').value);
      
      try {
        const res = await fetch(`${API_URL}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: params
        });
        const data = await res.json();
        if (res.ok) {
          localStorage.setItem('token', data.access_token);
          localStorage.setItem('username', document.getElementById('username').value);
          window.location.href = 'dashboard.html';
        } else {
          alert('Login failed: ' + data.detail);
        }
      } catch (err) {
        console.error(err);
        alert('An error occurred during login.');
      }
    });
  }

  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
      };
      
      try {
        const res = await fetch(`${API_URL}/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok) {
          alert('Registration successful! Please login.');
          window.location.href = 'login.html';
        } else {
          alert('Registration failed: ' + data.detail);
        }
      } catch (err) {
        console.error(err);
        alert('An error occurred during registration.');
      }
    });
  }
});
