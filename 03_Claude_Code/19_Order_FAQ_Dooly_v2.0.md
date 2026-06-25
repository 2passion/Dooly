# 19_Order_FAQ_Dooly_v2.0.md
# KING Assistant OS — FAQ 추가 + Dooly 키워드 추가

---

# 수정 대상
C:\Obsidian\Dooly\04_Runtime\04_FAQ_v1.html
C:\Obsidian\Dooly\04_Runtime\06_Dooly_v1.html

---

# 작업 방식
HTML 구조/디자인은 건드리지 않는다.
JavaScript 데이터 배열만 수정한다.

---

# [수정 1] 04_FAQ_v1.html — CATEGORIES 배열 변경

기존:
```javascript
var CATEGORIES = ['전체', '복사기', '복테', '오답노트', '비품', '제본기'];
```

변경:
```javascript
var CATEGORIES = ['전체', '복테', '오답노트', '채점', '비품', '제본기', '복사기', '파일관리', '학생관리', '루틴'];
```

---

# [수정 2] 04_FAQ_v1.html — FAQS 배열에 10개 추가

기존 12개 배열 끝에 이어서 추가한다. id는 13번부터 시작.

```javascript
  {
    id: 13,
    category: '복테',
    question: '복테랑 오답노트가 뭐가 달라요?',
    answer: '복테(복습테스트)는 오답기록표를 바탕으로 매일 제공하는 일일 복습 테스트입니다. 오답노트는 교재 전체가 끝났을 때 복테 전체를 모아 제본한 누적 복습 자료입니다. 복테는 매일, 오답노트는 교재 종료 시 제작합니다.'
  },
  {
    id: 14,
    category: '채점',
    question: '채점 기호(O, /, △, ☆)는 어떻게 써요?',
    answer: 'O: 정답. /（슬래시）: 오답 1차. △（세모）: 스스로 고쳐서 맞춤. ☆（별표）: 질문이 필요한 문제. ☆ 위에 큰 △: 질문 후 해결 완료(3차 채점). 숙제는 학생이 스스로 채점하고, 테스트는 조교가 채점합니다.'
  },
  {
    id: 15,
    category: '채점',
    question: '진단평가 커트라인이 어떻게 되나요?',
    answer: '1차 커트라인(70점 이상): 진단평가 오답만 연습장에 풀고 제출. 2차 커트라인(50~69점): 오답노트 다시 한 번 풀고 제출. 2차 미통과(50점 미만): 틀린문제 관련 과제를 별도로 받아서 풀고 제출합니다. 진단평가 결과는 시험지와 함께 학부모에게 전달됩니다.'
  },
  {
    id: 16,
    category: '채점',
    question: '교재검사는 어떻게 해요?',
    answer: '개념편과 유형편을 교대로 검사합니다. 예를 들어 개념편을 풀고 있으면 유형편을 검사합니다. 덜 완료된 페이지 번호만 목차에 기록하고(문제번호 X), 추가 검사 후 완료된 페이지에 슬래시(/) 표시, 전체 완료 시 "OK"를 기재합니다. 모르면 학생 또는 원장에게 확인하세요.'
  },
  {
    id: 17,
    category: '오답노트',
    question: '오답노트 폴더명은 어떻게 만들어요?',
    answer: '날짜 + 오답노트 + 교재 + 학생이름 순서로 만듭니다. 예) 260402 오답노트 중1-1 쎈 김철수. 오답기록표에 "끝"이라고 적혀있으면 오답노트 제작을 시작합니다. 첫 페이지 상단에 "오답노트"와 만든 날짜를 기입합니다.'
  },
  {
    id: 18,
    category: '파일관리',
    question: '파일명 규칙이 어떻게 되나요?',
    answer: 'hwp 파일: 날짜+복테+학년+교재+학생이름. WANT 프로그램: 날짜+교재+학생이름(복테 미포함). 스캔 파일: 오답노트_날짜 학년 교재 학생이름. 같은 복테 추가 시 끝에 -1, -2 번호 추가. 파일명 규칙 SOP를 참고하세요.'
  },
  {
    id: 19,
    category: '파일관리',
    question: '2022 교재와 22개정 교재 차이가 뭐예요?',
    answer: '2022는 출판사에서 출판한 연도(2022년)이고, 22개정은 교육부가 교육과정을 개정한 연도(2022년)입니다. 교육부가 22개정을 하면 출판사는 3~4년 후(2025~2026년)에 출판합니다. 같은 교재명이라도 학생마다 다를 수 있으니 복테 제작 시 반드시 확인하세요.'
  },
  {
    id: 20,
    category: '학생관리',
    question: '학생이 별표를 안 했어요',
    answer: '별표(☆)는 질문이 필요한 문제를 표시하는 항목입니다. 학생이 고민했지만 해결하지 못한 문제는 반드시 별표를 표시하도록 안내하세요. 별표 없이 넘어가는 것은 절대 금지 행동입니다.'
  },
  {
    id: 21,
    category: '학생관리',
    question: '숙제 베낌이 의심될 때 어떻게 해요?',
    answer: '조교 5초 판별 프로토콜을 사용하세요. STEP1(3초 스캔): 지나치게 깔끔/지우개 흔적 없음/계산 과정 없음/글씨체 변화 중 2개 이상이면 의심. STEP2(2초 질문): "이 문제 어떻게 풀었어요?" STEP3(5초 확정): 같은 문제 다시 풀리기 또는 숫자 바꿔 재풀이, 못 풀면 베낌 확정. 베낌 판별 SOP를 참고하세요.'
  },
  {
    id: 22,
    category: '루틴',
    question: '첫 출근인데 뭐부터 해야 하나요?',
    answer: '1. 서류 제출(등본, 재학증명서). 2. 성범죄 경력 조회(원장 안내 후 진행). 3. 이니셜 확인(원장에게 전달받기). 4. 조교할일 파일 확인(날짜-조교할일-이니셜 형식). 5. 학년별/반별 학생이름 확인. 6. 풀어볼거 진행(원장 설명 후). 신규 조교 온보딩 SOP를 참고하세요.'
  }
```

---

# [수정 3] 06_Dooly_v1.html — mockResponse 함수 확장

기존 mockResponse 함수 전체를 아래로 교체한다.

```javascript
function mockResponse(input) {
  var text = input.toLowerCase();

  // 기존 키워드
  if (text.includes('복사기') || text.includes('종이 걸') || text.includes('용지')) {
    return '복사기/스캔 SOP와 복사기 종이 걸림 SOP를 확인하세요.\n구겨진 종이는 ADF 대신 수동(평판) 스캔을 사용하세요.';
  }
  if (text.includes('복테 보관함') || text.includes('보관함')) {
    return '복테 보관함 운영 SOP를 확인하세요.\nX존(고등): 고3→고2→고1 / Y존(초중): 초등→중3→중2→중1 순서입니다.';
  }
  if (text.includes('복테')) {
    return '복테 관련 SOP를 확인하세요.\n제출함 관리 / 제작 / 보관함 운영 / 처리 및 폐기 SOP가 있습니다.';
  }
  if (text.includes('오답기록표') || text.includes('끝')) {
    return '오답기록표에 "끝"이 적혀있으면 오답노트 제본을 진행하세요.\n오답노트 제본 SOP를 확인하세요.';
  }
  if (text.includes('오답노트') || text.includes('제본')) {
    return '오답노트 제본 SOP를 확인하세요.\n20mm 링 사용, 첫 페이지에 만든날짜+오답노트 기입 후 학생에게 전달합니다.';
  }
  if (text.includes('연습장')) {
    return '연습장 보관함은 항상 5권을 유지해야 합니다.\n연습장 관리 SOP를 확인하세요.';
  }
  if (text.includes('이면지')) {
    return '이면지 보관함은 복테 제출함 아래에 있습니다.\n이면지 보관함 SOP를 확인하세요.';
  }
  if (text.includes('제본기') || text.includes('링')) {
    return '제본기 사용 SOP를 확인하세요.\n12mm: 얇은 자료 / 20mm: 두꺼운 자료. 작업 후 찌꺼기함을 반드시 비우세요.';
  }
  if (text.includes('비품') || text.includes('재고')) {
    return '소모품 재고 관리 SOP를 확인하세요.\n재고 20~30% 남았을 때 미리 원장에게 보고해야 합니다.';
  }
  if (text.includes('출근')) {
    return '출근 루틴 SOP를 확인하세요.\n복테 제출함 확인 → 조교할일 확인 → 연습장 보관함 확인 순서로 진행합니다.';
  }
  if (text.includes('퇴근')) {
    return '퇴근 루틴 SOP를 확인하세요.\n퇴근 30분 전 복테 프린트/저장, 퇴근 직전 주변 정리 및 PC 전원 끄기를 진행합니다.';
  }
  if (text.includes('인수인계')) {
    return '인수인계는 3단계로 진행합니다.\n1단계(모델링) → 2단계(코칭) → 3단계(독립 수행). 종합 가이드북을 참고하세요.';
  }

  // 신규 키워드
  if (text.includes('채점') || text.includes('별표') || text.includes('세모') || text.includes('슬래시')) {
    return '채점 규칙 SOP를 확인하세요.\nO(정답) / /(오답1차) / △(스스로해결) / ☆(질문필요) / ☆위에큰△(질문후해결)';
  }
  if (text.includes('교재검사') || text.includes('교재 검사')) {
    return '교재검사 SOP를 확인하세요.\n개념편과 유형편을 교대로 검사합니다. 덜 완료된 페이지 번호만 목차에 기록하세요.';
  }
  if (text.includes('진단평가') || text.includes('커트라인')) {
    return '진단평가 SOP를 확인하세요.\n1차 커트라인 70점 / 2차 커트라인 50점 기준으로 과제가 다릅니다.';
  }
  if (text.includes('파일명') || text.includes('파일 이름') || text.includes('폴더명')) {
    return '파일명 규칙 SOP를 확인하세요.\nhwp: 날짜+복테+학년+교재+학생이름 / WANT: 날짜+교재+학생이름';
  }
  if (text.includes('첫 출근') || text.includes('처음') || text.includes('온보딩') || text.includes('신규')) {
    return '신규 조교 온보딩 SOP를 확인하세요.\n서류제출 → 성범죄조회 → 이니셜확인 → 조교할일 확인 순서로 진행합니다.';
  }
  if (text.includes('베낌') || text.includes('베끼') || text.includes('의심')) {
    return '베낌 판별 SOP를 확인하세요.\n3초 스캔 → 2초 질문("이 문제 어떻게 풀었어요?") → 5초 확정(재풀이)';
  }
  if (text.includes('학생관리') || text.includes('규율') || text.includes('첨삭') || text.includes('습관')) {
    return '학생관리 SOP를 확인하세요.\n규율(습관잡기) / 첨삭(몰라서못함) / 검사(알지만안함) 3가지 유형으로 구분합니다.';
  }
  if (text.includes('22개정') || text.includes('2022') || text.includes('교육과정')) {
    return '파일명 규칙 SOP를 확인하세요.\n2022는 출판연도, 22개정은 교육과정 개정연도입니다. 복테 제작 시 학생별로 반드시 확인하세요.';
  }
  if (text.includes('프린터') || text.includes('인터넷') || text.includes('오류')) {
    return '인터넷/프린터 오류 SOP를 확인하세요.\n단독 해결 불가 시 원장에게 즉시 보고하세요.';
  }
  if (text.includes('분실') || text.includes('없어') || text.includes('못 찾')) {
    return '학생 자료 분실/누락 SOP를 확인하세요.\n복테 보관함 재확인 → 학생 폴더 확인 → 공유폴더 확인 → 재출력 순서로 진행합니다.';
  }

  return '확인이 필요합니다. SOP 또는 FAQ를 검색해보세요.';
}
```

---

# 작업 완료 후

git add . && git commit -m "feat: FAQ 12개→22개, Dooly 키워드 12개→23개 추가" && git push
