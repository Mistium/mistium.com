import modsData from './mods-data.js';

document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('gravity-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d', { alpha: false }); // High performance non-alpha canvas context

  // Controls
  const searchInput = document.getElementById('gravity-search');
  const zoomInBtn = document.getElementById('zoom-in');
  const zoomOutBtn = document.getElementById('zoom-out');
  const zoomResetBtn = document.getElementById('zoom-reset');

  // Inspector Elements
  const drawer = document.getElementById('inspector-drawer');
  const backdrop = document.getElementById('inspector-backdrop');
  const drawerCloseBtn = document.getElementById('drawer-close');
  const drawerAvatar = document.getElementById('drawer-avatar');
  const drawerName = document.getElementById('drawer-name');
  const drawerBranch = document.getElementById('drawer-branch');
  const drawerCommit = document.getElementById('drawer-commit');
  const drawerGen = document.getElementById('drawer-gen');
  const drawerFollowers = document.getElementById('drawer-followers');
  const drawerForksCount = document.getElementById('drawer-forks-count');
  const drawerOrgName = document.getElementById('drawer-org-name');
  const drawerOrgLink = document.getElementById('drawer-org-link');
  const drawerDesc = document.getElementById('drawer-desc');
  const drawerLineage = document.getElementById('drawer-lineage');
  const drawerForks = document.getElementById('drawer-forks');
  const drawerLaunchBtn = document.getElementById('drawer-launch-btn');

  // Lookup maps
  const modMap = new Map();
  modsData.forEach(m => modMap.set(m.key, m));
  const modIdMap = new Map();
  modsData.forEach(m => modIdMap.set(m.id, m));
  const kidsMap = new Map();
  modsData.forEach(m => kidsMap.set(m.key, m.childrenKeys || []));
  const parentMap = new Map();
  modsData.forEach(m => parentMap.set(m.key, m.parentKey));

  // ---------------------------------------------------------
  // 1. High DPI Canvas Setup
  // ---------------------------------------------------------
  let dpr = window.devicePixelRatio || 1;
  let width = window.innerWidth;
  let height = window.innerHeight;

  function resizeCanvas() {
    dpr = window.devicePixelRatio || 1;
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(dpr, dpr);
  }
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);

  // ---------------------------------------------------------
  // 2. Preload Avatar Images
  // ---------------------------------------------------------
  const imageCache = new Map();
  modsData.forEach(m => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.src = m.avatar;
    img.onerror = () => {
      img.src = 'https://www.google.com/s2/favicons?domain=scratch.mit.edu&sz=128';
    };
    imageCache.set(m.key, img);
  });

  // ---------------------------------------------------------
  // 3. Initialize Nodes with 360° Radial Freedom
  // ---------------------------------------------------------
  const nodes = [];
  const nodeKeyMap = new Map();
  const links = [];

  function getNodeColor(mod) {
    if (mod.key === 'Mistwarp' || mod.isMistium) return '#c299cf';
    if (mod.key === 'Turbowarp') return '#ef4444';
    if (mod.key === 'Penguinmod') return '#00c3ff';
    if (mod.key === 'SnailIDE') return '#10b981';
    if (mod.key === 'Dinosaurmod') return '#84cc16';
    if (['OpenBlock', 'ScratchArduino', 'MakeBlock'].includes(mod.key)) return '#14b8a6';
    if (['Ampmod', 'CodeSnap', 'Shredmod', 'RocketBlocks', 'NitroBolt', 'Nuclearmod'].includes(mod.key)) return '#eab308';
    if (['Cognimates', 'Poseblocks', 'MLFC', 'LearningML', 'Robobo'].includes(mod.key)) return '#ec4899';
    return mod.color || '#ffab19';
  }

  const cx = width / 2;
  const cy = height / 2;

  modsData.forEach((mod, idx) => {
    const depth = mod.depth || 0;
    const color = getNodeColor(mod);
    const directKidsCount = (kidsMap.get(mod.key) || []).length;
    const followers = mod.followers || 0;

    // Balanced Power-Law Sizing Formula:
    // Followers scale with F^0.40 (1000 followers -> +24.5px, 301 followers -> +15.1px, 2 followers -> +2.0px)
    // Direct children scale with K^0.75 (24 kids -> +24.0px, 4 kids -> +6.2px, 0 kids -> 0px)
    const followerTerm = Math.pow(Math.max(0, followers), 0.40) * 1.55;
    const childrenTerm = Math.pow(directKidsCount, 0.75) * 2.2;

    let r = 7.5 + followerTerm + childrenTerm;

    // Physical mass includes inertia scaling logarithmically with child forks
    const mass = 0.5 + Math.pow(r / 8.0, 2.0) + (Math.log(1 + directKidsCount) * 8.0);

    const angle = (idx / modsData.length) * 2 * Math.PI + Math.random() * 0.3;
    const dist = (depth * 48) + 30 + Math.random() * 25;

    let seedX = cx + Math.cos(angle) * dist;
    let seedY = cy + Math.sin(angle) * dist;

    if (mod.key === 'Scratch') { seedX = cx; seedY = cy; }

    const node = {
      mod,
      key: mod.key,
      name: mod.name,
      depth,
      r,
      mass,
      directKidsCount,
      followers,
      color,
      x: seedX,
      y: seedY,
      vx: (Math.random() - 0.5) * 2,
      vy: (Math.random() - 0.5) * 2,
      fx: null,
      fy: null
    };

    nodes.push(node);
    nodeKeyMap.set(mod.key, node);
  });

  // Build Spring Gravitational Links
  // - 0-children moons are kept very close to their parent
  // - Anything with >0 forks is pushed further out logarithmically by ln(1 + forks)
  modsData.forEach(mod => {
    if (mod.parentKey && nodeKeyMap.has(mod.parentKey) && nodeKeyMap.has(mod.key)) {
      const source = nodeKeyMap.get(mod.parentKey);
      const target = nodeKeyMap.get(mod.key);
      const k = target.directKidsCount;
      const sizeRatio = Math.min(source.r, target.r) / Math.max(source.r, target.r);
      
      let length;
      if (k === 0) {
        // Kept tight and close to parent
        length = source.r + target.r + 12 + Math.min(6, Math.sqrt(source.directKidsCount) * 1.0);
      } else {
        // Pushed further out logarithmically by the number of forks it has
        const logFactor = Math.log(1 + k);
        length = source.r + target.r + 18 + (logFactor * 85.0);
        if (sizeRatio > 0.4 && source.r > 25) {
          length += Math.pow(sizeRatio, 2.0) * 80.0;
        }
      }

      links.push({ source, target, length, color: target.color });
    }
  });

  // ---------------------------------------------------------
  // 4. Ultra-Fast Physics Engine
  // ---------------------------------------------------------
  let alpha = 1.0;
  const alphaDecay = 0.993;
  const alphaMin = 0.001;

  function reheatSimulation(amount = 0.8) {
    alpha = Math.max(alpha, amount);
  }

  function updatePhysics() {
    if (alpha < alphaMin && !draggedNode) return;

    const damping = 0.87;

    // 1. Gentle Center Universe Attraction (Allows big planets to spread out)
    nodes.forEach(node => {
      node.vx += (cx - node.x) * 0.0014 * alpha;
      node.vy += (cy - node.y) * 0.0014 * alpha;
    });

    // 2. Parent-Child Pull
    links.forEach(link => {
      const s = link.source;
      const t = link.target;

      const dx = t.x - s.x;
      const dy = t.y - s.y;
      const dist = Math.sqrt(dx * dx + dy * dy) || 1;
      const displacement = dist - link.length;

      const springK = (0.048 + Math.min(0.04, s.directKidsCount * 0.002)) * alpha;
      const force = displacement * springK;
      const fx = (dx / dist) * force;
      const fy = (dy / dist) * force;

      const invMassS = 1 / s.mass;
      const invMassT = 1 / t.mass;
      const totalInvMass = invMassS + invMassT;

      if (s !== draggedNode) {
        s.vx += fx * (invMassS / totalInvMass);
        s.vy += fy * (invMassS / totalInvMass);
      }
      if (t !== draggedNode) {
        t.vx -= fx * (invMassT / totalInvMass);
        t.vy -= fy * (invMassT / totalInvMass);
      }
    });

    // 3. Combined-Mass Multiplied Repulsion + Logarithmic Fork Repulsion
    const numNodes = nodes.length;
    for (let i = 0; i < numNodes; i++) {
      const n1 = nodes[i];
      for (let j = i + 1; j < numNodes; j++) {
        const n2 = nodes[j];
        const dx = n2.x - n1.x;
        const dy = n2.y - n1.y;
        let distSq = dx * dx + dy * dy;
        let dist = Math.sqrt(distSq) || 1;

        const minDist = n1.r + n2.r + 10;

        // Hard boundary touch collision to prevent visual overlap
        if (dist < minDist) {
          const overlap = minDist - dist;
          const invM1 = 1 / n1.mass;
          const invM2 = 1 / n2.mass;
          const totalInvM = invM1 + invM2;

          const px = (dx / dist) * overlap * 0.6;
          const py = (dy / dist) * overlap * 0.6;

          if (n1 !== draggedNode) {
            n1.x -= px * (invM1 / totalInvM);
            n1.y -= py * (invM1 / totalInvM);
          }
          if (n2 !== draggedNode) {
            n2.x += px * (invM2 / totalInvM);
            n2.y += py * (invM2 / totalInvM);
          }
        }

        // Masses Multiplied Force: 36.0 * (m1 * m2)^1.45
        const massProduct = Math.pow(n1.mass * n2.mass, 1.45);
        let repForce = (36.0 * alpha * massProduct) / (distSq + 350);

        // Sibling Children Repulsion: Children of the same fork actively repel each other
        const shareParent = n1.mod.parentKey && n2.mod.parentKey && n1.mod.parentKey === n2.mod.parentKey;
        if (shareParent) {
          repForce += (2800.0 * alpha) / (distSq + 220);
        }

        // Logarithmic Fork Repulsion from Big Bodies / Titans:
        // Pushed outward logarithmically by ln(1 + forks)
        const n1Kids = n1.directKidsCount;
        const n2Kids = n2.directKidsCount;
        const n1HasForks = n1Kids > 0;
        const n2HasForks = n2Kids > 0;
        const n1IsBig = n1.r > 20 || n1.mass > 12;
        const n2IsBig = n2.r > 20 || n2.mass > 12;

        if ((n1HasForks && n2IsBig) || (n2HasForks && n1IsBig)) {
          const logForks = (n1HasForks ? Math.log(1 + n1Kids) : 0) + (n2HasForks ? Math.log(1 + n2Kids) : 0);
          const bigR = Math.max(n1.r, n2.r);
          repForce += (28000.0 * alpha * logForks * Math.pow(bigR / 18.0, 1.2)) / (distSq + 350);
        }

        // Sub-Hub to Sub-Hub Repulsion: (both have >0 children)
        if (n1HasForks && n2HasForks) {
          const combinedLog = Math.log(1 + n1Kids) + Math.log(1 + n2Kids);
          repForce += (32000.0 * alpha * combinedLog) / (distSq + 300);
        }

        // Parent-Child Size Proximity Boost + Logarithmic Sub-tree Ejection
        const isParentChild = (n1.mod.parentKey === n2.key) || (n2.mod.parentKey === n1.key);
        if (isParentChild) {
          const sizeRatio = Math.min(n1.r, n2.r) / Math.max(n1.r, n2.r);
          const parentChildBoost = Math.pow(sizeRatio, 1.8) * 16000.0 * alpha;
          repForce += parentChildBoost / (distSq + 300);

          // Extra logarithmic push only for children with forks (0-child moons get 0 extra push)
          if (n1HasForks || n2HasForks) {
            const childLog = Math.log(1 + (n1HasForks ? n1Kids : n2Kids));
            repForce += (22000.0 * alpha * childLog) / (distSq + 300);
          }
        }

        const rfx = (dx / dist) * repForce;
        const rfy = (dy / dist) * repForce;

        if (n1 !== draggedNode) {
          n1.vx -= rfx / n1.mass;
          n1.vy -= rfy / n1.mass;
        }
        if (n2 !== draggedNode) {
          n2.vx += rfx / n2.mass;
          n2.vy += rfy / n2.mass;
        }
      }
    }

    // 4. Integrate Positions
    nodes.forEach(node => {
      if (node === draggedNode) {
        node.x = node.fx;
        node.y = node.fy;
        node.vx = 0;
        node.vy = 0;
        return;
      }

      node.vx *= damping;
      node.vy *= damping;

      node.x += node.vx;
      node.y += node.vy;
    });

    alpha *= alphaDecay;
  }

  // ---------------------------------------------------------
  // 5. High-Speed Direct GPU Canvas Rendering Loop
  // ---------------------------------------------------------
  let cameraX = 0;
  let cameraY = 0;
  let cameraScale = 0.82;

  let hoveredNode = null;
  let selectedNode = null;
  let draggedNode = null;

  let activeLineageKeys = new Set();

  function updateActiveLineage(node) {
    if (!node) {
      activeLineageKeys.clear();
      return;
    }
    const ancestors = new Set();
    let curr = node.key;
    while (curr) {
      ancestors.add(curr);
      curr = parentMap.get(curr);
    }
    const descendants = new Set();
    function collectKids(k) {
      descendants.add(k);
      (kidsMap.get(k) || []).forEach(collectKids);
    }
    collectKids(node.key);

    activeLineageKeys = new Set([...ancestors, ...descendants]);
  }

  function render() {
    updatePhysics();

    ctx.save();
    // Fill background solid fast
    ctx.fillStyle = '#08070c';
    ctx.fillRect(0, 0, width, height);

    // Apply Camera Transform
    ctx.translate(cameraX, cameraY);
    ctx.scale(cameraScale, cameraScale);

    const hasHighlight = activeLineageKeys.size > 0;

    // 1. Draw Links (Fast Multi-Pass Glowing Lines with Zero Shadow Blur)
    links.forEach(link => {
      const s = link.source;
      const t = link.target;
      const isHighlighted = hasHighlight && activeLineageKeys.has(s.key) && activeLineageKeys.has(t.key);

      ctx.save();
      ctx.beginPath();
      ctx.moveTo(s.x, s.y);
      ctx.lineTo(t.x, t.y);

      if (isHighlighted) {
        // Fast Outer Glow Beam (Wide translucent line)
        ctx.strokeStyle = `${t.color}55`;
        ctx.lineWidth = 7.0;
        ctx.stroke();

        // Crisp Inner Beam
        ctx.beginPath();
        ctx.moveTo(s.x, s.y);
        ctx.lineTo(t.x, t.y);
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2.5;
        ctx.stroke();
      } else if (hasHighlight) {
        ctx.strokeStyle = '#1d1a24';
        ctx.lineWidth = 1.0;
        ctx.globalAlpha = 0.15;
        ctx.stroke();
      } else {
        ctx.strokeStyle = t.color;
        ctx.lineWidth = 1.8;
        ctx.globalAlpha = 0.55;
        ctx.stroke();
      }

      // Directional arrow midway
      const midX = (s.x + t.x) * 0.5;
      const midY = (s.y + t.y) * 0.5;
      const angle = Math.atan2(t.y - s.y, t.x - s.x);
      const arrowSize = isHighlighted ? 6 : 4;

      ctx.beginPath();
      ctx.moveTo(midX + Math.cos(angle) * arrowSize, midY + Math.sin(angle) * arrowSize);
      ctx.lineTo(midX + Math.cos(angle + 2.4) * arrowSize, midY + Math.sin(angle + 2.4) * arrowSize);
      ctx.lineTo(midX + Math.cos(angle - 2.4) * arrowSize, midY + Math.sin(angle - 2.4) * arrowSize);
      ctx.closePath();
      ctx.fillStyle = isHighlighted ? '#ffffff' : (hasHighlight ? '#1d1a24' : t.color);
      ctx.fill();

      ctx.restore();
    });

    // 2. Draw Nodes (Instant GPU Ring Glows)
    nodes.forEach(node => {
      const isSelected = selectedNode === node;
      const isHovered = hoveredNode === node;
      const isHighlighted = hasHighlight && activeLineageKeys.has(node.key);
      const isDimmed = hasHighlight && !isHighlighted;

      ctx.save();
      ctx.globalAlpha = isDimmed ? 0.2 : 1.0;

      // Instant High-Speed Proportional Neon Glow Rings
      if (isSelected || isHovered || isHighlighted) {
        const outerHalo = node.r + Math.max(4, node.r * 0.22);
        const innerHalo = node.r + Math.max(2, node.r * 0.1);

        ctx.beginPath();
        ctx.arc(node.x, node.y, outerHalo, 0, Math.PI * 2);
        ctx.strokeStyle = `${node.color}33`;
        ctx.lineWidth = Math.max(2.5, node.r * 0.14);
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(node.x, node.y, innerHalo, 0, Math.PI * 2);
        ctx.strokeStyle = `${node.color}77`;
        ctx.lineWidth = Math.max(1.8, node.r * 0.08);
        ctx.stroke();
      }

      // Gravitational outer ring for major hubs
      if (node.directKidsCount > 1 || node.r >= 24) {
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.r + 6, 0, Math.PI * 2);
        ctx.strokeStyle = `${node.color}44`;
        ctx.lineWidth = 1.2;
        ctx.stroke();
      }

      // Node Body Circle
      ctx.beginPath();
      ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2);
      ctx.fillStyle = '#110f17';
      ctx.fill();

      // Node Avatar Image (Clipped inside circle)
      const img = imageCache.get(node.key);
      if (img && img.complete && img.naturalWidth > 0) {
        ctx.save();
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.r - 2, 0, Math.PI * 2);
        ctx.clip();
        ctx.drawImage(img, node.x - (node.r - 2), node.y - (node.r - 2), (node.r - 2) * 2, (node.r - 2) * 2);
        ctx.restore();
      }

      // Border Ring
      ctx.beginPath();
      ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2);
      ctx.lineWidth = isSelected || isHovered ? 3.0 : 1.8;
      ctx.strokeStyle = isSelected || isHovered ? '#ffffff' : node.color;
      ctx.stroke();

      // Label Pill
      const labelText = node.name + (node.mod.isMistium ? ' ★' : '');
      const fontSize = node.r >= 35 ? '12px' : (node.r >= 18 ? '11px' : '10px');
      ctx.font = `bold ${fontSize} Syne, sans-serif`;
      const textWidth = ctx.measureText(labelText).width;
      const pillW = Math.max(textWidth + 12, 46);
      const pillH = node.r >= 18 ? 18 : 16;
      const pillX = node.x - pillW / 2;
      const pillY = node.y + node.r + 4;

      ctx.fillStyle = 'rgba(10, 8, 14, 0.88)';
      ctx.beginPath();
      ctx.roundRect(pillX, pillY, pillW, pillH, 4);
      ctx.fill();
      ctx.strokeStyle = isHighlighted || isSelected ? node.color : 'rgba(255,255,255,0.1)';
      ctx.lineWidth = 1;
      ctx.stroke();

      // Label Text
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(labelText, node.x, pillY + pillH / 2);

      ctx.restore();
    });

    ctx.restore();
    requestAnimationFrame(render);
  }

  // ---------------------------------------------------------
  // 6. Interactive Pan, Zoom & Dragging
  // ---------------------------------------------------------
  let isPanning = false;
  let startPanX = 0;
  let startPanY = 0;
  let mouseDownScreenX = 0;
  let mouseDownScreenY = 0;
  let mouseDownHitNode = null;
  let hasDraggedSignificantly = false;

  function screenToWorld(sx, sy) {
    return {
      x: (sx - cameraX) / cameraScale,
      y: (sy - cameraY) / cameraScale
    };
  }

  function findNodeAt(wx, wy) {
    for (let i = nodes.length - 1; i >= 0; i--) {
      const n = nodes[i];
      const dx = wx - n.x;
      const dy = wy - n.y;
      if (dx * dx + dy * dy <= (n.r + 8) * (n.r + 8)) {
        return n;
      }
    }
    return null;
  }

  canvas.addEventListener('mousedown', (e) => {
    mouseDownScreenX = e.clientX;
    mouseDownScreenY = e.clientY;
    hasDraggedSignificantly = false;

    const wpos = screenToWorld(e.clientX, e.clientY);
    const hit = findNodeAt(wpos.x, wpos.y);
    mouseDownHitNode = hit;

    if (hit) {
      draggedNode = hit;
      draggedNode.fx = hit.x;
      draggedNode.fy = hit.y;
      reheatSimulation(0.6);
    } else {
      isPanning = true;
      startPanX = e.clientX - cameraX;
      startPanY = e.clientY - cameraY;
    }
  });

  window.addEventListener('mousemove', (e) => {
    const moveDist = Math.hypot(e.clientX - mouseDownScreenX, e.clientY - mouseDownScreenY);
    if (moveDist > 5) {
      hasDraggedSignificantly = true;
    }

    const wpos = screenToWorld(e.clientX, e.clientY);

    if (draggedNode) {
      draggedNode.fx = wpos.x;
      draggedNode.fy = wpos.y;
      reheatSimulation(0.4);
      return;
    }

    if (isPanning) {
      cameraX = e.clientX - startPanX;
      cameraY = e.clientY - startPanY;
      return;
    }

    // Instant Hover Detection
    const hit = findNodeAt(wpos.x, wpos.y);
    if (hit !== hoveredNode) {
      hoveredNode = hit;
      canvas.style.cursor = hit ? 'pointer' : 'grab';
      if (!selectedNode) {
        updateActiveLineage(hoveredNode);
      }
    }
  });

  window.addEventListener('mouseup', () => {
    if (draggedNode) {
      draggedNode.fx = null;
      draggedNode.fy = null;
      draggedNode = null;
    }
    isPanning = false;

    // Only open inspector if user clicked on a node WITHOUT dragging
    if (mouseDownHitNode && !hasDraggedSignificantly) {
      selectNode(mouseDownHitNode);
    }
    mouseDownHitNode = null;
  });

  // Wheel Zoom
  canvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.12 : 0.89;
    const newScale = Math.min(Math.max(0.2, cameraScale * zoomFactor), 2.5);

    const mouseX = e.clientX;
    const mouseY = e.clientY;

    cameraX = mouseX - (mouseX - cameraX) * (newScale / cameraScale);
    cameraY = mouseY - (mouseY - cameraY) * (newScale / cameraScale);
    cameraScale = newScale;
  }, { passive: false });

  // ---------------------------------------------------------
  // 7. Selection & Inspector Drawer
  // ---------------------------------------------------------
  function selectNode(node) {
    selectedNode = node;
    updateActiveLineage(node);
    reheatSimulation(0.3);
    openInspector(node.mod);
  }

  function flyCameraTo(tx, ty, targetScale = 1.05) {
    cameraScale = targetScale;
    cameraX = width / 2 - tx * cameraScale;
    cameraY = height / 2 - ty * cameraScale;
    reheatSimulation(0.4);
  }

  function centerOnKey(key, targetScale = 1.1) {
    const node = nodeKeyMap.get(key);
    if (!node) return;
    flyCameraTo(node.x, node.y, targetScale);
    selectNode(node);
  }

  function fitOverview() {
    cameraScale = Math.min(width / 950, height / 700, 1.15);
    cameraX = width / 2 - cx * cameraScale;
    cameraY = height / 2 - cy * cameraScale;
    reheatSimulation(0.5);
  }

  // Toolbar actions
  zoomInBtn?.addEventListener('click', () => {
    cameraScale = Math.min(2.5, cameraScale * 1.25);
  });
  zoomOutBtn?.addEventListener('click', () => {
    cameraScale = Math.max(0.2, cameraScale * 0.8);
  });
  zoomResetBtn?.addEventListener('click', fitOverview);

  // Search input
  searchInput?.addEventListener('input', (e) => {
    const q = e.target.value.trim().toLowerCase();
    if (!q) {
      selectedNode = null;
      updateActiveLineage(null);
      return;
    }

    const matched = modsData.find(m =>
      m.name.toLowerCase().includes(q) ||
      (m.githubOrg && m.githubOrg.toLowerCase().includes(q)) ||
      (m.tags && m.tags.some(t => t.toLowerCase().includes(q)))
    );

    if (matched && nodeKeyMap.has(matched.key)) {
      centerOnKey(matched.key, 1.25);
    }
  });

  // ---------------------------------------------------------
  // 8. Inspector Drawer Content
  // ---------------------------------------------------------
  function openInspector(mod) {
    drawerAvatar.src = mod.avatar;
    drawerName.textContent = mod.name;
    drawerBranch.textContent = mod.branchName || mod.branch;
    drawerBranch.style.color = mod.branchColor || mod.color;
    drawerCommit.textContent = `#${mod.commitHash}`;
    drawerGen.textContent = `Gen ${mod.depth}`;

    const fCount = mod.followers || 0;
    const fStr = fCount >= 1000 ? (fCount / 1000).toFixed(1).replace(/\.0$/, '') + 'k' : fCount;
    if (drawerFollowers) {
      drawerFollowers.textContent = `👥 ${fStr} followers`;
      drawerFollowers.style.display = fCount > 0 ? 'inline-block' : 'none';
    }
    if (drawerForksCount) {
      const directForks = (mod.childrenKeys || []).length;
      drawerForksCount.textContent = `🔱 ${directForks} ${directForks === 1 ? 'fork' : 'forks'}`;
    }

    if (mod.githubOrg) {
      drawerOrgName.textContent = `@${mod.githubOrg}`;
      drawerOrgLink.href = mod.githubUrl || `https://github.com/${mod.githubOrg}`;
      drawerOrgLink.style.display = 'inline-flex';
    } else {
      drawerOrgName.textContent = mod.author || 'Community';
      drawerOrgLink.style.display = 'none';
    }

    drawerDesc.textContent = mod.description;
    drawerLaunchBtn.href = mod.url;

    // Lineage breadcrumbs
    drawerLineage.innerHTML = '';
    (mod.lineage || []).forEach((item, idx) => {
      if (idx > 0) {
        const arr = document.createElement('span');
        arr.className = 'trail-arrow';
        arr.textContent = '→';
        drawerLineage.appendChild(arr);
      }
      const chip = document.createElement('button');
      chip.className = 'trail-item';
      chip.textContent = item.name;
      chip.addEventListener('click', () => {
        centerOnKey(item.key, 1.25);
      });
      drawerLineage.appendChild(chip);
    });

    // Child Forks
    drawerForks.innerHTML = '';
    if (mod.childrenKeys && mod.childrenKeys.length > 0) {
      mod.childrenKeys.forEach(childKey => {
        const childMod = modMap.get(childKey);
        if (!childMod) return;
        const forkBtn = document.createElement('button');
        forkBtn.className = 'fork-chip';
        forkBtn.innerHTML = `
          <img src="${childMod.avatar}" style="width: 14px; height: 14px; border-radius: 50%;" onerror="this.src='https://www.google.com/s2/favicons?domain=scratch.mit.edu&sz=128'" />
          <span>${childMod.name}</span>
        `;
        forkBtn.addEventListener('click', () => {
          centerOnKey(childMod.key, 1.25);
        });
        drawerForks.appendChild(forkBtn);
      });
    } else {
      drawerForks.innerHTML = '<span style="font-size: 11.5px; color: var(--text-faint)">No known child branches.</span>';
    }

    drawer.classList.add('open');
    backdrop.classList.add('open');
  }

  function closeDrawer() {
    drawer.classList.remove('open');
    backdrop.classList.remove('open');
    selectedNode = null;
    updateActiveLineage(null);
  }

  drawerCloseBtn?.addEventListener('click', closeDrawer);
  backdrop?.addEventListener('click', closeDrawer);

  // ---------------------------------------------------------
  // 9. Initial Start
  // ---------------------------------------------------------
  fitOverview();
  requestAnimationFrame(render);

  // Handle URL query parameter e.g. /mods?mod=mistwarp
  const urlParams = new URLSearchParams(window.location.search);
  const targetModParam = urlParams.get('mod');
  if (targetModParam) {
    const target = modIdMap.get(targetModParam) || modMap.get(targetModParam);
    if (target) {
      setTimeout(() => {
        centerOnKey(target.key, 1.25);
      }, 200);
    }
  }
});
