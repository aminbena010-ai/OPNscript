document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initNavigation();
    addScrollAnimations();
    initCopyButtons();
    initBackToTopButton();
    initRatingModal();
    initSettings();
    initInstallationTabs();
    initSyntaxHighlighting();
    initDataVault();
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
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    const mainContent = document.getElementById('main-content');
    
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
                scrollSidebarToActiveLink(this);
                // Cerrar sidebar en móvil al seleccionar una sección
                if (window.innerWidth <= 1024) {
                    sidebar.classList.remove('active');
                    overlay.classList.remove('active');
                }
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

    // Lógica para el menú en móvil
    if (menuToggle && sidebar && overlay) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
            if (sidebar.classList.contains('active')) {
                menuToggle.setAttribute('aria-label', 'Cerrar menú');
                // Mover foco al primer elemento del menú
                sidebar.querySelector('a').focus();
            } else {
                menuToggle.setAttribute('aria-label', 'Abrir menú');
            }
        });

        overlay.addEventListener('click', () => {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
            menuToggle.setAttribute('aria-label', 'Abrir menú');
        });
    }
}

function scrollSidebarToActiveLink(activeLink) {
    const sidebar = document.getElementById('sidebar-nav');
    if (!sidebar || !activeLink) return;

    const topPos = activeLink.offsetTop;
    sidebar.scrollTo({ top: topPos - (sidebar.clientHeight / 2) + (activeLink.clientHeight / 2), behavior: 'smooth' });
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
    
    document.querySelectorAll('.content-section h1, .content-section h2, .content-section h3, .content-section p, .content-section ul, .content-section ol, .feature-card, .code-block, .reference-table, .colors-grid, .info-box, .warning-box, .contact-button, .giscus-container, .setting-item, .stats-container').forEach(el => {
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
    
    // Usa main-content para el cálculo del viewport
    const mainContent = document.getElementById('main-content');
    sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        // Considera una sección como activa si está en la mitad superior de la pantalla
        if (rect.top <= mainContent.clientHeight / 2 && rect.bottom >= mainContent.clientHeight / 2) {
            currentSection = section.id;
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-section') === currentSection) {
            link.classList.add('active');
            scrollSidebarToActiveLink(link);
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

    const shouldShowModal = localStorage.getItem('ratingModalDisabled') !== 'true' && !localStorage.getItem('opnRatingDone');

    // Mostrar modal después de 15 segundos, si está permitido y no se ha hecho antes.
    if (shouldShowModal) {
        setTimeout(() => {
            modal.classList.add('visible');
        }, 15000);
    }

    closeModalBtn.addEventListener('click', () => {
        modal.classList.remove('visible');
        // Marcar como interactuado para no volver a mostrarlo.
        localStorage.setItem('opnRatingDone', 'true');
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
            // Marcar como hecho y cerrar.
            localStorage.setItem('opnRatingDone', 'true');
            modal.classList.remove('visible');
        }
    });
}

function initSettings() {
    const animationsToggle = document.getElementById('animations-toggle');
    const resetRatingBtn = document.getElementById('reset-rating-btn');
    const ratingModalToggle = document.getElementById('rating-modal-toggle');

    // Cargar estado de las animaciones
    const animationsEnabled = localStorage.getItem('animationsEnabled') !== 'false';
    animationsToggle.checked = animationsEnabled;
    if (!animationsEnabled) {
        document.body.classList.add('no-animations');
    } else {
        // Re-observar elementos si las animaciones se reactivan
        addScrollAnimations();
    }

    animationsToggle.addEventListener('change', () => {
        if (animationsToggle.checked) {
            localStorage.setItem('animationsEnabled', 'true');
            document.body.classList.remove('no-animations');
            // Re-inicializar las animaciones para que los elementos ya visibles no parpadeen
            document.querySelectorAll('.animate-on-scroll').forEach(el => el.classList.remove('is-visible'));
            addScrollAnimations();
        } else {
            localStorage.setItem('animationsEnabled', 'false');
            document.body.classList.add('no-animations');
        }
    });

    resetRatingBtn.addEventListener('click', () => {
        localStorage.removeItem('opnRatingDone');
        localStorage.removeItem('ratingModalDisabled');
        ratingModalToggle.checked = true;
        alert('Estado de valoración restablecido. El aviso aparecerá en tu próxima visita.');
    });

    // Cargar estado del modal de valoración
    const ratingModalDisabled = localStorage.getItem('ratingModalDisabled') === 'true';
    ratingModalToggle.checked = !ratingModalDisabled;

    ratingModalToggle.addEventListener('change', () => {
        if (ratingModalToggle.checked) {
            localStorage.removeItem('ratingModalDisabled');
            alert('Aviso de valoración activado.');
        } else {
            localStorage.setItem('ratingModalDisabled', 'true');
            alert('Aviso de valoración desactivado permanentemente.');
        }
    });
}

function initDataVault() {
    // Simulación de un "almacén de datos"
    const dataVault = {
        setData: function(key, value) {
            const jsonValue = JSON.stringify(value);
            // "Cifrado" simple usando Base64
            const encryptedValue = btoa(jsonValue);
            localStorage.setItem(`vault_${key}`, encryptedValue);
        },
        getData: function(key) {
            const encryptedValue = localStorage.getItem(`vault_${key}`);
            if (!encryptedValue) return null;
            try {
                // "Descifrado"
                const jsonValue = atob(encryptedValue);
                return JSON.parse(jsonValue);
            } catch (e) {
                console.error("Error al descifrar los datos de la bóveda:", e);
                return null;
            }
        }
    };

    // Ejemplo de uso: Guardar la última sección visitada
    window.addEventListener('hashchange', () => {
        const hash = window.location.hash;
        if (hash) {
            dataVault.setData('last_visited_section', hash);
        }
    });

    // Puedes acceder a los datos desde la consola del navegador con:
    // atob(localStorage.getItem('vault_last_visited_section'))
}

function initInstallationTabs() {
    const tabButtons = document.querySelectorAll('.os-tab-btn');
    const tabContents = document.querySelectorAll('.os-instructions-content');

    if (tabButtons.length === 0 || tabContents.length === 0) return;

    const activateTab = (os) => {
        tabButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.os === os);
        });
        tabContents.forEach(content => {
            content.classList.toggle('active', content.dataset.os === os);
        });
    };

    // Detectar OS y activar la pestaña correcta al cargar
    const userAgent = window.navigator.userAgent;
    let detectedOS;
    if (userAgent.includes("Win")) {
        detectedOS = "windows";
    } else if (userAgent.includes("Mac")) {
        detectedOS = "macos";
    } else if (userAgent.includes("Linux")) {
        detectedOS = "linux";
    } else {
        detectedOS = "windows"; // Por defecto
    }
    activateTab(detectedOS);

    // Añadir listeners para cambio manual
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const os = button.dataset.os;
            activateTab(os);
        });
    });
}

function initSyntaxHighlighting() {
    const opnKeywords = ['let', 'set', 'if', 'else', 'for', 'in', 'func', 'return', 'main', 'true', 'false'];
    const opnFunctions = ['py.print', 'py.input', 'py.random.randint', 'gfx.setup_canvas', 'gfx.draw_circle', 'gfx.draw_point', 'gfx.update_screen', 'gfx.get_random_color', 'c.printf', 'cpp.cout', 'cs.write_line', 'js.log', 'to_string', 'to_number', 'range'];

    const highlight = (code) => {
        return code
            // Comments
            .replace(/#.*$/gm, (match) => `<span class="token-comment">${match}</span>`)
            // Strings
            .replace(/&quot;([^&]*)&quot;/g, (match, p1) => `&quot;<span class="token-string">${p1}</span>&quot;`)
            // Keywords
            .replace(new RegExp(`\\b(${opnKeywords.join('|')})\\b`, 'g'), '<span class="token-keyword">$1</span>')
            // Functions
            .replace(new RegExp(`(${opnFunctions.join('|').replace('.', '\\.')})`, 'g'), '<span class="token-function">$1</span>')
            // Numbers
            .replace(/\b(\d+(\.\d+)?)\b/g, '<span class="token-number">$1</span>');
    };

    document.querySelectorAll('.code-block[data-lang="opn"] code, .code-block[data-lang="shell"] code').forEach(block => {
        // Evitar doble resaltado
        if (block.querySelector('.token-keyword')) return;

        // Escapar HTML para procesar, excepto los <br>
        let code = block.innerHTML
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/&lt;br&gt;/g, '<br>');

        if (block.closest('[data-lang="opn"]')) {
            block.innerHTML = highlight(code);
        }
    });
}
