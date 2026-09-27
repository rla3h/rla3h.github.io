# 수익화 설정 가이드 (최초 1회, 약 30분)

사이트와 도구는 모두 완성되어 있고 GitHub Pages에서 무료로 자동 운영됩니다.
**수익금을 받을 계정만은 본인 명의로 직접 만들어야 합니다** (신원 확인이 필요해 대신 만들 수 없음).
만 18세 미만이면 AdSense·후원 플랫폼 가입은 보호자 명의가 필요합니다.

## 1. 검색 노출 등록 (필수, 10분) — 트래픽의 원천
1. Google Search Console (https://search.google.com/search-console) → 속성 추가 → URL 접두어 `https://rla3h.github.io/`
2. 소유권 확인: 제공되는 HTML 파일을 저장소 루트에 올리기
3. 왼쪽 메뉴 "Sitemaps" → `sitemap.xml` 제출
4. 네이버 서치어드바이저 (https://searchadvisor.naver.com) 에서도 동일하게 등록 + 사이트맵 제출
   (한국 학생 검색은 네이버 비중이 크므로 꼭 등록)

## 2. 광고 연결 (택 1 또는 둘 다)
### Google AdSense
1. https://adsense.google.com 가입 → 사이트 `rla3h.github.io` 추가
2. 받은 게시자 ID(`ca-pub-...`)를 `tools/assets/config.js`의 `adsenseClient`에 입력
3. 저장소 루트에 `ads.txt` 파일 생성:
   `google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0`
4. 승인 후 광고 단위를 만들어 슬롯 ID를 `adsenseSlot`에 입력
   (승인 심사는 보통 수일~수주 소요)

### 카카오 애드핏
1. https://adfit.kakao.com 가입 → 매체 등록 → 320x100 광고 단위 생성
2. `DAN-...` 코드를 `config.js`의 `adfitUnit`에 입력

## 3. 후원 링크 (선택, 가장 빠른 첫 수익 경로)
Buy Me a Coffee, 투네이션, 토스 익명송금 링크 등을 만들어 `config.js`의 `supportUrl`에 입력.

## 4. 첫 방문자 모으기 (선택이지만 1주 내 수익을 원하면 사실상 필요)
검색 유입은 보통 2~8주 뒤부터 생깁니다. 그 전에는 반 단톡방, 학교 커뮤니티,
에브리타임/오르비 등 학생 커뮤니티에 링크를 한 번 공유하는 것이 가장 효과적입니다.
(스팸성 반복 게시는 금지)

---
`config.js`의 값이 비어 있으면 광고·후원 영역은 자동으로 숨겨지므로, 설정 전에도 사이트는 정상 작동합니다.
