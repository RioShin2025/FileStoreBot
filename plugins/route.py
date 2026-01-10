# ---------------------------------------------------
# File Name: Route.py
# Author: NeonAnurag
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# YouTube: https://youtube.com/@MyselfNeon
# Created: 2025-10-21
# Last Modified: 2025-10-22
# Version: Latest
# License: MIT License
# ---------------------------------------------------

from aiohttp import web
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.Response(
        text="""
        <!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>BotsKingdoms • File Store Bot</title>
<meta name="description" content="BotsKingdoms File Store Bot — store files and generate share links on Telegram." />

<style>
  :root{
    --bg0:#050815;
    --bg2:#0a1023;

    --text:#f6f8ff;
    --muted:rgba(255,255,255,.70);
    --muted2:rgba(255,255,255,.55);

    --border:rgba(255,255,255,.12);

    --brand:#4ae7ff;
    --brand2:#7dffd6;
    --ok:#3dff9a;

    --r14:14px;
    --r18:18px;
    --r22:22px;

    --shadow:0 22px 80px rgba(0,0,0,.52);
    --shadow2:0 12px 36px rgba(0,0,0,.38);
  }

  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{
    margin:0;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, "Noto Sans";
    color:var(--text);
    background:
      radial-gradient(900px 500px at 20% 0%, rgba(74,231,255,.18), transparent 60%),
      radial-gradient(900px 500px at 85% 25%, rgba(125,255,214,.14), transparent 60%),
      linear-gradient(180deg, var(--bg0), var(--bg2));
    overflow-x:hidden;
  }

  .grain{
    pointer-events:none;
    position:fixed;
    inset:0;
    opacity:.08;
    mix-blend-mode:overlay;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)' opacity='.55'/%3E%3C/svg%3E");
  }

  .wrap{max-width:1100px;margin:0 auto;padding: 14px 14px 60px;}

  /* NAV */
  .nav{
    position:sticky; top:10px; z-index:50;
    display:flex; justify-content:space-between; align-items:center; gap:10px;
    padding: 10px 12px;
    border-radius: var(--r22);
    border:1px solid var(--border);
    background: rgba(255,255,255,.05);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    box-shadow: var(--shadow2);
  }
  .nav-left{display:flex;align-items:center;gap:10px;min-width:0}
  .logo{width:38px;height:38px;border-radius:14px;object-fit:cover;border:1px solid rgba(74,231,255,.35)}
  .brand{display:flex;flex-direction:column;line-height:1.1;min-width:0}
  .brand b{letter-spacing:.1em;text-transform:uppercase;font-size:.9rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .brand span{color:var(--muted);font-size:.84rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}

  .nav-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:flex-end}
  .chip{
    display:inline-flex; align-items:center; gap:8px;
    padding: 9px 10px;
    border-radius: 999px;
    border:1px solid rgba(255,255,255,.12);
    background: rgba(0,0,0,.14);
    color: var(--muted);
    font-weight:800;
    font-size:.88rem;
    white-space:nowrap;
  }
  .dot{width:10px;height:10px;border-radius:999px;background:var(--ok);box-shadow:0 0 0 6px rgba(61,255,154,.14)}
  .start{
    text-decoration:none;
    padding: 10px 12px;
    border-radius: 999px;
    font-weight:900;
    color:#061018;
    background: linear-gradient(90deg, var(--brand), var(--brand2));
    box-shadow: 0 10px 24px rgba(74,231,255,.20);
  }

  .section{margin-top: 16px;}
  .panel{
    border:1px solid var(--border);
    background: rgba(255,255,255,.05);
    border-radius: var(--r22);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: var(--shadow);
    overflow:hidden;
    position:relative;
  }
  .panel::before{
    content:"";
    position:absolute; inset:-2px;
    background: radial-gradient(900px 260px at 18% 0%, rgba(74,231,255,.16), transparent 55%);
    pointer-events:none;
  }

  /* HERO */
  .hero{display:grid;grid-template-columns:1fr;gap:12px;}
  @media(min-width: 940px){ .hero{grid-template-columns: 1.05fr .95fr; gap: 18px;} }

  .hero-text{padding: 22px; display:flex; flex-direction:column; gap:12px}
  .kicker{
    width:max-content;
    display:inline-flex; align-items:center; gap:10px;
    padding:10px 12px; border-radius:999px;
    border:1px solid rgba(255,255,255,.12);
    background: rgba(0,0,0,.16);
    color: var(--muted);
    font-size:.9rem;
  }
  .pill{
    padding:4px 10px;border-radius:999px;
    border:1px solid rgba(74,231,255,.22);
    background: rgba(74,231,255,.12);
    font-weight:900;
    letter-spacing:.08em;
    text-transform:uppercase;
    font-size:.76rem;
    color: rgba(255,255,255,.9);
  }
  h1{
    margin:0;
    font-size: clamp(2.05rem, 7vw, 3.4rem);
    line-height:1.06;
    letter-spacing:-.03em;
  }
  .grad{
    background: linear-gradient(90deg, var(--brand), var(--brand2));
    -webkit-background-clip:text;
    background-clip:text;
    color:transparent;
  }
  .desc{margin:0;color:var(--muted);font-size:1.04rem;line-height:1.65}

  .cta{display:flex;gap:10px;flex-wrap:wrap}
  .btn{
    flex: 1 1 160px;
    display:inline-flex;align-items:center;justify-content:center;gap:10px;
    padding: 14px 14px;
    border-radius: var(--r14);
    border:1px solid rgba(255,255,255,.12);
    background: rgba(255,255,255,.04);
    color: var(--text);
    text-decoration:none;
    font-weight:900;
    transition: transform .18s ease, background .18s ease, border-color .18s ease;
  }
  .btn:hover{transform: translateY(-1px);border-color:rgba(255,255,255,.18);background:rgba(255,255,255,.06)}
  .btn.primary{
    border:none;color:#061018;
    background: linear-gradient(90deg, var(--brand), var(--brand2));
    box-shadow: 0 14px 30px rgba(74,231,255,.22);
  }

  /* SINGLE BIG IMAGE */
  .hero-media{padding: 12px;}
  .shot{
    border-radius: var(--r22);
    overflow:hidden;
    border:1px solid rgba(255,255,255,.12);
    background:#000;
    position:relative;
    min-height: 320px;
    isolation:isolate;
  }
  @media(min-width:940px){ .shot{min-height: 440px;} }

  .shot img{
    width:100%;
    height:100%;
    object-fit:cover;
    display:block;
    transform: scale(1.03);
    transition: transform .7s ease;
    will-change: transform;
  }
  .shot:hover img{ transform: scale(1.06); }

  .shot::after{
    content:"";
    position:absolute; inset:0;
    background: linear-gradient(180deg, rgba(0,0,0,.05), rgba(0,0,0,.68));
    pointer-events:none;
    z-index:2;
  }

  .glow{
    position:absolute;
    width:220px;height:220px;
    border-radius:999px;
    background: radial-gradient(circle at 30% 30%, rgba(74,231,255,.28), rgba(74,231,255,0) 65%);
    filter: blur(6px);
    opacity:.9;
    left:-60px; top:-60px;
    animation: float 4s ease-in-out infinite;
    z-index:1;
    pointer-events:none;
  }
  @keyframes float{
    0%{transform: translate(0,0) scale(1)}
    50%{transform: translate(22px,18px) scale(1.06)}
    100%{transform: translate(0,0) scale(1)}
  }

  /* cards */
  .grid{display:grid;grid-template-columns:1fr;gap:12px;}
  @media(min-width: 900px){ .grid{grid-template-columns: repeat(3,1fr);} }

  .card{
    padding: 18px;
    border-radius: var(--r22);
    border:1px solid rgba(255,255,255,.12);
    background: rgba(255,255,255,.04);
    box-shadow: var(--shadow2);
  }
  .icon{
    width:46px;height:46px;border-radius:16px;
    display:grid;place-items:center;
    background: rgba(74,231,255,.12);
    border:1px solid rgba(74,231,255,.18);
    margin-bottom:10px;
    font-size: 1.25rem;
  }
  .card b{display:block;margin-bottom:6px;font-size:1.05rem}
  .card p{margin:0;color:var(--muted);line-height:1.55}

  /* Credits */
  .faq{padding: 18px}
  .links{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px;}
  .alink{
    display:inline-flex;align-items:center;justify-content:center;gap:10px;
    padding: 12px 14px;
    border-radius: 14px;
    border:1px solid rgba(255,255,255,.12);
    background: rgba(0,0,0,.14);
    color: var(--text);
    text-decoration:none;
    font-weight:900;
    flex: 1 1 180px;
  }
  .alink:hover{background: rgba(255,255,255,.06); border-color: rgba(255,255,255,.18)}
  .subtext{color:var(--muted); font-weight:700; font-size:.92rem; margin-top: 8px; line-height:1.6;}

  /* Footer */
  footer{
    margin-top: 14px;
    border:1px solid rgba(255,255,255,.12);
    background: rgba(255,255,255,.03);
    border-radius: var(--r22);
    padding: 14px 16px;
    display:flex;
    justify-content:space-between;
    gap: 12px;
    flex-wrap:wrap;
    color: var(--muted2);
  }
  footer a{color: rgba(255,255,255,.85); text-decoration:none; border-bottom:1px dashed rgba(255,255,255,.28)}
  footer a:hover{border-bottom-color: rgba(74,231,255,.6)}

  /* Reveal animation */
  .reveal{opacity:0; transform: translateY(16px); transition: opacity .7s ease, transform .7s ease; will-change: opacity, transform;}
  .reveal.in{opacity:1; transform: translateY(0);}
  .pop{animation: pop .7s ease both;}
  @keyframes pop{0%{transform: translateY(8px); opacity:0}100%{transform: translateY(0); opacity:1}}

  @media (prefers-reduced-motion: reduce){
    html{scroll-behavior:auto}
    .grain{display:none}
    .reveal{opacity:1; transform:none; transition:none}
    .glow{animation:none}
    .shot img{transition:none}
  }
</style>
</head>

<body>
<div class="grain"></div>

<div class="wrap">

  <!-- NAV -->
  <header class="nav reveal pop">
    <div class="nav-left">
      <img class="logo" src="https://i.rj1.dev/dDVPf.jpg" alt="BotsKingdoms logo">
      <div class="brand">
        <b>BOTSKINGDOMS</b>
        <span>File Store Bot</span>
      </div>
    </div>

    <div class="nav-right">
      <span class="chip"><span class="dot"></span> Online</span>
      <a class="start" href="https://t.me/MaxMayfieldXBot" target="_blank" rel="noopener noreferrer">Start</a>
    </div>
  </header>

  <!-- HERO -->
  <section class="section hero">
    <div class="panel hero-text reveal">
      <div class="kicker">
        <span class="pill">TELEGRAM</span>
       RioShin • BotsKingdoms
      </div>

      <h1>• <span class="grad">File Store Bot</span>  By RioShin•</h1>

      <p class="desc">
        BotsKingdoms File Store Bot helps you save files and create clean share links in seconds —
        fast, simple, and reliable.
      </p>

      <div class="cta">
        <a class="btn primary" href="https://t.me/MaxMayfieldXBot" target="_blank" rel="noopener noreferrer">🚀 Start Bot</a>
        <a class="btn" href="#credits">⭐ Credits</a>
      </div>
    </div>

    <!-- ONLY ONE IMAGE -->
    <div class="panel hero-media reveal">
      <div class="shot">
        <div class="glow" aria-hidden="true"></div>
        <img src="https://i.rj1.dev/dDVPf.jpg" alt="BotsKingdoms preview image">
      </div>
    </div>
  </section>

  <!-- FEATURES -->
  <section id="features" class="section grid">
    <div class="card reveal">
      <div class="icon">🔗</div>
      <b>Clean Links</b>
      <p>Generate neat share links instantly for files and posts.</p>
    </div>
    <div class="card reveal">
      <div class="icon">⚡</div>
      <b>Fast & Stable</b>
      <p>Lightweight UI and optimized performance for quick loads.</p>
    </div>
    <div class="card reveal">
      <div class="icon">🛡️</div>
      <b>Reliable</b>
      <p>Built for daily usage — smooth flow and clean design.</p>
    </div>
  </section>

  <!-- CREDITS -->
  <section id="credits" class="section panel faq reveal">
    <h2 style="margin:0 0 8px; letter-spacing:-.02em;">Credits</h2>
    <div class="subtext">Official links & credits for BotsKingdoms File Store Bot.</div>

    <div class="links">
      <a class="alink" href="https://t.me/BOTSKINGDOMS" target="_blank" rel="noopener noreferrer">📣 BOTSKINGDOMS</a>
      <a class="alink" href="https://github.com/RioShin2025/FileStorebot" target="_blank" rel="noopener noreferrer">💻 GitHub Repo</a>
      <a class="alink" href="https://t.me/RioShin" target="_blank" rel="noopener noreferrer">👤 Developer</a>
    </div>
  </section>

  <!-- FOOTER -->
  <footer class="section reveal">
    <span>•© <span id="y"></span> BotsKingdoms • File Store Bot•</span>
    <span>
      <a href="https://t.me/BOTSKINGDOMS" target="_blank" rel="noopener noreferrer">•BOTSKINGDOMS•</a>
      •
      <a href="https://github.com/RioShin2025/FileStorebot" target="_blank" rel="noopener noreferrer">•GitHub Repo•</a>
      •
      <a href="https://t.me/RioShin" target="_blank" rel="noopener noreferrer">•Developer•</a>
    </span>
  </footer>

</div>

<script>
  document.getElementById("y").textContent = new Date().getFullYear();

  // scroll reveal
  const els = document.querySelectorAll(".reveal");
  const io = new IntersectionObserver((entries) => {
    for(const e of entries){
      if(e.isIntersecting){
        e.target.classList.add("in");
        io.unobserve(e.target);
      }
    }
  }, {threshold: 0.12});
  els.forEach(el => io.observe(el));
</script>
</body>
</html>
        """,
        content_type="text/html"
    )

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app


# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
