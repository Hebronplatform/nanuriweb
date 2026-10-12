/**
 * 새순가정교회 · Saesun Home Church
 * 예시 데이터 (실존 교회 아님 · 모든 텍스트는 예시)
 *
 * NanuriWeb 교회 템플릿 20종이 공통으로 사용하는 자료 한 벌.
 * 나중에 셀프 편집기(왼쪽 칸·오른쪽 미리보기)를 얹을 수 있도록,
 * 디자인이 바뀌어도 이 자료는 그대로 쓰이는 구조.
 */
window.CHURCH = {
  meta: {
    isSample: true,
    sampleLabel: "예시 · 실존 교회 아님",
    lang: "ko",
    lastUpdated: "2026-09-17"
  },

  identity: {
    nameKo: "새순가정교회",
    nameEn: "Saesun Home Church",
    tagline: "환대의 문이 열려 있습니다",
    verse: {
      ko: "너희는 나그네를 사랑하라 너희도 애굽 땅에서 나그네 되었음이니라",
      ref: "신명기 10:19",
      en: "Love the sojourner, therefore, for you were sojourners in the land of Egypt.",
      refEn: "Deuteronomy 10:19 (ESV)"
    },
    denominationNote: "가정교회 · Home Church Ministry",
    incorporation: {
      status: "501(c)(3) 등록 · Washington State",
      ein: "00-0000000",
      einNote: "예시 · 실제 EIN은 공개 안 함"
    }
  },

  contact: {
    // 자택 주소·개인 전화는 공개하지 않는다는 원칙에 따라
    // 우편함 주소 · 사무 전화 · 이메일만 예시로 둔다.
    mailingAddress: "PO Box 1234, Tacoma, WA 98401",
    officeHours: "화·목 오전 10시 ~ 오후 2시",
    phone: "(253) 555-0123",
    email: "hello@saesun.example",
    // 자세한 위치는 문의 시 안내
    directionsNote: "정확한 예배 장소는 문의 시 안내드립니다",
    mapEmbedUrl: null
  },

  services: [
    {
      key: "sunday_union",
      titleKo: "주일 연합예배",
      titleEn: "Sunday Union Service",
      day: "주일",
      time: "오전 11시",
      timeEn: "Sunday 11:00 AM",
      language: "한국어 (영어 통역 요청 시)",
      note: "온 세대가 함께 모여 드리는 한 예배입니다"
    },
    {
      key: "saturday_dawn",
      titleKo: "토요 새벽기도회",
      titleEn: "Saturday Dawn Prayer",
      day: "토요일",
      time: "오전 6시",
      timeEn: "Saturday 6:00 AM",
      language: "한국어",
      note: "말씀 짧게 · 기도 길게"
    }
  ],

  firstVisit: {
    headingKo: "처음 오시나요",
    headingEn: "First Time Visitor",
    steps: [
      { n: "01", title: "시간 약속", body: "미리 알려 주시면 자리를 준비해 드립니다" },
      { n: "02", title: "환영합니다", body: "명찰·회비·정해진 순서 없이 그냥 오십시오" },
      { n: "03", title: "말씀·나눔", body: "예배 후 목장에서 짧게 인사 나눕니다" }
    ],
    parking: "무료 주차 · 안내표시 따라 오시면 됩니다",
    dressCode: "편한 복장으로 오시면 됩니다",
    childCare: "새 세대(어린이) 프로그램은 예배 중 함께 · 문의 부탁드립니다",
    planVisitCta: "방문 예약 · 문의하기"
  },

  welcomeCards: [
    { key: "worship", ko: "주일 연합예배", en: "SUNDAY WORSHIP", value: "오전 11시", link: "#worship" },
    { key: "directions", ko: "오시는 길", en: "DIRECTIONS", value: "Tacoma, WA · 문의 안내", link: "#contact" },
    { key: "news", ko: "이번 주 소식", en: "THIS WEEK", value: "매주 목요일 갱신", link: "#news" },
    { key: "first", ko: "처음 오시나요", en: "FIRST TIME", value: "환영합니다", link: "#first-visit" }
  ],

  aboutBlocks: [
    {
      key: "pastor_greeting",
      eyebrow: "PASTOR'S GREETING",
      title: "담임목사 인사말",
      body: "안녕하십니까. 우리는 큰 예배당 대신 각자의 집을 열어 서로를 환대합니다. 많은 사람 앞에서 잘 보이는 신앙이 아니라, 한 사람을 정성으로 맞이하는 신앙을 배웁니다. 말씀 앞에서 함께 앉고, 삶의 자리에서 함께 기도합니다. 문은 늘 열려 있으니 오십시오.",
      signature: "담임목사 · Rev. 홍길동"
    },
    {
      key: "vision",
      eyebrow: "VISION",
      title: "우리 교회 표어",
      body: "환대의 문이 열려 있는 교회. 세 축(예배·목장·삶공부)과 네 기둥(말씀·기도·교제·섬김)으로 서로를 세우고, 이웃을 손님이 아니라 식구로 맞이합니다."
    }
  ],

  homegroups: {
    eyebrow: "HOME GROUPS",
    heading: "목장",
    intro: "가정교회의 심장은 주중에 각 가정에서 모이는 목장입니다. 목자·목녀 부부가 섬기고, 처음 오신 분(VIP)을 품습니다.",
    principles: [
      "한 목장은 열 명 안팎으로 유지합니다. 커지면 나눕니다.",
      "매주 한 번, 서로의 이름을 부르며 음식을 나눕니다.",
      "VIP 한 사람의 얼굴을 마음에 품고 기도합니다.",
      "8주 뒤에는 함께 감사하고, 다음 한 사람을 다시 품습니다."
    ],
    // 개별 목장 정보는 이름 대신 지역만 예시로
    groups: [
      { area: "Tacoma North", meets: "화요일 저녁 7시" },
      { area: "Federal Way", meets: "수요일 저녁 7시 30분" },
      { area: "Puyallup", meets: "목요일 저녁 7시" }
    ]
  },

  discipleship: {
    eyebrow: "DISCIPLESHIP",
    heading: "삶공부",
    intro: "삶으로 배우는 성경. 강의보다 나눔이 많은 반편성입니다.",
    courses: [
      { title: "새 가족 반", duration: "6주", note: "교회를 알아가는 시간" },
      { title: "생명의 삶", duration: "12주", note: "복음의 뿌리를 놓는 반" },
      { title: "경건의 삶", duration: "10주", note: "예배와 기도의 리듬" },
      { title: "확신의 삶", duration: "8주", note: "말씀 앞에 서는 훈련" }
    ]
  },

  newGeneration: {
    eyebrow: "NEW GENERATION",
    heading: "새 세대",
    intro: "우리 교회는 지금은 규모가 크지 않아, 어린이도 어른과 한 자리에서 예배드립니다. 필요할 때는 옆방을 열어 아이를 위한 짧은 나눔을 준비합니다. 자세한 것은 문의 부탁드립니다.",
    contactNote: "부모님께서 미리 알려 주시면 준비해 드리겠습니다"
  },

  sermons: {
    eyebrow: "SERMONS",
    heading: "말씀 다시 보기",
    intro: "지난 주일 설교를 언제든 다시 들으실 수 있습니다.",
    latest: [
      { date: "2026-09-14", title: "환대의 식탁", verse: "누가복음 14:12–14", speaker: "담임목사" },
      { date: "2026-09-07", title: "손님을 향한 문", verse: "히브리서 13:2", speaker: "담임목사" },
      { date: "2026-08-31", title: "한 사람을 위한 예배", verse: "누가복음 15:1–7", speaker: "담임목사" }
    ]
  },

  news: {
    eyebrow: "NEWS",
    heading: "교회 소식",
    latest: [
      { date: "2026-09-15", title: "가을 새 가족 반 등록을 받습니다", tag: "안내" },
      { date: "2026-09-12", title: "목장 모임 지역 지도 갱신", tag: "목장" },
      { date: "2026-09-08", title: "9월 지역 섬김의 날 사진", tag: "섬김" }
    ]
  },

  giving: {
    eyebrow: "GIVING",
    heading: "온라인 헌금",
    intro: "지금까지 하나님께서 부어 주신 은혜에 감사하며 드립니다.",
    methods: [
      { title: "Tithe.ly (안전한 카드·계좌 결제)", note: "가장 편리한 방법" },
      { title: "Zelle · Check", note: "우편함 주소로 보내 주시면 됩니다" }
    ],
    receiptNote: "미국 국세청(IRS) 기준으로 한 번에 $250 이상 헌금하신 경우, 세금 공제를 위해 교회의 서면 확인서가 필요합니다. 연말에 확인서를 보내 드립니다. 501(c)(3) 등록 · EIN 00-0000000 (예시)."
  },

  policy: {
    eyebrow: "POLICY",
    heading: "약속 · 안내",
    draftLabel: "변호사 검토 전 초안",
    items: [
      { title: "개인정보 처리방침 (Privacy Policy)", body: "이름·연락처·기도 제목만 받고, 팔지 않습니다. 분석·추적 쿠키를 심지 않습니다. 자세한 문안은 검토 전 초안입니다." },
      { title: "접근성 안내 (Accessibility Statement)", body: "ADA·WCAG 2.1 AA 기준을 지향합니다. 어려운 부분은 알려 주십시오. 함께 고쳐 나갑니다." },
      { title: "어린이 안전 (Child Safety)", body: "13세 미만의 정보는 부모님을 통해서만 받습니다. 새 세대 문의는 부모님께서 부탁드립니다." }
    ]
  },

  cta: {
    primary: { label: "제작 문의하기", href: "mailto:hello@saesun.example" },
    secondary: { label: "이번 주 소식 보기", href: "#news" },
    visit: { label: "방문 예약", href: "#first-visit" }
  }
};
