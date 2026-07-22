import re

file_path = r"c:\Janith\Incbotic\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Fonts & Add Lucide in <head>
content = content.replace(
    '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Work+Sans:wght@400;500;600&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">',
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n<script src="https://unpkg.com/lucide@latest"></script>'
)

# 2. Update CSS Fonts
content = content.replace("'Work Sans', sans-serif", "'Inter', sans-serif")
content = content.replace("'Fraunces', serif", "'Outfit', sans-serif")
content = content.replace("'Space Mono', monospace", "'JetBrains Mono', monospace")

# 3. Add Advanced CSS Animations & floating nav & showcase styles
css_injections = """
  /* --- Advanced Animations --- */
  .reveal-text {
    display: inline-block;
    overflow: hidden;
  }
  .reveal-text span {
    display: inline-block;
    transform: translateY(100%);
    opacity: 0;
    transition: transform 0.8s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.8s ease;
  }
  .reveal-text.in span {
    transform: translateY(0);
    opacity: 1;
  }
  
  .glass-card {
    background: rgba(9, 22, 42, 0.4);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 32px;
    transition: transform 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
  }
  .glass-card:hover {
    transform: translateY(-8px) scale(1.02);
    border-color: var(--copper-bright);
    box-shadow: 0 20px 40px -10px rgba(6, 182, 212, 0.3);
  }

  /* --- Showcase Section --- */
  .showcase-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
    margin-top: 60px;
  }
  .showcase-item {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    aspect-ratio: 16/9;
  }
  .showcase-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s ease;
  }
  .showcase-item:hover img {
    transform: scale(1.05);
  }
  .showcase-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(0deg, rgba(4,11,22,0.9) 0%, transparent 60%);
    display: flex;
    align-items: flex-end;
    padding: 24px;
  }
  .showcase-overlay h3 {
    margin: 0;
    font-size: 20px;
    color: var(--ink);
  }
"""
content = content.replace("</style>", css_injections + "\n</style>")

# 4. Modify Hero section for text reveal
content = content.replace(
    '<h1>Boards built to hold a signal,<br> not just a <span class="accent">shape.</span></h1>',
    '<h1 class="reveal-text"><span>Boards built to hold a signal,</span><br><span>not just a <span class="accent">shape.</span></span></h1>'
)

# 5. Modify Capabilities to use glass-card and Lucide icons
content = content.replace('class="layer-card reveal"', 'class="glass-card reveal"')
content = content.replace(
    '<svg class="layer-icon" viewBox="0 0 40 40"><path d="M8 20h6M26 20h6M20 8v6M20 26v6" stroke-linecap="round"/><rect x="14" y="14" width="12" height="12" rx="2"/></svg>',
    '<i data-lucide="cpu" class="layer-icon" style="color: var(--copper-bright); width:38px; height:38px; margin-bottom:20px;"></i>'
)
content = content.replace(
    '<svg class="layer-icon" viewBox="0 0 40 40"><path d="M6 12h10l4 6h14M6 28h8l6-6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="6" cy="12" r="2"/><circle cx="34" cy="18" r="2"/><circle cx="6" cy="28" r="2"/></svg>',
    '<i data-lucide="network" class="layer-icon" style="color: var(--copper-bright); width:38px; height:38px; margin-bottom:20px;"></i>'
)
content = content.replace(
    '<svg class="layer-icon" viewBox="0 0 40 40"><rect x="7" y="7" width="26" height="26" rx="2"/><path d="M14 7v26M26 7v26M7 14h26M7 26h26"/></svg>',
    '<i data-lucide="layers" class="layer-icon" style="color: var(--copper-bright); width:38px; height:38px; margin-bottom:20px;"></i>'
)
content = content.replace(
    '<svg class="layer-icon" viewBox="0 0 40 40"><rect x="10" y="10" width="20" height="20" rx="2"/><path d="M4 16h6M4 24h6M30 16h6M30 24h6M16 4v6M24 4v6M16 30v6M24 30v6"/></svg>',
    '<i data-lucide="microchip" class="layer-icon" style="color: var(--copper-bright); width:38px; height:38px; margin-bottom:20px;"></i>'
)

# 6. Insert Showcase Section before SPECS
showcase_html = """
  <!-- SHOWCASE -->
  <section id="showcase">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">Facilities</div>
        <h2>Advanced Manufacturing & Labs.</h2>
        <p>Take a look inside our high-tech assembly and engineering environments.</p>
      </div>
      <div class="showcase-grid">
        <div class="showcase-item reveal">
          <img src="assets/pcb_manufacturing.png" alt="PCB Manufacturing">
          <div class="showcase-overlay">
            <h3>Automated Optical Inspection</h3>
          </div>
        </div>
        <div class="showcase-item reveal">
          <img src="assets/hardware_lab.png" alt="Hardware Engineering Lab">
          <div class="showcase-overlay">
            <h3>Hardware Engineering Lab</h3>
          </div>
        </div>
      </div>
    </div>
  </section>
"""
content = content.replace('  <!-- SPECS -->', showcase_html + '\n  <!-- SPECS -->')

# 7. Update script to initialize Lucide and text-reveal
script_addition = """
  // Initialize Lucide Icons
  lucide.createIcons();

  // Text Reveal Observer
  const revealTextEls = document.querySelectorAll('.reveal-text');
  const textIo = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      if(e.isIntersecting){ 
        e.target.classList.add('in'); 
        
        // Stagger children
        const spans = e.target.querySelectorAll(':scope > span');
        spans.forEach((span, i) => {
           span.style.transitionDelay = `${i * 0.15}s`;
        });
        
        textIo.unobserve(e.target); 
      }
    });
  }, {threshold:0.1});
  revealTextEls.forEach(el=>textIo.observe(el));
"""
content = content.replace('</script>', script_addition + '\n</script>')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("HTML updated successfully.")
