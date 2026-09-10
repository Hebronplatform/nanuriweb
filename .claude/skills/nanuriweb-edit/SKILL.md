---
name: nanuriweb-edit
description: NanuriWeb(nanuriweb.com) 사이트를 편집·빌드·검증·배포하는 워크플로우와 ko/en/es 문구 동기화, 가격 위치 지도, 배포 안전 규칙. 사이트의 내용·디자인·가격·문구를 수정하거나 배포할 때 사용한다.
---

# NanuriWeb 편집·배포 워크플로우

NanuriWeb은 **단일 HTML 정적 사이트**다. 실배포본은 `index.html`(Vercel, remote=Hebronplatform/nanuriweb, canonical=www.nanuriweb.com).

## 절대 규칙 (먼저 읽기)

1. **편집은 `index.src.html`에만.** `index.html`은 `build.py`가 자동 생성 → 직접 편집 금지(다음 빌드에 덮어씀).
2. **배포 순서:** `index.src.html` 편집 → `python build.py` → `git add index.src.html index.html` → commit → `git push origin HEAD:main` (Vercel 자동배포). **main에 직접 푸시**한다(이 repo의 배포 방식).
3. **`build.py`가 배포 전 JS 문법을 검증**한다(`node --check`). 실패하면 배포 중단 — **오류를 고치고 다시 빌드**할 것. (통과 메시지: "인라인 스크립트 N개 — 문법 통과")

## i18n 3중 동기화 (문구 수정 시 필수)

문구는 `data-i18n` / `data-i18n-html` 로 다국어 처리된다. 하나를 바꾸면 **네 곳 모두** 바꾼다:
- **fallback HTML** (본문의 `data-i18n="key">…</…>` 안 텍스트)
- **`LANG.ko`**, **`LANG.en`**, **`LANG.es`** (인라인 `<script>`의 LANG 객체)

언어: `setLang()`/`currentLang`/`document.documentElement.lang`. 브라우저 자동감지(ko→ko, 그 외→en), 선택은 localStorage. 단일 토글 버튼(글로브 + 클릭 시 한↔영), 데스크톱·모바일 모두 노출.

### ⚠ i18n 문자열 안 따옴표 (2026-09 사고)
LANG 값은 **작은따옴표 `'…'`** 로 감싼다. 값 안에 작은따옴표를 넣으면 문자열이 조기 종료되어 **스크립트 전체가 깨지고 `.reveal` 요소가 안 나타나 사이트 내용이 사라진다.** → 값 안에서는 반드시 **큰따옴표 `"…"`** 를 쓸 것. (`build.py`의 JS 검증이 이제 이런 오류를 잡아준다.)

## 가격 위치 지도 (가격 변경 시 전부 동기화)

한 플랜의 가격은 여러 곳에 흩어져 있다. 예: Starter 제작비를 바꾸면 아래 **전부**:
- 플랜 카드 `.plan-price2`
- House Church 비교표 (special 카드 안 요약)
- 연락 드롭다운 `contact.plan.g1o*` (ko/en/es)
- 모바일 메뉴 `mob.nav.plans.desc` (ko/en/es)
- `fork.church.desc` (ko/en/es)
- JSON-LD `"price"` (구조화 데이터)

관리비는 **월 표기 + 실제 연납**이 원칙. 라벨은 "관리비"(연관리비 아님).

## 콘텐츠·브랜딩 원칙

- **HebronGuide = "글로벌 환대 플랫폼"** (한인 디렉터리로 축소 금지). 홈페이지 완성 즉시 자동 등재가 핵심 차별점.
- **톤: 존중·동행** ("몰라도 됩니다" 같은 무시성 표현 금지 → "함께 고민/맡겠습니다"). 결과 중심("만드는 순간 발견됩니다"). 사명 우선(개척교회·환대).
- **주장엔 근거를 각주에** (예: "시중가 대비 80%"는 시장조사 근거를 각주에). 과장 금지.
- 화면 문구는 **한/영만**. SEO 메타/JSON-LD의 스페인어 키워드는 유지(검색 노출). es 번역 테이블은 비노출로 유지.
- 이모지 대신 SVG 아이콘. 아이콘은 `<use href="#ic-…"/>` — 참조 전에 `<symbol id="ic-…">`가 정의됐는지 확인(없으면 빈칸).
- 히어로: 데스크톱=사진 위 글자 오버레이, 모바일=사진 상단/글자 하단(상하분리). 밝은 사진 톤 선호.

## 배포·인프라 주의

- **기밀 폴더 커밋 금지:** `ops/ clients/ Doc/ agency/ _vercel/ _claude/ 강의이미지` (gitignore됨). `git add -A` 주의 — 가능하면 파일 명시.
- **`vercel.json`에 www→apex redirect 재추가 금지** (대시보드 apex→www와 충돌해 무한루프). apex canonical 원하면 Vercel 대시보드에서 Primary 설정 먼저.
- 라이브 변경은 **목사님(kchurch911) 승인 후 배포**. 배포 전 로컬 미리보기(`python -m http.server`)로 확인 권장.
- `{HG_CITIES}`/`{HG_TARGET}` 토큰은 `build.py`가 치환(SEO 크롤러 대비). 브라우저 JS도 런타임 치환.

## 빠른 체크리스트
1. `index.src.html` 편집 (문구면 ko/en/es 4곳)
2. `python build.py` → **JS 검증 통과** 확인
3. 로컬/브라우저로 눈으로 확인
4. `git add index.src.html index.html` → commit → `git push origin HEAD:main`
5. 라이브(nanuriweb.com) 반영 확인
