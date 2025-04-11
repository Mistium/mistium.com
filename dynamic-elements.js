/**
 * Dynamic Elements - Adds interactive and animated elements to the website
 * Includes scroll-activated animations, counters, and filtering functionality
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all dynamic elements
    initSkillBars();
    initCounters();
    
    // Re-check elements visibility on scroll
    window.addEventListener('scroll', function() {
        checkElementsVisibility();
    });
    
    // Initial check for elements in viewport
    checkElementsVisibility();
});

/**
 * Initialize animated skill bars
 */
function initSkillBars() {
    const skillBars = document.querySelectorAll('.skill-progress');
    
    skillBars.forEach(bar => {
        // Store the target progress percentage
        const progress = bar.getAttribute('data-progress');
        
        // Set initial width to 0
        bar.style.width = '0%';
        
        // Add to elements to animate when visible
        bar.classList.add('animate-on-scroll');
        
        // Store the target value as a data attribute
        bar.setAttribute('data-target-width', progress + '%');
    });
}

/**
 * Initialize counter animations
 */
function initCounters() {
    const counters = document.querySelectorAll('.stat-count');
    
    counters.forEach(counter => {
        // Get the target count value
        const target = parseInt(counter.getAttribute('data-count'));
        
        // Add to elements to animate when visible (but don't reset value)
        counter.classList.add('animate-on-scroll');
        
        // Store the target value
        counter.setAttribute('data-target-count', target);
    });
}

/**
 * Check if elements are visible in the viewport and animate them
 */
function checkElementsVisibility() {
    const elementsToAnimate = document.querySelectorAll('.animate-on-scroll');
    
    elementsToAnimate.forEach(element => {
        if (isElementInViewport(element) && !element.classList.contains('animated')) {
            element.classList.add('animated');
            
            // Animate counters
            if (element.classList.contains('stat-count')) {
                animateCounter(element);
            }
            
            // Animate skill bars
            if (element.classList.contains('skill-progress')) {
                animateSkillBar(element);
            }
        }
    });
}

/**
 * Animate a counter from 0 to target value
 * @param {HTMLElement} counterElement - The counter element to animate
 */
function animateCounter(counterElement) {
    const target = parseInt(counterElement.getAttribute('data-target-count'));
    const current = parseInt(counterElement.textContent);
    
    // If the current value is already the target, skip animation
    if (current === target) return;
    
    const duration = 2000; // 2 seconds
    const stepTime = 20; // update every 20ms
    
    // Dynamically calculate increment based on target value
    let increment = target / (duration / stepTime);
    let currentValue = 0;
    
    const timer = setInterval(() => {
        currentValue += increment;
        
        // Update the counter text
        counterElement.textContent = Math.floor(currentValue);
        
        // Stop the animation when target is reached
        if (currentValue >= target) {
            clearInterval(timer);
            counterElement.textContent = target; // Ensure final value is exact
        }
    }, stepTime);
}

/**
 * Animate a skill bar from 0 to target width
 * @param {HTMLElement} skillBar - The skill bar element to animate
 */
function animateSkillBar(skillBar) {
    const targetWidth = skillBar.getAttribute('data-target-width');
    const duration = 1500; // 1.5 seconds
    
    // Use CSS transition for smoother animation
    skillBar.style.transition = `width ${duration}ms ease-out`;
    
    // Trigger reflow to ensure the transition applies
    void skillBar.offsetWidth;
    
    // Set the final width
    skillBar.style.width = targetWidth;
}

/**
 * Check if an element is in the viewport
 * @param {HTMLElement} element - The element to check
 * @returns {boolean} - True if the element is in the viewport
 */
function isElementInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.8 &&
        rect.left >= 0 &&
        rect.bottom >= 0 &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}