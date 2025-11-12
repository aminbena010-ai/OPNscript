document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initNavigation();
    initSearch();
    addScrollAnimations();
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

function initSearch() {
    const searchInput = document.getElementById('search-bar');
    const searchResults = document.getElementById('search-results');
    
    const searchIndex = createSearchIndex();
    
    searchInput.addEventListener('input', function() {
        const query = this.value.trim().toLowerCase();
        
        if (query.length < 2) {
            searchResults.classList.remove('active');
            return;
        }
        
        const results = performSearch(query, searchIndex);
        displaySearchResults(results, searchResults);
    });
    
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-container')) {
            searchResults.classList.remove('active');
        }
    });
}

function createSearchIndex() {
    const sections = document.querySelectorAll('.content-section');
    const index = [];
    
    sections.forEach(section => {
        const id = section.id;
        const h1 = section.querySelector('h1');
        const title = h1 ? h1.textContent : '';
        
        const content = section.textContent
            .toLowerCase()
            .split('\n')
            .slice(0, 5)
            .join(' ')
            .substring(0, 150);
        
        if (title) {
            index.push({
                id,
                title,
                preview: content,
                fullText: section.textContent.toLowerCase()
            });
        }
    });
    
    return index;
}

function performSearch(query, index) {
    return index.filter(item => {
        return item.title.toLowerCase().includes(query) ||
               item.fullText.includes(query);
    }).slice(0, 5);
}

function displaySearchResults(results, container) {
    if (results.length === 0) {
        container.innerHTML = '<div style="padding: 16px; color: var(--text-tertiary);">No se encontraron resultados</div>';
        container.classList.add('active');
        return;
    }
    
    container.innerHTML = results.map(result => `
        <div class="search-result-item" onclick="document.querySelector('[data-section=\"${result.id}\"]').click()">
            <div class="search-result-title">${result.title}</div>
            <div class="search-result-preview">${result.preview}...</div>
        </div>
    `).join('');
    
    container.classList.add('active');
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
