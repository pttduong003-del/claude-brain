# claude-brain

Memory, skills, hooks và settings của Claude Code, đồng bộ giữa các máy.

## Máy mới (một lần)

```powershell
git clone <URL repo> $env:USERPROFILE\claude-brain
powershell -ExecutionPolicy Bypass -File $env:USERPROFILE\claude-brain\pull.ps1
```

## Cập nhật hằng ngày

- Máy vừa thay đổi bộ não: `powershell -ExecutionPolicy Bypass -File $env:USERPROFILE\claude-brain\push.ps1`
- Máy khác nhận bản mới: `powershell -ExecutionPolicy Bypass -File $env:USERPROFILE\claude-brain\pull.ps1`

## Lưu ý

- API key (AI33_API_KEY, AI33_KEY.txt) KHÔNG nằm trong repo. Mỗi máy tự đặt.
- Memory gắn với đường dẫn project tính từ thư mục user (vd `Desktop\ai-animation-director`). Máy khác phải để project ở cùng vị trí tương đối đó.
- pull.ps1 ghi đè settings.json của máy nhận.
