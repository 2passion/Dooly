# 52Y_Order_Rollback_to_52E_v1.0.md

작성일: 2026-06-30
작업 번호: Task #52-Y (롤백)
작업명: 52-E 상태로 롤백 (출처 태그 복원)
대상 파일: docs/06_Dooly_v1.html, api/gemini.js, docs/api/gemini.js
롤백 목표 커밋: d98cfb9 (52-E 완료 상태)

---

## 롤백 이유

현재 상태(52-F 롤백, 커밋 5281c6e)는 출처 태그가 없음.
52-E(커밋 d98cfb9)는 출처 태그(FAQ Q:, SOP) 정상 표시 + 답변 정상 상태.
52-G에서 출처 번호 수정 시도가 오히려 성능 저하를 일으켰으므로
52-E 상태로 되돌린다.

---

## 작업

```
cd C:\Obsidian\Dooly

git checkout d98cfb9 -- docs/06_Dooly_v1.html
git checkout d98cfb9 -- docs/api/gemini.js
git checkout d98cfb9 -- api/gemini.js

git add docs/06_Dooly_v1.html docs/api/gemini.js api/gemini.js
git commit -m "revert: 52-E(d98cfb9) 상태로 복원 (출처 태그 복원)"
git push
```

---

## 완료 기준

- [ ] git push 완료
- [ ] Vercel 배포 후 테스트
- [ ] 출처 태그 표시 확인 (FAQ Q:, SOP 태그)
- [ ] 답변 정상 출력 확인
- [ ] 속도 정상 확인

---

## END OF ORDER
