# 38_Order_MockFallback_v1.0.md
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

RAG 서버 연결 실패 시 자동으로 Mock 모드로 전환

현재 문제:
```
서버 없을 때
→ "RAG 서버에 연결할 수 없습니다. run_server.bat을 실행해주세요." 출력
→ 대화 종료
```

수정 후:
```
서버 없을 때
→ Mock 모드 자동 전환
→ data.js 기반 FAQ/SOP 내용 답변
→ 답변 하단에 "[Mock 모드]" 표시
```

---

# STEP 1 — 06_Dooly_v1.html sendMessage 함수 수정

## 수정 대상 파일

```
C:\Obsidian\Dooly\04_Runtime\06_Dooly_v1.html
```

## 수정 내용

sendMessage 함수 안의 fetch 실패 처리 부분을 찾아서 교체한다.

### 현재 코드 (찾을 부분)

```javascript
    }).catch(function(err) {
      var loadingEl = document.getElementById(loadingId);
      if (loadingEl) loadingEl.remove();
      addMsg('dooly', 'RAG 서버에 연결할 수 없습니다. run_server.bat을 실행해주세요.');
      saveChatHistory();
    });
```

### 변경 후 코드 (교체할 내용)

```javascript
    }).catch(function(err) {
      var loadingEl = document.getElementById(loadingId);
      if (loadingEl) loadingEl.remove();
      var mockAnswer = mockResponse(text);
      addMsg('dooly', mockAnswer + '\n\n[Mock 모드 — 서버 미연결]');
      saveChatHistory();
    });
```

---

# STEP 2 — 동작 확인

## 서버 없이 파일 직접 열기

```
탐색기에서
C:\Obsidian\Dooly\04_Runtime\06_Dooly_v1.html
더블클릭
```

## 테스트 입력 및 기대 결과

| 입력 | 기대 결과 |
|---|---|
| `복사기 종이 먹었어요` | [FAQ 1] 내용 + [Mock 모드 — 서버 미연결] |
| `연습장 부족해요` | [FAQ 4] 내용 + [Mock 모드 — 서버 미연결] |
| `출근하면 뭐해요` | [SOP-12] 출근 루틴 내용 + [Mock 모드 — 서버 미연결] |
| `오답기록표 끝` | [FAQ 3] or [SOP-5] 내용 + [Mock 모드 — 서버 미연결] |
| `모르는질문` | 확인이 필요합니다 + [Mock 모드 — 서버 미연결] |

## 완료 확인

```
✅ 서버 없이 열었을 때 Mock 답변 나옴
✅ 답변 하단에 [Mock 모드 — 서버 미연결] 표시됨
✅ "RAG 서버에 연결할 수 없습니다" 메시지 사라짐
```

---

# STEP 3 — git 커밋 및 push

```
cd C:\Obsidian\Dooly

git add .
git commit -m "fix: RAG 서버 연결 실패 시 Mock 모드 자동 전환"
git push
```

## 완료 확인

```
✅ git push 완료
```

---

# 전체 작업 완료 조건

```
✅ STEP 1 완료 (sendMessage catch 수정)
✅ STEP 2 완료 (Mock 모드 동작 확인)
✅ STEP 3 완료 (git push)
```

---

# 참고 — 전체 동작 흐름 (수정 후)

```
질문 입력
    │
    ▼
RAG 서버 연결 시도
    │
    ├── 성공 → Ollama 답변 (출처 태그 포함)
    │
    └── 실패 → Mock 모드 자동 전환
              → data.js 키워드 매칭
              → FAQ/SOP 내용 답변
              → [Mock 모드 — 서버 미연결] 표시
```

---

# 다음 작업

39번 → PWA service-worker.js + 아이콘 추가 (192px, 512px)

---

# END OF ORDER
