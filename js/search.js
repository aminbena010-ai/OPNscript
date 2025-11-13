document.addEventListener('DOMContentLoaded', function() {
    initSearch();
});
/**
 * Debounce function to limit the rate at which a function gets called.
 * @param {Function} func The function to debounce.
 * @param {number} delay The delay in milliseconds.
 * @returns {Function} The debounced function.
 */
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}
function initSearch() {
    const searchInput = document.getElementById('search-bar');
    const searchResults = document.getElementById('search-results');
    
    if (!searchInput || !searchResults) return;

    const searchIndex = createSearchIndex();
    
    const debouncedSearch = debounce(function() {
        const query = this.value.trim().toLowerCase();
        
        if (query.length < 2) {
            searchResults.classList.remove('active');
            return;
        }
        
        const results = performSearch(query, searchIndex);
        displaySearchResults(results, searchResults, query);
    }, 250);
    
    searchInput.addEventListener('input', debouncedSearch);
    
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-container')) {
            searchResults.classList.remove('active');
        }
    });
}
function createSearchIndex() {
    const sections = document.querySelectorAll('.content-section');
    const index = [];
    let idCounter = 0;
    
    sections.forEach(section => {
        const sectionTitle = section.querySelector('h1')?.textContent.trim() || 'Sección';
        
        section.querySelectorAll('h1, h2, h3, h4').forEach(heading => {
            if (!heading.id) {
                heading.id = `search-target-${idCounter++}`;
            }
            const title = heading.textContent.trim();
            const parentContent = heading.parentElement.textContent;
            
            let rank = 1;
            if (heading.tagName === 'H1') rank = 5;
            if (heading.tagName === 'H2') rank = 3;
            if (heading.tagName === 'H3') rank = 2;
            
            index.push({
                id: heading.id,
                title: title,
                section: sectionTitle,
                content: parentContent.toLowerCase(),
                rank: rank
            });
        });
    });

    return index;
}
function performSearch(query, index) {
    const results = [];
    const queryParts = query.split(' ').filter(p => p.length > 0);
    
    index.forEach(item => {
        let score = 0;
        const titleLower = item.title.toLowerCase();
        
        queryParts.forEach(part => {
            if (titleLower.includes(part)) {
                score += item.rank * 10; // High score for title match
            }
            if (item.content.includes(part)) {
                score += 1; // Low score for content match
            }
        });
        
        if (score > 0) {
            results.push({ ...item, score });
        }
    });
    
    return results.sort((a, b) => b.score - a.score).slice(0, 7);
}
function displaySearchResults(results, container, query) {
    const highlight = (text, term) => {
        if (!term) return text;
        const regex = new RegExp(`(${term.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    };
    
    container.innerHTML = results.length === 0 
        ? '<div class="search-result-item" style="text-align: center; color: var(--text-tertiary);">No se encontraron resultados</div>'
        : results.map(result => `
            <div class="search-result-item" data-target-id="${result.id}">
                <div class="search-result-title">${highlight(result.title, query)}</div>
                <div class="search-result-preview">${result.section}</div>
            </div>
        `).join('');

    container.classList.add('active');
    
    // Add click listeners to new results
    container.querySelectorAll('.search-result-item').forEach(item => {
        item.addEventListener('click', () => {
            const targetId = item.dataset.targetId;
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                // Find the parent section and activate it
                const parentSection = targetElement.closest('.content-section');
                if (parentSection) {
                    const navLink = document.querySelector(`[data-section="${parentSection.id}"]`);
                    if (navLink) navLink.click();
                }

                // Scroll to the specific heading
                setTimeout(() => {
                    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    targetElement.classList.add('highlight-search');
                    setTimeout(() => targetElement.classList.remove('highlight-search'), 2500);
                }, 100); // Timeout to allow section to become visible
            }
            searchResults.classList.remove('active');
        });
    });
}