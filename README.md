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

## Máy không có Claude Code (dùng Antigravity)

```powershell
powershell -ExecutionPolicy Bypass -File $env:USERPROFILE\claude-brain\pull-antigravity.ps1
```
Memory được ghi vào một khối trong `~/.gemini/GEMINI.md` (global rules); phần bạn tự viết ngoài khối được giữ nguyên. Skill được chép vào `~/.gemini/config/skills` và `~/.gemini/antigravity/skills`.

## File riêng từng máy

Tạo `%USERPROFILE%\.claude\brain-local.txt`, mỗi dòng một tên file (vd `detective-protagonist.md`).
File có tên trong danh sách sẽ không bị pull ghi đè và không bị push đẩy lên. Mỗi máy giữ bản riêng.
