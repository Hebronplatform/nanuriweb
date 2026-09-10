#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NanuriWeb 업종별 랜딩페이지 생성기
====================================
시애틀 지역 × 6개 업종 랜딩페이지를 생성한다. 한국어 + 영어.

왜 필요한가
-----------
현재 nanuriweb.com은 index.html 한 장뿐이고 sitemap에도 URL이 1개다.
페이지 하나로는 잡을 수 있는 검색어가 하나뿐이다.
업종별 페이지를 나누면 "시애틀 한인 식당 홈페이지" 같은
구체적이고 경쟁이 낮은 검색어를 각각 잡을 수 있다.

사용법
------
    python build_landing.py            # 6개 페이지 + sitemap.xml 생성
    python build_landing.py --list     # 생성될 페이지 목록만 출력

편집 규칙
---------
    본문 내용은 아래 INDUSTRIES 딕셔너리에서 수정한다.
    HTML 레이아웃은 TEMPLATE 에서 수정한다.
    생성된 /seattle-*/index.html 은 직접 편집하지 말 것.
"""

import argparse
import html as html_mod
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://nanuriweb.com"

# ──────────────────────────────────────────────────────────────
# 업종별 내용. 여기만 고치면 페이지가 바뀐다.
#   pain  : 그 업종 사장님이 실제로 겪는 구체적 고통 (막연한 말 금지)
#   fix   : 그 고통에 대한 우리의 해결
# ──────────────────────────────────────────────────────────────
INDUSTRIES = [
    {
        "slug": "seattle-korean-restaurant-website",
        "kind": "식당 · 카페 · 매장",
        "kind_en": "Restaurants & Cafés",
        "title": "시애틀 한인 식당 홈페이지 제작",
        "title_en": "Korean Restaurant Website Design in Seattle",
        "lede": "메뉴가 안 보여서 전화가 안 옵니다. 그건 음식 문제가 아닙니다.",
        "lede_en": "The food isn't the problem. People just can't find your menu.",
        "keywords": "시애틀 한인 식당 홈페이지, 시애틀 한식당 웹사이트, 식당 홈페이지 제작, Korean restaurant website Seattle",
        "hero_stat": "손님의 첫 질문은 언제나 같습니다 — 오늘 여나요? 메뉴가 뭐죠? 주차 되나요?",
        "pains": [
            {
                "pain": "구글 지도에 메뉴가 없어서, 손님이 전화로 물어봅니다",
                "detail": "점심 피크에 전화를 받느라 주방이 멈춥니다. 그런데 대부분은 \"오늘 문 여세요?\" 한 마디입니다.",
                "fix": "메뉴·영업시간·주차 안내를 첫 화면에 고정합니다. 스크롤 없이 5초 안에 답이 끝납니다.",
            },
            {
                "pain": "메뉴를 바꿀 때마다 업체에 연락하고 돈을 냅니다",
                "detail": "가격 한 줄 고치는 데 며칠 걸리고 청구서가 옵니다. 그래서 결국 옛날 가격을 그대로 둡니다.",
                "fix": "사장님이 직접 메뉴와 가격을 고칩니다. 휴대폰으로도 됩니다. 추가 비용 없습니다.",
            },
            {
                "pain": "옐프와 구글 리뷰로만 알려지고, 우리 얼굴이 없습니다",
                "detail": "리뷰 사이트가 우리 가게를 대신 설명합니다. 어떤 마음으로 하는 장사인지는 아무 데도 없습니다.",
                "fix": "가게 이야기와 실제 음식 사진을 우리 주소에 둡니다. 리뷰는 거들 뿐, 중심은 우리가 잡습니다.",
            },
            {
                "pain": "영어로 검색하는 손님을 놓칩니다",
                "detail": "시애틀 손님의 상당수는 한국어를 모릅니다. 한국어만 있는 페이지는 그들에게 없는 것과 같습니다.",
                "fix": "한국어·영어를 함께 담습니다. 필요하면 스페인어까지. 같은 가게, 두 배의 손님.",
            },
        ],
        "includes": [
            "메뉴 페이지 (사진 · 가격 · 사장님이 직접 수정)",
            "영업시간 · 휴무일 · 주차 안내",
            "구글 지도 연동 · 원터치 전화 걸기",
            "예약 · 케이터링 문의 폼",
            "한국어 · 영어 병기",
            "HebronGuide 82개 도시 자동 등재",
        ],
        "plan": "Solo Plan $299",
        "plan_note": "5페이지 · 연관리비 $150/yr · 창업 3년 이내는 Startup Plan 50% 할인",
        "faq": [
            ("사진이 없는데 괜찮나요?",
             "괜찮습니다. 어떤 사진이 필요한지 목록으로 알려드리고, 휴대폰으로 찍는 법도 안내합니다. 실제 음식 사진이 스톡 사진보다 훨씬 잘 팔립니다."),
            ("배달앱이 있는데 홈페이지가 또 필요한가요?",
             "배달앱은 수수료를 가져가고 손님 정보도 앱이 가집니다. 홈페이지는 그 손님을 직접 만나는 통로입니다. 둘은 경쟁이 아니라 역할이 다릅니다."),
            ("얼마나 걸리나요?",
             "상담 후 기획서까지 3~5 영업일, 확정 후 완성까지 보통 2~3주입니다."),
        ],
    },
    {
        "slug": "seattle-korean-salon-website",
        "kind": "미용실 · 네일 · 뷰티샵",
        "kind_en": "Salons & Beauty",
        "title": "시애틀 한인 미용실 홈페이지 제작",
        "title_en": "Korean Salon Website Design in Seattle",
        "lede": "예약 전화 받느라 가위를 놓습니다. 그게 하루에 몇 번인가요.",
        "lede_en": "You put down the scissors to answer the phone. How many times a day?",
        "keywords": "시애틀 한인 미용실 홈페이지, 시애틀 헤어샵 웹사이트, 미용실 예약 홈페이지, Korean salon website Seattle",
        "hero_stat": "손님은 시술 사진을 먼저 보고, 가격을 확인하고, 그다음에 예약합니다.",
        "pains": [
            {
                "pain": "손님 머리를 하다가 예약 전화를 받습니다",
                "detail": "손에 염색약을 묻힌 채 전화를 받고, 앉아 계신 손님은 기다립니다. 양쪽 다 손해입니다.",
                "fix": "24시간 온라인 예약 폼을 둡니다. 손님은 새벽에도 예약하고, 사장님은 가위를 놓지 않습니다.",
            },
            {
                "pain": "시술 사진이 인스타에만 있어서, 검색으로는 못 찾습니다",
                "detail": "인스타는 이미 아는 사람만 봅니다. 시애틀에 막 이사 온 사람은 인스타 계정을 모릅니다.",
                "fix": "시술 갤러리를 검색되는 페이지에 둡니다. 인스타는 연동해서 자동으로 함께 보이게 합니다.",
            },
            {
                "pain": "가격을 안 적어서 문의만 오고 예약이 안 됩니다",
                "detail": "\"얼마예요?\" 문자에 답하는 데 하루가 갑니다. 답을 받고도 안 오는 사람이 대부분입니다.",
                "fix": "시술별 가격표를 공개합니다. 물어볼 필요가 없어지면, 문의가 아니라 예약이 옵니다.",
            },
            {
                "pain": "한국식 시술을 찾는 손님이 우리를 못 찾습니다",
                "detail": "매직·볼륨매직·열펌을 영어로 뭐라 검색해야 할지 손님도 모릅니다.",
                "fix": "한국어 시술명과 영어 설명을 함께 넣습니다. 양쪽 검색어 모두에서 걸립니다.",
            },
        ],
        "includes": [
            "시술 갤러리 (전후 사진 · 직접 업로드)",
            "시술별 가격표",
            "24시간 온라인 예약 문의 폼",
            "디자이너 소개 · 경력",
            "인스타그램 자동 연동",
            "한국어 · 영어 병기",
        ],
        "plan": "Solo Plan $299",
        "plan_note": "5페이지 · 연관리비 $150/yr · 예약 시스템 확장은 Business Growth $999",
        "faq": [
            ("예약이 자동으로 잡히나요?",
             "Solo Plan은 예약 '문의'가 이메일과 카톡으로 오는 방식입니다. 캘린더에 자동으로 잡히는 실시간 예약 시스템은 Business Growth 플랜에서 제공합니다."),
            ("인스타를 이미 열심히 하는데 홈페이지가 필요할까요?",
             "인스타는 팔로워에게 보이고, 홈페이지는 검색하는 사람에게 보입니다. 새 손님은 대부분 검색에서 옵니다."),
            ("사진을 계속 올려야 하나요?",
             "직접 올리실 수 있게 만들어 드립니다. 인스타에 올리면 자동으로 홈페이지에도 뜨게 연동할 수도 있습니다."),
        ],
    },
    {
        "slug": "seattle-korean-academy-website",
        "kind": "학원 · 과외 · 코칭",
        "kind_en": "Academies & Tutoring",
        "title": "시애틀 한인 학원 홈페이지 제작",
        "title_en": "Korean Academy Website Design in Seattle",
        "lede": "학부모는 학원을 고를 때, 무엇보다 먼저 믿을 만한지를 봅니다.",
        "lede_en": "Parents look for one thing first — can I trust this place with my child?",
        "keywords": "시애틀 한인 학원 홈페이지, 시애틀 한글학교 웹사이트, 학원 홈페이지 제작, Korean academy website Seattle",
        "hero_stat": "학부모는 카톡방 추천을 받고 나서, 반드시 검색으로 한 번 더 확인합니다.",
        "pains": [
            {
                "pain": "카톡방 추천을 받고 검색했는데 아무것도 안 나옵니다",
                "detail": "추천은 받았는데 확인할 데가 없으면 학부모는 망설입니다. 그 망설임에서 대부분 놓칩니다.",
                "fix": "검색하면 나오는 공식 페이지를 만듭니다. 추천이 확신으로 바뀌는 지점이 여기입니다.",
            },
            {
                "pain": "커리큘럼과 강사 이력이 어디에도 없습니다",
                "detail": "\"어떻게 가르치세요?\"를 매번 전화로 설명합니다. 같은 설명을 백 번 반복합니다.",
                "fix": "커리큘럼·강사 이력·수업 방식을 페이지에 정리합니다. 한 번 쓰면 계속 일합니다.",
            },
            {
                "pain": "수업료를 안 적어서 문의 전화가 가격 질문으로만 끝납니다",
                "detail": "가격을 듣고 끊는 전화가 대부분입니다. 정작 우리 수업의 강점은 말할 기회조차 없습니다.",
                "fix": "수업료를 공개하고, 그 옆에 왜 그 값인지를 씁니다. 남는 문의는 진짜 관심입니다.",
            },
            {
                "pain": "학기마다 바뀌는 시간표를 알릴 방법이 카톡뿐입니다",
                "detail": "공지가 카톡방에 묻힙니다. 새로 온 학부모는 지난 공지를 볼 수 없습니다.",
                "fix": "공지·시간표를 직접 올리는 게시판을 둡니다. 카톡은 알림용으로만 쓰면 됩니다.",
            },
        ],
        "includes": [
            "커리큘럼 · 과목별 소개",
            "강사 소개 · 경력",
            "수업료 · 학사 일정",
            "공지사항 게시판 (직접 작성)",
            "상담 · 등록 문의 폼",
            "한국어 · 영어 병기",
        ],
        "plan": "Solo Plan $299 · Business Growth $999",
        "plan_note": "공지 게시판과 학사 일정이 필요하면 Business Growth를 권합니다",
        "faq": [
            ("공지를 제가 직접 올릴 수 있나요?",
             "Business Growth 플랜부터 CMS가 포함되어, 워드 문서 쓰듯이 직접 올리실 수 있습니다. 사용법은 완성 후 함께 익히실 때까지 안내합니다."),
            ("학생 수가 적은데 홈페이지가 과할까요?",
             "학생이 적을수록 새 학생 한 명의 비중이 큽니다. 연 $150이면 한 달 $12.5입니다. 학생 한 명만 더 와도 회수됩니다."),
            ("한글학교나 비영리도 되나요?",
             "됩니다. 비영리 단체는 상담 때 말씀해 주시면 예산에 맞춰 함께 방법을 찾습니다."),
        ],
    },
    {
        "slug": "seattle-korean-church-website",
        "kind": "교회 · 선교단체",
        "kind_en": "Churches & Ministries",
        "title": "시애틀 한인 교회 홈페이지 제작",
        "title_en": "Korean Church Website Design in Seattle",
        "lede": "낯선 도시에 막 도착한 사람이 검색합니다. 그때 우리가 없으면, 없는 교회입니다.",
        "lede_en": "Someone just arrived in a new city and searched. If you're not there, you don't exist.",
        "keywords": "시애틀 한인 교회 홈페이지, 교회 홈페이지 제작, 개척교회 홈페이지, Korean church website Seattle",
        "hero_stat": "처음 오는 사람이 알고 싶은 것은 셋뿐입니다 — 언제, 어디서, 무엇을 입고.",
        "pains": [
            {
                "pain": "예배 시간이 검색에 안 나옵니다",
                "detail": "\"시애틀 한인교회 예배시간\"을 검색해도 우리 교회 시간은 나오지 않습니다. 찾다 지친 사람은 다음 교회로 갑니다.",
                "fix": "예배 시간·주소·주차 안내를 첫 화면에 고정합니다. 스크롤도, 클릭도 필요 없게 만듭니다.",
            },
            {
                "pain": "처음 오는 사람이 무엇을 각오해야 할지 모릅니다",
                "detail": "옷차림, 헌금, 등록 절차, 아이는 어디로. 묻기 민망한 것들이라 아예 안 옵니다.",
                "fix": "'처음 오시는 분' 페이지 하나로 그 모든 불안을 미리 없앱니다. 이 페이지가 새가족 등록을 가장 많이 만듭니다.",
            },
            {
                "pain": "설교가 유튜브에만 있고 교회 이름으로는 안 걸립니다",
                "detail": "귀한 설교가 쌓여 있는데, 우리 교회를 찾는 사람에게 닿지 않습니다.",
                "fix": "설교를 교회 주소 안에 담고 유튜브와 연동합니다. 설교 하나하나가 교회를 찾는 통로가 됩니다.",
            },
            {
                "pain": "홈페이지 만드는 건을 당회에 어떻게 올릴지 모르겠습니다",
                "detail": "예산·범위·기대효과를 문서로 정리해야 하는데, 그걸 쓸 사람이 없습니다.",
                "fix": "당회·제직회 심의용 기획서를 무료로 함께 작성해 드립니다. 통과되지 않아도 비용은 없습니다.",
            },
        ],
        "includes": [
            "예배 안내 (시간 · 장소 · 주차)",
            "'처음 오시는 분' 안내 페이지",
            "설교 아카이브 · 유튜브 연동",
            "새가족 · 기도 요청 폼",
            "목장 · 소그룹 소개",
            "당회 기획서 무료 작성",
            "HebronGuide 82개 도시 자동 등재",
        ],
        "plan": "Church Plant $299 · Starter $499 · Growth $799",
        "plan_note": "설립 3년 이내·성도 50명 이하 개척교회는 $299에 Growth 전 기능 + 연관리비 2년 무료",
        "faq": [
            ("개척교회인데 예산이 정말 없습니다",
             "Church Plant 플랜이 그래서 있습니다. $299에 Growth Plan 전 기능이 들어가고 연관리비가 2년 무료입니다. 그래도 어려우시면 상담 때 솔직히 말씀해 주세요 — 함께 방법을 찾습니다."),
            ("가정교회인데 일반 교회 홈페이지와 다르지 않나요?",
             "다릅니다. 가정교회는 목장 구조와 목자 체계가 홈페이지 설계에 반영되어야 합니다. House Church 플랜은 먼저 무료 상담으로 방향을 잡는 것부터 시작합니다."),
            ("당회 기획서가 정말 무료인가요?",
             "무료입니다. 예산 계획·제작 범위·기대 효과를 담은 정식 문서로 드립니다. 심의에서 부결되어도 청구하지 않습니다."),
            ("목사님이 직접 공지를 올릴 수 있나요?",
             "Growth Plan부터 CMS가 포함됩니다. 컴퓨터를 잘 모르셔도 됩니다 — 익숙해지실 때까지 함께합니다."),
        ],
    },
    {
        "slug": "seattle-korean-clinic-website",
        "kind": "병원 · 치과 · 한의원",
        "kind_en": "Clinics & Dental",
        "title": "시애틀 한인 병원 · 한의원 홈페이지 제작",
        "title_en": "Korean Clinic & Dental Website Design in Seattle",
        "lede": "아픈 사람은 오래 찾지 않습니다. 먼저 보이는 곳으로 갑니다.",
        "lede_en": "People in pain don't search long. They go to whoever shows up first.",
        "keywords": "시애틀 한인 병원 홈페이지, 시애틀 한의원 웹사이트, 치과 홈페이지 제작, Korean clinic website Seattle",
        "hero_stat": "한국어로 진료받고 싶은 환자는, 한국어로 검색합니다.",
        "pains": [
            {
                "pain": "보험을 받는지 알 수 없어서 전화부터 옵니다",
                "detail": "접수 직원이 하루 종일 보험 질문에 답합니다. 그중 절반은 우리가 안 받는 보험입니다.",
                "fix": "취급 보험 목록을 페이지에 공개합니다. 헛걸음과 헛전화가 동시에 줄어듭니다.",
            },
            {
                "pain": "진료 과목을 몰라서 다른 곳으로 갑니다",
                "detail": "우리가 하는 시술인데 환자는 모르고 다른 병원을 예약합니다. 알릴 데가 없었을 뿐입니다.",
                "fix": "진료 과목과 시술을 하나씩 페이지로 정리합니다. 각 항목이 검색에서 따로 걸립니다.",
            },
            {
                "pain": "한국어 진료가 강점인데 그게 안 보입니다",
                "detail": "영어가 불편한 어르신들이 가장 필요로 하는 정보인데, 어디에도 안 적혀 있습니다.",
                "fix": "한국어 진료 가능을 첫 화면에 명시합니다. 이것 하나가 가장 강한 차별점입니다.",
            },
            {
                "pain": "첫 방문 서류를 현장에서 작성하느라 대기가 길어집니다",
                "detail": "대기실이 밀리고, 환자는 짜증나고, 진료 시간은 줄어듭니다.",
                "fix": "초진 서류를 미리 내려받거나 온라인으로 작성하게 합니다. 오는 순간부터 진료가 시작됩니다.",
            },
        ],
        "includes": [
            "진료 과목 · 시술별 안내 페이지",
            "취급 보험 목록",
            "의료진 소개 · 자격",
            "진료 시간 · 오시는 길 · 주차",
            "초진 서류 다운로드 · 예약 문의",
            "한국어 · 영어 병기",
        ],
        "plan": "Business Growth $999",
        "plan_note": "10페이지 · 연관리비 $480/yr · 소규모 클리닉은 Solo Plan $299부터",
        "faq": [
            ("의료 광고 규정에 걸리지 않나요?",
             "저희는 검증되지 않은 효과나 치료 보장 문구를 쓰지 않습니다. 다만 주(州)별 의료 광고 규정은 다르므로, 문구 최종 확정 전에는 담당 변호사나 협회 지침 확인을 권해 드립니다."),
            ("환자 정보를 받는 폼이 HIPAA에 문제가 없나요?",
             "일반 문의 폼은 진료 정보가 아닌 연락처와 방문 희망 시간만 받도록 설계합니다. 실제 진료 정보를 온라인으로 받으셔야 한다면 HIPAA 준수 전용 시스템이 별도로 필요하며, 상담 때 안내해 드립니다."),
            ("기존 홈페이지가 있는데 옮길 수 있나요?",
             "가능합니다. 도메인과 기존 내용을 그대로 가져오고, 검색 순위가 떨어지지 않도록 주소 연결을 처리합니다."),
        ],
    },
    {
        "slug": "seattle-korean-association-website",
        "kind": "한인회 · 비영리 · 단체",
        "kind_en": "Associations & Nonprofits",
        "title": "시애틀 한인회 · 단체 홈페이지 제작",
        "title_en": "Korean Association & Nonprofit Website Design in Seattle",
        "lede": "홈페이지 없는 한인회는, 디지털 세상에서 존재하지 않는 것과 같습니다.",
        "lede_en": "An association without a website simply doesn't exist online.",
        "keywords": "시애틀 한인회 홈페이지, 한인 단체 웹사이트, 비영리 홈페이지 제작, Korean association website Seattle",
        "hero_stat": "이 도시에 막 온 동포가 가장 먼저 검색하는 것이 '한인회'입니다.",
        "pains": [
            {
                "pain": "새로 온 동포가 '이 도시 한인회'를 검색해도 안 나옵니다",
                "detail": "정작 가장 도움이 필요한 사람이 우리를 못 찾습니다. 섬기려고 만든 단체인데 섬길 기회가 없습니다.",
                "fix": "단체 이름과 도시 이름으로 검색되는 공식 페이지를 만듭니다. 이것이 첫 번째 환대입니다.",
            },
            {
                "pain": "행사 공지가 카톡방과 페이스북에 흩어져 있습니다",
                "detail": "어디에 올렸는지 임원도 헷갈립니다. 지난 행사 기록은 사실상 사라집니다.",
                "fix": "행사 일정과 기록을 한 곳에 모읍니다. SNS는 링크만 뿌리는 용도로 씁니다.",
            },
            {
                "pain": "임원이 바뀔 때마다 자료가 사라집니다",
                "detail": "전임자 개인 계정에 있던 사진과 문서가 인수인계 때 통째로 없어집니다.",
                "fix": "단체 명의 도메인과 계정으로 만듭니다. 사람이 바뀌어도 기록은 남습니다.",
            },
            {
                "pain": "후원·기부를 받을 창구가 없습니다",
                "detail": "돕고 싶다는 연락이 와도 계좌번호를 문자로 보내는 수준입니다. 신뢰가 안 생깁니다.",
                "fix": "후원 안내와 온라인 신청 창구를 둡니다. 단체의 목적과 재정 원칙을 함께 밝힙니다.",
            },
        ],
        "includes": [
            "단체 소개 · 연혁 · 임원",
            "행사 일정 · 지난 행사 기록",
            "공지사항 게시판 (직접 작성)",
            "회원 가입 · 후원 문의 폼",
            "정착 안내 자료실",
            "한국어 · 영어 병기",
        ],
        "plan": "Business Growth $999",
        "plan_note": "연관리비 $480/yr — 한 달 $40. 예산이 빠듯하시면 상담 때 말씀해 주세요",
        "faq": [
            ("비영리라 예산이 정말 빠듯합니다",
             "연 $480은 한 달 $40입니다. 플라이어 한 번 인쇄비보다 적은 돈으로 365일 24시간 커뮤니티를 안내합니다. 그래도 어려우시면 상담에서 솔직하게 말씀해 주세요 — 함께 방법을 찾습니다."),
            ("임원이 매년 바뀌는데 관리가 될까요?",
             "그래서 단체 명의 도메인과 계정으로 만듭니다. 인수인계 문서도 함께 드리고, 새 임원이 오시면 사용법을 다시 안내해 드립니다."),
            ("기존에 페이스북 페이지만 있습니다",
             "페이스북은 페이스북 회원에게만 제대로 보이고, 검색에서는 약합니다. 홈페이지를 중심에 두고 페이스북을 연동하는 구조를 권합니다."),
        ],
    },
]

# ──────────────────────────────────────────────────────────────

TEMPLATE = """<!DOCTYPE html>
<!-- 자동 생성 파일 — build_landing.py 가 만듭니다. 직접 편집하지 마세요. -->
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | NanuriWeb</title>
<meta name="description" content="{meta_desc}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="{site}/{slug}/">
<meta property="og:title" content="{title} | NanuriWeb">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="{site}/{slug}/">
<meta property="og:type" content="website">
<meta property="og:image" content="{site}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{site}/og-image.png">
<meta name="twitter:title" content="{title} | NanuriWeb">
<meta name="twitter:description" content="{meta_desc}">
<meta property="og:site_name" content="NanuriWeb">
<meta property="og:locale" content="ko_KR">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="Hebron Platform LLC">
<meta name="geo.region" content="US-WA">
<meta name="geo.placename" content="Seattle">
<link rel="icon" href="{site}/icon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Noto+Serif+KR:wght@400;600;700&display=swap" rel="stylesheet">
<script type="application/ld+json">
{jsonld}
</script>
<style>
:root{{--navy:#0B1628;--navy-mid:#1F3864;--gold:#C9A84C;--gold-light:#F0D98A;--gold-pale:#FDF8EC;
--ink:#16181D;--body:#3D4149;--mute:#6B7280;--line:#E5E7EB;--white:#fff;--soft:#F8F9FB;
--fn:'Noto Serif KR',serif;--fb:'Noto Sans KR',sans-serif;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html{{scroll-behavior:smooth;}}
body{{font-family:var(--fb);color:var(--body);background:var(--white);font-size:16px;line-height:1.8;-webkit-font-smoothing:antialiased;}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 24px;}}
a{{color:inherit;}}

/* nav */
.nav{{position:sticky;top:0;z-index:50;background:rgba(11,22,40,.97);backdrop-filter:blur(8px);border-bottom:1px solid rgba(201,168,76,.18);}}
.nav-in{{max-width:1080px;margin:0 auto;padding:14px 24px;display:flex;align-items:center;justify-content:space-between;gap:16px;}}
.nav-logo{{font-family:var(--fn);font-weight:700;font-size:20px;color:#fff;text-decoration:none;letter-spacing:-.4px;}}
.nav-logo span{{color:var(--gold);}}
.nav-cta{{background:var(--gold);color:var(--navy);font-weight:700;font-size:14px;padding:9px 20px;border-radius:8px;text-decoration:none;white-space:nowrap;}}
.nav-cta:hover{{background:var(--gold-light);}}

/* hero */
.hero{{background:linear-gradient(160deg,#0B1628 0%,#12233F 55%,#0B1628 100%);color:#fff;padding:76px 0 84px;}}
.eyebrow{{display:inline-block;font-size:12px;letter-spacing:2px;color:var(--gold);border:1px solid rgba(201,168,76,.34);border-radius:20px;padding:6px 16px;margin-bottom:26px;}}
.hero h1{{font-family:var(--fn);font-size:clamp(30px,5vw,46px);line-height:1.32;font-weight:700;color:#fff;margin-bottom:22px;letter-spacing:-.5px;}}
.hero h1 em{{font-style:normal;color:var(--gold-light);}}
.hero-lede{{font-size:clamp(17px,2.2vw,21px);color:rgba(255,255,255,.9);line-height:1.75;margin-bottom:14px;font-weight:500;}}
.hero-stat{{font-size:15px;color:rgba(255,255,255,.58);margin-bottom:34px;}}
.btn-row{{display:flex;gap:12px;flex-wrap:wrap;}}
.btn{{display:inline-block;padding:15px 30px;border-radius:10px;font-weight:700;font-size:16px;text-decoration:none;}}
.btn-gold{{background:var(--gold);color:var(--navy);}}
.btn-gold:hover{{background:var(--gold-light);}}
.btn-ghost{{border:1px solid rgba(255,255,255,.32);color:#fff;}}
.btn-ghost:hover{{background:rgba(255,255,255,.08);}}

/* sections */
section{{padding:74px 0;}}
.sec-kicker{{font-size:12px;letter-spacing:2.4px;color:var(--gold);font-weight:700;text-transform:uppercase;margin-bottom:14px;}}
.sec-h{{font-family:var(--fn);font-size:clamp(24px,3.4vw,34px);font-weight:700;color:var(--ink);line-height:1.42;margin-bottom:14px;letter-spacing:-.4px;}}
.sec-sub{{font-size:16px;color:var(--mute);margin-bottom:44px;max-width:660px;}}

/* pain cards */
.pain{{border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:12px;padding:30px 32px;margin-bottom:20px;background:var(--white);}}
.pain-q{{font-family:var(--fn);font-size:19px;font-weight:700;color:var(--ink);line-height:1.5;margin-bottom:12px;}}
.pain-d{{font-size:15.5px;color:var(--body);margin-bottom:20px;}}
.pain-f{{background:var(--gold-pale);border-radius:8px;padding:16px 20px;font-size:15.5px;color:var(--ink);}}
.pain-f b{{color:#8A6D3B;display:block;font-size:12px;letter-spacing:1.4px;margin-bottom:6px;font-weight:700;}}

/* includes */
.inc{{background:var(--soft);}}
.inc-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin-bottom:40px;}}
.inc-item{{background:#fff;border:1px solid var(--line);border-radius:10px;padding:18px 22px;font-size:15.5px;color:var(--ink);display:flex;gap:12px;align-items:flex-start;}}
.inc-item .ck{{color:var(--gold);font-weight:900;flex-shrink:0;}}
.price-box{{background:var(--navy);color:#fff;border-radius:14px;padding:34px 36px;text-align:center;}}
.price-plan{{font-family:var(--fn);font-size:26px;font-weight:700;color:var(--gold-light);margin-bottom:10px;}}
.price-note{{font-size:14.5px;color:rgba(255,255,255,.68);margin-bottom:24px;}}

/* faq */
.faq-i{{border-bottom:1px solid var(--line);padding:24px 0;}}
.faq-q{{font-family:var(--fn);font-size:17.5px;font-weight:700;color:var(--ink);margin-bottom:10px;}}
.faq-a{{font-size:15.5px;color:var(--body);}}

/* proof */
.proof{{background:var(--soft);}}
.proof-in{{display:grid;grid-template-columns:1.15fr 1fr;gap:44px;align-items:center;}}
.proof img{{width:100%;border-radius:12px;border:1px solid var(--line);box-shadow:0 14px 40px rgba(11,22,40,.13);display:block;}}
.proof-tag{{font-size:12px;letter-spacing:2px;color:var(--gold);font-weight:700;margin-bottom:12px;}}
.proof-quote{{font-family:var(--fn);font-size:19px;line-height:1.7;color:var(--ink);margin-bottom:16px;}}
.proof-by{{font-size:14px;color:var(--mute);}}

/* cta */
.cta{{background:linear-gradient(160deg,#0B1628,#12233F);color:#fff;text-align:center;}}
.cta h2{{font-family:var(--fn);font-size:clamp(24px,3.4vw,32px);font-weight:700;margin-bottom:16px;color:#fff;}}
.cta p{{color:rgba(255,255,255,.76);margin-bottom:30px;font-size:16px;}}

/* footer */
.ft{{background:var(--navy);color:rgba(255,255,255,.55);padding:44px 0;font-size:13.5px;border-top:1px solid rgba(201,168,76,.16);}}
.ft a{{color:var(--gold);text-decoration:none;}}
.ft-links{{margin-bottom:16px;display:flex;gap:18px;flex-wrap:wrap;}}
.crumb{{font-size:13px;color:var(--mute);padding:16px 0;border-bottom:1px solid var(--line);}}
.crumb a{{color:var(--mute);text-decoration:none;}}
.crumb a:hover{{color:var(--gold);}}
@media(max-width:820px){{
  .proof-in{{grid-template-columns:1fr;gap:26px;}}
  section{{padding:54px 0;}}
  .hero{{padding:54px 0 60px;}}
  .pain{{padding:24px 22px;}}
}}
</style>
</head>
<body>

<nav class="nav"><div class="nav-in">
  <a href="{site}/" class="nav-logo">Nanuri<span>Web</span></a>
  <a href="{site}/#contact" class="nav-cta">무료 상담 신청</a>
</div></nav>

<div class="wrap"><div class="crumb">
  <a href="{site}/">NanuriWeb</a> &rsaquo; 시애틀 &rsaquo; <span>{kind}</span>
</div></div>

<header class="hero"><div class="wrap">
  <div class="eyebrow">시애틀 · {kind}</div>
  <h1>{h1}</h1>
  <p class="hero-lede">{lede}</p>
  <p class="hero-stat">{hero_stat}</p>
  <div class="btn-row">
    <a href="{site}/#contact" class="btn btn-gold">무료 기획서 신청 →</a>
    <a href="#included" class="btn btn-ghost">무엇이 들어가나요</a>
  </div>
</div></header>

<section><div class="wrap">
  <div class="sec-kicker">실제로 겪는 문제</div>
  <h2 class="sec-h">{kind_short} 사장님들이<br>공통으로 말씀하시는 것들</h2>
  <p class="sec-sub">일반론이 아닙니다. 상담에서 실제로 반복해 들은 이야기와, 그에 대한 저희의 해결입니다.</p>
  {pain_html}
</div></section>

<section class="inc" id="included"><div class="wrap">
  <div class="sec-kicker">포함 내용</div>
  <h2 class="sec-h">{kind_short} 홈페이지에<br>기본으로 들어가는 것</h2>
  <p class="sec-sub">업종에 필요 없는 기능을 넣고 값을 올리지 않습니다. 실제로 쓰는 것만 담습니다.</p>
  <div class="inc-grid">{inc_html}</div>
  <div class="price-box">
    <div class="price-plan">{plan}</div>
    <div class="price-note">{plan_note}</div>
    <a href="{site}/#contact" class="btn btn-gold">무료 기획서 받아보기 →</a>
  </div>
</div></section>

<section class="proof"><div class="wrap">
  <div class="proof-in">
    <img src="{site}/images/portfolio/edendallas-desktop.jpg" alt="에덴교회 달라스 홈페이지 — NanuriWeb 제작" width="1424" height="715" loading="lazy">
    <div>
      <div class="proof-tag">실제 제작 사례</div>
      <p class="proof-quote">&ldquo;처음에는 어떻게 시작해야 할지 막막했는데, 한국어로 차근차근 설명해 주셔서 편하게 진행할 수 있었습니다. 기대 이상의 결과물이었어요.&rdquo;</p>
      <p class="proof-by">에덴교회 달라스 담임목사 · <a href="https://edendallas.org" target="_blank" rel="noopener" style="color:#8A6D3B;">edendallas.org</a></p>
    </div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="sec-kicker">자주 묻는 질문</div>
  <h2 class="sec-h">{kind_short} 사장님들이<br>가장 많이 물으시는 것</h2>
  <div style="margin-top:32px;">{faq_html}</div>
</div></section>

<section class="cta"><div class="wrap">
  <h2>기획서를 받아보신 후에 결정하세요</h2>
  <p>기획서 제공까지는 비용이 없습니다 · 48시간 이내 한국어로 직접 연락드립니다</p>
  <a href="{site}/#contact" class="btn btn-gold">무료 상담 신청하기 →</a>
</div></section>

<footer class="ft"><div class="wrap">
  <div class="ft-links">
    <a href="{site}/">홈</a>
    <a href="{site}/#plans">요금</a>
    <a href="{site}/#faq">FAQ</a>
    <a href="{site}/#contact">문의</a>
    <a href="https://hebronguide.com" target="_blank" rel="noopener">HebronGuide</a>
  </div>
  <div style="margin-bottom:10px;">다른 업종 보기: {siblings}</div>
  <div>Hebron Platform LLC · Seattle, WA · <a href="mailto:hello@nanuriweb.com">hello@nanuriweb.com</a></div>
  <div style="margin-top:8px;">&copy; 2026 Hebron Platform LLC. All rights reserved.</div>
</div></footer>

</body>
</html>
"""


def esc(s):
    return html_mod.escape(s, quote=True)


def build_page(ind, all_inds):
    pain_html = "\n".join(
        f'''<div class="pain">
    <div class="pain-q">&ldquo;{esc(p["pain"])}&rdquo;</div>
    <div class="pain-d">{esc(p["detail"])}</div>
    <div class="pain-f"><b>NANURIWEB 의 해결</b>{esc(p["fix"])}</div>
  </div>'''
        for p in ind["pains"]
    )

    inc_html = "\n".join(
        f'<div class="inc-item"><span class="ck">✓</span><span>{esc(i)}</span></div>'
        for i in ind["includes"]
    )

    faq_html = "\n".join(
        f'<div class="faq-i"><div class="faq-q">{esc(q)}</div><div class="faq-a">{esc(a)}</div></div>'
        for q, a in ind["faq"]
    )

    siblings = " · ".join(
        f'<a href="{SITE}/{o["slug"]}/">{esc(o["kind"].split(" ·")[0])}</a>'
        for o in all_inds if o["slug"] != ind["slug"]
    )

    kind_short = ind["kind"].split(" ·")[0]
    meta_desc = f'{ind["title"]}. {ind["lede"]} 한국어·영어 직접 상담 · 일회 제작비 · 숨겨진 비용 없음 · {ind["plan"]}부터.'

    # 구조화 데이터 — 문자열 조립 대신 dict → json.dumps 로 만든다.
    # 손으로 중괄호를 맞추면 반드시 깨진다.
    url = f"{SITE}/{ind['slug']}/"
    graph = [
        {   # 이 페이지가 파는 것
            "@type": "Service",
            "@id": url + "#service",
            "name": ind["title"],
            "serviceType": "Website design",
            "description": meta_desc,
            "url": url,
            "provider": {
                "@type": "Organization",
                "@id": f"{SITE}/#organization",
                "name": "NanuriWeb",
                "legalName": "Hebron Platform LLC",
                "url": SITE + "/",
                "email": "hello@nanuriweb.com",
            },
            "areaServed": {
                "@type": "City", "name": "Seattle",
                "addressRegion": "WA", "addressCountry": "US",
            },
            "availableLanguage": ["ko", "en", "es"],
            "offers": {
                "@type": "Offer",
                "priceCurrency": "USD",
                "price": _price_of(ind["plan"]),
                "availability": "https://schema.org/InStock",
                "url": f"{SITE}/#plans",
            },
        },
        {   # 검색 결과에 경로가 보이게
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "NanuriWeb", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": ind["kind"], "item": url},
            ],
        },
        {   # 검색 결과에 질문이 펼쳐지게
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in ind["faq"]
            ],
        },
    ]
    import json as _json
    jsonld = _json.dumps(
        {"@context": "https://schema.org", "@graph": graph},
        ensure_ascii=False, indent=2,
    )

    return TEMPLATE.format(
        site=SITE,
        slug=ind["slug"],
        title=esc(ind["title"]),
        h1=esc(ind["title"]),
        kind=esc(ind["kind"]),
        kind_short=esc(kind_short),
        lede=esc(ind["lede"]),
        hero_stat=esc(ind["hero_stat"]),
        keywords=esc(ind["keywords"]),
        meta_desc=esc(meta_desc),
        plan=esc(ind["plan"]),
        plan_note=esc(ind["plan_note"]),
        pain_html=pain_html,
        inc_html=inc_html,
        faq_html=faq_html,
        siblings=siblings,
        jsonld=jsonld,
    )


def _json_str(s):
    import json
    return json.dumps(s, ensure_ascii=False)


def _price_of(plan_text):
    """'Solo Plan $299' → '299'. 여러 개면 가장 낮은 값(진입가)을 쓴다."""
    nums = [int(n.replace(",", "")) for n in re.findall(r"\$([\d,]+)", plan_text)]
    return str(min(nums)) if nums else "299"


def write_sitemap():
    from datetime import date
    today = date.today().isoformat()
    urls = [(f"{SITE}/", "1.0", "weekly")]
    urls += [(f"{SITE}/{i['slug']}/", "0.8", "monthly") for i in INDUSTRIES]
    body = "\n".join(
        "  <url>\n"
        f"    <loc>{u}</loc>\n"
        f"    <lastmod>{today}</lastmod>\n"
        f"    <changefreq>{c}</changefreq>\n"
        f"    <priority>{p}</priority>\n"
        "  </url>"
        for u, p, c in urls
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    return len(urls)


def write_robots():
    """검색엔진에는 열어두되, 학습용 대량 수집 봇은 막는다."""
    blocked = ["GPTBot", "CCBot", "ClaudeBot", "Google-Extended",
               "anthropic-ai", "Bytespider", "PerplexityBot"]
    lines = ["User-agent: *", "Allow: /", ""]
    lines += ["# 내부 · 작업용 경로는 색인 제외",
              "Disallow: /clients/",
              "Disallow: /agency/",
              "Disallow: /ops/",
              "Disallow: /shared/",
              "Disallow: /99_Archive/",
              "Disallow: /*.src.html$",
              ""]
    for b in blocked:
        lines += [f"User-agent: {b}", "Disallow: /", ""]
    lines += [f"Sitemap: {SITE}/sitemap.xml", ""]
    (ROOT / "robots.txt").write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list:
        for i in INDUSTRIES:
            print(f"  {SITE}/{i['slug']}/   — {i['kind']}")
        return

    print("=" * 56)
    print(" NanuriWeb 업종별 랜딩페이지 생성")
    print("=" * 56)

    for ind in INDUSTRIES:
        d = ROOT / ind["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(build_page(ind, INDUSTRIES), encoding="utf-8")
        size = (d / "index.html").stat().st_size
        print(f"  {ind['slug']}/index.html  ({size:,} bytes)  — {ind['kind']}")

    n = write_sitemap()
    write_robots()
    print(f"\n  sitemap.xml  — URL {n}개")
    print("  robots.txt   — 생성")
    print("\n완료. 배포:  vercel --prod")
    print("배포 후 구글 서치 콘솔에 sitemap.xml 제출하세요.")
    print("=" * 56)


if __name__ == "__main__":
    main()
