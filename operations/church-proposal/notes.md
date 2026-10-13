# notes.md — 수정 기록 (최신이 위)

> 매 사용 뒤 5분. 오류·수정·배운 것을 날짜별로 남깁니다.
> **채팅에서 고치지 말고 폴더에서 고칩니다** — 이 파일이 그 증거.

---

## 2026-10-02 · HebronGuide 수치 갱신 "78+" → "81+"

- **무엇**: 목사님이 알려주신 현재 수치 (81개 도시) 를 반영.
- **레이어**: 툴박스 (정본 1개 수정 → 참조 체인 가동).
- **변경 파일**:
  - 정본: `files/hebronguide-blurb.md` (3 버전 + 금지 섹션 설명 모두)
  - 참조: `files/tone-rules.md` · `files/price-breakdown.md`
  - 상위 문서: `docs/03_교회섹션_재구성안.md` (4곳) · `docs/04_세일즈_스크립트.md` (2곳) · `docs/05_1페이지_소개서.md` (1곳)
- **사이트 본문** (`index.src.html` / `index.html`): build.py 가 hebronguide.com/city-count.js 에서 실시간 치환하므로 자동. 수동 수정 불필요.
- **배운 것 → 1.1 로**: "정본 하나만 수정" 이 이상이지만, **과거에 복사된 하드코딩**은 참조 체인에 안 들어와 있음. 다음 번에는 **처음부터 토큰(`{HG_CITIES}`) 또는 변수 참조**로 쓰도록 템플릿을 보강. (`proposal-template.md` 에서 숫자 대신 `[HG_CITIES]` 같은 자리표시자를 쓰고 생성 시 치환하는 방식 검토.)

## 2026-10-02 · 1.0 확정

- **무엇**: 증명 5개 · 가격 ($299·$999·$1,799) · HebronGuide "78+ 도시" · 교회 성격 6 유형 추천 모두 그대로 승인 (목사님 결정).
- **1.0 구성**: SKILL.md + files/ 6개 (정본 2개: price-breakdown · hebronguide-blurb) + examples/README.
- **다음**: 실제 다음 상담 뒤 적용 → 결과를 notes.md 에 기록 → 수정이 쌓이면 1.1 로 올림.

## 2026-10-02 · 1.0-draft 생성

- **무엇**: 두 번째 스킬 폴더 (`church-proposal`) 뼈대와 1.0 초안을 올림.
- **구성**: SKILL.md (프로세스 · 결정 규칙 6개 · 증명 5개) + files/ 6개 (template · price-breakdown [정본] · recommended-designs · legal-boilerplate · hebronguide-blurb [정본] · tone-rules · INDEX) + examples/README.
- **정본 2개 선정**: `price-breakdown.md` (가격) · `hebronguide-blurb.md` (자동 등재 안내) — 다른 자료가 모두 참조.
- **다음**: 목사님 1차 검토 → 수정 지시 → 1.0 확정 → 실제 다음 상담 뒤 적용.

## (여기부터 실제 사용 뒤 추가)

### YYYY-MM-DD · [무엇이 잘못됐는가] → [무엇을 바꿨는가]
- 어느 레이어 실패 (프로세스 / 툴박스 / 증명)
- 어느 파일을 어떻게 바꿨는지
- 같은 오류가 2회째라면 명시적 규칙으로 격상
