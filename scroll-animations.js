document.addEventListener('DOMContentLoaded', function() {
    // Add a subtle purple glow to headings
    const headings = document.querySelectorAll('h1, h2, h3');
    headings.forEach(heading => {
        heading.style.textShadow = '0 0 10px rgba(157, 129, 199, 0.2)';
    });

    // Function to check if element is in viewport
    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.bottom >= 0
        );
    }

    // Function to handle scroll animations
    function handleScrollAnimations() {
        // Get all project cards and about section
        const projectCards = document.querySelectorAll('.project-card');
        const aboutSection = document.querySelector('.about');
        
        // Add parallax effect to elements
        const parallaxElements = document.querySelectorAll('.parallax');
        parallaxElements.forEach(element => {
            const speed = element.getAttribute('data-speed') || 0.5;
            const yPos = -(window.scrollY * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });

        // Add subtle rotation to project cards on scroll
        projectCards.forEach(card => {
            if (isInViewport(card)) {
                const scrollPosition = window.scrollY;
                const rotationValue = Math.sin(scrollPosition / 1000) * 1.5; // Reduced rotation
                const scaleValue = 1 + Math.sin(scrollPosition / 1500) * 0.01; // Reduced scale effect
                card.style.transform = `translateY(-5px) rotate(${rotationValue}deg) scale(${scaleValue})`;
            }
        });
        
        // Add subtle color shift to gradient elements on scroll
        const gradientElements = document.querySelectorAll('[class*="gradient"]');
        const scrollPercent = window.scrollY / (document.body.scrollHeight - window.innerHeight);
        const hueShift = Math.floor(scrollPercent * 10); // Reduced hue shift
        
        gradientElements.forEach(element => {
            element.style.filter = `hue-rotate(${hueShift}deg)`;
        });
    }

    // Add parallax class to elements
    document.querySelector('h1').classList.add('parallax');
    document.querySelector('h1').setAttribute('data-speed', '0.2');
    
    // Add smooth scroll behavior to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                document.querySelector(targetId).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Listen for scroll events
    window.addEventListener('scroll', handleScrollAnimations);
    
    // Initial call to set positions
    handleScrollAnimations();
}); 