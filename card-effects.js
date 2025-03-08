/**
 * Card Effects - Handles mouse movement effects for cards
 * Creates a radial gradient highlight effect that follows the mouse cursor
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize card structures
    initializeCards();
    
    // Set up event handlers
    setupProjectCardEffects();
    setupAboutSectionEffects();
    
    // Prevent layout shifts
    preventLayoutShifts();
});

/**
 * Initialize card structures by ensuring they have proper content wrappers
 */
function initializeCards() {
    // Fix for project cards - ensure they have proper structure
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        // Only wrap content if it's not already wrapped
        if (!card.querySelector('.card-content')) {
            const cardContent = card.innerHTML;
            card.innerHTML = `<div class="card-content">${cardContent}</div>`;
        }
    });
    
    // Fix for about section
    const aboutSection = document.querySelector('.about');
    if (aboutSection && !aboutSection.querySelector('.card-content')) {
        // Create a wrapper for the about content if it doesn't exist
        const aboutContent = aboutSection.innerHTML;
        aboutSection.innerHTML = `
            <div class="card-content">
                ${aboutContent}
            </div>
        `;
    }
}

/**
 * Set up mouse movement effects for project cards
 */
function setupProjectCardEffects() {
    const projectCardsContainer = document.querySelector('.project-cards-container');
    if (projectCardsContainer) {
        projectCardsContainer.onmousemove = e => {
            for (const card of document.querySelectorAll('.project-card')) {
                updateMousePosition(card, e);
            }
        };
    }
}

/**
 * Set up mouse movement effects for the about section
 */
function setupAboutSectionEffects() {
    const aboutSection = document.querySelector('.about');
    if (aboutSection) {
        // Add the same hover effects to the about section
        aboutSection.classList.add('card-with-effect');
        
        // Add before and after pseudo-elements via CSS
        aboutSection.style.position = 'relative';
        aboutSection.style.cursor = 'pointer';
        
        // Handle mouse movement
        aboutSection.onmousemove = e => {
            updateMousePosition(aboutSection, e);
        };
    }
}

/**
 * Update mouse position CSS variables for a card element
 * @param {HTMLElement} element - The card element to update
 * @param {MouseEvent} e - The mouse event
 */
function updateMousePosition(element, e) {
    const rect = element.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    element.style.setProperty("--mouse-x", `${x}px`);
    element.style.setProperty("--mouse-y", `${y}px`);
}

/**
 * Prevent layout shifts by pre-calculating hover states
 */
function preventLayoutShifts() {
    document.querySelectorAll('.project-card, .about').forEach(card => {
        // Create a clone to measure the hovered dimensions
        const clone = card.cloneNode(true);
        clone.style.position = 'absolute';
        clone.style.visibility = 'hidden';
        clone.style.pointerEvents = 'none';
        clone.classList.add('hover-clone');
        
        // Add hover class to simulate hover state
        clone.classList.add('hover-simulation');
        
        // Append to body, measure, then remove
        document.body.appendChild(clone);
        
        // Force layout calculation
        const width = clone.offsetWidth;
        const height = clone.offsetHeight;
        
        // Remove the clone
        document.body.removeChild(clone);
    });
} 