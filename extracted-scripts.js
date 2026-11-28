(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-N68QQVKV');

// ===== EXTRACTED SCRIPT BLOCK =====

window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}

  // Only load after explicit consent
  window.loadAnalytics = function(){
    if (window.__analyticsLoaded) return;
    window.__analyticsLoaded = true;

    const ga = document.createElement('script');
    ga.async = true;
    ga.src = 'https://www.googletagmanager.com/gtag/js?id=G-P1DMJ7E22B';
    document.head.appendChild(ga);

    gtag('js', new Date());
    gtag('config', 'G-P1DMJ7E22B', { send_page_view: true });

    // Meta Pixel — consent-gated
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '2856593904741515');
    fbq('track', 'PageView');
    // To re-enable, add a dedicated opt-in toggle in the cookie banner.
  };

  // Load on return visit if already accepted
  if (localStorage.getItem('cookiesAccepted') === 'true') {
    window.loadAnalytics();
  }

// ===== EXTRACTED SCRIPT BLOCK =====

{
      "imports": {
        "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
        "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
      }
    }

// ===== EXTRACTED SCRIPT BLOCK =====

(async function(){
      var container = document.getElementById('implant3d');
      if(!container) return;
      var loading = document.getElementById('implant3dLoading');

      // ⚡ Lazy-load Three.js — فقط عند التمرير لقسم الـ 3D
      await new Promise((resolve) => {
        if (!('IntersectionObserver' in window)) return resolve();
        var obs = new IntersectionObserver((entries) => {
          if (entries[0].isIntersecting) { obs.disconnect(); resolve(); }
        }, { rootMargin: '300px' });
        obs.observe(container);
      });

      let THREE, OrbitControls, RoomEnvironment;
      try {
        THREE = await import('three');
        ({ OrbitControls } = await import('three/addons/controls/OrbitControls.js'));
        ({ RoomEnvironment } = await import('three/addons/environments/RoomEnvironment.js'));
      } catch(e) {
        if (loading) loading.textContent = '3D viewer unavailable — try another browser';
        return;
      }

      // 1. Scene & Renderer
      var scene = new THREE.Scene();
      var camera = new THREE.PerspectiveCamera(40, container.clientWidth / container.clientHeight, 0.1, 100);
      camera.position.set(0, 3, 8); // زاوية رؤية احترافية

      var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setSize(container.clientWidth, container.clientHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.setClearColor(0x000000, 0);
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.2;
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      container.appendChild(renderer.domElement);

      // 2. Realistic Studio Lighting
      var pmremGenerator = new THREE.PMREMGenerator(renderer);
      scene.environment = pmremGenerator.fromScene(new RoomEnvironment(), 0.04).texture;
      
      var ambientLight = new THREE.AmbientLight(0xffffff, 0.3);
      scene.add(ambientLight);

      var keyLight = new THREE.DirectionalLight(0xffffff, 2.5);
      keyLight.position.set(5, 10, 5);
      keyLight.castShadow = true;
      keyLight.shadow.mapSize.width = 2048;
      keyLight.shadow.mapSize.height = 2048;
      scene.add(keyLight);

      var fillLight = new THREE.DirectionalLight(0xcce0ff, 1.0); // ضوء أزرق خفيف
      fillLight.position.set(-5, 3, 5);
      scene.add(fillLight);

      // 3. Anatomy Groups
      var anatomyGroup = new THREE.Group();
      var implantGroup = new THREE.Group();
      scene.add(anatomyGroup);
      scene.add(implantGroup);

      // --- أ) بناء العظم (Bone / Jaw) ---
      // رسم مقطع جانبي للعظم باستخدام Spline
      var boneShape = new THREE.Shape();
      boneShape.moveTo(-4, 0);
      boneShape.bezierCurveTo(-4, 1.5, -3, 2, -2, 2);
      boneShape.lineTo(2, 2);
      boneShape.bezierCurveTo(3, 2, 4, 1.5, 4, 0);
      boneShape.lineTo(4, -1);
      boneShape.lineTo(-4, -1);
      boneShape.lineTo(-4, 0);

      var extrudeSettings = { depth: 2, bevelEnabled: true, bevelSegments: 4, steps: 2, bevelSize: 0.2, bevelThickness: 0.2 };
      var boneGeo = new THREE.ExtrudeGeometry(boneShape, extrudeSettings);
      // توسيط العظم
      boneGeo.center();

      var boneMat = new THREE.MeshPhysicalMaterial({ 
        color: 0xE6DCC3, // لون عظمي فاتح
        transparent: true, 
        opacity: 0.45,
        roughness: 0.7,
        metalness: 0.1,
        transmission: 0.2, // يعطي تأثير شفاف
        side: THREE.DoubleSide,
        depthWrite: false
      });
      var boneMesh = new THREE.Mesh(boneGeo, boneMat);
      boneMesh.position.y = -1.5;
      boneMesh.castShadow = true;
      boneMesh.receiveShadow = true;
      boneMesh.name = 'jaw';
      anatomyGroup.add(boneMesh);

      // --- ب) بناء اللثة (Gum) ---
      var gumShape = new THREE.Shape();
      gumShape.moveTo(-4.2, 0);
      gumShape.bezierCurveTo(-4.2, 1.2, -3.2, 1.8, -2, 1.8);
      gumShape.lineTo(2, 1.8);
      gumShape.bezierCurveTo(3.2, 1.8, 4.2, 1.2, 4.2, 0);
      gumShape.lineTo(4.2, -0.5);
      gumShape.lineTo(-4.2, -0.5);
      gumShape.lineTo(-4.2, 0);

      var gumGeo = new THREE.ExtrudeGeometry(gumShape, { depth: 2.2, bevelEnabled: true, bevelSegments: 2, steps: 1, bevelSize: 0.1, bevelThickness: 0.1 });
      gumGeo.center();

      var gumMat = new THREE.MeshPhysicalMaterial({ 
        color: 0xE0888A, // لون وردي للثة
        transparent: true, 
        opacity: 0.35,
        roughness: 0.3,
        transmission: 0.4, // شفافية أعلى
        thickness: 0.5,
        side: THREE.DoubleSide,
        depthWrite: false
      });
      var gumMesh = new THREE.Mesh(gumGeo, gumMat);
      gumMesh.position.y = -0.2;
      gumMesh.castShadow = true;
      gumMesh.name = 'gum';
      anatomyGroup.add(gumMesh);

      // --- ج) بناء الزرعة (Implant) بشكل واقعي ---
      var implantMat = new THREE.MeshStandardMaterial({ 
        color: 0xC8C8C8, // لون التيتانيوم
        metalness: 0.95, 
        roughness: 0.15,
        envMapIntensity: 1.5
      });

      // 1. الجسم المخروطي (Screw)
      var screwGeo = new THREE.CylinderGeometry(0.25, 0.15, 2.5, 32);
      var screwMesh = new THREE.Mesh(screwGeo, implantMat);
      screwMesh.position.y = -1.0;
      screwMesh.castShadow = true;
      implantGroup.add(screwMesh);

      // 2. الخيوط الحلزونية (Threads) - حلقات حول الجسم
      for(var i=0; i<12; i++) {
        var threadGeo = new THREE.TorusGeometry(0.25 - (i*0.008), 0.02, 16, 32);
        var threadMesh = new THREE.Mesh(threadGeo, implantMat);
        threadMesh.rotation.x = Math.PI / 2;
        threadMesh.position.y = -2.1 + (i * 0.2);
        threadMesh.castShadow = true;
        implantGroup.add(threadMesh);
      }

      // 3. القاعدة (Abutment)
      var abutmentGeo = new THREE.CylinderGeometry(0.15, 0.25, 0.6, 32);
      var abutmentMesh = new THREE.Mesh(abutmentGeo, implantMat);
      abutmentMesh.position.y = 0.55;
      abutmentMesh.castShadow = true;
      implantGroup.add(abutmentMesh);

      // 4. التاج (Crown) - تصميم واقعي باستخدام LatheGeometry (شكل بيضاوي)
      var crownPoints = [];
      for(var i=0; i<=10; i++) {
        var t = i / 10;
        var x = Math.sin(t * Math.PI) * 0.6; // العرض
        var y = t * 1.2; // الارتفاع
        crownPoints.push(new THREE.Vector2(x, y));
      }
      var crownGeo = new THREE.LatheGeometry(crownPoints, 32);
      var crownMat = new THREE.MeshPhysicalMaterial({ 
        color: 0xFAFAFA, // لون أبيض عاجي
        roughness: 0.1, 
        metalness: 0.0,
        transmission: 0.3, // شفافية خفيفة
        thickness: 1.0,
        clearcoat: 1.0,
        clearcoatRoughness: 0.1
      });
      var crownMesh = new THREE.Mesh(crownGeo, crownMat);
      crownMesh.position.y = 0.85;
      crownMesh.castShadow = true;
      crownMesh.name = 'crown';
      implantGroup.add(crownMesh);

      // 4. Controls & Animation
      var controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.minDistance = 4;
      controls.maxDistance = 15;
      controls.target.set(0, -0.5, 0); // التركيز على الزرعة
      controls.autoRotate = true;
      controls.autoRotateSpeed = 1.0;

      controls.addEventListener('start', function(){ controls.autoRotate = false; });

      
        if(loading) loading.style.display = 'none';

        // Pause 3D rendering when not in viewport to save CPU
        let is3DVisible = false;
        const obs3D = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            is3DVisible = entry.isIntersecting;
            if (is3DVisible) animate();
          });
        }, { threshold: 0 });
        obs3D.observe(container);

        function animate(){
          if (!is3DVisible) return; // Stop infinite loop
          requestAnimationFrame(animate);
          controls.update();
          renderer.render(scene, camera);
        }
        

      // 6. Layer Toggles
      var toggleBone = document.getElementById('toggleBone');
      var toggleGum = document.getElementById('toggleGum');
      
      if(toggleBone) {
        toggleBone.addEventListener('change', function(e) {
          boneMesh.visible = e.target.checked;
        });
      }
      if(toggleGum) {
        toggleGum.addEventListener('change', function(e) {
          gumMesh.visible = e.target.checked;
        });
      }

      // 7. Resize
      window.addEventListener('resize', function(){
        if(!container) return;
        var w = container.clientWidth, h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      }, { passive: true });

    })();

// ===== EXTRACTED SCRIPT BLOCK =====

(function(){
  const co = document.getElementById('estCountry');
  const tr = document.getElementById('estTreatment');
  const ad = document.getElementById('estAddon');
  const ho = document.getElementById('estHotel');
  const out = document.getElementById('estPrice');
  const brk = document.getElementById('estBreakdown');
  if(!co || !tr || !ad || !out) return;

  function fmt(n){ return '$' + Math.round(n).toLocaleString('en-US'); }

  function update(){
    const c = parseFloat(co.value) || 0;
    const tRaw = tr.value;
    const a = parseFloat(ad.value) || 0;
    const h = ho ? (parseFloat(ho.value) || 0) : 0;

    const parts = tRaw === '0|0' ? [0,0] : tRaw.split('|').map(Number);
    const t = parts[0];
    const visits = parts[1] || 0;

    if(t === 0){
      out.textContent = '—';
      if(brk) brk.innerHTML = '';
      return;
    }

    const flightCost = c * (visits || 1);
    const base = t + a + h + flightCost;
    const low  = Math.round(base * 0.9);
    const high = Math.round(base * 1.15);

    out.textContent = fmt(low) + ' – ' + fmt(high);

    if(brk){
      let b = '';
      b += '<div>Treatment (clinical only): ' + fmt(t) + '</div>';
      if(h > 0) b += '<div>Hotel (10 nights): ' + fmt(h) + '</div>';
      if(a > 0) b += '<div>Concierge add-on: ' + fmt(a) + '</div>';
      if(flightCost > 0) b += '<div>Flights: ' + fmt(flightCost) + ' (' + (visits||1) + ' visit' + (visits>1?'s':'') + ')</div>';
      brk.innerHTML = b;
    }
  }

  co.addEventListener('change', update);
  tr.addEventListener('change', update);
  ad.addEventListener('change', update);
  if(ho) ho.addEventListener('change', update);
})();

// ===== EXTRACTED SCRIPT BLOCK =====

(function(){
  var data = {
    single:     { AU:5500,  US:5500,  CA:4800,  UK:3500, NZ:5200, Nile:899 },
    overdenture:{ AU:9500,  US:10000, CA:8500,  UK:7500, NZ:9500, Nile:4490 },
    allon4:     { AU:22000, US:25000, CA:19000, UK:16000, NZ:22000, Nile:6490 },
    allon6:     { AU:28000, US:32000, CA:25000, UK:20000, NZ:28000, Nile:8490 },
    fullmouth:  { AU:50000, US:55000, CA:42000, UK:38000, NZ:48000, Nile:11490 },
    zygomatic:  { AU:45000, US:50000, CA:42000, UK:38000, NZ:45000, Nile:19900 }
  };
  
  var co = document.getElementById('savCountry');
  var tr = document.getElementById('savTreatment');
  var ho = document.getElementById('savHotel');
  var outHome = document.getElementById('savHome');
  var outNile = document.getElementById('savNile');
  var outDiff = document.getElementById('savDiff');
  var outPct = document.getElementById('savPct');
  if(!co || !tr || !outHome) return;

  function fmt(n){ return '$' + Math.round(n).toLocaleString('en-US'); }

  function update(){
    var c = co.value, t = tr.value;
    var hotelCost = ho ? (parseFloat(ho.value) || 0) : 0;
    var homePrice = data[t][c];
    var nilePrice = data[t].Nile + hotelCost;
    var savings = homePrice - nilePrice;
    var pct = Math.round((savings / homePrice) * 100);

    outHome.textContent = fmt(homePrice);
    outNile.textContent = fmt(nilePrice) + (hotelCost > 0 ? ' (incl. hotel)' : '');
    outDiff.textContent = fmt(savings);
    outPct.textContent = 'You save ' + pct + '% — that\'s real money back in your pocket.';
  }

  co.addEventListener('change', update);
  tr.addEventListener('change', update);
  if(ho) ho.addEventListener('change', update);
  update();
})();

// ===== EXTRACTED SCRIPT BLOCK =====

(function(){
  const tabs = document.querySelectorAll('.tab-guarantees');
  const contents = document.querySelectorAll('.tab-content-guarantees');
  tabs.forEach(btn => {
    btn.addEventListener('click', () => {
      tabs.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      contents.forEach(c => c.classList.add('hidden'));
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');
      const target = document.getElementById('tab-' + btn.dataset.tab);
      if(target) target.classList.remove('hidden');
    });
    // كيبورد
    btn.addEventListener('keydown', (e) => {
      if(e.key === 'ArrowRight' || e.key === 'ArrowLeft'){
        const arr = Array.from(tabs);
        const i = arr.indexOf(btn);
        const next = e.key === 'ArrowRight' 
          ? arr[(i + 1) % arr.length] 
          : arr[(i - 1 + arr.length) % arr.length];
        next.focus();
      }
    });
  });
})();

// ===== EXTRACTED SCRIPT BLOCK =====

(function(){
  var form = document.getElementById('leadForm');
  if(!form) return;
  var steps = form.querySelectorAll('.form-step');
  var dots = form.querySelectorAll('.form-step-dot');
  var current = 1;
  var uploadedFile = null;

  function showStep(n){
    current = n;
    steps.forEach(function(s){ s.style.display = 'none'; });
    var target = form.querySelector('.form-step[data-step="' + n + '"]');
    if(target){ target.style.display = 'block'; }
    dots.forEach(function(d, i){
      d.classList.remove('active','completed');
      if(i + 1 === n) d.classList.add('active');
      if(i + 1 < n) d.classList.add('completed');
    });
  }

  form.querySelectorAll('.form-next').forEach(function(btn){
    btn.addEventListener('click', function(){
      // Validate current step
      var step = form.querySelector('.form-step[data-step="' + current + '"]');
      var required = step.querySelectorAll('[required]');
      var valid = true;
      required.forEach(function(f){
        if(!f.value.trim()){ valid = false; f.style.borderColor = '#C85A5A'; }
        else { f.style.borderColor = ''; }
      });
      if(!valid) return;
      if(current < 3) showStep(current + 1);
    });
  });

  form.querySelectorAll('.form-prev').forEach(function(btn){
    btn.addEventListener('click', function(){
      if(current > 1) showStep(current - 1);
    });
  });

  // File upload — REMOVED (fake upload was misleading; patient sends via WhatsApp)
  // To re-enable real upload: connect to Formspree/Basin/Cloudflare Worker endpoint

  // Submit
  form.addEventListener('submit', function(e){
    e.preventDefault();
    if(form.dataset.submitting === '1') return;
    form.dataset.submitting = '1';

    // ✅ Loading state — المريض يشوف حاجة بتحصل
    var submitBtn = form.querySelector('button[type="submit"]');
    var originalBtnHTML = submitBtn ? submitBtn.innerHTML : '';
    if(submitBtn){
      submitBtn.disabled = true;
      submitBtn.innerHTML = '⏳ Sending…';
    }
    form.classList.add('form-loading');

    var country = (document.getElementById('formCountry')||{}).value || '';
    var treatment = (document.getElementById('formTreatment')||{}).value || '';
    var name = (document.getElementById('formName')||{}).value || '';
    var email = (document.getElementById('formEmail')||{}).value || '';
    var phone = (document.getElementById('formPhone')||{}).value || '';

    // Email validation — يمنع الفورم إنه يعلق في حالة Loading
    if(!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){
      form.dataset.submitting = '';
      if(submitBtn){ submitBtn.disabled = false; submitBtn.innerHTML = originalBtnHTML; }
      form.classList.remove('form-loading');
      return;
    }

    var msg = 'Hi Nile Smile, I would like a free X-ray review.\n\nName: ' + name + '\nCountry: ' + country + '\nTreatment: ' + treatment + '\nEmail: ' + email + '\nPhone: ' + phone;

    try {
      var leads = JSON.parse(localStorage.getItem('nile_leads') || '[]');
      // إزالة كل lead أقدم من 30 يوم (GDPR retention)
      var THIRTY_DAYS = 30 * 24 * 60 * 60 * 1000;
      leads = leads.filter(function(l){ return Date.now() - l.timestamp < THIRTY_DAYS; });
      leads.push({ name:name, email:email, phone:phone, country:country, treatment:treatment, hasXray: !!uploadedFile, timestamp: Date.now(), source:'consult_form_v2' });
      localStorage.setItem('nile_leads', JSON.stringify(leads));
    } catch(err) {}

    var wa = document.createElement('a');
    wa.href = 'https://wa.me/201503308333?text=' + encodeURIComponent(msg);
    wa.target = '_blank'; wa.rel = 'noopener'; wa.style.display = 'none';
    document.body.appendChild(wa); wa.click();
    setTimeout(function(){ document.body.removeChild(wa); }, 100);

    if(typeof gtag === 'function'){
      gtag('event', 'lead_form_submit_v2', { country: country, treatment: treatment, has_xray: !!uploadedFile });
    }

    // Success state — تسجيل النجاح
    form.classList.remove('form-loading');
    form.innerHTML = '<div style="background:rgba(174,145,100,.1);border:1px solid rgba(174,145,100,.4);padding:2rem;border-radius:4px;text-align:center"><div style="width:64px;height:64px;border-radius:50%;background:linear-gradient(135deg,#AE9164,#E8C88A);display:flex;align-items:center;justify-content:center;margin:0 auto 1.25rem"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#1F2A36" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div><h3 style="color:#E8C88A;font-family:Playfair Display,serif;font-size:1.5rem;margin-bottom:.75rem">Thank You!</h3><p style="color:#F6F3EE;font-size:.95rem;line-height:1.7">A licensed dentist will review your case and respond within <strong style="color:#E8C88A">24–72 hours</strong>.</p><p style="color:#8FA1B2;font-size:.8rem;margin-top:1rem">WhatsApp opened for you — if not, message <a href="https://wa.me/201503308333" target="_blank" style="color:#C9A96E;text-decoration:underline">+20 150 330 8333</a>.</p></div>';
  });
})();

// ===== EXTRACTED SCRIPT BLOCK =====

(function(){
  'use strict';

  /* ═════════ 2. SCROLL PROGRESS ═════════ */
  const progress = document.getElementById('progress');
  let progTick = false;
  function updateProgress(){
    if(progTick) return;
    progTick = true;
    requestAnimationFrame(()=>{
      const h = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = h > 0 ? (window.scrollY/h*100)+'%' : '0%';
      progTick = false;
    });
  }

  /* ═════════ 3. HEADER: SMOOTH SHRINK ONLY (NO HIDE) ═════════ */
  const header = document.getElementById('header');
  let navTick = false;
  function updateHeader(){
    if(navTick) return;
    navTick = true;
    requestAnimationFrame(()=>{
      const y = window.scrollY;
      // بس بنضيف/نشيل كلاس scrolled — الهيدر ثابت
      if(y > 60) header.classList.add('scrolled');
      else header.classList.remove('scrolled');
      navTick = false;
    });
  }

  window.addEventListener('scroll', ()=>{
    updateProgress();
    updateHeader();
    if (typeof updateActiveChip === 'function') updateActiveChip();
    if (typeof revealManualFallback === 'function') revealManualFallback();
  }, {passive:true});

  /* ═════════ 4. REVEAL ON SCROLL — PREMIUM SHADE ═════════ */
  const revealEls = document.querySelectorAll('.reveal, .stagger');
  const io = 'IntersectionObserver' in window
    ? new IntersectionObserver(function(entries, observer){
        entries.forEach(function(e){
          if(e.isIntersecting){
            requestAnimationFrame(function(){
              e.target.classList.add('visible');
              observer.unobserve(e.target);
            });
          }
        });
      }, {rootMargin:'0px 0px -60px 0px', threshold:0.1})
    : null;

  if(io){
    revealEls.forEach(el=>io.observe(el));
  } else {
    revealEls.forEach(el=>el.classList.add('visible'));
  }

  /* Fallback removed for performance */

  /* ✅ Fallback 2: ضمان نهائي — يشتغل بس لو IO مش مدعوم */
  if(!('IntersectionObserver' in window)){
    setTimeout(()=>{
      document.querySelectorAll('.reveal:not(.visible), .stagger:not(.visible)')
        .forEach(el=>el.classList.add('visible'));
    }, 800);
  }

  /* ═════════ 5. MOBILE MENU ═════════ */
  const menuBtn = document.getElementById('menuBtn');
  const mobileMenu = document.getElementById('mobileMenu');
  if(menuBtn && mobileMenu){
    menuBtn.addEventListener('click', ()=>{
      const open = mobileMenu.classList.toggle('open');
      menuBtn.classList.toggle('open', open);
      menuBtn.setAttribute('aria-expanded', String(open));
    });
    mobileMenu.querySelectorAll('a').forEach(a=>{
      a.addEventListener('click', ()=>{
        mobileMenu.classList.remove('open');
        menuBtn.classList.remove('open');
        menuBtn.setAttribute('aria-expanded','false');
      });
    });
  }

 /* ═════════ 6. MOTION PREFERENCE (Native smooth scroll active) ═════════ */
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ═════════ 8. HERO PARALLAX (subtle) ═════════ */
  const heroImg = document.getElementById('heroImg');
  if(heroImg && !prefersReduced && window.innerWidth > 768){
    let heroTick = false;
    window.addEventListener('scroll', ()=>{
      if(heroTick) return;
      heroTick = true;
      requestAnimationFrame(()=>{
        const y = window.scrollY;
        if(y < window.innerHeight){
          heroImg.style.transform = 'translateY(' + (y * 0.22) + 'px) scale(1.04)';
        }
        heroTick = false;
      });
    }, {passive:true});
  }

  /* ═════════ 9. MAGNETIC BUTTONS ═════════ */
  /* Magnetic buttons disabled for performance */

  /* ═════════ 10. MODALS ═════════ */
  let lastFocused = null;
  window.openModal = function(id){
    const m = document.getElementById(id);
    if(!m) return;
    lastFocused = document.activeElement;
    m.classList.add('open');
    document.body.style.overflow = 'hidden';
    const focusables = m.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    if (focusables.length) setTimeout(() => focusables[0].focus(), 60);
  };
  window.closeModal = function(id){
    const m = document.getElementById(id);
    if(!m) return;
    m.classList.remove('open');
    document.body.style.overflow = '';
    if (lastFocused && typeof lastFocused.focus === 'function') lastFocused.focus();
  };

  // Focus trap — يمنع الـTab يخرج من الـmodal المفتوح
  document.addEventListener('keydown', e => {
    if (e.key !== 'Tab') return;
    const open = document.querySelector('.modal.open, .search-modal.open, .gallery-lightbox.open, .exit-popup.open');
    if (!open) return;
    const focusables = Array.from(open.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'))
      .filter(el => !el.disabled && el.offsetParent !== null);
    if (!focusables.length) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });
  document.querySelectorAll('.modal').forEach(m=>{
    m.addEventListener('click', e=>{ if(e.target === m) window.closeModal(m.id); });
  });
  document.addEventListener('keydown', e=>{
    if(e.key === 'Escape'){
      document.querySelectorAll('.modal.open').forEach(m=>window.closeModal(m.id));
    }
  });

  /* ═════════ 12. AUTO-ENHANCE ═════════ */
  document.querySelectorAll('.logo-wrap').forEach(wrap => {
    if (!wrap.querySelector('.signature-line')) {
      const line = document.createElement('span');
      line.className = 'signature-line';
      line.setAttribute('aria-hidden','true');
      wrap.appendChild(line);
    }
  });
 document.querySelectorAll('.btn-gold').forEach(btn => {
    const text = (btn.textContent || '').toLowerCase().trim();
    
    // كل الأزرار الذهبية تاخد shine-auto
    btn.classList.add('shine-auto');
    
    // الأزرار الرئيسية تاخد breathe كمان
    if (text.includes('consultation') || 
        text.includes('book free')) {
      btn.classList.add('breathe');
    }
  });
   document.querySelectorAll('section h2, footer h2').forEach(h2 => {
    const section = h2.closest('section, footer');
    if (!section) return;
    
    // لو القسم داكن → جراديينت ذهبي
    const isDark = section.classList.contains('bg-nile-blue') ||
                   section.classList.contains('bg-nile-blue-dark') ||
                   section.id === 'science' ||
                   section.id === 'consult' ||
                   section.tagName === 'FOOTER';
    
    h2.classList.add(isDark ? 'gold-grad' : 'section-heading');
  });

  /* ═════════ 13. COOKIE BANNER ═════════ */
  if (!localStorage.getItem('cookiesAccepted')) {
    setTimeout(() => {
      const banner = document.getElementById('cookieBanner');
      if (banner) {
        banner.classList.remove('hidden');
        document.body.classList.add('has-cookie-banner');
      }
    }, 2500);
  }
  // إضافة class للـ sticky-mobile (يتحدّث مع الـ resize)
  function syncStickyMobileClass(){
    document.body.classList.toggle('has-sticky-mobile', window.innerWidth < 768);
  }
  syncStickyMobileClass();
  window.addEventListener('resize', syncStickyMobileClass, {passive:true});

  /* ═════════ 16. SCROLL BUTTON FEEDBACK ═════════ */
  document.querySelectorAll('a[href^="#"]:not(#appleDock a)').forEach(btn => {
    btn.addEventListener('click', function() {
      // تأثير بصري عند الضغط
      this.style.transform = 'scale(0.96)';
      setTimeout(() => {
        this.style.transform = '';
      }, 180);
    });
  });
    /* ═════════ 15. QUICK BAR — DISABLED (no .quick-chip elements exist) ═════════ */
  // Quick bar HTML was removed. To re-enable, add .quick-chip elements
  // with data-section attributes inside a .quick-bar container.

  /* ═════════ 17. ANIMATED COUNTERS — MOVED TO CSS ═════════
     Counters now use @property + animation-timeline: view() (pure CSS).
     This JS block was removed to reduce main-thread work. */

  /* ═════════ 18. GA4 SCROLL DEPTH TRACKING ═════════ */
  const depthMarks = [25, 50, 75, 90];
  const depthFired = new Set();
  let depthTick = false;
  window.addEventListener('scroll', () => {
    if (depthTick) return;
    depthTick = true;
    requestAnimationFrame(() => {
      if (typeof gtag !== 'function') { depthTick = false; return; }
      const h = document.documentElement.scrollHeight - window.innerHeight;
      const pct = h > 0 ? (window.scrollY / h) * 100 : 0;
      depthMarks.forEach(mark => {
        if (pct >= mark && !depthFired.has(mark)) {
          depthFired.add(mark);
          gtag('event', 'scroll_depth', {
            depth: mark,
            page_location: window.location.href,
            page_title: document.title
          });
        }
      });
      depthTick = false;
    });
  }, { passive: true });

})();

// ===== EXTRACTED SCRIPT BLOCK =====

/* ═══════════ DISCOVER EGYPT — Dynamic Gallery ═══════════ */
(function(){
  const galleryData = [
    // Historical
    { src:'images/spencer-davis-ONVA6s03hg8-unsplash.jpg', title:'Pyramids of Giza', desc:'The only surviving Ancient Wonder of the World.', cat:'historical' },
    { src:'images/rosario-janza-69qTN3L5c-unsplash.jpg', title:'Pyramids of Giza', desc:'Majestic view of the ancient pyramids.', cat:'historical' },
    { src:'images/marco-d-abramo-aWx7N6qpZbM-unsplash.jpg', title:'Pyramids of Giza', desc:'Timeless wonders under the Egyptian sun.', cat:'historical' },
    { src:'images/shreyas-nair-AA3QOukE92w-unsplash.jpg', title:'Abu Simbel Temple', desc:'The magnificent rock-cut temples of Abu Simbel.', cat:'historical' },
    { src:'images/mo-gabrail-iuC3w8mLDCs-unsplash.jpg', title:'Dendera Temple', desc:'An ancient Egyptian temple with stunning carvings.', cat:'historical' },
    { src:'images/ahmed-shabana-ADa9bb3tqR4-unsplash.jpg', title:'Pharaonic Temple', desc:'Ancient carvings and seated statues of gods.', cat:'historical' },
    { src:'images/abdullah-helwa-xcSzpi6zbW0-unsplash.jpg', title:'Aswan Feluccas', desc:'Traditional feluccas sailing on the Nile.', cat:'historical' },
    { src:'images/michael-starkie-l7Wdq5aNLLI-unsplash.jpg', title:'Aswan Feluccas', desc:'A serene sunset on the Nile river.', cat:'historical' },
    { src:'images/gjis-jakobs-LmgBEnYBOtM-unsplash.jpg', title:'Aswan Feluccas', desc:'Sailing on the legendary Nile river.', cat:'historical' },
    { src:'images/martijn-vonk-jaqKMULkw2M-unsplash.jpg', title:'Philae Temple', desc:'The majestic temple on the Nile in Aswan.', cat:'historical' },
    { src:'images/nathalie-lays-klXlZELq3No-unsplash.jpg', title:'Hot Air Balloon, Luxor', desc:'Sunrise balloon ride over the Valley of the Kings.', cat:'historical' },
    // Cairo & Nile
    { src:'images/jaydee-kerol-IpWl7cc5ag4-unsplash.jpg', title:'Nile River, Cairo', desc:'Breathtaking views of the Nile in Cairo.', cat:'cairo' },
    { src:'images/hatem-ramadan-59RY-ykUIAg-unsplash.jpg', title:'Nile River, Cairo', desc:'The heart of Cairo flowing with history.', cat:'cairo' },
    { src:'images/thales-botelho-de-sousa-MB2eogIiNKw-unsplash.jpg', title:'Khan el-Khalili', desc:"Cairo's most famous historic bazaar.", cat:'cairo' },

    { src:'images/johannes-hubner-Ck8sEhD2K4o-unsplash.jpg', title:'Alexandria Coast', desc:'Mediterranean shoreline with palm trees.', cat:'coast' },
    { src:'images/mohamed-ahmed-hXVQFxodBuY-unsplash.jpg', title:'Cairo Cityscape', desc:'View from Cairo Tower.', cat:'cairo' },
    { src:'images/dmitrii-zhodzishskii-5aEHQbZQ2kU-unsplash.jpg', title:'Islamic Cairo', desc:'Interior of a historic mosque in Islamic Cairo.', cat:'cairo' },
    // Red Sea
    { src:'images/kristina-loburets-KIwh5F4eY4-unsplash.jpg', title:'Red Sea Diving', desc:'Diving with dolphins and vibrant marine life.', cat:'redsea' },
    { src:'images/nils-Ir0qXcaJfik-unsplash.jpg', title:'Red Sea Beach', desc:'Pristine beaches and turquoise waters.', cat:'redsea' },
    { src:'images/pascal-van-de-vende-l-wPdBmBwyuE-unsplash.jpg', title:'Red Sea Coral Reef', desc:'Vibrant coral reefs in Hurghada &amp; Sharm.', cat:'redsea' },
    { src:'images/pascal-van-de-vende-I-CNdMGaVEozQ-unsplash.jpg', title:'Red Sea Coral Reef', desc:'Rich underwater ecosystems.', cat:'redsea' },
    { src:'images/jean-baptiste-d-fF8JX8lZnTc-unsplash.jpg', title:'Red Sea Beach', desc:'Relaxing by the Red Sea.', cat:'redsea' },
    { src:'images/geoff-trodd-qCkX-fMGziE-unsplash.jpg', title:'Red Sea Coral Reef', desc:'World-class diving spots.', cat:'redsea' },
    { src:'images/geoff-trodd-ovRUj2lZi2l-unsplash.jpg', title:'Red Sea Sea Turtle', desc:'Swimming with sea turtles.', cat:'redsea' },
    { src:'images/geoff-trodd-7l5PiZ2nK_M-unsplash.jpg', title:'Ras Mohammed Reef', desc:'Vibrant coral reef at Ras Mohammed.', cat:'redsea' },
    // Coast
    { src:'images/dmitrii-zhodzishskii-4-kii4XH-E9XeW-unsplash.jpg', title:'Citadel of Qaitbay', desc:'A 15th-century fortress in Alexandria.', cat:'coast' },
    { src:'images/bogdan-kupriets-5_cDWMfmONWs-unsplash.jpg', title:'Alexandria Harbor', desc:"Beautiful views of Alexandria's historic harbor.", cat:'coast' },
    { src:'images/flo-p-zpmvpEXM_Qc-unsplash.jpg', title:'Alexandria Harbor', desc:'The historic harbor of Alexandria.', cat:'coast' },
    { src:'images/bahaa-mourad-EFtGuBFJ7l0-unsplash.jpg', title:'Agiba Beach', desc:'Stunning aerial view in Marsa Matrouh.', cat:'coast' },
    { src:'images/youhana-nassif-9BZVfjEDWvU-unsplash.jpg', title:'Agiba Beach', desc:'Crystal clear waters and stunning cliffs.', cat:'coast' }
  ];

  const track = document.getElementById('galleryTrack');
  const tabs = document.querySelectorAll('.gallery-tab');
  const lightbox = document.getElementById('galleryLightbox');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxTitle = document.getElementById('lightboxTitle');
  const lightboxDesc = document.getElementById('lightboxDesc');

  if(!track) return;

  function render(category){
    const items = category === 'all' ? galleryData : galleryData.filter(i => i.cat === category);
    track.innerHTML = items.map(item => `
      <div class="gallery-card">
        <img src="${item.src}" loading="lazy" alt="${item.title} — ${item.desc}">
        <div class="gallery-card-overlay"></div>
        <div class="gallery-card-text">
          <h3>${item.title}</h3>
          <p>${item.desc}</p>
        </div>
      </div>
    `).join('');
    track.scrollLeft = 0;

    // اربط onerror كـ listener (بدون inline)
    track.querySelectorAll('.gallery-card img').forEach(img => {
      img.addEventListener('error', function(){
        this.parentElement.style.display = 'none';
      }, { once: true });
    });
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      render(tab.dataset.cat);
    });
  });

  track.addEventListener('click', (e) => {
    const card = e.target.closest('.gallery-card');
    if(!card) return;
    const img = card.querySelector('img');
    if(!img || !img.src) return;
    const title = card.querySelector('h3').textContent;
    const desc = card.querySelector('p').textContent;
    lightboxImg.src = img.src;
    lightboxImg.alt = title + ' — ' + desc;
    lightboxTitle.textContent = title;
    lightboxDesc.textContent = desc;
    lightbox.classList.add('open');
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  });

  function closeLightbox(){
    lightbox.classList.remove('open');
    lightbox.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }
  document.getElementById('lightboxClose').addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', (e) => { if(e.target === lightbox) closeLightbox(); });
  document.addEventListener('keydown', (e) => { if(e.key === 'Escape') closeLightbox(); });

  const prev = document.getElementById('galleryPrev');
  const next = document.getElementById('galleryNext');
  if(prev) prev.addEventListener('click', () => track.scrollBy({left:-340, behavior:'smooth'}));
  if(next) next.addEventListener('click', () => track.scrollBy({left:340, behavior:'smooth'}));

  render('all');
})();

// ===== EXTRACTED SCRIPT BLOCK =====

/* FIXED STICKY TOC — Optimized with requestAnimationFrame and Cached Positions */
(function(){
  const toc = document.getElementById('stickyToc');
  if (!toc) return;
  const dots = toc.querySelectorAll('.toc-dot');
  const sections = Array.from(dots).map(d => document.querySelector(d.getAttribute('href'))).filter(Boolean);
  let sectionTops = [];
  
  function calcTops() {
    sectionTops = sections.map(sec => ({
      id: sec.id,
      top: sec.getBoundingClientRect().top + window.scrollY - 200
    }));
  }
  
  let ticking = false;
  function updateToc(){
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const scrollY = window.scrollY;
      if (scrollY > 600) toc.classList.add('show');
      else toc.classList.remove('show');
      
      let current = null;
      for (let i = 0; i < sectionTops.length; i++) {
        if (scrollY >= sectionTops[i].top) current = sectionTops[i].id;
      }
      
      dots.forEach(d => {
        d.classList.toggle('active', d.getAttribute('href') === '#' + current);
      });
      ticking = false;
    });
  }
  
  window.addEventListener('load', calcTops);
  window.addEventListener('resize', () => { calcTops(); updateToc(); });
  window.addEventListener('scroll', updateToc, {passive: true});
  calcTops();
  updateToc();
})();

// ===== EXTRACTED SCRIPT BLOCK =====

(function() {
  'use strict';

  /* ═══════════════════════════════════════════
     A/B TESTING SUITE v2.0
     - Unified variant assignment
     - GA4 event tracking (impression + click + conversion)
     - localStorage persistence
     - GDPR-compliant: no personal data collected
     ═══════════════════════════════════════════ */

  // ─── Helper: Get or assign variant ───
  function getVariant(testName, variants) {
    const key = 'ab_' + testName;
    let variant = localStorage.getItem(key);
    if (!variant || !variants.includes(variant)) {
      variant = variants[Math.floor(Math.random() * variants.length)];
      localStorage.setItem(key, variant);
    }
    return variant;
  }

  // ─── Helper: Track GA4 event ───
  function trackEvent(eventName, params) {
    if (typeof gtag === 'function') {
      gtag('event', eventName, Object.assign({
        event_category: 'AB Testing',
        event_label: params.test_name + '_' + params.variant
      }, params));
    }
    // Also push to dataLayer for GTM
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({
      event: eventName,
      event_category: 'AB Testing'
    }, params));
  }

  // ═══ TEST 1: Hero CTA Text ═══
  (function() {
    const TEST = 'hero_cta_text';
    const VARIANTS = ['A', 'B', 'C'];
    const variant = getVariant(TEST, VARIANTS);

    const heroCta = document.getElementById('heroMainCta');
    if (!heroCta) return;

    // Apply variant
    if (variant === 'B') {
      heroCta.textContent = 'Get My Free Treatment Plan →';
    } else if (variant === 'C') {
      heroCta.textContent = 'Save 60–75% — Start Free Review →';
    }
    // Variant A = default (Request Clinical Review)

    // Track impression (when CTA enters viewport)
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            trackEvent('ab_test_impression', { test_name: TEST, variant: variant });
            observer.disconnect();
          }
        });
      }, { threshold: 0.5 });
      observer.observe(heroCta);
    } else {
      trackEvent('ab_test_impression', { test_name: TEST, variant: variant });
    }

    // Track click
    heroCta.addEventListener('click', () => {
      trackEvent('ab_test_click', { test_name: TEST, variant: variant });
    });
  })();

  // ═══ TEST 2: Price Anchoring (Premium Package) ═══
  (function() {
    const TEST = 'price_anchoring';
    const VARIANTS = ['A', 'B'];
    const variant = getVariant(TEST, VARIANTS);

    const priceEl = document.getElementById('premiumPrice');
    if (!priceEl) return;

    if (variant === 'B') {
      priceEl.innerHTML = '<span style="text-decoration:line-through;color:#8FA1B2;font-size:1.2rem;font-family:sans-serif;font-weight:400;margin-right:8px;">$1,700</span> + $3,600 <span class="text-base font-sans font-normal text-nile-muted">USD</span>';
    }

    trackEvent('ab_test_impression', { test_name: TEST, variant: variant });

    const card = priceEl.closest('.card');
    if (card) {
      const selectBtn = card.querySelector('.btn-gold, .btn-outline-dark');
      if (selectBtn) {
        selectBtn.addEventListener('click', () => {
          trackEvent('ab_test_click', { test_name: TEST, variant: variant });
        });
      }
    }
  })();

  // ═══ TEST 3: Founding Patients — Urgency Message ═══
  (function() {
    const TEST = 'founding_urgency';
    const VARIANTS = ['A', 'B'];
    const variant = getVariant(TEST, VARIANTS);

    // دوّر على لينك "Check Current Availability" في قسم founding patients
    const availabilityLink = document.querySelector('#reviews a[href*="Founding"]');
    if (!availabilityLink) {
      trackEvent('ab_test_impression', { test_name: TEST, variant: variant });
      return;
    }

    if (variant === 'B') {
      const urgencyEl = document.createElement('p');
      urgencyEl.className = 'text-nile-gold text-xs italic mt-3';
      urgencyEl.textContent = 'Limited to 20 founding patients — first-come, first-served.';
      availabilityLink.parentElement.appendChild(urgencyEl);
    }

    trackEvent('ab_test_impression', { test_name: TEST, variant: variant });
  })();

})();

// ===== EXTRACTED SCRIPT BLOCK =====

(function(){
  'use strict';

  /* ═══════════════════════════════════════════
     STICKY CTA — Show after scroll, hide on click
     ═══════════════════════════════════════════ */
  const stickyCta = document.getElementById('stickyCta');
  if (stickyCta) {
    let ctaDismissed = sessionStorage.getItem('stickyCtaDismissed') === 'true';
    let stickyTick = false;

    function updateSticky() {
      if (stickyTick || ctaDismissed) return;
      stickyTick = true;
      requestAnimationFrame(() => {
        const y = window.scrollY;
        const vh = window.innerHeight;
        const docH = document.documentElement.scrollHeight;
        // Show between 800px scroll and 90% of page
        if (y > 800 && y < docH - vh - 400) {
          stickyCta.classList.add('show');
          stickyCta.setAttribute('aria-hidden', 'false');
        } else {
          stickyCta.classList.remove('show');
          stickyCta.setAttribute('aria-hidden', 'true');
        }
        stickyTick = false;
      });
    }

    window.addEventListener('scroll', updateSticky, { passive: true });
    updateSticky();

    // Close button
    const closeBtn = stickyCta.querySelector('.sticky-cta-btn-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        ctaDismissed = true;
        sessionStorage.setItem('stickyCtaDismissed', 'true');
        stickyCta.classList.remove('show');
        stickyCta.setAttribute('aria-hidden', 'true');
      });
    }

    // Hide on primary click (navigating to consult)
    const primaryBtn = stickyCta.querySelector('.sticky-cta-btn-primary');
    if (primaryBtn) {
      primaryBtn.addEventListener('click', () => {
        stickyCta.classList.remove('show');
      });
    }
  }

  /* ═══════════════════════════════════════════
     EXIT INTENT POPUP
     - Triggers on: mouseleave (desktop) + back button (mobile)
     - Fires only ONCE per session
     - Fires only after 15s on page (avoid spam)
     - Doesn't fire if user already submitted lead
     ═══════════════════════════════════════════ */
  const exitPopup = document.getElementById('exitPopup');
  if (!exitPopup) return;

  const DISMISS_KEY = 'exitPopupDismissed_v1';
  const SUBMITTED_KEY = 'nile_leads';

  // Already dismissed this session?
  if (sessionStorage.getItem(DISMISS_KEY) === 'true') return;

  // Already submitted a lead?
  try {
    const leads = JSON.parse(localStorage.getItem(SUBMITTED_KEY) || '[]');
    if (leads.length > 0) return;
  } catch(e) {}

  let popupShown = false;
  let timeOnPage = Date.now();
  const MIN_TIME_MS = 15000; // 15s

  function showPopup() {
    if (popupShown) return;
    if (Date.now() - timeOnPage < MIN_TIME_MS) return;
    popupShown = true;
    exitPopup.classList.add('open');
    exitPopup.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    // Track event
    if (typeof gtag === 'function') {
      gtag('event', 'exit_intent_shown', { event_category: 'Engagement' });
    }
  }

  function closePopup() {
    exitPopup.classList.remove('open');
    exitPopup.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    sessionStorage.setItem(DISMISS_KEY, 'true');
    if (typeof gtag === 'function') {
      gtag('event', 'exit_intent_dismissed', { event_category: 'Engagement' });
    }
  }

  // ─── Trigger 1: Mouse leaves through TOP of viewport (desktop) ───
  document.addEventListener('mouseleave', (e) => {
    if (e.clientY <= 0) showPopup();
  });

  // ─── Trigger 2: Mobile — history back button (once per session) ───
  var backTriggerUsed = false;
  if (window.history && window.history.pushState) {
    try {
      history.pushState({ backGuard: true }, '', location.href);
      window.addEventListener('popstate', () => {
        if (backTriggerUsed) {
          // المستخدم قرر يمشي خلاص — سيبه يرجع
          return;
        }
        backTriggerUsed = true;
        showPopup();
        // أعد الضغط مرة واحدة بس عشان مايمشيش دلوقتي
        history.pushState({ backGuard: true }, '', location.href);
      }, { passive: true });
    } catch(e) {}
  }

  // ─── Trigger 3: Fallback — after 45s + scroll near bottom ───
  let fallbackTriggered = false;
  window.addEventListener('scroll', () => {
    if (fallbackTriggered || popupShown) return;
    const y = window.scrollY;
    const vh = window.innerHeight;
    const docH = document.documentElement.scrollHeight;
    // If user has been on page > 45s AND scrolled 75% down
    if (Date.now() - timeOnPage > 45000 && y > docH * 0.75) {
      fallbackTriggered = true;
      showPopup();
    }
  }, { passive: true });

  // ─── Close handlers ───
  exitPopup.querySelector('.exit-popup-close').addEventListener('click', closePopup);
  exitPopup.querySelector('.exit-popup-skip').addEventListener('click', closePopup);
  exitPopup.querySelector('.exit-popup-overlay').addEventListener('click', closePopup);

  // ESC key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && exitPopup.classList.contains('open')) closePopup();
  });

  // ─── Form submit ───
  const form = document.getElementById('exitForm');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = (form.querySelector('input[type="email"]') || {}).value || '';

      // Save lead
      try {
        const leads = JSON.parse(localStorage.getItem(SUBMITTED_KEY) || '[]');
        leads.push({ email, timestamp: Date.now(), source: 'exit_intent_popup' });
        localStorage.setItem(SUBMITTED_KEY, JSON.stringify(leads));
      } catch(e2) {}

      // Open WhatsApp
      const msg = encodeURIComponent(`Hi Nile Smile, I'd like a free X-ray review. My email: ${email}`);
      const wa = document.createElement('a');
      wa.href = 'https://wa.me/201503308333?text=' + msg;
      wa.target = '_blank';
      wa.rel = 'noopener';
      wa.style.display = 'none';
      document.body.appendChild(wa);
      wa.click();
      setTimeout(() => document.body.removeChild(wa), 100);

      // Track
      if (typeof gtag === 'function') {
        gtag('event', 'exit_intent_conversion', {
          event_category: 'Lead',
          value: 1
        });
      }

      // Show success state
      const box = exitPopup.querySelector('.exit-popup-box');
      const successHTML = `
        <div class="exit-popup-success">
          <div class="exit-popup-success-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#1F2A36" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          </div>
          <h3>Request Received</h3>
          <p>We've opened WhatsApp for you. A licensed dentist will review your case and respond within <strong>24–72 hours</strong>.</p>
          <p style="margin-top:1rem;font-size:.78rem;color:#AE9164;font-style:italic">If WhatsApp didn't open, message us at +20 150 330 8333.</p>
        </div>
      `;
      // Keep close button, replace rest
      const closeBtn = box.querySelector('.exit-popup-close');
      box.innerHTML = '';
      box.appendChild(closeBtn);
      box.insertAdjacentHTML('beforeend', successHTML);

      // Auto-close after 6s
      setTimeout(() => closePopup(), 6000);
    });
  }

})();

// ===== EXTRACTED SCRIPT BLOCK =====

(function(){
  'use strict';
  function initBASliders(){
    const resultsSection = document.getElementById('results');
    if (!resultsSection) return;
    const grid = resultsSection.querySelector('.grid.grid-cols-1.md\\:grid-cols-3');
    if (!grid) return;

    const cards = grid.querySelectorAll('.card.overflow-hidden');
    cards.forEach((card, idx) => {
      const imgs = card.querySelectorAll('img');
      if (imgs.length < 2) return;
      const beforeImg = imgs[0].src;
      const afterImg = imgs[1].src;
      const altB = imgs[0].alt || 'Before';
      const altA = imgs[1].alt || 'After';

      const mediaWrapper = card.querySelector('.grid.grid-cols-2');
      if (!mediaWrapper) return;

      const sliderHTML = `
        <div class="ba-slider-wrap">
          <div class="ba-slider">
            <img class="ba-after" src="${afterImg}" alt="${altA}">
            <div class="ba-before-layer">
              <img class="ba-before" src="${beforeImg}" alt="${altB}">
            </div>
            <div class="ba-handle">
              <div class="ba-handle-circle">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="15 18 9 12 15 6"></polyline>
                </svg>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-left:-4px">
                  <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
              </div>
            </div>
            <span class="ba-label ba-label-before">Before</span>
            <span class="ba-label ba-label-after">After</span>
          </div>
        </div>
      `;
      mediaWrapper.outerHTML = sliderHTML;

      const slider = card.querySelector('.ba-slider');
      const beforeLayer = card.querySelector('.ba-before-layer');
      const beforeImgEl = card.querySelector('.ba-before');
      const handle = card.querySelector('.ba-handle');

      function syncBeforeImgWidth() {
        beforeImgEl.style.width = slider.offsetWidth + 'px';
      }
      syncBeforeImgWidth();
      window.addEventListener('resize', syncBeforeImgWidth, {passive:true});

      let dragging = false;

      function setPercent(pct) {
        pct = Math.max(0, Math.min(100, pct));
        beforeLayer.style.width = pct + '%';
        handle.style.left = pct + '%';
      }

      function onStart(clientX) {
        dragging = true;
        slider.style.cursor = 'grabbing';
      }
      function onMove(clientX) {
        if (!dragging) return;
        const rect = slider.getBoundingClientRect();
        const x = clientX - rect.left;
        setPercent((x / rect.width) * 100);
      }
      function onEnd() {
        dragging = false;
        slider.style.cursor = 'ew-resize';
      }

      slider.addEventListener('mousedown', e => { e.preventDefault(); onStart(e.clientX); });
      window.addEventListener('mousemove', e => onMove(e.clientX));
      window.addEventListener('mouseup', onEnd);

      slider.addEventListener('touchstart', e => onStart(e.touches[0].clientX), {passive:true});
      slider.addEventListener('touchmove', e => onMove(e.touches[0].clientX), {passive:true});
      slider.addEventListener('touchend', onEnd, {passive:true});

      if ('IntersectionObserver' in window) {
        let animated = false;
        const obs = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting && !animated) {
              animated = true;
              setTimeout(() => {
                let start = null;
                const keyframes = [{t:0,v:50},{t:500,v:20},{t:1100,v:80},{t:1700,v:50}];
                function stepAnim(ts) {
                  if (!start) start = ts;
                  const elapsed = ts - start;
                  let fromKf = keyframes[0], toKf = keyframes[1];
                  for (let i = 0; i < keyframes.length - 1; i++) {
                    if (elapsed >= keyframes[i].t && elapsed <= keyframes[i+1].t) {
                      fromKf = keyframes[i]; toKf = keyframes[i+1]; break;
                    }
                  }
                  const p = (elapsed - fromKf.t) / (toKf.t - fromKf.t);
                  const eased = 1 - Math.pow(1 - Math.min(p,1), 3);
                  setPercent(fromKf.v + (toKf.v - fromKf.v) * eased);
                  if (elapsed < keyframes[keyframes.length-1].t) requestAnimationFrame(stepAnim);
                }
                requestAnimationFrame(stepAnim);
              }, idx * 300);
              obs.disconnect();
            }
          });
        }, { threshold: 0.3 });
        obs.observe(slider);
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBASliders);
  } else {
    initBASliders();
  }
})();

// ===== EXTRACTED SCRIPT BLOCK =====

(function(){
  'use strict';

  /* ═══════════════════════════════════════════
     CTA OPTIMIZATION LOGIC
     - Removes redundant buttons
     - Confirms primary CTA hierarchy
     - Tracks button count in console
     ═══════════════════════════════════════════ */

  function optimizeCTAs() {
    // ─── 1. إخفاء أزرار الباكدجات المكررة (نبقي زر واحد فقط) ───
    // Keep all 5 package buttons but they're now outline (via CSS)

    // ─── 2. حذف زر Refund (خلاص Read Full Terms بيفي بالغرض) ───
    const refundBtn = document.querySelector('#guarantees button[onclick*="refundModal"]');
    if (refundBtn) {
      refundBtn.remove();
    }

    // ─── 3. تبسيط CTA المكرر في Founding ───
    // (CSS handles visual downgrade)

    // ─── 4. إخفاء Quick Bar chips الزائدة ───
    ['founder', 'guarantees'].forEach(sec => {
      const chip = document.querySelector('.quick-chip[data-section="' + sec + '"]');
      if (chip) {
        chip.remove();
      }
    });

    // ─── 4b. الأقسام المخفية — تمت إزالتها لأنها مضافة للـORDER ───
    // (savings ظاهر الآن حسب ترتيب ORDER)

    // ─── 5. تبسيط CTA في Itemized (بيبقى text link) ───
    // (CSS handles it)

    // ─── 6. تحويل CTA المكرر في "Curated Tours" إلى text link ───
    // (CSS handles)

    // ─── 7. تأكيد إن كل الأزرار الأساسية بتوصل لـ consult ───
    document.querySelectorAll('.btn-gold').forEach(btn => {
      const href = btn.getAttribute('href');
      const onclick = btn.getAttribute('onclick') || '';
      if (href && !href.includes('#consult') && !href.includes('wa.me') && !onclick.includes('Modal')) {
        // Sadece log — don't change anything
        // console.log('Non-consult gold button:', btn.textContent.trim());
      }
    });

    // ─── 9. Track CTA clicks in GA4 ───
    document.querySelectorAll('.btn-gold, .btn-outline, .btn-outline-dark, .sticky-cta-btn-primary, .exit-popup-submit').forEach(btn => {
      btn.addEventListener('click', function() {
        const text = (this.textContent || '').trim().substring(0, 40);
        const href = this.getAttribute('href') || 'button';
        if (typeof gtag === 'function') {
          gtag('event', 'cta_click', {
            event_category: 'CTA',
            event_label: text,
            link_url: href
          });
        }
      });
    });
  }

  // شغل بعد تحميل الصفحة
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', optimizeCTAs);
  } else {
    optimizeCTAs();
  }

})();

// ===== EXTRACTED SCRIPT BLOCK =====

(function(){
  'use strict';
  var mqMobile = window.matchMedia('(max-width: 767px)');
  if (!mqMobile.matches) return;

  // Haptic feedback (اهتزاز خفيف عند اللمس - أندرويد فقط)
  function haptic(ms){
    if (navigator.vibrate) try { navigator.vibrate(ms||8); } catch(e){}
  }
  document.querySelectorAll('.sticky-mobile a, .quick-chip, .btn-gold, .btn-outline, .gallery-card').forEach(el=>{
    el.addEventListener('touchstart', ()=>haptic(8), {passive:true});
  });

  // Hero parallax ناعم
  const heroImg = document.getElementById('heroImg');
  if (heroImg && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    let ticking = false;
    window.addEventListener('scroll', ()=>{
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(()=>{
        const y = window.scrollY;
        if (y < 600) heroImg.style.transform = `translateY(${y * 0.28}px) scale(1.06)`;
        ticking = false;
      });
    }, {passive:true});
  }

  // Reveal on scroll — enhance
  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver((entries)=>{
      entries.forEach(e=>{
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          obs.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -50px 0px' });
    document.querySelectorAll('.reveal, .stagger').forEach(el=>obs.observe(el));
  }
})();

// ===== EXTRACTED SCRIPT BLOCK =====

/* ═══════════════════ SEARCH ENGINE ═══════════════════ */
(function(){
  'use strict';

  /* ───── Build Search Index from all sections ───── */
  var searchIndex = [];

  function buildIndex(){
    searchIndex = [];
    var main = document.getElementById('main');
    if(!main) return;

    // Manual friendly titles + keywords
    var meta = {
      'packages':        { title:'Treatment Packages & Pricing', kw:'prices cost all-on-4 implants full-arch money quote' },
      'founder':         { title:'Meet the Founder — Dr. Omar Fathi', kw:'doctor dentist clinician licensed bds omar' },
      'results':         { title:'Before & After — Clinical Cases', kw:'results gallery photos clinical cases smile' },
      'reviews':         { title:'Founding Patients Program', kw:'reviews testimonials patients trust' },
      'guarantees':      { title:'Guarantees & Warranty', kw:'warranty refund guarantee protection policy' },
      'legal':           { title:'Legal Framework', kw:'law legal rights protection patient' },
      'faq':             { title:'Frequently Asked Questions', kw:'questions answers faq help support' },
      'consult':         { title:'Free Clinical Review', kw:'consult contact free review x-ray consultation' },
      'science':         { title:'Clinical Science', kw:'science evidence research implants biology' },
      'why-egypt':       { title:'Why Egypt', kw:'egypt destination travel tourism location' },
      'why-prices':      { title:'Why Our Prices', kw:'pricing transparency why cost' },
      'comparison':      { title:'Egypt vs Turkey vs Mexico', kw:'compare comparison competition vs' },
      'team':            { title:'Our Specialists', kw:'team doctors dentists surgeons specialists' },
      'comfort':         { title:'Anesthesia & Comfort', kw:'anesthesia sedation pain comfort iv local' },
      'bone-graft':      { title:'Bone Graft Materials', kw:'bone graft grafting sinus augmentation' },
      'crown-materials': { title:'Crown & Prosthesis Materials', kw:'zirconia emax crown prosthesis materials' },
      'orthodontics':    { title:'Orthodontics — Aligners vs Braces', kw:'aligners braces orthodontics invisalign' },
      'travel':          { title:'Travel & Logistics', kw:'travel logistics flights airport transfer' },
      'travel-addons':   { title:'Travel Add-Ons', kw:'add-ons vip premium signature recovery care' },
      'curated-tours':   { title:'Curated Tours & Experiences', kw:'tours pyramids luxor nile excursion' },
      'journey':         { title:'Patient Journey', kw:'journey steps process timeline' },
      'timeline':        { title:'Day-by-Day Timeline', kw:'timeline days schedule protocol' },
      'recovery':        { title:'Recovery — Week by Week', kw:'recovery healing weeks aftercare' },
      'risks':           { title:'Risks & Complications', kw:'risks complications safety side effects' },
      'payment':         { title:'Payment Security', kw:'payment pay deposit milestone money' },
      'discover-egypt':  { title:'Discover Egypt', kw:'discover egypt gallery photos tourism' },
      'location':        { title:'Our Clinic Location', kw:'location address map clinic cairo giza' },
      'academic':        { title:'Academic Pedigree', kw:'academic university training education' },
      'price-anchor':    { title:'Price Comparison', kw:'price compare cheap affordable save' },
      'trust':           { title:'Accreditations', kw:'accreditations trust gahar iso eda iti' },
      'trust-stats':     { title:'Trust Statistics', kw:'stats numbers experience success rate' },
      'global-patients': { title:'Our Global Patients — World Map', kw:'global countries markets international map worldwide patients destinations usa canada uk australia new zealand' },
      'who-for':         { title:'Who This Service Is For', kw:'who for eligibility candidates' },
      'peace-of-mind':   { title:'Peace of Mind', kw:'peace of mind aftercare follow-up' },
      'implant-systems': { title:'Implant Systems — Full Transparency', kw:'straumann nobel osstem implant brand comparison tier premium mid entry' },
      'brutal-truth':    { title:'The Brutal Truth About Cheap Implants', kw:'cheap implant generic risk failure cost' },
      'surface-material':{ title:'Surface & Material Science', kw:'slactive roxolid tiunite surface alloy osseointegration' },
      'technology-stack':{ title:'Technology Stack 2026', kw:'cbct robotics dynamic navigation surgical guide ai' },
      'clinical-protocol':{ title:'Clinical Protocol — Prehabilitation', kw:'prevention peri-implantitis maintenance spic' },
      'cost-of-cheap':   { title:'The Real Cost of a Cheap Implant', kw:'cost cheap failure replacement redo' },
      'warranty-truth':  { title:'Warranty — What Actually Travels', kw:'manufacturer warranty clinic warranty lifetime lot number' },
      'implant-passport':{ title:'Implant Passport', kw:'implant passport lot number qr warranty claim' },
      'verify-us':       { title:'Verify Us — Credentials', kw:'verify license accreditation certificate documents' },
      'doctor-credentials':{ title:'Doctor Credentials', kw:'credentials license syndicate msc phd experience' },
      'destination-deep-dive':{ title:'Egypt vs Turkey vs Mexico', kw:'turkey mexico comparison destination deep dive' }
    };

    // Build from DOM
    main.querySelectorAll('section[id]').forEach(function(sec){
      var id = sec.id;
      var m = meta[id] || {};
      var heading = sec.querySelector('h2, h3.h2-as-h3');
      var title = m.title || (heading ? heading.textContent.trim() : id);
      var kw = (m.kw || '') + ' ' + title + ' ' + (sec.textContent || '').slice(0, 800);
      searchIndex.push({
        id: id,
        title: title,
        keywords: kw.toLowerCase(),
        anchor: '#' + id
      });
    });
  }

  /* ───── Search function ───── */
  function search(query){
    if(!query || query.length < 2) return [];
    var q = query.toLowerCase().trim();
    var terms = q.split(/\s+/).filter(function(t){ return t.length > 0; });

    var results = [];
    searchIndex.forEach(function(item){
      var score = 0;
      var text = item.keywords;
      var titleLower = item.title.toLowerCase();

      // Score: title match = 5, keyword match = 1 per term
      terms.forEach(function(term){
        if(titleLower.indexOf(term) !== -1) score += 5;
        var re = new RegExp(term, 'gi');
        var matches = text.match(re);
        if(matches) score += matches.length;
      });

      if(score > 0) results.push({ item: item, score: score });
    });

    results.sort(function(a,b){ return b.score - a.score; });
    return results.slice(0, 8);
  }

  /* ───── Highlight matched text ───── */
  function highlight(text, query){
    if(!query) return text;
    var terms = query.toLowerCase().split(/\s+/).filter(function(t){ return t.length > 1; });
    var out = text;
    terms.forEach(function(t){
      var re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
      out = out.replace(re, '<mark>$1</mark>');
    });
    return out;
  }

  /* ───── Render results ───── */
  var modal = document.getElementById('searchModal');
  var input = document.getElementById('searchModalInput');
  var resultsEl = document.getElementById('searchModalResults');
  var activeIndex = 0;
  var currentResults = [];

  function renderResults(query){
    currentResults = search(query);
    activeIndex = 0;

    if(!query || query.length < 2){
      resultsEl.innerHTML = '<div class="search-empty">' +
        '<strong>Start typing…</strong>' +
        'Search: packages, prices, results, founder, warranty, FAQ, tours, location — anything.' +
      '</div>';
      return;
    }

    if(currentResults.length === 0){
      resultsEl.innerHTML = '<div class="search-empty">' +
        '<strong>No results found</strong>' +
        'Try: "packages", "prices", "founder", "warranty", "tours", "FAQ"' +
      '</div>';
      return;
    }

    resultsEl.innerHTML = currentResults.map(function(r, i){
      return '<a href="' + r.item.anchor + '" class="search-result-item' +
        (i === 0 ? ' active' : '') + '" data-index="' + i + '">' +
        '<strong>' + highlight(r.item.title, query) + '</strong>' +
        '<span>Jump to section →</span>' +
      '</a>';
    }).join('');
  }

  function openSearch(){
    if(!modal) return;
    buildIndex();
    modal.classList.add('open');
    modal.setAttribute('aria-hidden','false');
    document.body.style.overflow = 'hidden';
    setTimeout(function(){ input.focus(); input.select(); }, 100);
    renderResults(input.value);
  }
  function closeSearch(){
    if(!modal) return;
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden','true');
    document.body.style.overflow = '';
    input.value = '';
  }

  /* ───── Keyboard nav ───── */
  function moveActive(delta){
    if(currentResults.length === 0) return;
    activeIndex = (activeIndex + delta + currentResults.length) % currentResults.length;
    var items = resultsEl.querySelectorAll('.search-result-item');
    items.forEach(function(el, i){
      el.classList.toggle('active', i === activeIndex);
    });
    var active = items[activeIndex];
    if(active) active.scrollIntoView({ block:'nearest', behavior:'smooth' });
  }

  function jumpToActive(){
    if(currentResults.length === 0) return;
    var target = currentResults[activeIndex].item.anchor;
    closeSearch();
    setTimeout(function(){
      var el = document.querySelector(target);
      if(el){
        var headerH = (document.querySelector('.site-header') || {}).offsetHeight || 0;
        var y = el.getBoundingClientRect().top + window.pageYOffset - headerH - 20;
        window.scrollTo({ top:y, behavior:'smooth' });
      }
    }, 150);
  }

  /* ───── Attach events ───── */
  var trigger = document.getElementById('searchTrigger');
  if(trigger){
    trigger.addEventListener('click', openSearch);
  }

  // Mobile search button
  var mobileSearchBtn = document.getElementById('mobileSearchBtn');
  if(mobileSearchBtn){
    mobileSearchBtn.addEventListener('click', function(){
      openSearch();
      var menu = document.getElementById('mobileMenu');
      var btn = document.getElementById('menuBtn');
      if(menu) menu.classList.remove('open');
      if(btn) btn.classList.remove('open');
    });
  }

  if(modal){
    document.querySelectorAll('[data-search-close]').forEach(function(el){
      el.addEventListener('click', closeSearch);
    });

    document.addEventListener('keydown', function(e){
      // ⌘K / Ctrl+K to open
      if((e.metaKey || e.ctrlKey) && e.key === 'k'){
        e.preventDefault();
        if(modal.classList.contains('open')) closeSearch();
        else openSearch();
        return;
      }
      if(!modal.classList.contains('open')) return;

      if(e.key === 'Escape'){ e.preventDefault(); closeSearch(); }
      if(e.key === 'ArrowDown'){ e.preventDefault(); moveActive(1); }
      if(e.key === 'ArrowUp'){ e.preventDefault(); moveActive(-1); }
      if(e.key === 'Enter'){ e.preventDefault(); jumpToActive(); }
    });

    if(input){
      input.addEventListener('input', function(){
        renderResults(this.value);
      });
    }

    resultsEl.addEventListener('click', function(e){
      var item = e.target.closest('.search-result-item');
      if(!item) return;
      e.preventDefault();
      var idx = parseInt(item.dataset.index || '0', 10);
      activeIndex = idx;
      jumpToActive();
    });
  }
})();

// ===== EXTRACTED SCRIPT BLOCK =====

(function() {
  // 1. إخفاء أكواد الـ CSS القديمة اللي بتظهر الصفر
  const style = document.createElement('style');
  style.innerHTML = '.css-counter::after { display: none !important; }';
  document.head.appendChild(style);

  // 2. انتظار انتهاء سكريبت ترتيب الأقسام (1.5 ثانية) ثم تشغيل العداد
  setTimeout(() => {
    const counters = document.querySelectorAll('.css-counter');
    
    const animateCounter = (el) => {
      if (el.dataset.animated) return; // يشتغل مرة واحدة بس
      el.dataset.animated = 'true';

      const styleAttr = el.getAttribute('style') || '';
      const match = styleAttr.match(/--target:\s*(\d+)/);
      if (!match) return;
      
      const target = parseInt(match[1], 10);
      const duration = 1800;
      const startTime = performance.now();
      
      const update = (currentTime) => {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easeOut = 1 - Math.pow(1 - progress, 3);
        
        el.textContent = Math.floor(easeOut * target);
        
        if (progress < 1) {
          requestAnimationFrame(update);
        } else {
          el.textContent = target;
        }
      };
      requestAnimationFrame(update);
    };

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1 });

      counters.forEach(counter => {
        counter.textContent = '0';
        observer.observe(counter);
      });
    } else {
      counters.forEach(animateCounter);
    }
  }, 1500);
})();

// ===== EXTRACTED SCRIPT BLOCK =====

(function(){
  var toggles = document.querySelectorAll('#darkModeToggle, #mobileDarkModeToggle');
  if(toggles.length === 0) return;
  var isDark = localStorage.getItem('nileDarkMode') === 'true';
  if(isDark) document.documentElement.classList.add('dark-mode');
  toggles.forEach(function(btn) {
    btn.addEventListener('click', function(){
      var dark = document.documentElement.classList.toggle('dark-mode');
      localStorage.setItem('nileDarkMode', dark ? 'true' : 'false');
    });
  });
})();

// ===== EXTRACTED SCRIPT BLOCK =====

(function(){
  'use strict';
  function centerMapOnMobile(){
    if (window.innerWidth > 767) return;
    var wrap = document.querySelector('.world-map-wrap');
    if (!wrap) return;
    // Center on Egypt (hub at 55% of SVG)
    var maxScroll = wrap.scrollWidth - wrap.clientWidth;
    if (maxScroll <= 0) return;
    // Egypt is at ~50% of SVG width after viewBox change
    var targetScroll = maxScroll * 0.5;
    wrap.scrollLeft = targetScroll;
  }
  // Center on load (after layout settles)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function(){ setTimeout(centerMapOnMobile, 100); });
  } else {
    setTimeout(centerMapOnMobile, 100);
  }
  // Re-center on resize (debounced)
  var resizeTimer;
  window.addEventListener('resize', function(){
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(centerMapOnMobile, 200);
  }, { passive: true });
})();

// ===== EXTRACTED SCRIPT BLOCK =====

(function(){
  'use strict';

  function updateClocks(){
    var clocks = document.querySelectorAll('.map-stat-time[data-tz]');
    var now = new Date();
    clocks.forEach(function(el){
      try {
        var tz = el.getAttribute('data-tz');
        var time = new Intl.DateTimeFormat('en-GB', {
          timeZone: tz,
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        }).format(now);
        el.textContent = time;
      } catch (e) {
        el.textContent = '—';
      }
    });
  }

  // First render
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateClocks);
  } else {
    updateClocks();
  }

  // Update every 15 seconds (accurate enough for minute display)
  setInterval(updateClocks, 15000);
})();

// ===== EXTRACTED SCRIPT BLOCK =====

(function() {
  'use strict';

  // 1. Search Modal Logic (Toggle & Fix)
  var trigger = document.getElementById('searchTrigger');
  var modal = document.getElementById('searchModal');
  
  if (trigger && modal) {
    trigger.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation(); // Prevent event bubbling
      
      var isOpen = modal.classList.contains('open');
      if (isOpen) {
        modal.classList.remove('open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      } else {
        modal.classList.add('open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        var input = document.getElementById('searchModalInput');
        if (input) setTimeout(function() { input.focus(); }, 100);
      }
    });
    
    // Close on overlay click or close button
    modal.addEventListener('click', function(e) {
      if (e.target === modal || e.target.hasAttribute('data-search-close') || e.target.closest('[data-search-close]')) {
        modal.classList.remove('open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      }
    });
    
    // ESC key to close
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && modal.classList.contains('open')) {
        modal.classList.remove('open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      }
    });
  }

  // 2. Dynamic Header & Dock Theming (Pure IntersectionObserver — Zero Layout Thrashing)
  var header = document.getElementById('header');
  var dock = document.getElementById('appleDock');
  var darkSections = document.querySelectorAll('.hero, .bg-nile-blue, .bg-nile-blue-dark, #science, #consult, #turkey-rescue, #top-tier, #guarantees, #legal');

  if (header && darkSections.length) {
    var intersectingDarkHeader = new Set();
    var wasHeaderDark = null;
    var headerObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          intersectingDarkHeader.add(entry.target);
        } else {
          intersectingDarkHeader.delete(entry.target);
        }
      });
      var isDark = intersectingDarkHeader.size > 0;
      if (isDark !== wasHeaderDark) {
        wasHeaderDark = isDark;
        requestAnimationFrame(function() {
          header.classList.toggle('theme-dark', isDark);
          header.classList.toggle('theme-light', !isDark);
        });
      }
    }, { rootMargin: '0px 0px -85% 0px', threshold: 0 });

    darkSections.forEach(function(sec) { headerObserver.observe(sec); });
  }

  if (dock && darkSections.length) {
    var intersectingDarkDock = new Set();
    var wasDockDark = null;
    var dockThemeObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          intersectingDarkDock.add(entry.target);
        } else {
          intersectingDarkDock.delete(entry.target);
        }
      });
      var isDark = intersectingDarkDock.size > 0;
      if (isDark !== wasDockDark) {
        wasDockDark = isDark;
        requestAnimationFrame(function() {
          dock.classList.toggle('theme-dark', isDark);
          dock.classList.toggle('theme-light', !isDark);
        });
      }
    }, { rootMargin: '-85% 0px 0px 0px', threshold: 0 });

    darkSections.forEach(function(sec) { dockThemeObserver.observe(sec); });
  }

  // 3. Dock Active State (Debounced & Layout-Thrashing-Proof)
  var dockItems = document.querySelectorAll('.dock-item[data-target]');
  if (dockItems.length) {
    var navSections = Array.from(dockItems).map(function(item) {
      return { el: document.getElementById(item.getAttribute('data-target')), link: item };
    }).filter(function(s) { return s.el !== null; });

    var currentActive = '';
    var activeObserver = new IntersectionObserver(function(entries) {
      var latestIntersectingId = null;
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          latestIntersectingId = entry.target.id;
        }
      });

      if (latestIntersectingId && latestIntersectingId !== currentActive) {
        currentActive = latestIntersectingId;
        requestAnimationFrame(function() {
          dockItems.forEach(function(item) {
            item.classList.toggle('active', item.getAttribute('data-target') === currentActive);
          });
        });
      }
    }, { rootMargin: '-20% 0px -50% 0px', threshold: 0.1 });

    navSections.forEach(function(s) { activeObserver.observe(s.el); });
  }
})();

// ===== EXTRACTED SCRIPT BLOCK =====

(function(){
      var mapWrap = document.querySelector('.world-map-wrap');
      if(!mapWrap) return;
      var svg = mapWrap.querySelector('svg');
      if(!svg) return;
      
      var observer = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if(entry.isIntersecting){
            if(svg.unpauseAnimations) svg.unpauseAnimations();
          } else {
            if(svg.pauseAnimations) svg.pauseAnimations();
          }
        });
      }, { threshold: 0 });
      observer.observe(mapWrap);
    })();

// ===== EXTRACTED SCRIPT BLOCK =====

(function(){
  'use strict';
  // أسعار تحويل تقريبية (يمكنك تعديلها لاحقاً)
  const rates = {
    USD: 1,
    AUD: 1.52,
    GBP: 0.78,
    EUR: 0.92,
    CAD: 1.36
  };

  const symbols = {
    USD: '$',
    AUD: 'A$',
    GBP: '£',
    EUR: '€',
    CAD: 'C$'
  };

  // إضافة أزرار العملات داخل قسم الباقات
  const packagesSection = document.getElementById('packages');
  if(packagesSection){
    const header = packagesSection.querySelector('.text-center');
    if(header){
      const switcherHTML = `
        <div class="currency-switcher mt-6">
          <button class="currency-btn active" data-currency="USD">USD ($)</button>
          <button class="currency-btn" data-currency="AUD">AUD (A$)</button>
          <button class="currency-btn" data-currency="GBP">GBP (£)</button>
          <button class="currency-btn" data-currency="EUR">EUR (€)</button>
          <button class="currency-btn" data-currency="CAD">CAD (C$)</button>
        </div>
      `;
      header.insertAdjacentHTML('beforeend', switcherHTML);
    }
  }

  // دالة تحويل الأسعار
  function convertPrices(currency) {
    const rate = rates[currency];
    const symbol = symbols[currency];
    
    // البحث عن كل الأسعار داخل قسم الباقات
    const priceElements = document.querySelectorAll('#packages .font-serif.font-bold.text-nile-gold');
    
    priceElements.forEach(el => {
      const text = el.innerText;
      const match = text.match(/([\d,]+)/);
      if (match) {
        const originalNum = parseFloat(match[0].replace(/,/g, ''));
        if (originalNum > 0) {
          const newNum = Math.round(originalNum * rate);
          const formattedNewNum = newNum.toLocaleString('en-US');
          const newText = text.replace(match[0], formattedNewNum).replace('$', symbol);
          el.innerHTML = newText;
        }
      }
    });
  }

  // تفعيل الأزرار
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('currency-btn')) {
      document.querySelectorAll('.currency-btn').forEach(btn => btn.classList.remove('active'));
      e.target.classList.add('active');
      convertPrices(e.target.dataset.currency);
    }
  });
})();