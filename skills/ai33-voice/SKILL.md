---
name: ai33-voice
description: Biến kịch bản thành giọng đọc qua API AI33 (ai33.pro). Phân tích ngữ cảnh, tự chèn tag cảm xúc/nhấn nhá/trầm/cao/ngắt nghỉ, cho người dùng duyệt, rồi gọi API tạo mp3. Dùng khi người dùng dán kịch bản và muốn "tạo giọng đọc", "đọc kịch bản", "lồng tiếng", "voice ai33", "/ai33-voice".
---

# AI33 Voice

Kịch bản thô → kịch bản gắn tag → duyệt → mp3 + srt.

Script: `~/.claude/skills/ai33-voice/ai33_tts.py` (chỉ dùng thư viện chuẩn Python). API key lấy từ biến môi trường `AI33_API_KEY`, hoặc file `AI33_KEY.txt` trong thư mục đang chạy lệnh (repo ai-animation-director đã có sẵn). Không bao giờ in key ra, ghi key vào file hay hỏi key trong chat. Nếu thiếu key, bảo người dùng tự đặt biến môi trường rồi mở lại terminal:

```
setx AI33_API_KEY "<key>"
```

## Quy trình

1. **Nhận kịch bản.** Từ đoạn dán hoặc file. Lưu nguyên văn vào `<ten>.txt` trong thư mục hiện tại.
2. **Chọn giọng.** Kịch bản tiếng Nhật: narrator chính mặc định là `Akio shima - Rich, Deep Japanese Actor` (`elevenlabs_BSPow8LcoXJ0UVg1ws3x`), không cần hỏi. Ngôn ngữ khác: hỏi `voice_id` nếu người dùng chưa đưa. Tìm giọng:
   `python ~/.claude/skills/ai33-voice/ai33_tts.py voices --provider elevenlabs --language Japanese`
   Ưu tiên giọng `elevenlabs_*`: script tự gửi `model_id=eleven_v3`, tag cảm xúc có tác dụng thật.
   Giọng `clone_*` (ví dụ `masane`) chạy MiniMax trên AI33: đã thử 2026-11, tag, `emotion`, `pitch` đều bị bỏ qua, chỉ còn tốc độ và ngắt `<#0.6#>`. Chỉ dùng khi người dùng yêu cầu giọng clone, và báo trước là sẽ đọc đều, ít cảm xúc.
3. **Phân tích ngữ cảnh.** Xác định: thể loại, người nghe, mạch cảm xúc từng đoạn, cao trào, chỗ chuyển ý. Ghi tóm tắt 3–5 dòng cho người dùng.
4. **Chèn tag** theo luật bên dưới. Ghi ra `<ten>.tagged.txt`.
5. **Kiểm tra:** `python ~/.claude/skills/ai33-voice/ai33_tts.py check <ten>.tagged.txt --voice <voice_id>`. Sửa đến khi không còn lỗi.
6. **Cho duyệt.** Hiện bản đã gắn tag (hoặc các đoạn có tag nếu dài) và số lượng tag. Tạo giọng tốn credit, nên chờ người dùng đồng ý rồi mới làm bước 7.
7. **Tạo giọng:**
   `python ~/.claude/skills/ai33-voice/ai33_tts.py tts <ten>.tagged.txt --voice <voice_id> --out audio`
   Chạy nền nếu kịch bản dài. Báo đường dẫn mp3/srt và `credit_cost`.
   Tag trong SRT bị lọc tự động, phụ đề chỉ còn lời đọc.
   **Trong repo ai-animation-director** (có thư mục `DAU_VAO/`): xuất thẳng vào inbox để làm video, giữ `<ten>.tagged.txt` ở ngoài thư mục đó:
   `python ~/.claude/skills/ai33-voice/ai33_tts.py tts <ten>.tagged.txt --voice <voice_id> --out DAU_VAO/<ten> --script <ten>.txt`
   Ra `DAU_VAO/<ten>/<ten>.mp3`, `<ten>.srt`, `<ten>.txt`. Bước tiếp: `py -3.11 scripts/make_video.py setup --project du-an/<ten>`.

## Luật chèn tag (eleven_v3, giọng `elevenlabs_*`)

Không đổi, thêm hay bớt chữ nào của kịch bản. Chỉ chèn tag, và được thêm `…` để tạo ngắt.

Tag v3 là chữ tiếng Anh tự do, 1–3 từ, trong ngoặc vuông. Dùng các tag đã quen thuộc với v3:

| Nhóm | Tag | Khi nào |
|---|---|---|
| Cảm xúc | `[curious]` `[thoughtful]` `[sad]` `[happy]` `[excited]` `[nervous]` `[angry]` `[surprised]` `[sarcastic]` `[calm]` | Đầu câu/đoạn mà cảm xúc đổi |
| Cách nói | `[whispers]` `[quietly]` `[softly]` `[shouts]` `[slowly]` `[dramatically]` | Thì thầm, nói nhỏ, nhấn mạnh câu chốt |
| Phản ứng | `[sighs]` `[exhales]` `[laughs]` `[chuckles]` `[clears throat]` `[gulps]` | Tiếng thở dài, cười, hắng giọng. Chỉ khi ngữ cảnh gợi ý |
| Ngắt | `…` hoặc `……` (không phải tag) | Trước câu tiết lộ, sau câu hỏi tu từ, chuyển ý |

Không dùng (vô tác dụng trên v3, `check` sẽ báo lỗi): `[pause]` `[long_pause]` `[speed_*]` `[pitch_*]` `[expressive_*]` `<break .../>`.

Mật độ và vị trí:
- Trung bình tối đa 1 tag cho mỗi 1–2 câu. Đoạn tường thuật đều có thể không có tag. Dư tag làm giọng giả.
- Tag đặt ngay trước cụm từ nó tác động, cách chữ sau 1 dấu cách: `[whispers] あの人は私を認めていない`.
- Được ghép tối đa 2 tag liền nhau: `[sad][slowly] Bà đã đi rồi.`
- Không lặp cùng một tag cảm xúc ở các câu liên tiếp.
- Dấu câu sẵn có đã tạo ngắt tự nhiên. Chỉ thêm `…` ở chỗ cần ngắt dài hơn.

Theo thể loại (mặc định, người dùng có thể đổi):
- Truyện kể/kinh dị/noir: `[quietly]`, `[whispers]`, `[sighs]`, `…` trước tình tiết.
- Quảng cáo/review: `[excited]`, `[happy]`, ít ngắt.
- Tin tức/giáo dục: rất ít tag. `[calm]`, `[thoughtful]` ở ý chính.
- Tâm sự/triết lý/tâm lý: `[thoughtful]`, `[softly]`, `[sighs]`, `[curious]` ở câu hỏi, `……` sau câu đắt.

Giọng không phải ElevenLabs (`minimax`, `vbee`, `fishaudio`): dùng bộ tag cũ của app AI33 (`[pitch_low]`, `[pause]`, `<break time="0.7s"/>`…), `check --voice <id>` sẽ kiểm theo bộ đó.

## Lưu ý

- Lần đầu dùng một giọng, nên tạo thử 1 đoạn ngắn (~150 ký tự, ~200 credit) để nghe tag có tác dụng không.
- Chi phí đo được: ~1,3 credit/ký tự tiếng Nhật (155 ký tự = 195 credit, gồm phí SRT).
- Kịch bản rất dài trên eleven_v3 chưa thử. Nếu lỗi độ dài, chia `<ten>.tagged.txt` theo đoạn, tạo từng phần rồi ghép.
- `speed` (tham số cả bài) từ 0.5 đến 1.5. AI33 áp bằng kéo giãn audio sau khi tạo.
- Tải lại task đã xong (không tốn credit): thêm `--task <task_id>`.
- Lỗi HTTP: báo nguyên văn cho người dùng, không tự thử lại liên tục (mỗi lần tốn credit).
