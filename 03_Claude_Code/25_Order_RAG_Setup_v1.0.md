# 25_Order_RAG_Setup_v1.0.md
# KING Assistant OS — RAG 서버 구축 (FastAPI + Chroma + Ollama)

---

# 작업 개요
- 05_RAG 폴더에 필요한 파일 생성
- SOP/FAQ 데이터를 Chroma 벡터DB에 임베딩
- FastAPI 서버로 Dooly HTML과 연동
- SESSION_HANDOVER.md 및 PROJECT_MASTER.md 폴더 구조 업데이트

---

# 사전 확인
아래가 모두 완료된 상태에서 진행:
- Python 3.13.9 설치 완료
- Ollama 0.30.10 설치 완료
- qwen2.5:7b 모델 다운로드 완료
- fastapi, uvicorn, chromadb, sentence-transformers, ollama, PyPDF2 설치 완료
- C:\Obsidian\Dooly\05_RAG\db\ 폴더 존재
- C:\Obsidian\Dooly\05_RAG\docs\ 폴더 존재

---

# [작업 1] SOP/FAQ 텍스트 파일 생성

## 1-1. SOP 데이터 파일 생성
아래 내용으로 C:\Obsidian\Dooly\05_RAG\docs\sop_data.txt 파일을 생성한다:

```
[SOP-1] 복테 제출함 관리 SOP | 카테고리: 복테
학생 하원 즉시 제출함을 비운다. 내용물은 오답기록표와 복습테스트(복테)다. 오답기록표는 챙겨서 다음 등원용 복테 제작에 활용한다. 복테가 완료된 경우 점수 기록 후 스캔하여 학생 폴더에 저장한다. 복테가 미완료인 경우 복테 보관함으로 이동한다. 원칙: 학생이 하원하면 제출함은 반드시 비운다.

[SOP-2] 복테 제작 SOP | 카테고리: 복테
학생이 제출한 오답기록표를 확인한다. 오답기록표의 날짜/페이지/문제번호를 바탕으로 복테를 제작한다. 제작 완료 후 PC 저장 후 프린트하여 복테 보관함에 보관한다. 퇴근 30분 전에 학생별 복테 프린트 후 PC 저장, 작업완료 폴더에 저장한다. 복테는 다음 등원 시 학생에게 즉시 제공 가능해야 한다.

[SOP-3] 복테 보관함 운영 SOP | 카테고리: 복테
보관함 배치 규칙: X존(고등)은 고3, 고2, 고1 순서(위에서 아래). Y존(초중)은 초등 전체, 중3, 중2, 중1 순서(위에서 아래). 학년 칸 내 A반/B반 섹션파일로 구분한다. 앞부분에 복습테스트와 프린트물, 뒷부분에 오답기록표를 보관한다. 자료 찾기는 학년(X/Y존) 후 반(A/B) 순서로 확인한다.

[SOP-4] 복테 처리 및 폐기 SOP | 카테고리: 복테
완료된 복테는 스캔 후 학생 폴더에 저장한다. 스캔 완료된 문제지는 분리수거(폐기)한다. 빠른 정답지(뒷면 백지)는 이면지 보관함으로 이동한다. 미완료 복테는 복테 보관함에 보관하여 다음 시간에 재사용한다. 완료 기준: 모든 별표(★) 문제가 큰 세모(△)로 해결된 상태.

[SOP-5] 오답기록표 관리 SOP | 카테고리: 오답노트
학생은 등원 시 오답기록표를 찾아 오늘 틀린 문제를 기록한다. 기록 항목은 날짜, 페이지, 문제 번호(세로로 기록)다. 질문 필요 문제는 문제 번호 뒤에 별표(★) 표시한다. 하원 시 반드시 학원에 제출하며 개별 소지는 금지다. 오답기록표에 끝이 기재되면 교재 전체 오답을 모아 제본한다.

[SOP-6] 오답노트 제본 SOP | 카테고리: 오답노트
오답기록표에 끝이 기재된 경우 오답노트 제본을 진행한다. 교재 전체 오답기록표를 수집한다. 제본 링 사이즈는 20mm를 사용한다. 제본 방법은 한 번에 최대 20장씩 펀칭하고 좌측 끝에 붙여서 삽입한다. 첫 페이지에 만든날짜와 오답노트를 기입한다. 완성된 오답노트를 학생에게 전달한다. 작업 후 제본기 찌꺼기함을 반드시 비운다.

[SOP-7] 연습장 관리 SOP | 카테고리: 비품
연습장 보관함은 항상 5권을 유지한다(50매 양식 사용). 오답기록표 정리 시 보관함을 확인한다. 5권 미만이면 즉시 제작하여 채워 넣는다. 제본 링 사이즈는 12mm를 사용한다. 연습장이 없는 학생은 이면지 보관함에서 이면지를 꺼내 사용한다.

[SOP-8] 이면지 보관함 SOP | 카테고리: 비품
위치는 복테 제출함 아래다. 수거 대상은 스캔/프린트 후 발생한 깨끗한 이면지다. 조교는 작업 후 이면지를 즉시 폐기하지 말고 보관함에 정리한다. 학생은 연습장 미지참 시 자유롭게 꺼내 사용할 수 있다. 수시로 정리하여 항상 사용 가능한 상태를 유지한다.

[SOP-9] 소모품 재고 관리 SOP | 카테고리: 비품
관리 대상은 A4 용지(복사기 근처)와 제본 링(제본기 근처)이다. 보고 시점은 재고 20~30% 남았을 때 미리 원장에게 보고한다. 재고 소진 후 보고는 금지다. 제본 링 사이즈 기준: 12mm는 연습장 등 얇은 자료, 20mm는 오답노트 등 두꺼운 자료.

[SOP-10] 복사기/스캔 SOP | 카테고리: 장비
ADF(자동)는 많은 양의 깨끗한 종이 스캔 시 사용한다. 수동(평판)은 종이가 얇거나 구겨진 경우 반드시 사용한다. 복사 설정 원칙은 양면 출력(양면→양면)이 기본이다. 구겨진 종이는 반드시 수동 스캔한다. 종이 걸릴 것 같으면 무리하게 ADF에 넣지 않는다.

[SOP-11] 제본기 사용 SOP | 카테고리: 장비
펀칭 단위는 한 번에 최대 20장씩 나누어 펀칭한다. 정렬 방법은 종이를 좌측 끝에 완전히 붙여서 삽입한다. 링 사이즈: 12mm는 얇은 자료, 20mm는 두꺼운 자료. 작업 후 반드시 하단 찌꺼기함(폐지통)을 비운다. 찌꺼기함을 비우지 않으면 기기 고장 원인이 된다.

[SOP-12] 출근 루틴 SOP | 카테고리: 루틴
복테 제출함을 확인한다. 조교할일(이니셜)을 확인하고 업무를 시작한다. 이해 안 되는 업무는 즉시 원장에게 질문한다. 연습장 보관함을 확인하여 5권을 유지한다. 이면지 보관함을 정리한다. 필기구 배치 기준을 확인한다.

[SOP-13] 퇴근 루틴 SOP | 카테고리: 루틴
퇴근 30분 전에 학생별 복테 프린트, PC 저장, 작업완료 폴더 저장, 바탕화면 날짜 폴더 자료를 학생별 폴더에 저장한다. 퇴근 직전에 주변 정리(책상 위, 의자 위, 바닥 순서), 필기구 원위치, PC 및 모니터 전원을 끈다.

[SOP-14] 채점 규칙 SOP | 카테고리: 채점
채점 기호: O는 정답, /(슬래시)는 오답 1차, △(세모)는 스스로 고쳐서 맞춤, ☆(별표)는 질문이 필요한 문제, ☆ 위에 큰 △는 질문 후 해결 완료(3차 채점). 숙제 채점은 학생 스스로 한다. 1차 채점은 정답 보고 채점, 2차 채점은 스스로 고친 후 다시 채점, 3차 채점은 해설지 참고 후 질문하여 해결한다. 테스트 채점은 조교가 진행한다.

[SOP-15] 교재검사 SOP | 카테고리: 채점
개념편과 유형편을 교대로 검사한다. 개념편을 풀고 있으면 유형편을 검사하고, 유형편을 풀고 있으면 개념편을 검사한다. 모르겠으면 학생에게 물어보거나 원장에게 확인한다. 목차 위에 덜 완료된 페이지 번호만 기록한다(문제번호 X). 추가 검사 후 완료된 페이지에 슬래시(/) 표시, 전체 완료 시 OK를 기재한다.

[SOP-16] 진단평가 SOP | 카테고리: 채점
교재 전체 누적테스트로 단원별 중요문제 20~25개를 선별하여 시간을 재고 풀고 제출한다. 1차 커트라인(70점 이상): 진단평가 오답만 연습장에 풀고 제출. 2차 커트라인(50~69점): 오답노트 다시 한 번 풀고 제출. 2차 커트라인 미통과(50점 미만): 진단평가 틀린문제 관련 과제 별도 제공. 진단평가 결과는 시험지와 함께 학부모에게 전달한다.

[SOP-17] 신규 조교 온보딩 SOP | 카테고리: 루틴
첫 출근 전 준비: 서류 제출(등본, 재학증명서), 성범죄 경력 조회(범죄경력회보서 발급시스템 http://crims.police.go.kr 에서 공인인증서 또는 카카오톡 인증으로 본인인증 후 진행). 첫 출근 시 확인사항: 이니셜 확인(원장에게 업무용 이니셜 전달받기), 조교할일 파일 확인(날짜-조교할일-이니셜 형식), 학년별/반별 학생이름 확인, 공휴일 일정 확인. 교육 3단계: 1단계 모델링(기존 조교가 직접 시범), 2단계 코칭(신규 조교가 직접 수행, 기존 조교가 교정), 3단계 독립 수행.

[SOP-18] 파일명 규칙 SOP | 카테고리: 루틴
복테 파일명 규칙: hwp 파일은 날짜+복테+학년+교재+학생이름, WANT 프로그램은 날짜+교재+학생이름(파일명에 복테 넣지 않음). 스캔 파일명 규칙: 오답노트_날짜 학년 교재 학생이름. 같은 복테를 추가할 때는 끝에 -1, -2 번호 추가. 오답노트 폴더명 규칙: 날짜+오답노트+교재+학생이름. 교재 구분 주의: 2022는 출판연도, 22개정은 교육과정 개정연도로 학생마다 다를 수 있으니 복테 제작 시 반드시 확인.

[SOP-19] 베낌 판별 SOP | 카테고리: 학생관리
조교 5초 판별 프로토콜. STEP1 3초 스캔: 지나치게 깔끔, 지우개 흔적 없음, 계산 과정 없음, 문제-풀이 불일치, 글씨체 변화 중 2개 이상이면 의심. STEP2 2초 질문: 이 문제 어떻게 풀었어요? 설명하지 못하면 의심 확정. STEP3 5초 확정: 같은 문제 다시 풀리기 또는 숫자 바꿔서 재풀이, 못 풀면 100% 베낌. 절대 금지 행동: 친구 풀이 베끼기, 답 먼저 보고 끼워 맞추기, 일부러 틀리기, 별표만 치고 넘어가기.

[SOP-20] 학생관리 SOP | 카테고리: 학생관리
학생 유형 분류. 규율(습관을 잡아야 하는 학생): 몰라요 하면서 그냥 물어봄, 쓰기 귀찮아함, 시키지 않으면 안 함, 글씨체가 삐뚤삐뚤. 대응: 학생 설명에 특이사항 기록. 첨삭(몰라서 못하는 학생): 실수를 많이 함, 이해보다 암기하고 넘어가려 함, 노트정리를 너무 예쁘게 하려 함. 대응: 지우개 사용 줄이기 지도. 검사(알지만 안 하는 학생): 물어보지 않으면 질문 안 함, 숙제를 밀리는 경우 있음, 졸리면 자세가 흐트러짐. 대응: 채점 V 표시로 확인.

[SOP-21] 복사기 종이 걸림 SOP | 카테고리: 예외상황
무리하게 잡아당기지 않는다. 복사기 오류 코드를 확인한다. 복사기 옆면/앞면 덮개를 열어서 용지를 조심히 제거한다. 단독 해결 불가 시 원장에게 즉시 보고한다. 예방법: 구겨진 종이는 반드시 수동(평판) 스캔 사용, ADF에 무리하게 넣지 않는다.

[SOP-22] 학생 자료 분실/누락 SOP | 카테고리: 예외상황
복테 분실 시: 복테 보관함 재확인(X존/Y존 배치 확인), 학생 폴더에서 파일 확인, 공유폴더 확인, 재출력 후 제공. 오답기록표 분실 시: 오답기록표는 학원에서만 보관하는 자료(학생이 개별 소지하면 안 됨), 원장에게 보고 후 조치. 복테 날짜 오류 시: 오류 날짜 확인, 파일 수정 후 재출력. 원칙: 모르면 추측하지 말고 원장에게 확인, 혼자 판단하여 처리하지 않는다.
```

## 1-2. FAQ 데이터 파일 생성
아래 내용으로 C:\Obsidian\Dooly\05_RAG\docs\faq_data.txt 파일을 생성한다:

```
[FAQ-1] 복사기가 종이를 먹었어요 | 카테고리: 복사기
종이가 구겨진 경우 ADF를 사용하지 말고 수동(평판) 스캔으로 진행하세요. 무리하게 ADF에 넣으면 용지 걸림이 발생합니다. 복사기/스캔 SOP를 확인하세요.

[FAQ-2] 학생이 복테를 못 찾겠어요 | 카테고리: 복테
복테 보관함 배치 순서를 확인하세요. X존(고등): 고3→고2→고1, Y존(초중): 초등→중3→중2→중1 순서입니다. 학년 내 A반/B반 섹션파일 앞부분을 확인하세요. 복테 보관함 운영 SOP를 참고하세요.

[FAQ-3] 오답기록표에 끝이라고 적혀있어요 | 카테고리: 오답노트
오답노트 제본을 진행해야 합니다. 교재 전체 오답기록표를 수집하고, 20mm 링으로 제본 후 첫 페이지에 만든날짜와 오답노트를 기입하여 학생에게 전달하세요. 오답노트 제본 SOP를 참고하세요.

[FAQ-4] 연습장이 부족해요 | 카테고리: 비품
연습장 보관함은 항상 5권을 유지해야 합니다. 5권 미만이면 즉시 제작하세요(50매 양식, 12mm 링 사용). 연습장이 없는 학생은 이면지 보관함에서 이면지를 사용하도록 안내하세요.

[FAQ-5] ADF 스캔과 수동 스캔 차이가 뭐예요 | 카테고리: 복사기
ADF(자동 원고 급지)는 깨끗하고 많은 양의 종이를 한 번에 스캔할 때 사용합니다. 수동(평판) 스캔은 종이가 얇거나 구겨진 경우에 사용합니다. 구겨진 종이를 ADF에 넣으면 용지 걸림이 발생하므로 반드시 수동으로 진행하세요.

[FAQ-6] 제본링 사이즈는 어떻게 선택해요 | 카테고리: 제본기
12mm 링: 연습장, 내신모의 10회분 등 얇은 자료에 사용합니다. 20mm 링: 오답노트, 기출 20개 학교 등 두꺼운 자료에 사용합니다.

[FAQ-7] 제본기 찌꺼기는 언제 비워요 | 카테고리: 제본기
제본기 사용 후 매번 반드시 하단 찌꺼기함(폐지통)을 비워야 합니다. 찌꺼기를 비우지 않으면 기기 고장의 원인이 됩니다.

[FAQ-8] 복테 보관함 배치 순서가 어떻게 돼요 | 카테고리: 복테
X존(고등): 위에서부터 고3→고2→고1 순서입니다. Y존(초중): 위에서부터 초등 전체→중3→중2→중1 순서입니다. 학년 칸 안에는 A반/B반 섹션파일이 있으며, 앞부분에 복테/프린트물, 뒷부분에 오답기록표를 보관합니다.

[FAQ-9] 비품이 부족할 때 언제 보고해요 | 카테고리: 비품
재고가 20~30% 남았을 때 미리 원장에게 보고해야 합니다. 재고가 완전히 소진된 후 보고하면 업무 공백이 발생합니다.

[FAQ-10] 이면지는 어디에 보관해요 | 카테고리: 비품
이면지 보관함은 복테 제출함 아래에 있습니다. 스캔/프린트 후 발생한 뒷면이 깨끗한 종이를 이면지 보관함에 정리하세요.

[FAQ-11] 복테 완료 기준이 뭐예요 | 카테고리: 복테
모든 별표(★) 문제가 큰 세모(△)로 해결된 상태가 완료입니다. 완료된 복테는 점수 칸에 세모 표시 후 스캔하여 학생 폴더에 저장합니다. 미완료 복테는 복테 보관함에 넣어 다음 시간에 다시 풀도록 합니다.

[FAQ-12] 연습장은 몇 권 유지해야 해요 | 카테고리: 비품
연습장 보관함은 항상 5권을 유지해야 합니다(50매 양식 사용). 오답기록표 정리 시마다 보관함을 확인하고, 5권 미만이면 즉시 제작하여 채워 넣습니다.

[FAQ-13] 복테랑 오답노트가 뭐가 달라요 | 카테고리: 복테
복테(복습테스트)는 오답기록표를 바탕으로 매일 제공하는 일일 복습 테스트입니다. 오답노트는 교재 전체가 끝났을 때 복테 전체를 모아 제본한 누적 복습 자료입니다. 복테는 매일, 오답노트는 교재 종료 시 제작합니다.

[FAQ-14] 채점 기호는 어떻게 써요 | 카테고리: 채점
O는 정답, /(슬래시)는 오답 1차, △(세모)는 스스로 고쳐서 맞춤, ☆(별표)는 질문이 필요한 문제, ☆ 위에 큰 △는 질문 후 해결 완료(3차 채점)입니다. 숙제는 학생이 스스로 채점하고, 테스트는 조교가 채점합니다.

[FAQ-15] 진단평가 커트라인이 어떻게 되나요 | 카테고리: 채점
1차 커트라인(70점 이상): 진단평가 오답만 연습장에 풀고 제출. 2차 커트라인(50~69점): 오답노트 다시 한 번 풀고 제출. 2차 미통과(50점 미만): 틀린문제 관련 과제를 별도로 받아서 풀고 제출합니다.

[FAQ-16] 교재검사는 어떻게 해요 | 카테고리: 채점
개념편과 유형편을 교대로 검사합니다. 덜 완료된 페이지 번호만 목차에 기록하고(문제번호 X), 추가 검사 후 완료된 페이지에 슬래시(/) 표시, 전체 완료 시 OK를 기재합니다.

[FAQ-17] 오답노트 폴더명은 어떻게 만들어요 | 카테고리: 오답노트
날짜+오답노트+교재+학생이름 순서로 만듭니다. 예) 260402 오답노트 중1-1 쎈 김철수. 오답기록표에 끝이라고 적혀있으면 오답노트 제작을 시작합니다.

[FAQ-18] 파일명 규칙이 어떻게 되나요 | 카테고리: 파일관리
hwp 파일: 날짜+복테+학년+교재+학생이름. WANT 프로그램: 날짜+교재+학생이름(복테 미포함). 스캔 파일: 오답노트_날짜 학년 교재 학생이름. 같은 복테 추가 시 끝에 -1, -2 번호 추가.

[FAQ-19] 2022 교재와 22개정 교재 차이가 뭐예요 | 카테고리: 파일관리
2022는 출판사에서 출판한 연도(2022년)이고, 22개정은 교육부가 교육과정을 개정한 연도(2022년)입니다. 교육부가 22개정을 하면 출판사는 3~4년 후(2025~2026년)에 출판합니다. 같은 교재명이라도 학생마다 다를 수 있으니 복테 제작 시 반드시 확인하세요.

[FAQ-20] 학생이 별표를 안 했어요 | 카테고리: 학생관리
별표(☆)는 질문이 필요한 문제를 표시하는 항목입니다. 학생이 고민했지만 해결하지 못한 문제는 반드시 별표를 표시하도록 안내하세요.

[FAQ-21] 숙제 베낌이 의심될 때 어떻게 해요 | 카테고리: 학생관리
조교 5초 판별 프로토콜을 사용하세요. 3초 스캔: 지나치게 깔끔/지우개 흔적 없음/계산 과정 없음/글씨체 변화 중 2개 이상이면 의심. 2초 질문: 이 문제 어떻게 풀었어요? 5초 확정: 같은 문제 다시 풀리기 또는 숫자 바꿔 재풀이, 못 풀면 베낌 확정.

[FAQ-22] 첫 출근인데 뭐부터 해야 하나요 | 카테고리: 루틴
1. 서류 제출(등본, 재학증명서). 2. 성범죄 경력 조회(원장 안내 후 진행, http://crims.police.go.kr). 3. 이니셜 확인(원장에게 전달받기). 4. 조교할일 파일 확인(날짜-조교할일-이니셜 형식). 5. 학년별/반별 학생이름 확인. 6. 풀어볼거 진행(원장 설명 후). 신규 조교 온보딩 SOP를 참고하세요.
```

---

# [작업 2] embed.py 생성

아래 내용으로 C:\Obsidian\Dooly\05_RAG\embed.py 파일을 생성한다:

```python
# embed.py — SOP/FAQ 문서를 Chroma 벡터DB에 임베딩

import os
import chromadb
from chromadb.utils import embedding_functions

# 경로 설정
DOCS_DIR = r"C:\Obsidian\Dooly\05_RAG\docs"
DB_DIR   = r"C:\Obsidian\Dooly\05_RAG\db"

# 임베딩 함수 (로컬 모델, 인터넷 불필요)
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)

# Chroma 클라이언트 초기화
client = chromadb.PersistentClient(path=DB_DIR)

# 기존 컬렉션 삭제 후 재생성 (재임베딩 시)
try:
    client.delete_collection("dooly_docs")
    print("기존 컬렉션 삭제 완료")
except:
    pass

collection = client.create_collection(
    name="dooly_docs",
    embedding_function=emb_fn
)

# docs 폴더의 모든 txt 파일 읽기
docs = []
ids  = []
metas = []

for filename in os.listdir(DOCS_DIR):
    if not filename.endswith(".txt"):
        continue

    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 빈 줄 기준으로 청크 분할
    chunks = [c.strip() for c in content.split("\n\n") if c.strip()]

    for i, chunk in enumerate(chunks):
        doc_id = f"{filename}_{i}"
        docs.append(chunk)
        ids.append(doc_id)
        metas.append({"source": filename, "chunk": i})

# 벡터DB에 저장
if docs:
    collection.add(
        documents=docs,
        ids=ids,
        metadatas=metas
    )
    print(f"임베딩 완료: {len(docs)}개 청크 저장됨")
else:
    print("docs 폴더에 txt 파일이 없습니다.")
```

---

# [작업 3] server.py 생성

아래 내용으로 C:\Obsidian\Dooly\05_RAG\server.py 파일을 생성한다:

```python
# server.py — FastAPI + Chroma + Ollama RAG 서버

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
import ollama

# 경로 설정
DB_DIR = r"C:\Obsidian\Dooly\05_RAG\db"
MODEL  = "qwen2.5:7b"

# FastAPI 앱 초기화
app = FastAPI()

# CORS 설정 (HTML 파일에서 API 호출 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chroma 초기화
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)
chroma_client = chromadb.PersistentClient(path=DB_DIR)
collection = chroma_client.get_collection(
    name="dooly_docs",
    embedding_function=emb_fn
)

# 요청 모델
class ChatRequest(BaseModel):
    message: str

# 시스템 프롬프트
SYSTEM_PROMPT = """당신은 킹수학 학원의 AI 업무 도우미 둘리(Dooly)입니다.
조교들의 업무를 도와주는 역할을 합니다.

규칙:
1. 반드시 한국어로 답변합니다.
2. 제공된 SOP/FAQ 내용을 기반으로 답변합니다.
3. 모르는 내용은 추측하지 말고 "확인이 필요합니다. 원장에게 문의하세요."라고 답변합니다.
4. 답변은 간결하고 명확하게 합니다.
5. 학생이나 학부모에게 직접 약속하지 않습니다."""

@app.get("/")
def root():
    return {"status": "Dooly RAG 서버 실행 중"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        # 1. 벡터DB에서 관련 문서 검색 (상위 3개)
        results = collection.query(
            query_texts=[req.message],
            n_results=3
        )

        # 2. 검색된 문서 컨텍스트 생성
        context_docs = results["documents"][0] if results["documents"] else []
        context = "\n\n---\n\n".join(context_docs)

        # 3. Ollama에 질문 + 컨텍스트 전달
        prompt = f"""다음은 킹수학 학원의 SOP/FAQ 내용입니다:

{context}

위 내용을 참고하여 아래 질문에 답변하세요:
질문: {req.message}"""

        response = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt}
            ]
        )

        answer = response["message"]["content"]
        return {"answer": answer, "sources": results["metadatas"][0] if results["metadatas"] else []}

    except Exception as e:
        return {"answer": f"오류가 발생했습니다: {str(e)}", "sources": []}
```

---

# [작업 4] start.bat 생성 (서버 실행 편의용)

아래 내용으로 C:\Obsidian\Dooly\05_RAG\start.bat 파일을 생성한다:

```bat
@echo off
echo Dooly RAG 서버 시작 중...
echo.
echo 1. 임베딩 실행 (최초 1회 또는 데이터 변경 시)
echo    python embed.py
echo.
echo 2. 서버 실행
cd /d C:\Obsidian\Dooly\05_RAG
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
pause
```

---

# [작업 5] 06_Dooly_v1.html 수정 — FastAPI 연동

C:\Obsidian\Dooly\04_Runtime\06_Dooly_v1.html 에서
기존 mockResponse 방식을 FastAPI 호출 방식으로 교체한다.

## 5-1. sendMessage() 함수 교체

기존:
```javascript
  function sendMessage() {
    var input = document.getElementById('chatInput');
    var text = input.value.trim();
    if (!text) return;

    addMsg('user', text);
    input.value = '';
    input.style.height = '';

    var response = mockResponse(text);
    setTimeout(function() {
      addMsg('dooly', response);
    }, 300);
  }
```

변경:
```javascript
  var RAG_SERVER = 'http://localhost:8000';

  function sendMessage() {
    var input = document.getElementById('chatInput');
    var text = input.value.trim();
    if (!text) return;

    addMsg('user', text);
    input.value = '';
    input.style.height = '';

    // 로딩 메시지 표시
    var loadingId = 'loading_' + Date.now();
    addMsgWithId('dooly', '답변을 생성 중입니다...', loadingId);

    // FastAPI 서버 호출
    fetch(RAG_SERVER + '/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    })
    .then(function(res) { return res.json(); })
    .then(function(data) {
      // 로딩 메시지 교체
      var loadingEl = document.getElementById(loadingId);
      if (loadingEl) {
        loadingEl.querySelector('.msg-bubble').textContent = data.answer;
      }
    })
    .catch(function(err) {
      var loadingEl = document.getElementById(loadingId);
      if (loadingEl) {
        loadingEl.querySelector('.msg-bubble').textContent =
          'RAG 서버에 연결할 수 없습니다.\nC:\\Obsidian\\Dooly\\05_RAG\\start.bat 을 실행해주세요.';
      }
    });
  }
```

## 5-2. addMsgWithId() 함수 추가
기존 addMsg() 함수 아래에 추가:

```javascript
  function addMsgWithId(who, text, id) {
    var area = document.getElementById('chatArea');
    var div = document.createElement('div');
    div.className = 'msg ' + who;
    div.id = id;
    div.innerHTML = [
      '<div class="msg-sender">' + (who === 'dooly' ? 'Dooly' : '나') + '</div>',
      '<div class="msg-bubble">' + escHtml(text) + '</div>'
    ].join('');
    area.appendChild(div);
    area.scrollTop = area.scrollHeight;
  }
```

## 5-3. mockResponse 함수는 그대로 유지 (삭제하지 않음)
서버 연결 실패 시 fallback으로 활용 가능하도록 유지.

---

# [작업 6] SESSION_HANDOVER.md 업데이트

C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md 에
아래 내용을 추가한다:

```
## 05_RAG 구조 (신규)

C:\Obsidian\Dooly\05_RAG\
├── docs\
│   ├── sop_data.txt     ← SOP 22개 텍스트
│   └── faq_data.txt     ← FAQ 22개 텍스트
├── db\                  ← Chroma 벡터DB 저장 위치
├── embed.py             ← 문서 임베딩 스크립트
├── server.py            ← FastAPI RAG 서버
└── start.bat            ← 서버 실행 배치 파일

## RAG 서버 실행 방법

1. 최초 1회 임베딩:
   cd C:\Obsidian\Dooly\05_RAG
   python embed.py

2. 서버 실행:
   start.bat 더블클릭
   또는
   python -m uvicorn server:app --host 0.0.0.0 --port 8000

3. 브라우저에서 확인:
   http://localhost:8000

4. Dooly 챗봇에서 사용:
   04_Runtime\index.html → Dooly 탭

## 설치 완료 목록

- Python 3.13.9 ✅
- Ollama 0.30.10 ✅
- qwen2.5:7b 모델 ✅
- fastapi, uvicorn, chromadb, sentence-transformers, ollama, PyPDF2 ✅
```

---

# [작업 7] .gitignore 업데이트

C:\Obsidian\Dooly\.gitignore 에 아래 내용 추가:

```
05_RAG/db/
05_RAG/__pycache__/
```

벡터DB 파일은 용량이 크므로 git에서 제외한다.

---

# 작업 완료 후 실행 순서

## 커밋 및 푸시
```
git add . && git commit -m "feat: RAG setup with FastAPI + Chroma + Ollama, Dooly API integration" && git push
```

## RAG 서버 실행 (Claude Code가 아닌 별도 cmd에서)
```
cd C:\Obsidian\Dooly\05_RAG
python embed.py
python -m uvicorn server:app --host 0.0.0.0 --port 8000
```

## 테스트
브라우저에서 index.html 열기 → Dooly 탭 → 질문 입력
예) "복테 완료 기준이 뭐예요?" → RAG 기반 답변 확인
