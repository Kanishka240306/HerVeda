(function () {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');

  if (toggle && links) {
    toggle.addEventListener('click', function () {
      const isOpen = links.classList.toggle('is-open');
      toggle.classList.toggle('is-active', isOpen);
      toggle.setAttribute('aria-expanded', isOpen);
      toggle.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
    });

    links.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        links.classList.remove('is-open');
        toggle.classList.remove('is-active');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', 'Open menu');
      });
    });
  }

  const form = document.querySelector('.waitlist-form');
  if (form) {
    form.addEventListener('submit', async function (e) {
      e.preventDefault();

      const input = form.querySelector('input[type="email"]');
      const status = document.querySelector('.waitlist-status');
      const email = input ? input.value.trim() : '';

      const submitButton = form.querySelector('button[type="submit"]');
      if (!email) {
        if (status) {
          status.textContent = 'Please enter your email address.';
          status.classList.add('status-error');
        }
        return;
      }

      if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = 'Joining...';
      }

      try {
        const response = await fetch('/waitlist', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email }),
        });

        const result = await response.json();

        if (status) {
          status.textContent = result.message || 'Server did not return a response.';
          status.classList.toggle('status-error', !result.success);
        }

        if (result.success && input) {
          input.value = '';
        }
      } catch (error) {
        if (status) {
          status.textContent = 'Unable to send your request right now. Please try again later.';
          status.classList.add('status-error');
        }
        console.error('Waitlist submission failed', error);
      } finally {
        if (submitButton) {
          submitButton.disabled = false;
          submitButton.textContent = 'Join the Waitlist — It\'s Free';
        }
      }
    });
  }
})();
