/* Urban Puff Lounge and Bar — site behaviour */
(function () {
  'use strict';

  /* ---- sticky header ---- */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 24);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- mobile nav ---- */
  var toggle = document.querySelector('.nav__toggle');
  var links = document.querySelector('.nav__links');
  if (toggle && links) {
    var setNav = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      links.classList.toggle('is-open', open);
      document.body.classList.toggle('nav-open', open);
    };
    toggle.addEventListener('click', function () {
      setNav(toggle.getAttribute('aria-expanded') !== 'true');
    });
    links.addEventListener('click', function (e) {
      if (e.target.closest('a')) setNav(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setNav(false);
    });
  }

  /* ---- reveal on scroll ---- */
  var reveals = document.querySelectorAll('.reveal');
  if (reveals.length) {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            io.unobserve(entry.target);
          }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
      reveals.forEach(function (el, i) {
        el.style.transitionDelay = (Math.min(i % 4, 3) * 80) + 'ms';
        io.observe(el);
      });
    } else {
      reveals.forEach(function (el) { el.classList.add('is-in'); });
    }
  }

  /* ---- current year ---- */
  var yr = document.querySelector('[data-year]');
  if (yr) yr.textContent = new Date().getFullYear();

  /* ---- contact form ---- */
  var form = document.querySelector('[data-validate]');
  if (!form) return;

  // JS is present, so take over from the browser's native bubbles and show
  // our own inline messages. Without JS the `required` attributes still apply
  // and the form falls back to a normal POST.
  form.setAttribute('novalidate', 'novalidate');

  var statusBox = document.querySelector('[data-form-status]');
  var emailRe = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i;
  var digitsRe = /\d/g;

  function fieldOf(input) { return input.closest('.field'); }

  function setError(input, message) {
    var wrap = fieldOf(input);
    if (!wrap) return;
    var err = wrap.querySelector('.err');
    if (message) {
      wrap.classList.add('is-invalid');
      input.setAttribute('aria-invalid', 'true');
      if (err) err.textContent = message;
    } else {
      wrap.classList.remove('is-invalid');
      input.removeAttribute('aria-invalid');
      if (err) err.textContent = '';
    }
  }

  function validateField(input) {
    var value = (input.value || '').trim();

    if (input.hasAttribute('required') && !value) {
      setError(input, input.name === 'Phone'
        ? 'We need a phone number so we can reach you.'
        : (input.tagName === 'SELECT' ? 'Please choose one.' : 'This field is required.'));
      return false;
    }
    if (input.name === 'Phone' && value) {
      var digits = (value.match(digitsRe) || []).length;
      if (digits < 10) {
        setError(input, 'Please enter a full phone number, including area code.');
        return false;
      }
    }
    if (input.name === 'Email' && value && !emailRe.test(value)) {
      setError(input, 'Please enter a valid email address.');
      return false;
    }
    if (input.type === 'date' && value && input.min && value < input.min) {
      setError(input, 'Please pick a date from today onwards.');
      return false;
    }
    setError(input, '');
    return true;
  }

  var fields = Array.prototype.slice.call(
    form.querySelectorAll('input:not([type=hidden]), textarea, select')
  );

  // Reservations can't be made for a date that has already gone.
  var dateField = form.querySelector('input[type=date]');
  if (dateField && !dateField.min) {
    try {
      var today = new Intl.DateTimeFormat('en-CA', {
        timeZone: 'America/New_York', year: 'numeric', month: '2-digit', day: '2-digit'
      }).format(new Date());
      dateField.min = today;
    } catch (e) { /* leave it open */ }
  }

  fields.forEach(function (input) {
    input.addEventListener('blur', function () { validateField(input); });
    input.addEventListener('change', function () { validateField(input); });
    input.addEventListener('input', function () {
      var wrap = fieldOf(input);
      if (wrap && wrap.classList.contains('is-invalid')) validateField(input);
    });
  });

  var ICONS = {
    ok: '<svg viewBox="0 0 24 24" stroke="currentColor"><circle cx="12" cy="12" r="9.2"/><path d="M8 12.4l2.7 2.7L16 9.6"/></svg>',
    err: '<svg viewBox="0 0 24 24" stroke="currentColor"><circle cx="12" cy="12" r="9.2"/><path d="M12 7.6v5.2M12 16.4h.01"/></svg>',
    info: '<svg viewBox="0 0 24 24" stroke="currentColor"><circle cx="12" cy="12" r="9.2"/><path d="M12 11v5.4M12 7.7h.01"/></svg>'
  };

  function showStatus(state, title, body) {
    if (!statusBox) return;
    statusBox.setAttribute('data-state', state);
    statusBox.innerHTML =
      '<span class="form-status__icon">' + (ICONS[state] || ICONS.info) + '</span>' +
      '<p><strong>' + title + '</strong>' + body + '</p>';
    statusBox.classList.add('is-shown');
    statusBox.setAttribute('role', state === 'err' ? 'alert' : 'status');
    statusBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  form.addEventListener('submit', function (e) {
    var ok = true;
    var firstBad = null;

    fields.forEach(function (input) {
      var good = validateField(input);
      if (!good && !firstBad) firstBad = input;
      if (!good) ok = false;
    });

    if (!ok) {
      e.preventDefault();
      if (firstBad) {
        firstBad.focus();
        firstBad.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      return;
    }

    // Everything valid — send it in the background so the visitor stays here.
    // fetch missing (very old browser)? let the normal POST happen instead.
    if (typeof window.fetch !== 'function') return;

    e.preventDefault();

    var btn = form.querySelector('button[type=submit]');
    var label = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }

    var endpoint = form.getAttribute('data-endpoint') || form.action;

    fetch(endpoint, {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    })
      .then(function (r) { return r.json().catch(function () { return {}; }); })
      .then(function (data) {
        var sent = data && (data.success === true || data.success === 'true');
        var pending = data && /confirm|activat/i.test(data.message || '');

        if (sent) {
          form.classList.add('is-sent');
          showStatus('ok', 'Message sent',
            'Thanks — we’ve got it. Someone from the Urban Puff team will get ' +
            'back to you shortly, usually the same day.');
        } else if (pending) {
          showStatus('info', 'Almost there',
            'This form is awaiting a one-time confirmation on our side. Your ' +
            'message hasn’t reached us yet — please email us directly at ' +
            '<a href="mailto:urbanpuff1@gmail.com">urbanpuff1@gmail.com</a> in the meantime.');
        } else {
          throw new Error('unexpected response');
        }
      })
      .catch(function () {
        showStatus('err', 'That didn’t go through',
          'Something went wrong sending your message. Please try again, or ' +
          'email us directly at <a href="mailto:urbanpuff1@gmail.com">urbanpuff1@gmail.com</a>.');
      })
      .then(function () {
        if (btn) { btn.disabled = false; btn.textContent = label; }
      });
  });
})();
