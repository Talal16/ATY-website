
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    const langSelect = document.getElementById('lang-select');
    const allLangElements = document.querySelectorAll('[data-lang]');
    const allLangListItems = document.querySelectorAll('[data-lang-list-item]');

    // Function to update text content based on language
    const updateLanguage = (lang) => {
        // Set document direction
        document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
        document.documentElement.lang = lang;


        // Update text for simple elements
        allLangElements.forEach(el => {
            const key = el.getAttribute('data-lang');
            const translation = key.split('.').reduce((obj, k) => (obj && obj[k] !== 'undefined') ? obj[k] : '', content[lang]);
            if (translation) {
                el.textContent = translation;
            }
        });

        // Update text for list items
        allLangListItems.forEach(el => {
            const key = el.getAttribute('data-lang-list-item');
            const keys = key.split('.');
            const list = keys.slice(0, -1).reduce((obj, k) => (obj && obj[k] !== 'undefined') ? obj[k] : '', content[lang]);
            const index = parseInt(keys.slice(-1)[0]);

            if (list && list[index]) {
                el.textContent = list[index];
            }
        });
    };

    // Handle language selection change
    langSelect.addEventListener('change', () => {
        updateLanguage(langSelect.value);
    });

    // Set initial language from local storage or default to 'en'
    const savedLang = localStorage.getItem('lang') || 'en';
    langSelect.value = savedLang;
    updateLanguage(savedLang);

    // Active page highlighting
    const currentPath = window.location.pathname.split("/").pop();
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Tab functionality for products page
    const tabs = document.querySelectorAll('.tab-link');
    const tabContents = document.querySelectorAll('.tab-content');
    const allContent = document.getElementById('all');

    if (tabs.length > 0 && allContent) {
        // Amalgamate all content into the 'All' tab
        let allHTML = '';
        tabContents.forEach(content => {
            if (content.id !== 'all') {
                allHTML += content.innerHTML;
            }
        });
        allContent.innerHTML = allHTML;
    }


});

function openTab(evt, tabName) {
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.style.display = 'none');

    const tabLinks = document.querySelectorAll('.tab-link');
    tabLinks.forEach(link => link.classList.remove('active'));

    document.getElementById(tabName).style.display = 'block';
    evt.currentTarget.classList.add('active');
}

