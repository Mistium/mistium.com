document.addEventListener('DOMContentLoaded', function() {
    // Create theme toggle button
    const themeToggle = document.createElement('div');
    themeToggle.className = 'theme-toggle';
    themeToggle.innerHTML = `
        <svg class="sun-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3zm-9 4h2c.55 0 1-.45 1-1s-.45-1-1-1H3c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h-2c-.55 0-1-.45-1-1s.45-1 1-1h2c.55 0 1 .45 1 1s-.45 1-1 1zM13 3v2c0 .55.45 1 1 1s1-.45 1-1V3c0-.55-.45-1-1-1s-1 .45-1 1zm0 16v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41.39.39 1.03.39 1.41 0l1.06-1.06zM7.05 18.36c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41.39.39 1.03.39 1.41 0l1.06-1.06z"/>
        </svg>
        <svg class="moon-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" style="display:none;">
            <path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z"/>
        </svg>
    `;
    document.body.appendChild(themeToggle);

    // Check for saved theme preference or use device preference
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    const savedTheme = localStorage.getItem('theme');
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDarkScheme.matches)) {
        document.documentElement.setAttribute('data-theme', 'dark');
        toggleThemeIcons(true);
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        toggleThemeIcons(false);
    }

    // Toggle theme on button click
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        toggleThemeIcons(newTheme === 'dark');
    });

    function toggleThemeIcons(isDark) {
        const sunIcon = document.querySelector('.sun-icon');
        const moonIcon = document.querySelector('.moon-icon');
        
        if (isDark) {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
        } else {
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
        }
    }

    // Add highlight elements to cards
    const cards = document.querySelectorAll('.project-card, .profile-card, .about');
    cards.forEach(card => {
        const highlight = document.createElement('div');
        highlight.className = 'card-highlight';
        card.appendChild(highlight);
        
        // Windows-like highlight effect that follows mouse
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Calculate distance from each edge
            const top = y;
            const right = rect.width - x;
            const bottom = rect.height - y;
            const left = x;
            
            // Find the closest edge
            const min = Math.min(top, right, bottom, left);
            
            // Reset all borders
            highlight.style.borderTop = 'none';
            highlight.style.borderRight = 'none';
            highlight.style.borderBottom = 'none';
            highlight.style.borderLeft = 'none';
            
            // Highlight the closest edge
            if (min === top) {
                highlight.style.borderTop = '2px solid var(--accent-primary)';
            } else if (min === right) {
                highlight.style.borderRight = '2px solid var(--accent-primary)';
            } else if (min === bottom) {
                highlight.style.borderBottom = '2px solid var(--accent-primary)';
            } else if (min === left) {
                highlight.style.borderLeft = '2px solid var(--accent-primary)';
            }
        });
        
        // Remove highlight when mouse leaves
        card.addEventListener('mouseleave', function() {
            highlight.style.borderTop = 'none';
            highlight.style.borderRight = 'none';
            highlight.style.borderBottom = 'none';
            highlight.style.borderLeft = 'none';
        });
    });
}); 