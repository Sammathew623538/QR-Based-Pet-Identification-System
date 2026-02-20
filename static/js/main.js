
// 1. Smooth Toggle Menu with Body Lock
const menuToggle = document.getElementById('mobile-menu');
const navMenu = document.getElementById('nav-menu');
if (menuToggle && navMenu) {
    menuToggle.addEventListener('click', () => {
        menuToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
        document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : 'initial';
    });
    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('click', () => {
            menuToggle.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.style.overflow = 'initial';
        });
    });
}

// 2. Stable Scroll Effect
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const header = document.getElementById('header');
    if (header) {
        const currentScroll = window.pageYOffset;
        if (currentScroll > 20) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        lastScroll = currentScroll;
    }
});

// 3. Staggered Reveal Animation for Cards
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
        }
    });
}, {
    threshold: 0.15,
    rootMargin: "0px 0px -50px 0px"
});
document.querySelectorAll('.reveal, .reveal-footer').forEach(el => observer.observe(el));

// 4. Mobile Footer Accordion Logic
const footerHeaders = document.querySelectorAll('.footer-col h5');
footerHeaders.forEach(header => {
    header.addEventListener('click', () => {
        if (window.innerWidth <= 968) {
            footerHeaders.forEach(otherHeader => {
                if (otherHeader !== header) {
                    otherHeader.parentElement.classList.remove('active');
                }
            });
            header.parentElement.classList.toggle('active');
        }
    });
});

// 5. Auto-dismiss alerts after 5 seconds
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        // Using Bootstrap 5 native dismissal if possible
        if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            } else {
                alert.classList.add('fade-out');
                setTimeout(() => alert.remove(), 1000);
            }
        } else {
            // Fallback smooth removal
            alert.style.transition = "opacity 1s ease, transform 1s ease";
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-40px)";
            setTimeout(() => alert.remove(), 1000);
        }
    });
}, 5000);
