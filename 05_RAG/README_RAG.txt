=============================================
  Dooly RAG 시스템 사용 방법
=============================================

[처음 설치 후]
1. run_embed.bat 더블클릭 → 임베딩 완료 대기
2. run_server.bat 더블클릭 → 서버 실행
3. 브라우저에서 index.html 열기 → Dooly 탭

[매일 사용할 때]
1. run_server.bat 더블클릭
2. 브라우저에서 index.html 열기 → Dooly 탭

[SOP/FAQ 데이터 변경 후]
1. run_embed.bat 더블클릭 → 재임베딩
2. run_server.bat 더블클릭 → 서버 재실행

[docs 폴더에 새 파일 추가 방법]
- C:\Obsidian\Dooly\05_RAG\docs\ 에 txt 파일 추가
- run_embed.bat 다시 실행
- 자동으로 검색 대상에 포함됨

[폴더 구조]
05_RAG\
├── docs\
│   ├── sop_data.txt     ← SOP 22개
│   └── faq_data.txt     ← FAQ 22개
│   └── (추가 txt 파일)  ← 자유롭게 추가 가능
├── db\                  ← 벡터DB (자동 생성)
├── embed.py             ← 임베딩 스크립트
├── server.py            ← FastAPI 서버
├── run_embed.bat        ← 임베딩 실행 (더블클릭)
├── run_server.bat       ← 서버 실행 (더블클릭)
└── README_RAG.txt       ← 이 파일

[서버 주소]
로컬: http://localhost:8001
같은 와이파이 스마트폰: http://[PC_IP]:8001
예) http://192.168.0.10:8001

[PC IP 확인 방법]
cmd에서: ipconfig
IPv4 주소 확인
=============================================
