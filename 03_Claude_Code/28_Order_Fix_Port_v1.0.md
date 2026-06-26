# 28_Order_Fix_Port_v1.0.md
# KING Assistant OS — RAG 서버 포트 8000 → 8001 변경

---

# 문제
localhost:8000 을 다른 앱(SMART)이 사용 중
→ Dooly RAG 서버를 8001 포트로 변경

---

# 수정 대상
C:\Obsidian\Dooly\05_RAG\run_server.bat
C:\Obsidian\Dooly\05_RAG\README_RAG.txt
C:\Obsidian\Dooly\04_Runtime\06_Dooly_v1.html

---

# [수정 1] run_server.bat — 포트 변경

기존:
```bat
python -m uvicorn server:app --host 0.0.0.0 --port 8000
```

변경:
```bat
python -m uvicorn server:app --host 0.0.0.0 --port 8001
```

상단 echo도 변경:
기존:
```bat
echo  URL: http://localhost:8000
```
변경:
```bat
echo  URL: http://localhost:8001
```

---

# [수정 2] README_RAG.txt — 포트 변경

기존:
```
[서버 주소]
로컬: http://localhost:8000
같은 와이파이 스마트폰: http://[PC_IP]:8000
예) http://192.168.0.10:8000
```

변경:
```
[서버 주소]
로컬: http://localhost:8001
같은 와이파이 스마트폰: http://[PC_IP]:8001
예) http://192.168.0.10:8001
```

---

# [수정 3] 06_Dooly_v1.html — RAG_SERVER 주소 변경

기존:
```javascript
  var RAG_SERVER = 'http://localhost:8000';
```

변경:
```javascript
  var RAG_SERVER = 'http://localhost:8001';
```

---

# 작업 완료 후

```
git add . && git commit -m "fix: change RAG server port 8000 -> 8001" && git push
```
