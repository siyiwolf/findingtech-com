/**
 * Finding Company - Main JavaScript
 */

// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.setAttribute(
                'aria-expanded',
                navMenu.classList.contains('active')
            );
        });

        // Close menu when clicking on a link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '#!') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Add scrolled class to navbar on scroll
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.style.boxShadow = 'var(--shadow-md)';
            } else {
                navbar.style.boxShadow = 'none';
            }
        });
    }

    // Intersection Observer for fade-in animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements with .fade-in class
    document.querySelectorAll('.fade-in').forEach(el => {
        el.classList.add('hidden');
        observer.observe(el);
    });
});

// Analytics (placeholder)
function trackEvent(category, action, label) {
    if (typeof gtag !== 'undefined') {
        gtag('event', action, {
            event_category: category,
            event_label: label
        });
    }
    console.log(`[Analytics] ${category} - ${action} - ${label}`);
}

// Form validation (for future contact forms)
function validateForm(form) {
    const required = form.querySelectorAll('[required]');
    let valid = true;

    required.forEach(field => {
        if (!field.value.trim()) {
            valid = false;
            field.classList.add('error');
        } else {
            field.classList.remove('error');
        }
    });

    return valid;
}

// Newsletter subscription
function subscribeNewsletter(email) {
    fetch('/api/newsletter/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('订阅成功！感谢您的关注。');
        } else {
            alert('订阅失败：' + (data.message || '请稍后重试'));
        }
    })
    .catch(error => {
        console.error('订阅错误：', error);
        alert('网络错误，请稍后重试');
    });
}

// Product image gallery (placeholder for future implementation)
function initProductGallery() {
    const gallery = document.querySelector('.product-gallery');
    if (!gallery) return;

    // Add click handlers for thumbnails
    const thumbs = gallery.querySelectorAll('.thumbnail');
    const mainImg = gallery.querySelector('.main-image img');

    thumbs.forEach(thumb => {
        thumb.addEventListener('click', function() {
            thumbs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            mainImg.src = this.dataset.full;
        });
    });
}