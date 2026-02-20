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
    const currentScroll = window.pageYOffset;

    if (header) {
        if (currentScroll > 20) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }
    lastScroll = currentScroll;
});

// 3. Staggered Reveal Animation for Cards
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
            // Optional: Stop observing once revealed
            // observer.unobserve(entry.target); 
        }
    });
}, {
    threshold: 0.15,
    rootMargin: "0px 0px -50px 0px" // Trigger slightly before element is fully in view
});

document.querySelectorAll('.reveal, .reveal-footer').forEach(el => observer.observe(el));

// 4. Mobile Footer Accordion Logic
const footerHeaders = document.querySelectorAll('.footer-col h5');

footerHeaders.forEach(header => {
    header.addEventListener('click', () => {
        if (window.innerWidth <= 968) {
            // Close others
            footerHeaders.forEach(otherHeader => {
                if (otherHeader !== header) {
                    otherHeader.parentElement.classList.remove('active');
                }
            });
            // Toggle current
            header.parentElement.classList.toggle('active');
        }
    });
});
