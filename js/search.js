document.addEventListener('DOMContentLoaded', function() {
    initSearch();
});

function initSearch() {
    const searchInput = document.getElementById('search-bar');
    const searchResults = document.getElementById('search-results');
    
    if (!searchInput || !searchResults) return;

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
        const title = h1 ? h1.textContent.trim() : '';
        const content = section.textContent.replace(/\s+/g, ' ').substring(0, 150);
        
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
    container.innerHTML = results.length === 0 
        ? '<div class="search-result-item" style="text-align: center; color: var(--text-tertiary);">No se encontraron resultados</div>'
        : results.map(result => `
            <div class="search-result-item" onclick="document.querySelector('[data-section=\\'${result.id}\\']').click(); document.getElementById('search-results').classList.remove('active');">
                <div class="search-result-title">${result.title}</div>
                <div class="search-result-preview">${result.preview}...</div>
            </div>
        `).join('');
    
    container.classList.add('active');
}