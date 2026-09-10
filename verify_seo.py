#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NanuriWeb SEO 검증
===================
배포 전에 반드시 돌린다. 하나라도 실패하면 종료 코드 1을 반환한다.

검사 항목
---------
  1. JSON-LD 가 실제로 파싱되는가 (손으로 만든 구조화 데이터는 잘 깨진다)
  2. 필수 메타 태그가 모두 있는가
  3. 치환 안 된 {HG_...} 토큰이 남았는가
  4. canonical 주소가 하나로 통일됐는가 (www 혼입 여부)
  5. title / description 길이가 검색 결과에서 잘리지 않는가
  6. h1 이 페이지당 정확히 하나인가
  7. img 에 alt 가 있는가
  8. sitemap 의 모든 URL 이 실제 파일로 존재하는가

사용법
------
    python verify_seo.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://nanuriweb.com"

REQUIRED_META = [
    ('rel="canonical"', "정규 주소"),
    ('name="description"', "설명"),
    ('name="robots"', "robots 지시"),
    ('property="og:title"', "OG 제목"),
    ('property="og:description"', "OG 설명"),
    ('property="og:image"', "OG 이미지"),
    ('property="og:url"', "OG 주소"),
    ('property="og:site_name"', "OG 사이트명"),
    ('property="og:locale"', "OG 언어"),
    ('name="twitter:card"', "트위터 카드"),
]

fails = []
warns = []


def fail(msg):
    fails.append(msg)
    print(f"  [실패] {msg}")


def warn(msg):
    warns.append(msg)
    print(f"  [주의] {msg}")


def ok(msg):
    print(f"  [통과] {msg}")


def pages():
    yield ROOT / "index.html"
    for p in sorted(ROOT.glob("seattle-*/index.html")):
        yield p


def rel(p):
    return str(p.relative_to(ROOT)).replace("\\", "/")


def main():
    print("=" * 58)
    print(" NanuriWeb SEO 검증")
    print("=" * 58)

    files = list(pages())
    if not files:
        print("검사할 파일이 없습니다. build.py 를 먼저 실행하세요.")
        sys.exit(1)

    # 1. JSON-LD
    print("\n[1] 구조화 데이터 파싱")
    for f in files:
        h = f.read_text(encoding="utf-8")
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
        if not blocks:
            fail(f"{rel(f)} — JSON-LD 없음")
            continue
        for b in blocks:
            try:
                d = json.loads(b)
            except Exception as e:
                fail(f"{rel(f)} — JSON 파싱 실패: {e}")
                continue
            nodes = d.get("@graph", [d])
            types = []
            for n in nodes:
                t = n.get("@type")
                types.append("/".join(t) if isinstance(t, list) else t)
            ok(f"{rel(f)} — {', '.join(types)}")

    # 2. 필수 메타
    print("\n[2] 필수 메타 태그")
    for f in files:
        h = f.read_text(encoding="utf-8")
        miss = [label for tag, label in REQUIRED_META if tag not in h]
        if miss:
            fail(f"{rel(f)} — 누락: {', '.join(miss)}")
        else:
            ok(f"{rel(f)} — {len(REQUIRED_META)}개 모두 존재")

    # 3. 잔여 토큰
    print("\n[3] 치환 안 된 토큰")
    for f in files:
        h = f.read_text(encoding="utf-8")
        # 정규식 리터럴(\{HG_)과 CSS 선택자는 코드이므로 제외
        display = re.findall(r'(?<!\\)\{HG_[A-Z_]+\}', h)
        display = [t for t in display if 'content*="{HG_' not in h[max(0, h.find(t) - 20):h.find(t) + 10]]
        if display:
            fail(f"{rel(f)} — 토큰 {len(display)}건 노출: {set(display)}")
        else:
            ok(f"{rel(f)} — 잔여 없음")

    # 4. 주소 통일
    print("\n[4] 도메인 신호 일관성")
    for f in files:
        h = f.read_text(encoding="utf-8")
        if "www.nanuriweb.com" in h:
            fail(f"{rel(f)} — www 주소가 섞여 있음")
            continue
        m = re.search(r'<link rel="canonical" href="([^"]+)"', h)
        if not m:
            fail(f"{rel(f)} — canonical 없음")
        elif not m.group(1).startswith(SITE):
            fail(f"{rel(f)} — canonical 이 {SITE} 로 시작하지 않음: {m.group(1)}")
        else:
            ok(f"{rel(f)} — {m.group(1)}")

    # 5. 길이
    print("\n[5] 제목·설명 길이 (검색 결과 잘림 방지)")
    for f in files:
        h = f.read_text(encoding="utf-8")
        t = re.search(r"<title>(.*?)</title>", h, re.S)
        d = re.search(r'<meta name="description" content="(.*?)"', h, re.S)
        if t:
            n = len(t.group(1))
            if n > 60:
                warn(f"{rel(f)} — title {n}자 (60자 이하 권장, 뒤가 잘립니다)")
            else:
                ok(f"{rel(f)} — title {n}자")
        if d:
            n = len(d.group(1))
            if n > 160:
                warn(f"{rel(f)} — description {n}자 (160자 이하 권장)")
            elif n < 70:
                warn(f"{rel(f)} — description {n}자 (너무 짧습니다)")
            else:
                ok(f"{rel(f)} — description {n}자")

    # 6. h1
    print("\n[6] h1 개수 (페이지당 정확히 1개)")
    for f in files:
        h = f.read_text(encoding="utf-8")
        n = len(re.findall(r"<h1[\s>]", h))
        if n == 1:
            ok(f"{rel(f)} — 1개")
        else:
            fail(f"{rel(f)} — {n}개")

    # 7. img alt
    print("\n[7] 이미지 대체 텍스트")
    for f in files:
        h = f.read_text(encoding="utf-8")
        imgs = re.findall(r"<img\s[^>]*>", h)
        bad = [i for i in imgs if "alt=" not in i]
        if bad:
            fail(f"{rel(f)} — alt 누락 {len(bad)}건")
        else:
            ok(f"{rel(f)} — {len(imgs)}개 모두 alt 있음")

    # 8. sitemap ↔ 실제 파일
    print("\n[8] sitemap 과 실제 파일 대조")
    sm = ROOT / "sitemap.xml"
    if not sm.exists():
        fail("sitemap.xml 없음")
    else:
        locs = re.findall(r"<loc>(.*?)</loc>", sm.read_text(encoding="utf-8"))
        for u in locs:
            path = u.replace(SITE, "").strip("/")
            target = ROOT / "index.html" if not path else ROOT / path / "index.html"
            if target.exists():
                ok(f"{u} → {rel(target)}")
            else:
                fail(f"{u} → 파일 없음 ({rel(target)})")
        # 반대 방향 — 파일은 있는데 sitemap에 없는 경우
        for d in sorted(ROOT.glob("seattle-*/")):
            u = f"{SITE}/{d.name}/"
            if u not in locs:
                warn(f"{d.name} — 파일은 있으나 sitemap 에 없음")

    # 결과
    print("\n" + "=" * 58)
    if fails:
        print(f" 실패 {len(fails)}건 · 주의 {len(warns)}건 — 배포 전에 고치세요")
        print("=" * 58)
        sys.exit(1)
    print(f" 전체 통과 · 주의 {len(warns)}건")
    print("=" * 58)


if __name__ == "__main__":
    main()
