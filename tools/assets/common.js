// 광고/후원 영역을 config.js 설정에 따라 렌더링
(function () {
  var c = window.SITE_CONFIG || {};

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
