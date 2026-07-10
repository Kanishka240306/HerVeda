document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('form');
  forms.forEach((form) => {
    form.addEventListener('submit', () => {
      const button = form.querySelector('button[type="submit"]');
      if (button) {
        button.disabled = true;
        button.textContent = 'Saving...';
      }
    });
  });

  const googleBtn = document.getElementById('google-signin-btn');
  if (googleBtn) {
    googleBtn.addEventListener('click', () => {
      googleBtn.disabled = true;
      googleBtn.textContent = 'Signing in...';

      const provider = new firebase.auth.GoogleAuthProvider();
      firebase.auth().signInWithPopup(provider)
        .then((result) => result.user.getIdToken())
        .then((idToken) => fetch('/google-signin', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ idToken }),
        }))
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            window.location.href = data.redirect;
          } else {
            alert(data.message || 'Google sign-in failed. Please try again.');
            googleBtn.disabled = false;
            googleBtn.textContent = 'Sign in with Google';
          }
        })
        .catch((error) => {
          alert('Google sign-in failed: ' + error.message);
          googleBtn.disabled = false;
          googleBtn.textContent = 'Sign in with Google';
        });
    });
  }
});