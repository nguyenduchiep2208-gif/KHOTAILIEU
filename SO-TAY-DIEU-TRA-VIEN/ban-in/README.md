# Bản in Sổ tay Điều tra viên

Thư mục này chứa bản dùng để in của Sổ tay Điều tra viên, trình bày theo thể thức văn bản hành chính quy định tại Nghị định số 30/2020/NĐ-CP ngày 05/3/2020 của Chính phủ về công tác văn thư.

| Tệp | Dung lượng | Dùng khi nào |
|---|---|---|
| [`SO TAY DIEU TRA VIEN.docx`](SO%20TAY%20DIEU%20TRA%20VIEN.docx) | 361 KB | Cần chỉnh sửa, thêm bớt nội dung, chèn con dấu hoặc chữ ký trước khi in |
| [`SO TAY DIEU TRA VIEN.pdf`](SO%20TAY%20DIEU%20TRA%20VIEN.pdf) | 6,1 MB | In ngay, giữ nguyên trình bày trên mọi máy |

## Thông số trình bày

| Tiêu chí | Thông số đã áp dụng |
|---|---|
| Khổ giấy | A4 (210 mm × 297 mm) |
| Lề trang | Trái 3 cm, phải 2 cm, trên 2 cm, dưới 2 cm |
| Phông chữ | Times New Roman, cỡ 14 cho phần nội dung |
| Giãn dòng | 1,15 dòng |
| Lùi đầu dòng | 1 cm |
| Căn lề | Đều hai bên |
| Số trang | Đặt giữa theo chiều ngang, trên lề trên, không hiển thị ở trang đầu |
| Tiêu đề phần | In đậm, màu đen, mỗi phần bắt đầu ở một trang mới |
| Bảng biểu | Có đường kẻ đầy đủ, chữ cỡ 11, dòng tiêu đề in đậm và lặp lại khi bảng sang trang |
| Sơ đồ | Phông Courier New cỡ 9 để giữ đúng khung và đường nối |
| Tổng số trang | 381 trang |
| Mục lục | 328 dòng, có số trang thật |

## Lưu ý khi in

1. Mục lục là mục lục tĩnh, số trang đã được tính sẵn. Nếu sửa nội dung bản Word thì số trang trong mục lục không tự cập nhật; khi đó cần dựng lại bằng `scripts/word/build.sh` hoặc sửa tay.
2. Các sơ đồ ở Phụ lục F dùng ký tự khung, cần phông **Courier New** để hiển thị đúng. Phông này có sẵn trên Windows và trong bộ Microsoft Office. Nếu máy in hoặc máy tính không có Courier New, hãy in từ bản PDF.
3. Tài liệu in hai mặt được; mỗi phần đã bắt đầu ở một trang mới nên không bị dính phần.
4. Bản PDF đã nhúng sẵn phông chữ nên in đúng trên mọi máy, kể cả máy không cài Times New Roman.

## Dựng lại bản in

Nguồn của bản in là 29 tệp Markdown trong thư mục `SO-TAY-DIEU-TRA-VIEN`, cộng phần mở đầu lấy từ `README.md` của sổ tay. Sau khi sửa nội dung, chạy:

```bash
scripts/word/build.sh
```

Dây chuyền gồm bảy bước: tạo tệp mẫu định dạng, ghép bản thảo, chuyển sang Word, dựng mục lục lượt một, dò số trang thật từ bản PDF, dựng lại mục lục lượt hai, chuẩn hóa OOXML cho Microsoft Word. Kết quả được chép vào chính thư mục này.

Yêu cầu công cụ: `pandoc`, `python3` kèm `python-docx`, `libreoffice`, `poppler-utils`.
