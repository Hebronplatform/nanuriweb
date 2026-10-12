/**
 * 이웃카페 · Neighbor Cafe
 * 예시 데이터 (실존 사업체 아님)
 *
 * 사업체(카페·세탁소·미용실 등 이웃 소상공인) 샘플.
 * 교회 샘플과 같은 구조의 다른 자료.
 */
window.BUSINESS = {
  meta: {
    isSample: true,
    sampleLabel: "예시 · 실존 사업체 아님",
    lang: "ko",
    lastUpdated: "2026-09-17",
    category: "business"
  },

  identity: {
    nameKo: "이웃카페",
    nameEn: "Neighbor Cafe",
    tagline: "동네에 오래 남는 한 잔",
    signature: {
      ko: "커피는 정성으로, 자리는 오래 앉을 수 있게",
      en: "Slow coffee, unhurried seats"
    },
    typeNote: "직접 볶은 원두 · 홈메이드 디저트",
    since: "2018년부터 같은 자리에서"
  },

  contact: {
    address: "1234 Pacific Ave, Tacoma, WA 98402",
    directionsNote: "주차 무료 · 매장 옆 골목 5대",
    phone: "(253) 555-0188",
    email: "hello@neighborcafe.example",
    mapEmbedUrl: null
  },

  hours: [
    { day: "월 · 화 · 수 · 목", time: "오전 7시 – 오후 6시" },
    { day: "금 · 토", time: "오전 7시 – 오후 8시" },
    { day: "일", time: "오전 8시 – 오후 3시" }
  ],

  welcomeCards: [
    { key: "hours", ko: "오늘의 영업", en: "TODAY", value: "오전 7시부터", link: "#hours" },
    { key: "directions", ko: "오시는 길", en: "VISIT", value: "Tacoma, WA", link: "#contact" },
    { key: "menu", ko: "이번 주 메뉴", en: "THIS WEEK", value: "가을 시즌 시작", link: "#menu" },
    { key: "reserve", ko: "자리 예약", en: "RESERVE", value: "그룹 4인 이상", link: "#reserve" }
  ],

  aboutBlocks: [
    {
      key: "owner_greeting",
      eyebrow: "OWNER'S NOTE",
      title: "주인장 인사",
      body: "커피는 빨리 만들면 값이 싸지고, 늦게 만들면 손님이 오래 앉습니다. 저희는 후자를 택했습니다. 원두는 매주 목요일 볶고, 디저트는 그날 아침 굽습니다. 급하지 않은 오후를 좋아하시는 분께 잘 어울리는 자리입니다.",
      signature: "대표 · Sample Owner"
    },
    {
      key: "story",
      eyebrow: "OUR STORY",
      title: "동네에 오래 남는 카페",
      body: "이웃카페는 2018년, 도서관 옆 작은 간판으로 시작했습니다. 처음 오신 분이 두 번째로 오시고, 이름을 부르며 인사하게 되는 자리를 만들고 싶었습니다. 지금도 같은 자리에 있습니다."
    }
  ],

  services: {
    eyebrow: "MENU",
    heading: "메뉴",
    intro: "가격은 예시입니다. 실제 메뉴판을 참고해 주십시오.",
    items: [
      { title: "핸드드립 커피", note: "그날의 원두 3종", price: "$5.5" },
      { title: "라떼 (오트/우유 선택)", note: "직접 볶은 원두", price: "$5.0" },
      { title: "시즌 디저트", note: "그날 굽는 것", price: "$4.5" },
      { title: "샌드위치 세트", note: "커피 포함", price: "$12" }
    ]
  },

  reviews: {
    eyebrow: "GUEST NOTES",
    heading: "손님 이야기",
    items: [
      { body: "오래 앉아도 눈치 주지 않는 자리. 일하기 좋습니다.", by: "M." },
      { body: "디저트가 그날 아침에 나오는 게 느껴져요.", by: "J." },
      { body: "이름을 기억해 주셔서 좋았어요.", by: "S." }
    ]
  },

  news: {
    eyebrow: "UPDATES",
    heading: "새 소식",
    latest: [
      { date: "2026-09-15", title: "가을 시즌 메뉴 시작 (호박·계피)", tag: "시즌" },
      { date: "2026-09-08", title: "일요일 오전 라이브 재개", tag: "이벤트" },
      { date: "2026-09-01", title: "새 원두 (에티오피아 Sidamo) 입고", tag: "원두" }
    ]
  },

  reserve: {
    eyebrow: "RESERVE",
    heading: "자리 예약",
    intro: "4인 이상 모임, 촬영·미팅, 스터디 그룹은 미리 알려 주시면 자리를 준비해 드립니다.",
    ctaLabel: "예약 문의하기"
  },

  policy: {
    eyebrow: "POLICY",
    heading: "안내",
    draftLabel: "검토 전 초안",
    items: [
      { title: "개인정보 처리방침", body: "예약 시 받는 정보(이름·전화)는 예약 안내 용도로만 사용합니다. 팔지 않습니다." },
      { title: "접근성", body: "휠체어 진입 가능 · 유아 의자 있음. 필요한 것 알려 주십시오." },
      { title: "환불·취소", body: "당일 3시간 전까지 취소 무료. 이후 절반 청구." }
    ]
  },

  cta: {
    primary: { label: "예약 문의하기", href: "mailto:hello@neighborcafe.example" },
    secondary: { label: "메뉴 보기", href: "#menu" },
    visit: { label: "오시는 길", href: "#contact" }
  }
};
