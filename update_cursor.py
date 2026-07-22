import re

file_path = r"c:\Janith\Incbotic\index.html"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add cursor HTML right after <body>
cursor_html = """
<div id="cursor-dot"></div>
<div id="cursor-ring"></div>
<div id="cursor-glow"></div>
"""
if '<div id="cursor-dot">' not in content:
    content = content.replace("<body>", f"<body>\n{cursor_html}")

# 2. Add cursor CSS and 3D tilt CSS to <style>
cursor_css = """
  /* --- Custom Cursor --- */
  body {
    cursor: none;
  }
  a, button, select, input, textarea {
    cursor: none !important;
  }
  #cursor-dot {
    position: fixed;
    top: 0; left: 0;
    width: 6px; height: 6px;
    background-color: var(--signal-bright);
    border-radius: 50%;
    pointer-events: none;
    z-index: 10000;
    transform: translate(-50%, -50%);
  }
  #cursor-ring {
    position: fixed;
    top: 0; left: 0;
    width: 32px; height: 32px;
    border: 1.5px solid var(--copper-bright);
    border-radius: 50%;
    pointer-events: none;
    z-index: 9999;
    transform: translate(-50%, -50%);
    transition: width 0.2s, height 0.2s, background-color 0.2s;
  }
  #cursor-glow {
    position: fixed;
    top: 0; left: 0;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(6, 182, 212, 0.08) 0%, transparent 60%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    transform: translate(-50%, -50%);
    transition: transform 0.1s ease-out;
  }
  
  /* --- 3D Parallax on Hero Art --- */
  .hero-art {
    perspective: 1000px;
  }
  .hero-art svg {
    transition: transform 0.1s ease-out;
    transform-style: preserve-3d;
  }
"""
if '/* --- Custom Cursor --- */' not in content:
    content = content.replace("</style>", cursor_css + "\n</style>")

# 3. Add JS for cursor and 3D tilt
cursor_js = """
  // Custom Cursor Logic
  const cursorDot = document.getElementById('cursor-dot');
  const cursorRing = document.getElementById('cursor-ring');
  const cursorGlow = document.getElementById('cursor-glow');

  let mouseX = 0, mouseY = 0;
  let ringX = 0, ringY = 0;

  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    
    // Dot follows immediately
    cursorDot.style.transform = `translate(${mouseX}px, ${mouseY}px)`;
    // Glow follows immediately
    cursorGlow.style.transform = `translate(${mouseX}px, ${mouseY}px)`;
    
    // 3D Tilt for Hero Art
    const heroArt = document.querySelector('.hero-art svg');
    if (heroArt) {
      const rect = heroArt.getBoundingClientRect();
      const artX = rect.left + rect.width / 2;
      const artY = rect.top + rect.height / 2;
      const deltaX = (mouseX - artX) / 15;
      const deltaY = (mouseY - artY) / 15;
      heroArt.style.transform = `rotateX(${-deltaY}deg) rotateY(${deltaX}deg)`;
    }
  });

  // Ring follow with requestAnimationFrame for smooth delay
  function animateRing() {
    ringX += (mouseX - ringX) * 0.2;
    ringY += (mouseY - ringY) * 0.2;
    cursorRing.style.transform = `translate(${ringX}px, ${ringY}px)`;
    requestAnimationFrame(animateRing);
  }
  animateRing();

  // Hover states for cursor
  const interactiveEls = document.querySelectorAll('a, button, input, textarea, select, .glass-card, .showcase-item');
  interactiveEls.forEach(el => {
    el.addEventListener('mouseenter', () => {
      cursorRing.style.width = '48px';
      cursorRing.style.height = '48px';
      cursorRing.style.borderColor = 'var(--signal-bright)';
      cursorRing.style.backgroundColor = 'rgba(20, 184, 166, 0.1)';
    });
    el.addEventListener('mouseleave', () => {
      cursorRing.style.width = '32px';
      cursorRing.style.height = '32px';
      cursorRing.style.borderColor = 'var(--copper-bright)';
      cursorRing.style.backgroundColor = 'transparent';
    });
  });
"""
if '// Custom Cursor Logic' not in content:
    content = content.replace("</script>", cursor_js + "\n</script>")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated cursors and animation!")
