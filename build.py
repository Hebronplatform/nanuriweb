#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NanuriWeb 빌드 스크립트
=======================
index.src.html (토큰 원본) → index.html (배포본)

왜 필요한가
-----------
{HG_CITIES} / {HG_TARGET} 토큰은 브라우저 JS가 치환한다.
그런데 구글·카카오톡·페이스북의 수집기는 JS를 실행하지 않는다.
그래서 검색 결과 제목과 공유 미리보기에 토큰이 그대로 노출됐다.
이 스크립트가 배포 전에 미리 치환해서 그 문제를 없앤다.

사용법
------
    python build.py                 # hebronguide.com에서 실시간 도시 수를 받아 빌드
    python build.py --cities 82     # 도시 수를 직접 지정해 빌드
    python build.py --check         # 빌드하지 않고 토큰 잔여만 검사

편집 규칙 (중요)
----------------
    index.src.html  ← 여기를 편집한다 (토큰 사용 가능)
    index.html      ← 자동 생성. 직접 편집하지 말 것. 편집해도 다음 빌드에 덮어써진다.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "index.src.html"
OUT = ROOT / "index.html"

COUNT_URL = "https://hebronguide.com/city-count.js"
FALLBACK_CITIES = 82          # city-count.js 접속 실패 시 사용
TARGET_CITIES = 500           # 목표 도시 수


def fetch_live_city_count():
    """hebronguide.com/city-count.js 에서 현재 도시 수를 읽어온다."""
    try:
        import urllib.request
        with urllib.request.urlopen(COUNT_URL, timeout=10) as r:
            js = r.read().decode("utf-8")
        m = re.search(r"window\.HG_CITY_COUNT\s*=\s*(\d+)", js)
        if m:
            return int(m.group(1)), "live"
    except Exception as e:
        print(f"  ! city-count.js 접속 실패 ({e.__class__.__name__}) — fallback 사용")
    return FALLBACK_CITIES, "fallback"


def check_tokens(path):
    """파일에 남은 토큰을 세어 보고한다."""
    if not path.exists():
        print(f"  ! 파일 없음: {path.name}")
        return -1
    html = path.read_text(encoding="utf-8")
    found = re.findall(r"\{HG_[A-Z_]+\}", html)
    if found:
        from collections import Counter
        for tok, n in Counter(found).most_common():
            print(f"  ! {path.name}: {tok} {n}건 남음")
    return len(found)


def build(cities, target):
    if not SRC.exists():
        print(f"오류: {SRC.name} 이 없습니다.")
        print("최초 1회만 다음을 실행하세요:  copy index.html index.src.html")
        sys.exit(1)

    html = SRC.read_text(encoding="utf-8")

    n_cities = html.count("{HG_CITIES}")
    n_target = html.count("{HG_TARGET}")

    html = html.replace("{HG_CITIES}", str(cities))
    html = html.replace("{HG_TARGET}", str(target))

    # JS fallback 상수도 최신 값으로 동기화 (JS가 꺼진 환경 대비)
    html = re.sub(
        r"(current:\s*)\d+(\s*,\s*//)",
        rf"\g<1>{cities}\g<2>",
        html,
        count=1,
    )
    html = re.sub(
        r"(target:\s*)\d+(\s*,\s*//)",
        rf"\g<1>{target}\g<2>",
        html,
        count=1,
    )

    # 배포본 상단에 경고 배너 삽입 (직접 편집 방지)
    banner = (
        "\n<!-- ============================================================\n"
        "     이 파일은 build.py 가 자동 생성했습니다. 직접 편집하지 마세요.\n"
        "     편집할 파일: index.src.html\n"
        "     재생성 명령: python build.py\n"
        f"     생성 시각: {__import__('datetime').datetime.now():%Y-%m-%d %H:%M}\n"
        f"     HebronGuide 도시 수: {cities} / 목표 {target}\n"
        "     ============================================================ -->"
    )
    html = re.sub(r"(<!DOCTYPE html>)", r"\1" + banner.replace("\\", "\\\\"), html, count=1)

    OUT.write_text(html, encoding="utf-8")

    print(f"  {OUT.name} 생성 완료")
    print(f"    {{HG_CITIES}} → {cities}   ({n_cities}건)")
    print(f"    {{HG_TARGET}} → {target}   ({n_target}건)")
    print(f"    크기 {OUT.stat().st_size:,} bytes")


def main():
    ap = argparse.ArgumentParser(description="NanuriWeb 빌드")
    ap.add_argument("--cities", type=int, help="도시 수 직접 지정")
    ap.add_argument("--target", type=int, default=TARGET_CITIES, help="목표 도시 수")
    ap.add_argument("--check", action="store_true", help="검사만 수행")
    args = ap.parse_args()

    print("=" * 52)
    print(" NanuriWeb 빌드")
    print("=" * 52)

    if args.check:
        print("\n[검사] index.src.html — 토큰이 있어야 정상")
        s = check_tokens(SRC)
        if s == 0:
            print("  ! 원본에 토큰이 없습니다. 원본이 이미 치환된 상태일 수 있습니다.")
        elif s > 0:
            print(f"  원본 토큰 {s}건 — 정상")

        print("\n[검사] index.html — 토큰이 0이어야 정상")
        o = check_tokens(OUT)
        if o == 0:
            print("  토큰 없음 — 정상")
        elif o > 0:
            print(f"  실패: 배포본에 토큰 {o}건이 남아 있습니다. 빌드를 실행하세요.")
            sys.exit(1)
        return

    if args.cities:
        cities, source = args.cities, "수동 지정"
    else:
        print(f"\n[1/3] 실시간 도시 수 확인 — {COUNT_URL}")
        cities, source = fetch_live_city_count()
    print(f"  도시 수: {cities} ({source}) · 목표: {args.target}")

    print("\n[2/3] 토큰 치환")
    build(cities, args.target)

    print("\n[3/3] 배포본 검증")
    left = check_tokens(OUT)
    if left == 0:
        print("  토큰 잔여 0건 — 통과")
    else:
        print(f"  실패: {left}건 남음")
        sys.exit(1)

    print("\n완료. 이제 배포하세요:  vercel --prod")
    print("=" * 52)


if __name__ == "__main__":
    main()
