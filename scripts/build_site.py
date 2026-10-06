#!/usr/bin/env python3
"""스쿨킷 정적 페이지 생성기.

scripts/guide_articles.py 의 원고로 다음을 만든다.
- tools/guide/<slug>.html, tools/guide/index.html
- index.html (사이트 루트 = 스쿨킷 메인)
- sitemap.xml

사용법: python3 scripts/build_site.py  (저장소 루트에서 실행)
"""
import html
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guide_articles import ARTICLES  # noqa: E402

SITE = "https://rla3h.github.io"
ADSENSE = "ca-pub-9311904562813203"
TODAY = "2026-10-06"

TOOLS = [
    ("char-count.html", "✍️", "글자수 세기 · 생기부 바이트", "공백 포함/제외 글자수와 NEIS 바이트를 실시간으로. 목표 바이트 진행 바까지.", "인기"),
    ("grade.html", "🏅", "내신 등급 계산기", "석차·수강자 수로 5등급제/9등급제 등급과 등급 컷을 한눈에.", ""),
    ("score.html", "📊", "성적 위치 계산기", "원점수·평균·표준편차로 상위 몇 %인지, 예상 등급을 그래프로 확인.", ""),
    ("timer.html", "⏱️", "뽀모도로 공부 타이머", "25분 집중 + 5분 휴식. 오늘 공부한 시간이 자동으로 쌓여요.", ""),
    ("dday.html", "📅", "수능 D-day · 디데이", "실시간 카운트다운, 디데이 목록 저장, 두 날짜 사이 일수 계산.", ""),
]


def head(title, desc, canonical, assets, extra=""):
    e = html.escape
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="google-adsense-account" content="{ADSENSE}" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(desc)}" />
  <meta property="og:site_name" content="스쿨킷" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta name="theme-color" content="#4c5cf5" />
  <link rel="stylesheet" href="{assets}style.css" />
  <script src="{assets}config.js"></script>
  <script src="{assets}common.js"></script>
{extra}</head>
<body>
"""


def article_page(a, idx):
    e = html.escape
    url = f"{SITE}/tools/guide/{a['slug']}.html"
    ld = ('  <script type="application/ld+json">{"@context":"https://schema.org","@type":"Article",'
          f'"headline":{json_str(a["title"])},"description":{json_str(a["desc"])},'
          f'"datePublished":"{TODAY}","dateModified":"{TODAY}","inLanguage":"ko",'
          '"author":{"@type":"Organization","name":"스쿨킷"},'
          '"publisher":{"@type":"Organization","name":"스쿨킷"},'
          f'"mainEntityOfPage":"{url}"' + '}</script>\n')
    others = [b for b in ARTICLES if b["slug"] != a["slug"]][:4]
    related = "".join(f'<li><a href="{b["slug"]}.html">{b["ico"]} {e(b["title"])}</a></li>' for b in others)
    tool_href, tool_name = a["tool"]
    return head(f"{a['title']} | 스쿨킷", a["desc"], url, "../assets/", ld) + f"""<div class="wrap">
  <article class="post">
    <nav class="crumbs"><a href="../../">스쿨킷</a> › <a href="./">공부 가이드</a></nav>
    <span class="eyebrow">{a['ico']} 공부 가이드</span>
    <h1>{e(a['title'])}</h1>
    <p class="lead">{e(a['desc'])}</p>
    <p class="small">스쿨킷 · {TODAY} 업데이트</p>
    <a class="tool-cta" href="{tool_href}">{a['ico']} <b>{e(tool_name)}</b> 바로 쓰기 →</a>
    <div class="post-body">{a['body']}</div>
    <div class="ad-slot" hidden></div>
    <a class="tool-cta" href="{tool_href}">{a['ico']} 직접 계산해 보기: <b>{e(tool_name)}</b> →</a>
    <section class="card related">
      <h2>함께 읽으면 좋은 글</h2>
      <ul>{related}</ul>
      <p class="small"><a href="./">공부 가이드 전체 보기 →</a></p>
    </section>
  </article>
  <div class="support" hidden></div>
</div>
</body>
</html>
"""


def json_str(s):
    import json
    return json.dumps(s, ensure_ascii=False)


def guide_index():
    e = html.escape
    cards = "".join(f"""
    <a class="card tool reveal" href="{a['slug']}.html">
      <span class="ico">{a['ico']}</span>
      <h2>{e(a['title'])}</h2>
      <p>{e(a['desc'])}</p>
      <span class="go">읽어보기 <i>→</i></span>
    </a>""" for a in ARTICLES)
    desc = "생기부 바이트, 내신 5등급제, 석차 백분율, 표준편차, 뽀모도로 공부법, 디데이 계획까지. 고등학생이 꼭 알아야 할 성적·공부 정보를 쉽게 정리한 스쿨킷 공부 가이드입니다."
    return head("공부 가이드 · 생기부, 내신 등급, 공부법 정리 | 스쿨킷", desc, f"{SITE}/tools/guide/", "../assets/") + f"""<div class="wrap wide">
  <span class="eyebrow">📚 공부 가이드</span>
  <h1>공부 가이드</h1>
  <p class="lead">{e(desc)}</p>
  <div class="tool-grid">{cards}
  </div>
  <div class="ad-slot" hidden></div>
</div>
</body>
</html>
"""


def root_index():
    e = html.escape
    desc = ("스쿨킷은 고등학생을 위한 무료 온라인 도구 모음입니다. 생기부 바이트 계산기, 글자수 세기, 내신 5등급제·9등급제 계산기, "
            "성적 위치(표준편차) 계산기, 뽀모도로 공부 타이머, 수능 D-day와 공부 가이드를 설치 없이 바로 사용하세요.")
    ld = ('  <script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite",'
          f'"name":"스쿨킷","url":"{SITE}/","description":"고등학생을 위한 무료 온라인 도구 모음"' + '}</script>\n')
    tools = "".join(f"""
    <a class="card tool reveal" href="tools/{h}">
      {f'<span class="badge">{b}</span>' if b else ''}
      <span class="ico">{i}</span>
      <h2>{e(n)}</h2>
      <p>{e(d)}</p>
      <span class="go">바로 쓰기 <i>→</i></span>
    </a>""" for h, i, n, d, b in TOOLS)
    guides = "".join(f'<li><a href="tools/guide/{a["slug"]}.html">{a["ico"]} {e(a["title"])}</a></li>' for a in ARTICLES)
    return head("스쿨킷 · 학생 무료 도구 모음 (글자수 세기, 내신 등급 계산기, 공부 타이머, 수능 디데이)", desc, f"{SITE}/", "tools/assets/", ld) + f"""<div class="wrap wide">
  <section class="hero">
    <span class="eyebrow">✨ 설치·로그인 없이 100% 무료</span>
    <h1><span class="rotator" id="rot"><span>생기부 쓸 때도</span></span><br /><span class="grad-text">스쿨킷</span> 하나면 끝</h1>
    <p class="lead">글자수 세기부터 내신 등급, 성적 위치, 공부 타이머, 수능 디데이까지. 학생에게 꼭 필요한 도구와 정보를 모았어요.</p>
    <div class="hero-cta">
      <a class="btn primary" href="tools/char-count.html">✍️ 바이트 계산하기</a>
      <a class="btn sub" href="#tools">전체 도구 보기 ↓</a>
    </div>
    <div class="hero-stats">
      <div><b data-count="{len(TOOLS)}">0</b><span>개 무료 도구</span></div>
      <div><b data-count="{len(ARTICLES)}">0</b><span>편 공부 가이드</span></div>
      <div><b data-count="100" data-suffix="%">0%</b><span>내 기기에만 저장</span></div>
    </div>
  </section>

  <div class="tool-grid" id="tools">{tools}
  </div>

  <div class="ad-slot" hidden></div>

  <section class="card reveal guide-list" style="margin-top:28px">
    <h2>📚 공부 가이드</h2>
    <p class="small">도구를 쓰기 전에 알아두면 좋은 기준과 방법을 정리했어요.</p>
    <ul>{guides}</ul>
    <p><a href="tools/guide/">가이드 전체 보기 →</a></p>
  </section>

  <section class="card reveal">
    <h2>스쿨킷은 이런 곳이에요</h2>
    <p>스쿨킷은 고등학생이 학교생활에서 자주 하는 계산을 빠르고 정확하게 할 수 있도록 만든 무료 도구 모음입니다. 생활기록부를 쓸 때 NEIS 바이트를 세고, 성적표를 받으면 내신 등급과 내 위치를 확인하고, 시험을 앞두고는 디데이와 공부 타이머로 계획을 지킬 수 있어요.</p>
    <p>모든 계산은 이용자의 브라우저 안에서 이루어지며, 입력한 글이나 성적은 서버로 전송되지 않습니다. 각 도구의 계산 기준은 공부 가이드에서 자세히 설명하고 있어요. <a href="tools/about.html">스쿨킷 소개 더 보기</a></p>
  </section>

  <div class="features">
    <div class="card reveal"><span class="e">🔒</span><h3>개인정보 걱정 없음</h3><p>입력한 글과 성적은 서버로 전송되지 않고 내 브라우저에만 저장돼요.</p></div>
    <div class="card reveal"><span class="e">⚡</span><h3>입력 즉시 계산</h3><p>버튼 누를 필요 없이 입력하는 순간 결과가 바로 바뀌어요.</p></div>
    <div class="card reveal"><span class="e">📱</span><h3>폰에서도 편하게</h3><p>모바일·태블릿·PC 어디서나 똑같이 쓸 수 있어요. 다크 모드도 지원해요.</p></div>
  </div>

  <div class="support" hidden></div>
</div>
<script>
  (function () {{
    var words = ["생기부 쓸 때도", "자소서 쓸 때도", "시험 끝나고도", "공부할 때도", "수능 앞두고도"], i = 0, el = document.getElementById("rot");
    setInterval(function () {{ i = (i + 1) % words.length; el.innerHTML = "<span>" + words[i] + "</span>"; }}, 2200);
  }})();
  document.addEventListener("DOMContentLoaded", function () {{
    document.querySelectorAll("[data-count]").forEach(function (el, i) {{
      setTimeout(function () {{ SK.countUp(el, +el.dataset.count, {{ suffix: el.dataset.suffix || "", duration: 1200 }}); }}, 300 + i * 150);
    }});
  }});
</script>
</body>
</html>
"""


def sitemap():
    urls = [f"{SITE}/"]
    urls += [f"{SITE}/tools/{t[0]}" for t in TOOLS]
    urls += [f"{SITE}/tools/guide/"] + [f"{SITE}/tools/guide/{a['slug']}.html" for a in ARTICLES]
    urls += [f"{SITE}/tools/{p}" for p in ("about.html", "contact.html", "privacy.html")]
    body = "\n".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", rel)


if __name__ == "__main__":
    for i, a in enumerate(ARTICLES):
        write(f"tools/guide/{a['slug']}.html", article_page(a, i))
    write("tools/guide/index.html", guide_index())
    write("index.html", root_index())
    write("sitemap.xml", sitemap())
