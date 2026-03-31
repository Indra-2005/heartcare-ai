// ── Ultra-compatible HeartCare AI JavaScript ──────────────────────────────────
// Wrapping features in error handlers to ensure one failing feature (on older mobile browsers)
// does not crash the entire execution engine.

window.addEventListener('load', function() {

  // 1. Navbar scroll effect
  try {
    var navbar = document.querySelector('.navbar');
    if (navbar) {
      window.addEventListener('scroll', function() {
        if (window.scrollY > 20) {
          navbar.classList.add('scrolled');
        } else {
          navbar.classList.remove('scrolled');
        }
      });
    }
  } catch(e) { console.error("Navbar scroll error", e); }

  // 2. Mobile nav toggle
  try {
    var navToggle = document.getElementById('navToggle');
    var navLinks = document.querySelector('.nav-links');
    if (navToggle && navLinks) {
      navToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        navLinks.classList.toggle('open');
        if (navLinks.classList.contains('open')) {
          navToggle.innerHTML = '<i class="fas fa-times"></i>';
        } else {
          navToggle.innerHTML = '<i class="fas fa-bars"></i>';
        }
      });
      document.addEventListener('click', function(e) {
        if (navbar && !navbar.contains(e.target)) {
          navLinks.classList.remove('open');
          navToggle.innerHTML = '<i class="fas fa-bars"></i>';
        }
      });
    }
  } catch(e) { console.error("Mobile toggle error", e); }

  // 3. Auto-dismiss toasts
  try {
    var toasts = document.querySelectorAll('.toast-item');
    for (var i = 0; i < toasts.length; i++) {
      (function(toast) {
        setTimeout(function() { toast.remove(); }, 5000);
        var closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) {
          closeBtn.addEventListener('click', function() { toast.remove(); });
        }
      })(toasts[i]);
    }
  } catch(e) { console.error("Toast error", e); }

  // 4. Intersection Observer for reveal animations
  try {
    var revealEls = document.querySelectorAll('[data-reveal]');
    if (revealEls.length > 0 && 'IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function(entries) {
        for (var j = 0; j < entries.length; j++) {
          var entry = entries[j];
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
          }
        }
      }, { threshold: 0.1 });
      for (var k = 0; k < revealEls.length; k++) {
        revealEls[k].style.opacity = '0';
        revealEls[k].style.transform = 'translateY(30px)';
        revealEls[k].style.transition = 'all 0.7s cubic-bezier(.4,0,.2,1)';
        observer.observe(revealEls[k]);
      }
    } else {
      // Fallback for very old browsers
      for (var l = 0; l < revealEls.length; l++) {
        revealEls[l].style.opacity = '1';
        revealEls[l].style.transform = 'translateY(0)';
      }
    }
  } catch(e) { console.error("Observer error", e); }

  // 5. Password visibility toggle
  try {
    var toggleBtns = document.querySelectorAll('.toggle-password');
    for (var m = 0; m < toggleBtns.length; m++) {
      toggleBtns[m].addEventListener('click', function(e) {
        e.preventDefault();
        var btn = this;
        var input = btn.previousElementSibling;
        var icon = btn.querySelector('i');
        if (input && input.type === 'password') {
          input.type = 'text';
          icon.className = 'fas fa-eye-slash';
        } else if (input) {
          input.type = 'password';
          icon.className = 'fas fa-eye';
        }
      });
    }
  } catch(e) { console.error("Password toggle error", e); }

  // 6. Password strength meter
  try {
    var pwInput = document.getElementById('password');
    var strengthBar = document.getElementById('strengthBar');
    var strengthText = document.getElementById('strengthText');
    if (pwInput && strengthBar) {
      pwInput.addEventListener('input', function() {
        var val = pwInput.value;
        var score = 0;
        if (val.length >= 6) score++;
        if (val.length >= 10) score++;
        if (/[A-Z]/.test(val)) score++;
        if (/[0-9]/.test(val)) score++;
        if (/[^A-Za-z0-9]/.test(val)) score++;
        var labels = ['', 'Very Weak', 'Weak', 'Fair', 'Strong', 'Very Strong'];
        var colors = ['', '#fc8181', '#f6ad55', '#fbd38d', '#68d391', '#48bb78'];
        var widths = ['0%', '20%', '40%', '60%', '80%', '100%'];
        
        strengthBar.style.width = widths[score] || '0%';
        strengthBar.style.background = colors[score] || 'transparent';
        if (strengthText) {
          strengthText.textContent = labels[score] || '';
        }
      });
    }
  } catch(e) { console.error("Password strength error", e); }

  // 7. Tooltips
  try {
    var tips = document.querySelectorAll('[data-tip]');
    for (var n = 0; n < tips.length; n++) {
      var el = tips[n];
      el.style.position = 'relative';
      var tip = document.createElement('div');
      tip.className = 'field-tip';
      tip.textContent = el.getAttribute('data-tip');
      tip.style.cssText = 'position:absolute;right:0;top:-36px;background:#1a1a26;color:#f0f0f5;font-size:0.75rem;padding:5px 10px;border-radius:6px;white-space:nowrap;opacity:0;pointer-events:none;transition:0.2s;border:1px solid rgba(0,151,167,0.3);z-index:10; box-shadow: 0 4px 12px rgba(0,0,0,0.4);';
      el.appendChild(tip);
      var inputEl = el.querySelector('input,select');
      if (inputEl) {
        (function(t) {
          inputEl.addEventListener('focus', function() { t.style.opacity = '1'; });
          inputEl.addEventListener('blur', function() { t.style.opacity = '0'; });
        })(tip);
      }
    }
  } catch(e) { console.error("Tooltip error", e); }

});
