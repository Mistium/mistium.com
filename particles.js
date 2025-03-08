document.addEventListener('DOMContentLoaded', function() {
    // Create canvas element
    const canvas = document.createElement('canvas');
    canvas.id = 'particles-canvas';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.zIndex = '-2';
    canvas.style.pointerEvents = 'none';
    document.body.appendChild(canvas);

    // Set canvas size
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Particle settings
    const particleCount = 60;
    const particles = [];
    
    // Function to get colors based on current theme
    function getThemeColors() {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        if (isDark) {
            return [
                'rgba(157, 129, 199, 0.3)', // Muted lilac
                'rgba(122, 108, 168, 0.25)', // Muted purple
                'rgba(180, 160, 220, 0.35)', // Light lavender
                'rgba(100, 80, 140, 0.2)'  // Darker purple
            ];
        } else {
            return [
                'rgba(157, 129, 199, 0.4)', // Muted lilac
                'rgba(122, 108, 168, 0.3)', // Muted purple
                'rgba(190, 180, 220, 0.5)', // Light lavender
                'rgba(210, 200, 240, 0.3)'  // Very light lilac
            ];
        }
    }
    
    // Create particles
    function createParticles() {
        particles.length = 0; // Clear existing particles
        const colors = getThemeColors();
        
        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                radius: Math.random() * 3 + 1,
                color: colors[Math.floor(Math.random() * colors.length)],
                speedX: Math.random() * 0.4 - 0.2,
                speedY: Math.random() * 0.4 - 0.2,
                opacity: Math.random() * 0.4 + 0.2
            });
        }
    }
    
    createParticles();

    // Animation function
    function animate() {
        requestAnimationFrame(animate);
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Update and draw particles
        particles.forEach(particle => {
            // Move particles
            particle.x += particle.speedX;
            particle.y += particle.speedY;

            // Wrap around edges
            if (particle.x < 0) particle.x = canvas.width;
            if (particle.x > canvas.width) particle.x = 0;
            if (particle.y < 0) particle.y = canvas.height;
            if (particle.y > canvas.height) particle.y = 0;

            // Draw particle
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            ctx.fillStyle = particle.color;
            ctx.globalAlpha = particle.opacity;
            ctx.fill();
            
            // Add subtle glow effect
            ctx.shadowBlur = 10;
            ctx.shadowColor = particle.color;
        });
    }

    // Handle window resize
    window.addEventListener('resize', function() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        createParticles(); // Recreate particles on resize
    });
    
    // Listen for theme changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'data-theme') {
                createParticles(); // Recreate particles with new theme colors
            }
        });
    });
    
    observer.observe(document.documentElement, { attributes: true });

    // Start animation
    animate();
}); 