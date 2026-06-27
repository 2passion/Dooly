# 32_Order_ProjectSummary_v1.0.md
# KING Assistant OS — 프로젝트 전체 가이드 문서 생성

---

# 작업 개요
지금까지 진행한 전체 작업을 빠짐없이, 중복없이 정리하여
나중에 처음부터 따라할 수 있는 단계별 가이드 문서를 생성한다.

---

# 읽을 파일 목록 (순서대로 모두 읽기)
1. C:\Obsidian\Dooly\00_System\01_PROJECT_MASTER.md
2. C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md
3. C:\Obsidian\Dooly\00_System\03_DEVELOPMENT_RULE_v1.0.md
4. C:\Obsidian\Dooly\03_Claude_Code\ 폴더 전체 파일 목록 확인
5. C:\Obsidian\Dooly\04_Runtime\ 폴더 전체 파일 목록 확인
6. C:\Obsidian\Dooly\05_RAG\ 폴더 전체 파일 목록 확인
7. C:\Obsidian\Dooly\.gitignore

---

# 생성할 파일
C:\Obsidian\Dooly\00_System\04_PROJECT_GUIDE_v1.0.md

---

# 문서 작성 기준
1. 빠짐없이: 프로젝트 시작부터 현재까지 모든 작업 포함
2. 중복없이: 같은 내용 반복 없음
3. 단계별로 따라할 수 있게: 순서대로 실행하면 동일한 결과가 나오도록
4. 트러블슈팅 포함: 실제로 겪은 오류와 해결 방법

---

# 문서 구조 (아래 구조로 작성)

```
# KING Assistant OS — 프로젝트 전체 가이드
> 킹수학 조교 운영 시스템 구축 전체 과정
> 작성일: 2026-06-26
> 최신 커밋: (SESSION_HANDOVER에서 확인)

---

## 1. 프로젝트 개요
### 1-1. 목적
### 1-2. 기술 스택
### 1-3. 폴더 구조
```
C:\Obsidian\Dooly\
├── 00_System\      ← 시스템 문서
├── 01_Project\     ← 설계 문서
├── 02_Claude_Project\ ← Claude Project 지침
├── 03_Claude_Code\ ← Claude Code 작업지시서
├── 04_Runtime\     ← HTML 실행 파일
├── 05_RAG\         ← RAG 서버
└── 99_Archive\     ← 아카이브 (git 제외)
```

---

## 2. 환경 준비 (Phase 0)
### 2-1. 필수 소프트웨어 설치
### 2-2. GitHub 저장소 생성 및 연결
### 2-3. Obsidian 폴더 구조 생성
### 2-4. .gitignore 설정
### 2-5. 시스템 문서 작성 (00_System)

---

## 3. HTML 프로토타입 구축 (Phase 1)
### 3-1. HTML 파일 6개 생성 (프롬프트 11번)
### 3-2. UI 개선 (프롬프트 12~15번)
### 3-3. 달력 + 설정 탭 추가 (프롬프트 17번)

---

## 4. 데이터 확장 (Phase 2)
### 4-1. SOP 22개 / 9카테고리 (프롬프트 18번)
### 4-2. FAQ 22개 / 10카테고리 + Dooly 키워드 23개 (프롬프트 19번)

---

## 5. UI 버그 수정 및 기능 개선 (Phase 3)
### 5-1. 체크박스 제거 + 상태 필터 (프롬프트 20번)
### 5-2. 주간 달력 화살표 버그 수정 (프롬프트 21번)
### 5-3. SOP/FAQ URL 링크 + 경로 복사 버튼 (프롬프트 22~23번)
### 5-4. 공지 탭 홈으로 통합 (프롬프트 24번)

---

## 6. RAG 서버 구축 (Phase 4)
### 6-1. 사전 설치 목록
- Python 버전 확인
- Ollama 설치
- 모델 다운로드 (qwen2.5:7b / qwen2.5:3b / gemma3:4b)
- Python 패키지 설치

### 6-2. 05_RAG 폴더 생성
### 6-3. RAG 서버 파일 생성 (프롬프트 25번)
- docs/sop_data.txt, faq_data.txt
- embed.py, server.py
### 6-4. 실행 스크립트 생성 (프롬프트 26번)
- run_embed.bat, run_server.bat, README_RAG.txt
### 6-5. 첫 실행 순서

---

## 7. Dooly AI 고도화 (Phase 5)
### 7-1. 모델 선택 드롭다운 + 출처 태그 (프롬프트 29번)
### 7-2. 대화 기록 localStorage 유지 (프롬프트 30번)
### 7-3. 스마트폰 접속 - HTML 서빙 (프롬프트 31번)

---

## 8. 현재 시스템 완성 상태
### 8-1. HTML 파일 목록 및 기능
### 8-2. RAG 서버 파일 목록
### 8-3. 설치 완료 목록
### 8-4. Git 커밋 히스토리 요약

---

## 9. 매일 사용 방법
### 9-1. 서버 시작
### 9-2. PC 접속
### 9-3. 스마트폰 접속
### 9-4. 데이터 변경 시 재임베딩

---

## 10. 다음 단계 (미완료)
### 10-1. Windows 작업 스케줄러 등록
### 10-2. PWA 전환
### 10-3. 외부 접속 (ngrok)
### 10-4. 답변 품질 개선

---

## 11. 트러블슈팅
- bat 파일 한글 깨짐 → 영문으로 교체
- 포트 8000 충돌 → 8001로 변경
- FAQ 필터 미작동 → localStorage 초기화
- Dooly 답변 부정확 → 재임베딩
- 스마트폰 접속 불가 → 게이트웨이 확인

---

## 12. 개발 워크플로우
### 12-1. Claude Code 작업지시서 규칙
### 12-2. 세션 인수인계 방법
### 12-3. Git 커밋 규칙
```

---

# 작업 완료 후

```
git add 00_System/04_PROJECT_GUIDE_v1.0.md && git commit -m "docs: add complete project setup guide v1.0" && git push
```
