// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
  // Check if mobile menu toggle exists, if not create it
  let mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
  const navContainer = document.querySelector('.nav-container');
  const navMenu = document.querySelector('.nav-menu');
  
  if (!mobileMenuToggle && navContainer) {
    // Create the toggle button with three bars
    mobileMenuToggle = document.createElement('button');
    mobileMenuToggle.className = 'mobile-menu-toggle';
    mobileMenuToggle.setAttribute('aria-label', 'Toggle navigation menu');
    
    // Add the three bars
    for (let i = 0; i < 3; i++) {
      const span = document.createElement('span');
      mobileMenuToggle.appendChild(span);
    }
    
    // Add it to the navigation container
    navContainer.appendChild(mobileMenuToggle);
  }
  
  // Make sure we have references to both elements
  if (mobileMenuToggle && navMenu) {
    // Toggle menu visibility when hamburger is clicked
    mobileMenuToggle.addEventListener('click', function(e) {
      e.stopPropagation(); // Prevent event from bubbling
      this.classList.toggle('active');
      navMenu.classList.toggle('active');
    });
    
    // Close menu when clicking on a menu item
    const menuItems = document.querySelectorAll('.nav-menu li a');
    menuItems.forEach(item => {
      item.addEventListener('click', function() {
        mobileMenuToggle.classList.remove('active');
        navMenu.classList.remove('active');
      });
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
      if (!navMenu.contains(e.target) && !mobileMenuToggle.contains(e.target)) {
        mobileMenuToggle.classList.remove('active');
        navMenu.classList.remove('active');
      }
    });
  }
  
  // Handle window resize
  window.addEventListener('resize', function() {
    if (window.innerWidth > 768 && navMenu.classList.contains('active')) {
      mobileMenuToggle.classList.remove('active');
      navMenu.classList.remove('active');
    }
  });
});
