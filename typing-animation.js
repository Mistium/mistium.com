/**
 * Typing Animation - Creates typewriter effect for specified elements
 * Adds a dynamic typing effect to elements with the .typing-text class
 */
document.addEventListener('DOMContentLoaded', function() {
  // Elements with class typing-text will have the typing animation
  const typingElements = document.querySelectorAll('.typing-text');
  
  typingElements.forEach(element => {
    const originalText = element.innerText;
    const typingSpeed = 100; // milliseconds per character
    const startDelay = 500; // wait before starting
    
    // Clear the text initially
    element.innerText = '';
    
    // Start the typing animation after a delay
    setTimeout(() => {
      let i = 0;
      const typingInterval = setInterval(() => {
        if (i < originalText.length) {
          element.innerText += originalText.charAt(i);
          i++;
        } else {
          // Add blinking cursor at the end
          element.classList.add('typing-done');
          clearInterval(typingInterval);
          
          // Optional: Add a blinking cursor after typing is complete
          const cursor = document.createElement('span');
          cursor.classList.add('typing-cursor');
          cursor.innerHTML = '|';
          element.appendChild(cursor);
        }
      }, typingSpeed);
    }, startDelay);
  });
});