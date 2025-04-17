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

    // Particle settings - increased count from 60 to 120
    const particleCount = 120;
    const particles = [];
    
    // Function to get colors based on current theme - increased opacity values
    function getThemeColors() {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        if (isDark) {
            return [
                'rgba(157, 129, 199, 0.6)', // Muted lilac - increased opacity
                'rgba(122, 108, 168, 0.55)', // Muted purple - increased opacity
                'rgba(180, 160, 220, 0.65)', // Light lavender - increased opacity
                'rgba(100, 80, 140, 0.5)'  // Darker purple - increased opacity
            ];
        } else {
            return [
                'rgba(157, 129, 199, 0.7)', // Muted lilac - increased opacity
                'rgba(122, 108, 168, 0.6)', // Muted purple - increased opacity
                'rgba(190, 180, 220, 0.8)', // Light lavender - increased opacity
                'rgba(210, 200, 240, 0.6)'  // Very light lilac - increased opacity
            ];
        }
    }
    
    // Create particles
    function createParticles() {
        particles.length = 0; // Clear existing particles
        const colors = getThemeColors();
        
        for (let i = 0; i < particleCount; i++) {
            // Create different types of particles for visual variety
            const isLargeParticle = Math.random() > 0.7; // 30% chance of being a large particle
            
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                // Increased size range from (1-4) to (2-8)
                radius: isLargeParticle ? Math.random() * 6 + 4 : Math.random() * 3 + 2,
                color: colors[Math.floor(Math.random() * colors.length)],
                // Increased movement speed from (-0.2 to 0.2) to (-0.5 to 0.5)
                speedX: Math.random() * 1.0 - 0.5,
                speedY: Math.random() * 1.0 - 0.5,
                // Increased opacity from (0.2-0.6) to (0.4-0.9)
                opacity: Math.random() * 0.5 + 0.4,
                // Add pulse effect
                pulse: Math.random() * 0.04 + 0.01,
                pulseDirection: 1,
                maxRadius: isLargeParticle ? Math.random() * 6 + 4 : Math.random() * 3 + 2
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
            
            // Add pulsing effect to make particles more dynamic
            if (particle.radius >= particle.maxRadius) {
                particle.pulseDirection = -1;
            } else if (particle.radius <= particle.maxRadius * 0.7) {
                particle.pulseDirection = 1;
            }
            
            particle.radius += particle.pulse * particle.pulseDirection;

            // Draw particle
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            ctx.fillStyle = particle.color;
            ctx.globalAlpha = particle.opacity;
            ctx.fill();
            
            // Enhanced glow effect - increased blur value from 10 to 15
            ctx.shadowBlur = 15;
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