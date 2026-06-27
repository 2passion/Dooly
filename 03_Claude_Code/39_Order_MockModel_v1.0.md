# 39_Order_MockModel_v1.0.md
# King Assistant OS v1.0
# Claude Code 작업지시서

Version: v1.0
Date: 2026-06-27

---

# 작업 시작 전 필수 확인

아래 파일을 읽어라.

```
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md
C:\Obsidian\Dooly\04_Runtime\06_Dooly_v1.html
```

---

# 작업 목표

모델 드롭다운에 Mock 옵션 추가 + 기본값으로 설정

현재 문제:
```
RAG 서버 모드가 기본값
→ "복사기 종이 먹었어요" 질문에 복테 관련 답변 출력
→ RAG 검색 품질이 낮아 엉뚱한 답변 발생
```

수정 후:
```
Mock 모드가 기본값
→ data.js 키워드 매칭으로 정확한 FAQ/SOP 답변
→ 서버 불필요, 오프라인 동작
→ RAG는 드롭다운에서 수동 선택 시만 사용
```

---

# STEP 1 — 드롭다운에 Mock 옵션 추가 + 기본값 설정

## 수정 대상 파일

```
C:\Obsidian\Dooly\04_Runtime\06_Dooly_v1.html
```

## 현재 코드 (찾을 부분)

```html
  <select class="model-select" id="modelSelect">
    <option value="qwen2.5:7b">모델 A — qwen2.5:7b (고품질)</option>
    <option value="qwen2.5:3b">모델 B — qwen2.5:3b (빠름)</option>
    <option value="gemma3:4b">모델 C — gemma3:4b (균형)</option>
  </select>
```

## 변경 후 코드

```html
  <select class="model-select" id="modelSelect">
    <option value="mock" selected>Mock — 오프라인 모드 (기본)</option>
    <option value="qwen2.5:7b">모델 A — qwen2.5:7b (고품질)</option>
    <option value="qwen2.5:3b">모델 B — qwen2.5:3b (빠름)</option>
    <option value="gemma3:4b">모델 C — gemma3:4b (균형)</option>
  </select>
```

---

# STEP 2 — sendMessage 함수에 Mock 모드 분기 추가

Mock 모델 선택 시 서버 호출 없이 바로 mockResponse 실행하도록 수정한다.

## 수정 대상

sendMessage 함수 안에서 fetch 호출 직전 부분을 찾아서 아래와 같이 수정한다.

## 현재 코드 (찾을 부분)

```javascript
    var model = document.getElementById('modelSelect').value;
```

이 줄 바로 아래에 아래 코드를 추가한다:

## 추가할 코드

```javascript
    // Mock 모드: 서버 호출 없이 즉시 답변
    if (model === 'mock') {
      var loadingEl2 = document.getElementById(loadingId);
      if (loadingEl2) loadingEl2.remove();
      var mockAns = mockResponse(text);
      addMsg('dooly', mockAns + '\n\n[Mock 모드]');
      saveChatHistory();
      return;
    }
```

## 완료 확인

```
✅ 드롭다운에 "Mock — 오프라인 모드 (기본)" 옵션 추가됨
✅ Mock이 selected (기본값)으로 설정됨
✅ Mock 선택 시 서버 호출 없이 즉시 답변
✅ 모델 A/B/C 선택 시 기존 RAG 서버 방식 유지
```

---

# STEP 3 — 테스트

## Mock 모드 테스트 (서버 없이)

```
브라우저에서 http://localhost:8001/app/06_Dooly_v1.html

드롭다운: Mock — 오프라인 모드 (기본) 확인
```

| 입력 | 기대 결과 |
|---|---|
| `복사기 종이 먹었어요` | [FAQ 1] 정확한 내용 + [Mock 모드] |
| `연습장 부족해요` | [FAQ 4] 정확한 내용 + [Mock 모드] |
| `출근하면 뭐해요` | [SOP-12] 출근 루틴 내용 + [Mock 모드] |
| `모르는질문` | 확인이 필요합니다 + [Mock 모드] |

## RAG 모드 테스트 (서버 켜져 있을 때)

```
드롭다운에서 모델 A 선택
→ "복사기 종이 먹었어요" 입력
→ RAG 서버 답변 확인
```

---

# STEP 4 — git 커밋 및 push

```
cd C:\Obsidian\Dooly

git add .
git commit -m "feat: Mock 모델 옵션 추가 + 기본값 설정 (오프라인 모드)"
git push
```

## 완료 확인

```
✅ git push 완료
```

---

# 전체 작업 완료 조건

```
✅ STEP 1 완료 (Mock 드롭다운 옵션 추가 + 기본값)
✅ STEP 2 완료 (Mock 모드 즉시 답변 분기 추가)
✅ STEP 3 완료 (Mock 모드 답변 정상 확인)
✅ STEP 4 완료 (git push)
```

---

# 참고 — 전체 동작 흐름 (수정 후)

```
드롭다운 선택
    │
    ├── Mock (기본값)
    │   → 서버 호출 없음
    │   → data.js 키워드 매칭
    │   → 정확한 FAQ/SOP 답변 즉시 출력
    │   → [Mock 모드] 표시
    │
    └── 모델 A/B/C
        → RAG 서버 호출
        → Ollama 답변 생성
        → 출처 태그 표시
        → 서버 실패 시 Mock 자동 전환
```

---

# 다음 작업

40번 → PWA service-worker.js + 아이콘 추가 (192px, 512px)

---

# END OF ORDER
