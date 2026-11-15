---
name: deepseek-only
description: Drama AI Studio đã bỏ hoàn toàn OpenAI — DeepSeek đảm nhiệm viết + kiểm duyệt cuối + vá lỗi
metadata: 
  node_type: memory
  type: project
  originSessionId: 5c558d3c-b09a-4a88-9850-e329a9f5c402
  modified: 2026-08-02T11:58:16.677Z
---

Theo yêu cầu chủ dự án (2026-08-02), Drama AI Studio **bỏ toàn bộ OpenAI, chỉ dùng DeepSeek** (lý do: lỗi HTTP 429 khi fallback gọi OpenAI). Khả thi vì lib đã có sẵn hàm DeepSeek tương đương.

Đã sửa (app/api/studio/route.ts):
- `finalizeWithGPTReview`: bỏ param `openAIKey` và yêu cầu OpenAI; `auditFinal`/`repairFinal` luôn dùng `auditFinalWithDeepSeek`/`repairFinalIssueWithDeepSeek`; `providerName` = "DeepSeek kiểm duyệt cuối". (Tên hàm vẫn giữ `finalizeWithGPTReview` và biến `allGPTFindings`/`gptRegressions` vì test khóa chuỗi — đừng đổi.)
- `repairReportedError`, `applyRepairTransaction`, `stabilizeRepairedScript`: bỏ param `openAIKey`; `repairReportedError` bỏ khối fallback `askOpenAI`, DeepSeek thất bại thì throw luôn.
- POST: bỏ gate `MISSING_OPENAI_KEY`; GET health chỉ trả `ready`. Bỏ import từ `@/lib/openai` và các hàm OpenAI của `@/lib/openai-review`. Nhãn stage "GPT…" → "cổng kiểm duyệt cuối".
- app/page.tsx: bỏ state/UI OpenAI (openAIKey/openAIReady, ô nhập OpenAI trong modal, header x-openai-key, đọc openAIReady). Chỉ cần một DeepSeek key.
- Tests: `openai-review.test.mjs` và `targeted-repair.test.mjs` đổi từ "bắt buộc OpenAI" sang "DeepSeek-only" (doesNotMatch askOpenAI/openAIKeyFrom/MISSING_OPENAI…).

Còn lại (cố ý, vô hại): lib/openai.ts và các hàm OpenAI trong lib/openai-review.ts vẫn tồn tại (code chết, không được route gọi) — vì openai.test.mjs / openai-review.test.mjs vẫn test trực tiếp chúng. Nếu muốn dọn hẳn thì phải xóa cả các test đó. Test: 97 pass.
