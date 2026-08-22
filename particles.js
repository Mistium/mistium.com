(() => {
  let canvas = document.getElementById("starfield");
  if (!canvas) {
    canvas = document.createElement("canvas");
    canvas.id = "starfield";
    Object.assign(canvas.style, {
      position: "fixed",
      inset: "0",
      width: "100vw",
      height: "100vh",
      zIndex: "-2",
      pointerEvents: "none",
    });
    document.body.appendChild(canvas);
  }
  const ctx = canvas.getContext("2d");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  let width = window.innerWidth;
  let height = window.innerHeight;
  let lastTime = performance.now();
  let animationFrame = 0;

  function sizeCanvas() {
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width * ratio;
    canvas.height = height * ratio;
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  }

  function createStar() {
    return {
      x: Math.random() * width,
      y: Math.random() * height,
      z: Math.random(),
      size: Math.random() < 0.3 ? 1.5 + Math.random() : 0.8 + Math.random() * 0.6,
      baseOpacity: 0.4 + Math.random() * 0.55,
      twinkleSpeed: 1.5 + Math.random() * 3,
      twinkleOffset: Math.random() * Math.PI * 2,
    };
  }

  function createShootingStar() {
    const angle = (20 + Math.random() * 20) * Math.PI / 180;
    return {
      x: Math.random() * width * 0.5 - 100,
      y: Math.random() * height * 0.4,
      angle,
      speed: 500 + Math.random() * 400,
      length: 80 + Math.random() * 100,
      life: 0,
      maxLife: 0.8 + Math.random() * 1.2,
      active: true,
    };
  }

  sizeCanvas();
  const stars = Array.from({ length: 100 }, createStar);
  const shootingStars = Array.from({ length: 3 }, (_, index) => {
    const star = createShootingStar();
    star.life = -index * 3;
    star.active = false;
    return star;
  });

  function drawStar(star, time) {
    const twinkle = Math.sin(time * 0.001 * star.twinkleSpeed + star.twinkleOffset);
    const opacity = star.baseOpacity * (0.5 + 0.5 * twinkle);
    const depthScale = 0.3 + star.z * 0.7;
    ctx.globalAlpha = opacity * depthScale;
    ctx.fillStyle = "#fff";
    ctx.beginPath();
    ctx.arc(star.x, star.y, star.size * depthScale, 0, Math.PI * 2);
    ctx.fill();
  }

  function drawShootingStar(star) {
    if (!star.active) return;
    const progress = star.life / star.maxLife;
    let opacity = 1;
    if (progress < 0.05) opacity = progress / 0.05;
    if (progress > 0.75) opacity = (1 - progress) / 0.25;
    opacity = Math.max(0, Math.min(1, opacity)) * 0.85;

    const tailX = star.x - Math.cos(star.angle) * star.length;
    const tailY = star.y - Math.sin(star.angle) * star.length;
    const gradient = ctx.createLinearGradient(tailX, tailY, star.x, star.y);
    gradient.addColorStop(0, "rgba(255,255,255,0)");
    gradient.addColorStop(0.25, `rgba(255,255,255,${0.1 * opacity})`);
    gradient.addColorStop(0.7, `rgba(255,255,255,${0.55 * opacity})`);
    gradient.addColorStop(0.9, `rgba(255,255,255,${0.9 * opacity})`);
    gradient.addColorStop(1, `rgba(255,255,255,${opacity})`);
    ctx.globalAlpha = 1;
    ctx.strokeStyle = gradient;
    ctx.lineWidth = 1.5;
    ctx.lineCap = "round";
    ctx.beginPath();
    ctx.moveTo(tailX, tailY);
    ctx.lineTo(star.x, star.y);
    ctx.stroke();
    ctx.globalAlpha = opacity * 0.9;
    ctx.fillStyle = "#fff";
    ctx.beginPath();
    ctx.arc(star.x, star.y, 1.5, 0, Math.PI * 2);
    ctx.fill();
  }

  function resetShootingStar(star) {
    Object.assign(star, createShootingStar());
  }

  function drawStatic() {
    ctx.clearRect(0, 0, width, height);
    stars.forEach(star => drawStar(star, 0));
    ctx.globalAlpha = 1;
  }

  function update(time) {
    const delta = Math.min((time - lastTime) / 1000, 0.1);
    lastTime = time;
    ctx.clearRect(0, 0, width, height);
    stars.forEach(star => drawStar(star, time));

    shootingStars.forEach(star => {
      if (star.active) {
        star.life += delta;
        star.x += Math.cos(star.angle) * star.speed * delta;
        star.y += Math.sin(star.angle) * star.speed * delta;
        if (star.life >= star.maxLife || star.x > width + 200 || star.y > height + 200) {
          resetShootingStar(star);
          star.active = false;
          star.life = -(2 + Math.random() * 4);
        }
      } else {
        star.life += delta;
        if (star.life >= 0) resetShootingStar(star);
      }
      drawShootingStar(star);
    });

    ctx.globalAlpha = 1;
    animationFrame = requestAnimationFrame(update);
  }

  function start() {
    cancelAnimationFrame(animationFrame);
    if (reducedMotion.matches) {
      drawStatic();
    } else {
      lastTime = performance.now();
      animationFrame = requestAnimationFrame(update);
    }
  }

  window.addEventListener("resize", () => {
    sizeCanvas();
    stars.forEach(star => Object.assign(star, createStar()));
    if (reducedMotion.matches) drawStatic();
  });
  reducedMotion.addEventListener("change", start);
  start();
})();
