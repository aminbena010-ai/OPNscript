document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initNavigation();
    addScrollAnimations();
    initCopyButtons();
    initBackToTopButton();
    initRatingModal();
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
                document.getElementById('main-content').scrollTo(0, 0);
            }
        });
    });
    
    // Permite cargar una sección desde el hash de la URL al cargar la página
    window.addEventListener('hashchange', function() {
        const hash = window.location.hash.slice(1);
        if (hash) {
            const link = document.querySelector(`[data-section="${hash}"]`);
            if (link) link.click();
            else { // Para secciones ocultas sin link
                const section = document.getElementById(hash);
                if (section && section.classList.contains('content-section')) {
                    document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
                    section.classList.add('active');
                    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                }
            }
        }
    });
    
    // Dispara el evento hashchange en la carga inicial
    if (window.location.hash) {
        window.dispatchEvent(new HashChangeEvent('hashchange'));
    }
}

function addScrollAnimations() {
    const observerOptions = {
        threshold: 0.05,
        rootMargin: '0px 0px -40px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.content-section h1, .content-section h2, .content-section h3, .content-section p, .content-section ul, .content-section ol, .feature-card, .code-block, .reference-table, .colors-grid, .info-box, .warning-box, .contact-button, .giscus-container').forEach(el => {
        el.classList.add('animate-on-scroll');
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

function initRatingModal() {
    const modal = document.getElementById('rating-modal');
    const closeModalBtn = document.getElementById('close-rating-modal');
    const stars = document.querySelectorAll('.rating-stars span');
    const feedback = document.getElementById('rating-feedback');
    const submitBtn = document.getElementById('submit-rating');

    if (!modal) return;

    let currentRating = 0;
    const feedbackMessages = [
        "Necesita mejorar",
        "Podría ser mejor",
        "Está bien",
        "¡Buen trabajo!",
        "¡Excelente!"
    ];

    // Mostrar modal después de 15 segundos, solo si no se ha mostrado antes en la sesión
    if (!sessionStorage.getItem('ratingModalShown')) {
        setTimeout(() => {
            modal.classList.add('visible');
            sessionStorage.setItem('ratingModalShown', 'true');
        }, 15000);
    }

    closeModalBtn.addEventListener('click', () => {
        modal.classList.remove('visible');
    });

    stars.forEach(star => {
        star.addEventListener('mouseover', () => {
            stars.forEach(s => s.textContent = '☆');
            for (let i = 0; i < star.dataset.value; i++) {
                stars[i].textContent = '★';
            }
        });

        star.addEventListener('mouseout', () => {
            stars.forEach(s => s.textContent = '☆');
            for (let i = 0; i < currentRating; i++) {
                stars[i].textContent = '★';
            }
        });

        star.addEventListener('click', () => {
            currentRating = star.dataset.value;
            feedback.textContent = feedbackMessages[currentRating - 1];
            submitBtn.disabled = false;
        });
    });

    submitBtn.addEventListener('click', () => {
        if (currentRating > 0) {
            const subject = `Valoración para OPN: ${currentRating}/5 estrellas`;
            const body = `Hola,\n\nMi valoración para el lenguaje OPN es de ${currentRating} de 5 estrellas.\n\nFeedback adicional:\n`;
            window.open(`mailto:amin.bena010@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`);
            modal.classList.remove('visible');
        }
    });
}
