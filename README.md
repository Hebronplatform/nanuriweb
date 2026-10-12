# NanuriWeb — Hebron Platform LLC

한인·이민자 커뮤니티 디지털 에이전시. 교회·비즈니스 웹사이트 제작.

## 폴더 구조

```
02_NanuriWeb/
├── Church/              교회 클라이언트
│   └── edendallas/      edendallas.org (담임 신종우 목사)
│       ├── deploy/      배포 사이트 (GitHub → Vercel)
│       ├── _docs/       기획서·설문지·전략 문서
│       ├── _assets/     로고 등 소스 에셋
│       └── _drafts/     이전 작업 파일
├── biz/                 비즈니스 클라이언트 (준비 중)
├── _agency/             NanuriWeb 에이전시 자체 파일
└── _docs/               NanuriWeb 레벨 문서 (인수인계서 등)
```

## 클라이언트 현황

| 클라이언트 | 도메인 | 상태 |
|---|---|---|
| 에덴교회 달라스 | edendallas.org | 배포 준비 중 |

## ★ 제작 레시피 / 플레이북 (교회 웹+앱 주문 시 여기부터)

**"시애틀지구촌교회처럼 만들어 달라"** 는 주문이 오면 아래 문서만 보고 복제한다.

- **플레이북**: `../../04_GMC_PWA/NANURIWEB_PLAYBOOK.md` — **부록 B(2026-09 현재 라이브 기준)를 먼저 읽을 것.**
  (호스팅=GitHub Pages, 공개 홈 VIP→제자 여정 섹션 순서, 상단 네비+햄버거, 셀폰 앱 아이콘/PWA 레시피, 백엔드 `출석부_통합설치.gs` J2116 목자코드, 교체 값 빠른 참조)
- **플래그십 실물(복제 소스)**: `../../04_GMC_PWA/` — 라이브 www.ijiguchon.org
  - 공개 홈: `website/index.html` · 삶공부 `study/` · 성장여정 `path/` · 교인앱 `gmc/` · 내 목양 `my/`
- **자기 홍보 훅**: 모든 사이트 푸터에 은근한 "제작 · NanuriWeb" 한 줄(→ nanuriweb.com) 기본 삽입.

## GitHub

Organization: [Hebronplatform](https://github.com/Hebronplatform)
- `nw-church` — 교회 클라이언트 모노레포
- `nw-biz` — 비즈니스 클라이언트 모노레포 (예정)
