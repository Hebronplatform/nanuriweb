#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NanuriWeb 구조화 데이터(JSON-LD) 생성기
=========================================
index.src.html 의 한국어 FAQ 사전에서 질문·답변을 자동으로 읽어
Organization · WebSite · ProfessionalService · FAQPage · OfferCatalog 를
하나의 @graph 로 만들어 index.src.html 의 JSON-LD 블록을 교체한다.

왜 자동 추출인가
----------------
FAQ를 손으로 두 벌 관리하면 반드시 어긋난다.
화면에 보이는 FAQ가 곧 구조화 데이터가 되게 해서, 어긋날 수가 없게 만든다.

사용법
------
    python build_seo.py          # JSON-LD 갱신
    python build_seo.py --show   # 생성될 JSON만 출력 (파일 수정 안 함)

실행 순서
---------
    python build_seo.py      → index.src.html 의 JSON-LD 갱신
    python build.py          → index.html 생성
    python build_landing.py  → 랜딩페이지 + sitemap
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "index.src.html"
SITE = "https://nanuriweb.com"

# 요금제 — 화면 요금표와 일치해야 한다
PLANS = [
    ("Church Plant",   299,  "개척교회 · 설립 3년 이내 · 성도 50명 이하 · 연관리비 2년 무료"),
    ("Church Starter", 499,  "소형교회 · 7페이지"),
    ("Church Growth",  799,  "중형교회 · 10페이지 · CMS"),
    ("Church Pro",     1299, "대형교회 · 15페이지 이상 · 온라인 헌금"),
    ("Business Solo",  299,  "1인 사업 · 프리랜서 · 5페이지"),
    ("Business Startup", 449, "창업 3년 이내 · 첫 해 50% 할인"),
    ("Business Growth", 999, "중소 사업체 · 10페이지 · 예약 시스템"),
    ("Business Pro",   1799, "중견 사업체 · 15페이지 이상 · 온라인 결제"),
]

LANDING = [
    ("seattle-korean-restaurant-website", "시애틀 한인 식당 홈페이지 제작"),
    ("seattle-korean-salon-website", "시애틀 한인 미용실 홈페이지 제작"),
    ("seattle-korean-academy-website", "시애틀 한인 학원 홈페이지 제작"),
    ("seattle-korean-church-website", "시애틀 한인 교회 홈페이지 제작"),
    ("seattle-korean-clinic-website", "시애틀 한인 병원 · 한의원 홈페이지 제작"),
    ("seattle-korean-association-website", "시애틀 한인회 · 단체 홈페이지 제작"),
]


def strip_html(s):
    """태그 제거 · 엔티티 복원 · 공백 정리. 구조화 데이터에는 순수 텍스트가 들어가야 한다."""
    import html as H
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = H.unescape(s)
    s = s.replace("\\'", "'")
    return re.sub(r"\s+", " ", s).strip()


def extract_faq(html):
    """한국어 LANG 사전의 첫 번째 faq.qN / faq.aN 쌍들을 뽑는다."""
    qs, as_ = {}, {}
    for m in re.finditer(r"'faq\.q(\d+)'\s*:\s*'((?:\\.|[^'\\])*)'", html):
        n = int(m.group(1))
        if n not in qs:
            qs[n] = strip_html(m.group(2))
    for m in re.finditer(r"'faq\.a(\d+)'\s*:\s*'((?:\\.|[^'\\])*)'", html):
        n = int(m.group(1))
        if n not in as_:
            as_[n] = strip_html(m.group(2))
    pairs = [(qs[n], as_[n]) for n in sorted(qs) if n in as_]
    return pairs


def build_graph(faq_pairs):
    org_id = f"{SITE}/#organization"
    site_id = f"{SITE}/#website"
    svc_id = f"{SITE}/#service"

    graph = [
        {
            "@type": "Organization",
            "@id": org_id,
            "name": "NanuriWeb",
            "alternateName": ["나누리웹", "NanuriWeb — 나누리웹"],
            "legalName": "Hebron Platform LLC",
            "url": SITE + "/",
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE}/icon-512.png",
                "width": 512,
                "height": 512,
            },
            "image": f"{SITE}/og-image.png",
            "email": "hello@nanuriweb.com",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Seattle",
                "addressRegion": "WA",
                "addressCountry": "US",
            },
            "sameAs": ["https://hebronguide.com"],
            "knowsLanguage": ["ko", "en", "es"],
            "description": "한인 교회·사업체·기관을 위한 맞춤 홈페이지 제작. 한국어·영어·스페인어 직접 상담.",
        },
        {
            "@type": "WebSite",
            "@id": site_id,
            "url": SITE + "/",
            "name": "NanuriWeb",
            "publisher": {"@id": org_id},
            "inLanguage": ["ko", "en", "es"],
        },
        {
            "@type": ["ProfessionalService", "WebDesignBusiness"],
            "@id": svc_id,
            "name": "NanuriWeb — 한인 교회·사업체 홈페이지 제작",
            "description": "한인 교회·사업체·기관 맞춤 홈페이지 제작. 템플릿을 쓰지 않는 100% 맞춤 설계. 한국어·영어·스페인어 직접 상담. 일회 제작비와 연관리비 외 숨겨진 비용 없음.",
            "url": SITE + "/",
            "image": f"{SITE}/og-image.png",
            "parentOrganization": {"@id": org_id},
            "email": "hello@nanuriweb.com",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Seattle",
                "addressRegion": "WA",
                "addressCountry": "US",
            },
            "areaServed": [
                {"@type": "City", "name": "Seattle"},
                {"@type": "Country", "name": "United States"},
                {"@type": "Country", "name": "Canada"},
                {"@type": "Country", "name": "South Korea"},
            ],
            "availableLanguage": [
                {"@type": "Language", "name": "Korean", "alternateName": "ko"},
                {"@type": "Language", "name": "English", "alternateName": "en"},
                {"@type": "Language", "name": "Spanish", "alternateName": "es"},
            ],
            "priceRange": "$299–$1799",
            "currenciesAccepted": "USD",
            "slogan": "사업체도, 교회도 온라인에서 첫날부터 발견됩니다",
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "홈페이지 제작 플랜",
                "itemListElement": [
                    {
                        "@type": "Offer",
                        "name": name,
                        "description": desc,
                        "price": str(price),
                        "priceCurrency": "USD",
                        "availability": "https://schema.org/InStock",
                        "url": f"{SITE}/#plans",
                    }
                    for name, price, desc in PLANS
                ],
            },
        },
    ]

    if faq_pairs:
        graph.append({
            "@type": "FAQPage",
            "@id": f"{SITE}/#faq",
            "isPartOf": {"@id": site_id},
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in faq_pairs
            ],
        })

    graph.append({
        "@type": "ItemList",
        "@id": f"{SITE}/#services-by-industry",
        "name": "업종별 홈페이지 제작 — 시애틀",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": title,
                "url": f"{SITE}/{slug}/",
            }
            for i, (slug, title) in enumerate(LANDING)
        ],
    })

    return {"@context": "https://schema.org", "@graph": graph}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", action="store_true")
    args = ap.parse_args()

    if not SRC.exists():
        print(f"오류: {SRC.name} 없음")
        sys.exit(1)

    html = SRC.read_text(encoding="utf-8")
    faq = extract_faq(html)

    print("=" * 52)
    print(" NanuriWeb 구조화 데이터 생성")
    print("=" * 52)
    print(f"\n[1/2] FAQ 추출 — {len(faq)}건")
    for q, _ in faq:
        print(f"    · {q[:52]}")
    if len(faq) < 5:
        print("  ! FAQ가 적게 잡혔습니다. 사전 형식이 바뀌었는지 확인하세요.")

    data = build_graph(faq)
    js = json.dumps(data, ensure_ascii=False, indent=2)

    if args.show:
        print("\n" + js)
        return

    print(f"\n[2/2] JSON-LD 교체")
    pat = re.compile(
        r'(<!-- JSON-LD 구조화 데이터 -->\s*<script type="application/ld\+json">)(.*?)(</script>)',
        re.S,
    )
    if not pat.search(html):
        pat = re.compile(
            r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S
        )
        if not pat.search(html):
            print("  ! JSON-LD 블록을 찾지 못했습니다.")
            sys.exit(1)

    html = pat.sub(lambda m: m.group(1) + "\n" + js + "\n" + m.group(3), html, count=1)
    SRC.write_text(html, encoding="utf-8")

    types = [n.get("@type") for n in data["@graph"]]
    print(f"  노드 {len(types)}개: {types}")
    print(f"  크기 {len(js):,}자")
    print("\n다음: python build.py  →  python build_landing.py")
    print("=" * 52)


if __name__ == "__main__":
    main()
