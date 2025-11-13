document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initNavigation();
    addScrollAnimations();
    initCopyButtons();
    initBackToTopButton();
});

function initTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;
    const savedTheme = localStorage.getItem('theme') || 'dark';
    
    html.setAttribute('data-theme', savedTheme);
    
    themeToggle.addEventListener('click', function() {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
}

function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.content-section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const sectionId = this.getAttribute('data-section');
            
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            sections.forEach(section => section.classList.remove('active'));
            
            const targetSection = document.getElementById(sectionId);
            if (targetSection) {
                targetSection.classList.add('active');
                window.scrollTo(0, 0);
            }
        });
    });
    
    window.addEventListener('hashchange', function() {
        const hash = window.location.hash.slice(1);
        if (hash) {
            const link = document.querySelector(`[data-section="${hash}"]`);
            if (link) link.click();
        }
    });
}

function addScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeIn 0.5s ease forwards';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.feature-card, .code-block, table').forEach(el => {
        observer.observe(el);
    });
}

function initCopyButtons() {
    const codeBlocks = document.querySelectorAll('.code-block');

    codeBlocks.forEach(block => {
        const button = document.createElement('button');
        button.className = 'copy-btn';
        button.title = 'Copiar código';
        
        const copyIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>`;
        const copiedIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;

        button.innerHTML = copyIcon;
        block.appendChild(button);

        button.addEventListener('click', () => {
            const codeElement = block.querySelector('code');
            const codeToCopy = codeElement.innerText;

            if (navigator.clipboard) {
                navigator.clipboard.writeText(codeToCopy).then(() => {
                    button.innerHTML = copiedIcon;
                    button.classList.add('copied');
                    setTimeout(() => {
                        button.innerHTML = copyIcon;
                        button.classList.remove('copied');
                    }, 2000);
                }).catch(err => {
                    console.error('Error al copiar el código: ', err);
                    button.innerHTML = 'Error';
                });
            }
        });
    });
}

window.addEventListener('scroll', debounce(function() {
    updateActiveSection();
}, 100));

function updateActiveSection() {
    const sections = document.querySelectorAll('.content-section');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let currentSection = null;
    
    sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        if (rect.top <= window.innerHeight / 2) {
            currentSection = section.id;
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-section') === currentSection) {
            link.classList.add('active');
        }
    });
}

function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

function initBackToTopButton() {
    const backToTopButton = document.getElementById('back-to-top');
    const mainContent = document.getElementById('main-content');

    if (!backToTopButton || !mainContent) return;

    mainContent.addEventListener('scroll', () => {
        if (mainContent.scrollTop > 300) {
            backToTopButton.classList.add('visible');
        } else {
            backToTopButton.classList.remove('visible');
        }
    });

    backToTopButton.addEventListener('click', () => {
        mainContent.scrollTo({ top: 0, behavior: 'smooth' });
    });
}
