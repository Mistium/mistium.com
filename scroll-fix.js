document.addEventListener('DOMContentLoaded', function() {
    // Prevent overscroll on mobile devices
    document.body.addEventListener('touchmove', function(e) {
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;
        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        
        // If we're at the bottom of the page and trying to scroll further down
        if (windowHeight + scrollTop >= documentHeight - 10) {
            // Check if the touch is moving downward
            if (e.touches[0].clientY < e.touches[0].screenY) {
                e.preventDefault();
            }
        }
        
        // If we're at the top of the page and trying to scroll further up
        if (scrollTop <= 0) {
            // Check if the touch is moving upward
            if (e.touches[0].clientY > e.touches[0].screenY) {
                e.preventDefault();
            }
        }
    }, { passive: false });
    
    // Fix for desktop browsers
    document.addEventListener('wheel', function(e) {
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;
        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        
        // If we're at the bottom of the page and trying to scroll further down
        if (windowHeight + scrollTop >= documentHeight - 10 && e.deltaY > 0) {
            e.preventDefault();
        }
        
        // If we're at the top of the page and trying to scroll further up
        if (scrollTop <= 0 && e.deltaY < 0) {
            e.preventDefault();
        }
    }, { passive: false });
}); 