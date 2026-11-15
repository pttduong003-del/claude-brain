---
name: final-logic-gate
description: Drama AI Studio — chống lỗi logic kịch bản bằng cách siết kiểm tra Story Bible ở bước phân tích
metadata: 
  node_type: memory
  type: project
  originSessionId: 5c558d3c-b09a-4a88-9850-e329a9f5c402
  modified: 2026-08-03T02:07:40.253Z
---

Trong Drama AI Studio (app/api/studio/route.ts), lỗi logic toàn cục của kịch bản (timeline/knowledge/ending) thường bắt nguồn từ **Story Bible tự mâu thuẫn** hoặc bản viết drift khỏi dàn bài. Ràng buộc kiến trúc cứng (test `tests/targeted-repair.test.mjs` cấm `repairStoryLogic(` trong route): **bước cuối chỉ được vá cục bộ nhỏ, cấm viết lại toàn văn** — để tránh "lan man". Hệ quả: vá cục bộ KHÔNG sửa nổi mâu thuẫn logic toàn cục → nếu cổng cuối chặn cứng trên các lỗi đó sẽ deadlock (422, không xuất được gì).

Quyết định của chủ dự án (2026-08-02): **chặn từ gốc — siết kiểm tra Story Bible**, không best-effort-export, không siết cổng cuối.

Cách đã làm:
- `lib/story-logic.ts` `inspectStoryPlanContinuity`: thêm 3 kiểm tra deterministic — (1) knownBy trỏ nhân vật không tồn tại (knowledge), (2) `changesAt` < `introducedAt` = dữ kiện đổi trước khi giới thiệu (timeline), (3) twist không tăng dần vị trí. Helper `sceneRef`/`leadingNumber`.
- `lib/logic-audit.ts` `auditStoryPlanLogic`: audit ngữ nghĩa dàn bài bằng DeepSeek (timeline/knowledge/ending/twist), lọc qua `usableLogicIssues`, **fail-safe** (`catch{return[]}`).
- `app/api/studio/route.ts` (action analyze): nếu deterministic sạch thì chạy `auditStoryPlanLogic`; kết quả chỉ tạo **áp lực xây lại 1 lần**. Cổng chặn cứng cuối cùng vẫn là `storyPlanIssues` (deterministic) → audit LLM không thể tự gây lỗi cứng/kẹt bước phân tích.

Bug đã sửa (2026-08-02, đợt 2): `targetFixed` ở cả `finalizeWithGPTReview` và `applyRepairTransaction` từng dùng `isSameLogicIssue` (so lỏng: cùng category + trùng 2 từ như tên nhân vật). Trong drama ít nhân vật, miếng vá đã sửa đúng lỗi mục tiêu nhưng nếu còn một lỗi KHÁC cùng loại (trùng tên nhân vật) thì bị gom chung → `targetFixed=false` → rollback oan → 422 "stableErrorId mục tiêu vẫn còn". Đã đổi sang so **đúng stableErrorId** (`found.stableErrorId||stableLogicErrorId(found)`), khớp với tên thông báo; lỗi liên quan khác giờ trôi sang vòng sau thay vì chặn cứng.

Bug đã sửa (2026-08-02, đợt 3): `applyTargetedPatches` (lib/targeted-repair.ts) từ chối cứng miếng vá có `find`<20 ký tự → 422 "thiếu đoạn neo đủ dài" khi model sửa lỗi trả neo ngắn. Đã thêm `growAnchor`: nếu neo ngắn nhưng xuất hiện đúng 1 lần, tự nới hai bên cho đủ ≥20 ký tự và thêm đúng phần nới vào `replace` (thay đổi văn bản y hệt). Neo ngắn trùng nhiều chỗ vẫn báo lỗi (không nới an toàn được). Fix tập trung nên phủ mọi đường vá (repairReportedError, repairFinalIssueWithOpenAI/DeepSeek).

Bug đã sửa (2026-08-02, đợt 4): `patchSemanticDrift` cấm sửa vùng hook (220 ký tự đầu) / ending (700 ký tự cuối) trừ khi lỗi "thuộc về" hook/ending. Ở cổng cuối, `finalizeWithGPTReview` chỉ truyền `issue.category` (một từ) → lỗi ending phân loại `causality`/`timeline` bị cấm sửa đoạn kết → rollback "semantic drift". Đã: (1) truyền thêm `issue.location+evidence+conflictWith+requiredFix` vào `patchSemanticDrift` ở cổng cuối; (2) nới regex `allowsHook`/`allowsEnding` thêm 冒頭/序盤/最後/終わり/ラスト/mở đầu/đoạn kết/cảnh cuối…

Van an toàn (2026-08-02, đợt 5 — chủ dự án CHỌN sau khi kẹt 422 nhiều lần): `finalizeWithGPTReview` giờ trả `{text,residual:FinalReviewIssue[]}` thay vì throw cứng. Trong vòng lặp, nếu một lỗi KHÔNG vá được cục bộ: nếu là lỗi bắt buộc (`MUST_FIX_FINAL`={youtube-safety,architecture,duration,hook}) thì vẫn throw 422; nếu là lỗi LOGIC thì đánh dấu `unfixableLogic` và bỏ qua (chọn lỗi kế bằng `find(!unfixableLogic.has(id))`). Sau 5 vòng: nếu chỉ còn lỗi logic → xuất bản tốt nhất + trả `residual`; route đưa vào `emit done {warnings:residualWarnings(...)}`; page.tsx ghi mỗi warning vào Nhật ký lỗi (nút "AI vá đúng đoạn này") + notice ok:false. An toàn/kiến trúc/thời lượng VẪN bắt buộc đạt (cổng ngoài route + MUST_FIX_FINAL). → Luôn có đầu ra; lỗi logic không sửa được cục bộ được báo minh bạch thay vì kẹt.

Ghi chú: các lỗi 422 của user xuất hiện theo tầng, sửa xong tầng này lộ tầng sau — thứ tự đã gặp: hồi quy (asymmetry, đã revert) → targetFixed lỏng → thiếu neo → semantic drift oan → (giới hạn thật: vá cục bộ không sửa nổi) → van an toàn. Mỗi lần user gửi lỗi 422 mới, đọc kỹ message để biết tầng nào.

**Đã hoàn nguyên (đừng làm lại):** từng thử (a) siết cổng cuối `finalizeWithGPTReview` bằng `beforeGuard.audit.issues` → gây deadlock; (b) leo thang `repairStoryLogic` toàn văn → vi phạm test guardrail + tái tạo "lan man". Cả hai đã revert. Bộ lọc lỗi logic: [[.]] `usableLogicIssues` trong lib/logic-audit.ts. Test: `node --test --experimental-strip-types tests/*.test.mjs` (95 test).
