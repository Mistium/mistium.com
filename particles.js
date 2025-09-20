document.addEventListener("DOMContentLoaded", function () {
  const canvas = document.createElement("canvas");
  canvas.id = "particles-canvas";
  canvas.style.position = "fixed";
  canvas.style.top = "0";
  canvas.style.left = "0";
  canvas.style.width = "100vw";
  canvas.style.height = "100vh";
  canvas.style.zIndex = "-2";
  canvas.style.pointerEvents = "none";
  document.body.appendChild(canvas);

  const ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const particleCount = 120;
  const particles = [];

  function getThemeColors() {
    const isDark =
      document.documentElement.getAttribute("data-theme") === "dark";
    if (isDark) {
      return [
        "rgba(157, 129, 199, 0.6)",
        "rgba(122, 108, 168, 0.55)",
        "rgba(180, 160, 220, 0.65)",
        "rgba(100, 80, 140, 0.5)",
      ];
    } else {
      return [
        "rgba(157, 129, 199, 0.7)",
        "rgba(122, 108, 168, 0.6)",
        "rgba(190, 180, 220, 0.8)",
        "rgba(210, 200, 240, 0.6)",
      ];
    }
  }

  function createParticles() {
    particles.length = 0;
    const colors = getThemeColors();

    for (let i = 0; i < particleCount; i++) {
      const isLargeParticle = Math.random() > 0.7;

      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: isLargeParticle ? Math.random() * 6 + 4 : Math.random() * 3 + 2,
        color: colors[Math.floor(Math.random() * colors.length)],
        speedX: Math.random() * 1.0 - 0.5,
        speedY: Math.random() * 1.0 - 0.5,
        opacity: Math.random() * 0.5 + 0.4,
        pulse: Math.random() * 0.04 + 0.01,
        pulseDirection: 1,
        maxRadius: isLargeParticle
          ? Math.random() * 6 + 4
          : Math.random() * 3 + 2,
      });
    }
  }

  createParticles();

  function animate() {
    requestAnimationFrame(animate);
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach((particle) => {
      particle.x += particle.speedX;
      particle.y += particle.speedY;

      if (particle.x < 0) particle.x = canvas.width;
      if (particle.x > canvas.width) particle.x = 0;
      if (particle.y < 0) particle.y = canvas.height;
      if (particle.y > canvas.height) particle.y = 0;

      if (particle.radius >= particle.maxRadius) {
        particle.pulseDirection = -1;
      } else if (particle.radius <= particle.maxRadius * 0.7) {
        particle.pulseDirection = 1;
      }

      particle.radius += particle.pulse * particle.pulseDirection;

      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      ctx.fillStyle = particle.color;
      ctx.globalAlpha = particle.opacity;
      ctx.fill();

      ctx.shadowBlur = 15;
      ctx.shadowColor = particle.color;
    });
  }

  let lastW = canvas.width;
  let lastH = canvas.height;
  window.addEventListener("resize", function () {
    const newW = window.innerWidth;
    const newH = window.innerHeight;
    const scaleX = newW / lastW;
    const scaleY = newH / lastH;
    canvas.width = newW;
    canvas.height = newH;

    particles.forEach((p) => {
      p.x *= scaleX;
      p.y *= scaleY;
    });

    const areaOld = lastW * lastH;
    const areaNew = newW * newH;
    const areaRatio = areaNew / areaOld;
    if (areaRatio > 1.2) {
      const target = Math.min(
        Math.round(particleCount * areaRatio),
        particleCount * 2,
      );
      const colors = getThemeColors();
      for (let i = particles.length; i < target; i++) {
        const isLarge = Math.random() > 0.7;
        particles.push({
          x: Math.random() * newW,
          y: Math.random() * newH,
          radius: isLarge ? Math.random() * 6 + 4 : Math.random() * 3 + 2,
          color: colors[Math.floor(Math.random() * colors.length)],
          speedX: Math.random() * 1.0 - 0.5,
          speedY: Math.random() * 1.0 - 0.5,
          opacity: Math.random() * 0.5 + 0.4,
          pulse: Math.random() * 0.04 + 0.01,
          pulseDirection: 1,
          maxRadius: isLarge ? Math.random() * 6 + 4 : Math.random() * 3 + 2,
        });
      }
    } else if (areaRatio < 0.8) {
      const target = Math.max(
        Math.round(particleCount * areaRatio),
        Math.floor(particleCount / 2),
      );
      if (particles.length > target) particles.length = target;
    }
    lastW = newW;
    lastH = newH;
  });

  const observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
      if (mutation.attributeName === "data-theme") {
        createParticles();
      }
    });
  });

  observer.observe(document.documentElement, { attributes: true });

  // Start animation
  animate();
});
