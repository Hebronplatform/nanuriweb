/**
 * 미주한인회 (샘플) · Sample Korean American Association
 * 예시 데이터 (실존 한인회 아님 · 특정 조직 흉내 금지)
 *
 * 비영리 기관·한인회·문화단체 샘플.
 * 교회·사업체와 같은 구조의 다른 자료.
 */
window.ORG = {
  meta: {
    isSample: true,
    sampleLabel: "예시 · 실존 한인회 아님",
    lang: "ko",
    lastUpdated: "2026-09-17",
    category: "organization"
  },

  identity: {
    nameKo: "미주한인회 (샘플)",
    nameEn: "Sample Korean American Association",
    tagline: "함께 배우고, 함께 남기고, 함께 이어갑니다",
    since: "설립 연도는 문의 시 안내",
    incorporation: {
      status: "501(c)(3) 비영리 · Washington State",
      ein: "00-0000000",
      einNote: "예시 · 실제 EIN은 공개 안 함"
    }
  },

  contact: {
    mailingAddress: "PO Box 5678, Federal Way, WA 98003",
    phone: "(253) 555-0155",
    email: "hello@kaa.example",
    officeHours: "월 · 수 · 금 오전 10시 – 오후 3시",
    directionsNote: "정확한 사무실 위치는 문의 시 안내드립니다"
  },

  welcomeCards: [
    { key: "notices", ko: "공지사항", en: "NOTICES", value: "이번 달 주요 공지", link: "#notices" },
    { key: "events", ko: "다가오는 행사", en: "EVENTS", value: "가을 문화 축제", link: "#events" },
    { key: "programs", ko: "주요 사업", en: "PROGRAMS", value: "네 가지 축", link: "#programs" },
    { key: "give", ko: "후원 안내", en: "GIVE", value: "세금 공제 가능", link: "#give" }
  ],

  aboutBlocks: [
    {
      key: "president_greeting",
      eyebrow: "PRESIDENT'S GREETING",
      title: "회장 인사말",
      body: "동포 여러분, 우리 한인회는 오래된 자랑 대신 오늘의 필요를 살피는 자리에 서 있습니다. 새로 오신 분에게는 손을 내밀고, 오래 계신 분에게는 자리를 지키며, 다음 세대에게는 이야기를 남기는 것 — 그 세 가지를 일로 삼습니다.",
      signature: "회장 · Sample President"
    },
    {
      key: "mission",
      eyebrow: "MISSION",
      title: "미션과 방향",
      body: "지역 한인 커뮤니티가 서로를 알고, 서로를 도우며, 다음 세대에게 전할 이야기를 함께 만듭니다. 정치·상업·개인의 이해를 위한 도구가 아니라, 이웃과 이웃을 잇는 다리로 쓰이길 바랍니다."
    }
  ],

  programs: {
    eyebrow: "PROGRAMS",
    heading: "주요 사업",
    intro: "네 가지 축으로 사업을 운영합니다.",
    items: [
      {
        title: "한국어 학교",
        subtitle: "Korean Language School",
        body: "차세대에게 한국어와 한국 문화를 가르칩니다. 학기별로 신입생을 받습니다."
      },
      {
        title: "한국어 도서관",
        subtitle: "Korean Library",
        body: "한국어 책과 자료를 이웃과 나눕니다. 회원 등록 없이 방문 대여가 가능합니다."
      },
      {
        title: "시니어 프로그램",
        subtitle: "Senior Program",
        body: "어르신들을 위한 정기 모임과 문화 나들이. 첫 방문은 모시러 갑니다."
      },
      {
        title: "커뮤니티 정원",
        subtitle: "Community Garden",
        body: "함께 가꾸는 지역 정원. 이웃 문화를 여는 자리."
      }
    ]
  },

  notices: {
    eyebrow: "NOTICES",
    heading: "공지사항",
    latest: [
      { date: "2026-09-16", title: "가을 문화 축제 자원봉사자 모집", tag: "모집" },
      { date: "2026-09-12", title: "한국어 학교 가을 학기 신입생 등록", tag: "안내" },
      { date: "2026-09-05", title: "9월 이사회 회의록 게시", tag: "공지" }
    ]
  },

  events: {
    eyebrow: "EVENTS",
    heading: "다가오는 행사",
    upcoming: [
      { date: "2026-10-05", title: "가을 문화 축제", place: "지역 커뮤니티 센터", note: "가족 단위 참여 환영" },
      { date: "2026-10-19", title: "차세대 리더 원탁 대화", place: "지역 도서관 대회의실", note: "고등학생·대학생" },
      { date: "2026-11-02", title: "시니어 감사 오찬", place: "한인회 사무실", note: "사전 신청" }
    ]
  },

  news: {
    eyebrow: "STORIES",
    heading: "이달의 이야기",
    latest: [
      { date: "2026-09-10", title: "한국어 학교 30주년, 세 세대가 함께한 사진" },
      { date: "2026-09-03", title: "새 이웃이 처음 사무실에 온 날" }
    ]
  },

  give: {
    eyebrow: "GIVE",
    heading: "후원 안내",
    intro: "후원은 오늘의 사업과 내일의 어린이를 잇는 자리입니다.",
    methods: [
      { title: "Zelle · Check", note: "우편함 주소로 보내 주시면 됩니다" },
      { title: "카드·계좌 (온라인)", note: "안전한 결제 시스템 사용" }
    ],
    receiptNote: "IRS 기준으로 한 번에 $250 이상 기부하신 경우, 세금 공제를 위한 서면 확인서를 연말에 보내 드립니다. 501(c)(3) 비영리 · EIN 00-0000000 (예시)."
  },

  policy: {
    eyebrow: "POLICY",
    heading: "약속 · 안내",
    draftLabel: "변호사 검토 전 초안",
    items: [
      { title: "개인정보 처리방침", body: "회원·행사·후원 시 받는 정보는 안내 목적으로만 사용합니다. 외부에 팔지 않습니다." },
      { title: "접근성 안내", body: "ADA·WCAG 2.1 AA를 지향합니다. 어려운 부분은 알려 주십시오." },
      { title: "자원봉사·아동 안전", body: "청소년 관련 프로그램은 보호자 동의를 먼저 받습니다. 자원봉사자 신원 확인 절차가 있습니다." }
    ]
  },

  cta: {
    primary: { label: "회원 · 후원 문의", href: "mailto:hello@kaa.example" },
    secondary: { label: "행사 일정 보기", href: "#events" },
    visit: { label: "공지사항", href: "#notices" }
  }
};
