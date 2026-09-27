// 스쿨킷 공통 스크립트: 테마, 네비/푸터, 모션, 광고·후원 렌더링
(function () {
  var c = window.SITE_CONFIG || {};
  var root = document.documentElement;

  // ---------- 테마 (깜빡임 방지를 위해 즉시 적용) ----------
  try {
    var saved = localStorage.getItem("sk-theme");
    if (saved === "light" || saved === "dark") root.setAttribute("data-theme", saved);
  } catch (e) {}
  function isDark() {
    var t = root.getAttribute("data-theme");
    if (t) return t === "dark";
    return window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches;
  }

  // ---------- 도구 목록 (네비·푸터 공용) ----------
  var TOOLS = [
    { href: "char-count.html", ico: "✍️", name: "글자수·바이트" },
    { href: "grade.html", ico: "🏅", name: "내신 등급" },
    { href: "score.html", ico: "📊", name: "성적 위치" },
    { href: "timer.html", ico: "⏱️", name: "공부 타이머" },
    { href: "dday.html", ico: "📅", name: "디데이" }
  ];

  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---------- 공용 헬퍼 ----------
  var SK = window.SK = {};
  SK.toast = function (msg) {
    var t = document.querySelector(".toast");
    if (!t) return;
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(SK._tt);
    SK._tt = setTimeout(function () { t.classList.remove("show"); }, 1800);
  };
  // 숫자를 부드럽게 증가/감소시키며 표시
  SK.countUp = function (el, to, opt) {
    opt = opt || {};
    var dec = opt.decimals || 0, suffix = opt.suffix || "";
    var from = parseFloat(el.dataset.v || "0") || 0;
    el.dataset.v = to;
    var fmt = function (v) { return (dec ? v.toFixed(dec) : Math.round(v).toLocaleString()) + suffix; };
    if (reduceMotion || from === to) { el.textContent = fmt(to); return; }
    var start = performance.now(), dur = opt.duration || 450;
    cancelAnimationFrame(el._raf);
    (function step(now) {
      var p = Math.min(1, (now - start) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(from + (to - from) * e);
      if (p < 1) el._raf = requestAnimationFrame(step);
    })(start);
  };
  SK.pop = function (el) {
    el.classList.remove("pop");
    void el.offsetWidth;
    el.classList.add("pop");
  };
  SK.store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v === null ? d : v; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  // ---------- 광고 ----------
  if (c.adsenseClient) {
    var s = document.createElement("script");
    s.async = true;
    s.crossOrigin = "anonymous";
    s.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" + encodeURIComponent(c.adsenseClient);
    document.head.appendChild(s);
  }
  function renderAd(slot) {
    if (c.adsenseClient && c.adsenseSlot) {
      var ins = document.createElement("ins");
      ins.className = "adsbygoogle";
      ins.style.display = "block";
      ins.setAttribute("data-ad-client", c.adsenseClient);
      ins.setAttribute("data-ad-slot", c.adsenseSlot);
      ins.setAttribute("data-ad-format", "auto");
      ins.setAttribute("data-full-width-responsive", "true");
      slot.appendChild(ins);
      try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) {}
      slot.hidden = false;
    } else if (c.adfitUnit) {
      var a = document.createElement("ins");
      a.className = "kakao_ad_area";
      a.style.display = "none";
      a.setAttribute("data-ad-unit", c.adfitUnit);
      a.setAttribute("data-ad-width", "320");
      a.setAttribute("data-ad-height", "100");
      slot.appendChild(a);
      var sc = document.createElement("script");
      sc.async = true;
      sc.src = "https://t1.daumcdn.net/kas/static/ba.min.js";
      slot.appendChild(sc);
      slot.hidden = false;
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    var body = document.body;
    var here = location.pathname.split("/").pop() || "index.html";

    // 배경
    var bg = document.createElement("div");
    bg.className = "bg-aurora";
    bg.setAttribute("aria-hidden", "true");
    bg.innerHTML = "<span></span><span></span><span></span>";
    body.prepend(bg);

    // 네비
    var nav = document.createElement("nav");
    nav.className = "nav";
    nav.innerHTML =
      '<div class="nav-inner"><a class="logo" href="./">🎒 <b>스쿨킷</b></a><div class="nav-links">' +
      TOOLS.map(function (t) {
        return '<a href="' + t.href + '"' + (t.href === here ? ' class="on"' : "") + ' title="' + t.name + '">' + t.ico + ' <span class="txt">' + t.name + "</span></a>";
      }).join("") +
      '</div><button class="theme-btn" type="button" aria-label="다크 모드 전환"></button></div>';
    body.prepend(nav);
    var tb = nav.querySelector(".theme-btn");
    var paintBtn = function () { tb.textContent = isDark() ? "☀️" : "🌙"; };
    paintBtn();
    tb.addEventListener("click", function () {
      var next = isDark() ? "light" : "dark";
      root.setAttribute("data-theme", next);
      SK.store.set("sk-theme", next);
      paintBtn();
    });

    // 푸터
    var ft = document.createElement("footer");
    ft.className = "site";
    ft.innerHTML =
      '<div class="links"><a href="./">스쿨킷 홈</a>' +
      TOOLS.map(function (t) { return '<a href="' + t.href + '">' + t.name + "</a>"; }).join("") +
      '<a href="privacy.html">개인정보처리방침</a></div>© ' + new Date().getFullYear() + " 스쿨킷 · 입력한 내용은 서버로 전송되지 않고 내 기기에만 저장됩니다.";
    body.appendChild(ft);

    // 토스트
    var toast = document.createElement("div");
    toast.className = "toast";
    toast.setAttribute("role", "status");
    body.appendChild(toast);

    // 페이지 진입 모션
    var main = document.querySelector(".wrap");
    if (main) main.classList.add("page-in");

    // 스크롤 등장
    var rv = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window && !reduceMotion) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
      }, { threshold: .12 });
      rv.forEach(function (el, i) { el.style.transitionDelay = (i % 6) * 60 + "ms"; io.observe(el); });
    } else {
      rv.forEach(function (el) { el.classList.add("in"); });
    }

    // 도구 카드 3D 틸트 + 스포트라이트
    if (!reduceMotion && matchMedia("(hover: hover)").matches) {
      document.querySelectorAll("a.tool").forEach(function (card) {
        card.addEventListener("mousemove", function (e) {
          var r = card.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
          card.style.setProperty("--mx", x * 100 + "%");
          card.style.setProperty("--my", y * 100 + "%");
          card.style.transform = "perspective(800px) rotateX(" + (0.5 - y) * 6 + "deg) rotateY(" + (x - 0.5) * 8 + "deg) translateY(-4px)";
        });
        card.addEventListener("mouseleave", function () { card.style.transform = ""; });
      });
    }

    // 광고·후원
    document.querySelectorAll(".ad-slot").forEach(renderAd);
    if (c.supportUrl) {
      document.querySelectorAll(".support").forEach(function (el) {
        var link = document.createElement("a");
        link.href = c.supportUrl;
        link.target = "_blank";
        link.rel = "noopener";
        link.textContent = c.supportLabel;
        el.appendChild(link);
        el.hidden = false;
      });
    }
  });
})();
