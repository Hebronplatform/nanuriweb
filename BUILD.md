# NanuriWeb 빌드 · 배포 안내

## 파일 구조 — 무엇을 편집하고 무엇을 건드리지 않는가

| 파일 | 성격 | 편집 |
|---|---|---|
| `index.src.html` | 메인 페이지 **원본**. `{HG_CITIES}` 토큰 사용 가능 | **여기를 편집** |
| `index.html` | 자동 생성된 배포본 | 편집 금지 (덮어써짐) |
| `build_landing.py` | 업종별 랜딩페이지의 **내용과 레이아웃** | **여기를 편집** |
| `seattle-*/index.html` | 자동 생성된 랜딩페이지 | 편집 금지 (덮어써짐) |
| `build_seo.py` | 구조화 데이터 정의 (요금제·업종 목록) | 요금 바뀌면 편집 |
| `sitemap.xml` · `robots.txt` | 자동 생성 | 편집 금지 |
| `vercel.json` · `404.html` | 수동 관리 | 필요 시 편집 |

---

## 배포 절차 — 이 순서를 지킨다

```bash
python build_seo.py       # 1. FAQ를 읽어 구조화 데이터 갱신
python build.py           # 2. 토큰 치환 → index.html 생성
python build_landing.py   # 3. 랜딩페이지 6종 + sitemap + robots 생성
python verify_seo.py      # 4. 검증 — 실패하면 배포하지 않는다
vercel --prod             # 5. 배포
```

한 줄로:

```bash
python build_seo.py && python build.py && python build_landing.py && python verify_seo.py && vercel --prod
```

`verify_seo.py`가 실패를 반환하면 `&&` 때문에 배포가 자동으로 멈춘다. 이게 이 구조의 핵심이다.

---

## 각 스크립트가 하는 일

### `build.py`
`{HG_CITIES}` · `{HG_TARGET}` 토큰을 실제 숫자로 바꾼다.

**왜 필요한가.** 브라우저 JS가 실행 시점에 치환하는 구조였는데, 구글·카카오톡·페이스북 수집기는 JS를 실행하지 않는다. 그래서 검색 결과 제목과 공유 미리보기에만 `{HG_CITIES}`가 그대로 노출됐다. 사람 눈에는 정상으로 보여서 발견이 늦었다.

hebronguide.com/city-count.js 에서 실시간 도시 수를 받아온다. 접속 실패 시 `FALLBACK_CITIES` 값을 쓴다.

```bash
python build.py               # 실시간 값으로
python build.py --cities 82   # 직접 지정
python build.py --check       # 검사만
```

### `build_seo.py`
`index.src.html`의 한국어 FAQ 사전을 읽어 JSON-LD를 만든다.

**왜 자동 추출인가.** FAQ를 화면용과 구조화 데이터용으로 두 벌 관리하면 반드시 어긋난다. 화면에 보이는 FAQ가 곧 구조화 데이터가 되게 해서 어긋날 수가 없게 만들었다.

생성 노드: `Organization` · `WebSite` · `ProfessionalService` · `FAQPage`(9문항) · `ItemList`(업종 6종)

요금이 바뀌면 이 파일의 `PLANS` 리스트를 화면 요금표와 함께 고친다.

### `build_landing.py`
업종별 랜딩페이지 6종을 만든다. 내용은 `INDUSTRIES` 딕셔너리에, 레이아웃은 `TEMPLATE`에 있다.

각 페이지 구성: 업종별 실제 고통 4가지 + 해결 → 포함 내용 → 권장 플랜 → 에덴교회 실사례 → 업종별 FAQ → CTA

`sitemap.xml`과 `robots.txt`도 함께 생성한다.

### `verify_seo.py`
배포 전 8가지를 검사하고, 하나라도 실패하면 종료 코드 1을 반환한다.

1. JSON-LD가 실제로 파싱되는가
2. 필수 메타 태그 10종이 있는가
3. 치환 안 된 토큰이 남았는가
4. canonical 주소가 통일됐는가 (www 혼입 여부)
5. title·description 길이가 검색 결과에서 잘리지 않는가
6. h1이 페이지당 정확히 하나인가
7. 모든 img에 alt가 있는가
8. sitemap의 URL이 실제 파일과 일치하는가

---

## 배포 후 한 번만 하는 일

### 1. Vercel — apex 도메인을 Primary로

현재 `nanuriweb.com` → `www.nanuriweb.com` 으로 리다이렉트되는데, 코드의 canonical은 `nanuriweb.com`(www 없음)을 가리킨다. 구글이 서로 다른 신호를 받아 평가가 분산된다.

`vercel.json`에 www → apex 리다이렉트를 넣어 두었지만, Vercel 대시보드 설정이 우선한다. 다음을 확인한다.

```
Vercel 대시보드 → nanuriweb 프로젝트 → Settings → Domains
  nanuriweb.com          ← 이쪽에 "Primary" 표시가 있어야 한다
  www.nanuriweb.com      ← "Redirect to nanuriweb.com" 이어야 한다
```

www 쪽이 Primary로 되어 있으면, `nanuriweb.com` 옆의 점 세 개 메뉴에서 **Set as Primary Domain**을 누른다.

확인 방법 — 브라우저 주소창에 `www.nanuriweb.com`을 치면 `nanuriweb.com`으로 바뀌어야 한다.

### 2. 구글 서치 콘솔 등록

1. [search.google.com/search-console](https://search.google.com/search-console) 접속
2. 속성 추가 → **도메인** 방식 선택 → `nanuriweb.com` 입력
   (도메인 방식이면 www 유무와 http/https를 한 번에 다 잡는다)
3. 표시되는 TXT 레코드를 도메인 DNS에 추가 → 확인
4. 좌측 메뉴 **Sitemaps** → `sitemap.xml` 입력 → 제출
5. 좌측 메뉴 **URL 검사**에 각 랜딩페이지 주소를 넣고 **색인 생성 요청**

색인까지 보통 며칠에서 2주가 걸린다. 조급해하지 않는다.

### 3. 확인해 볼 곳

| 무엇 | 어디서 |
|---|---|
| 구조화 데이터가 제대로 읽히는지 | [search.google.com/test/rich-results](https://search.google.com/test/rich-results) |
| 카카오톡·페이스북 공유 미리보기 | [developers.facebook.com/tools/debug](https://developers.facebook.com/tools/debug/) |
| 페이지 속도 | [pagespeed.web.dev](https://pagespeed.web.dev/) |

공유 미리보기가 예전 것으로 뜨면 페이스북 디버거에서 **Scrape Again**을 누른다. 카카오톡은 캐시가 오래 남으니 며칠 기다린다.

---

## robots.txt 정책

검색엔진(구글·빙·네이버)에는 열어 두고, 학습용 대량 수집 봇은 막아 두었다.

차단 목록: `GPTBot` · `CCBot` · `ClaudeBot` · `Google-Extended` · `anthropic-ai` · `Bytespider` · `PerplexityBot`

이 정책을 바꾸려면 `build_landing.py`의 `write_robots()` 안 `blocked` 리스트를 고친다.

색인 제외 경로: `/clients/` · `/agency/` · `/ops/` · `/shared/` · `/99_Archive/` · `*.src.html`

---

## 자주 겪을 상황

**Q. 도시 수가 82에서 90으로 늘었다.**
`python build.py` 만 다시 돌리면 hebronguide.com에서 새 값을 받아온다. `build.py`의 `FALLBACK_CITIES`도 같이 올려 두면 좋다.

**Q. FAQ를 하나 추가했다.**
`index.src.html`의 `'faq.q10'` · `'faq.a10'`을 추가한 뒤 `python build_seo.py`를 돌리면 구조화 데이터에 자동으로 들어간다.

**Q. 요금을 바꿨다.**
`index.src.html`의 요금표와 `build_seo.py`의 `PLANS`를 **둘 다** 고친다. 여기만 아직 자동화되어 있지 않다.

**Q. 새 업종 페이지를 추가하고 싶다.**
`build_landing.py`의 `INDUSTRIES` 리스트에 항목을 하나 더 넣고, `build_seo.py`의 `LANDING` 리스트에도 같이 넣는다. 그리고 `index.src.html`의 업종 카드에 링크를 추가한다.

**Q. `index.html`을 실수로 직접 고쳤다.**
다음 빌드에 사라진다. 파일 맨 위 경고 배너를 확인하고, 같은 내용을 `index.src.html`에 옮겨 적은 뒤 빌드한다.
