# Bản in tài liệu "Tội phạm trong lĩnh vực đấu thầu"

Thư mục này chứa bản dùng để in của tài liệu chuyên sâu "Tội phạm trong lĩnh vực đấu thầu", trình bày theo thể thức văn bản hành chính quy định tại Nghị định số 30/2020/NĐ-CP ngày 05/3/2020 của Chính phủ về công tác văn thư.

| Tệp | Dung lượng | Dùng khi nào |
|---|---|---|
| [`TOI PHAM DAU THAU.docx`](TOI%20PHAM%20DAU%20THAU.docx) | 247 KB | Cần chỉnh sửa, thêm bớt nội dung, trích một phần để làm tài liệu bồi dưỡng, chèn con dấu hoặc chữ ký trước khi in |
| [`TOI PHAM DAU THAU.pdf`](TOI%20PHAM%20DAU%20THAU.pdf) | 3,8 MB | In ngay, giữ nguyên trình bày trên mọi máy |

## Thông số trình bày

| Tiêu chí | Thông số đã áp dụng |
|---|---|
| Khổ giấy | A4 (210 mm × 297 mm) |
| Lề trang | Trái 3 cm, phải 2 cm, trên 2 cm, dưới 2 cm |
| Phông chữ | Times New Roman cho toàn bộ nội dung và tiêu đề; cỡ 14 cho phần nội dung |
| Giãn dòng | 1,15 dòng |
| Lùi đầu dòng | 1 cm |
| Căn lề | Đều hai bên |
| Số trang | Đặt giữa theo chiều ngang, trên lề trên, không hiển thị ở trang đầu |
| Tiêu đề chương | In đậm, màu đen, mỗi chương bắt đầu ở một trang mới |
| Trang ngăn cách | Mỗi phần lớn (Phần thứ nhất, Phần thứ hai, Phần thứ ba) có một trang ngăn cách riêng |
| Bảng biểu | Có đường kẻ đầy đủ, chữ cỡ 11, dòng tiêu đề in đậm và lặp lại khi bảng sang trang |
| Sơ đồ | Phông Courier New cỡ 9 để giữ đúng khung và đường nối |
| Tổng số trang | 242 trang |
| Mục lục | 256 dòng, có số trang thật, đã đối chiếu khớp với bản PDF |

## Cấu trúc bản in

1. Trang bìa.
2. Mục lục.
3. Lời nói đầu, cảnh báo sử dụng, quy ước trình bày và tra cứu nhanh.
4. Chương mở đầu: hướng dẫn sử dụng tài liệu.
5. Phần thứ nhất (Chương 1 đến Chương 7): nhận thức chung về đấu thầu và tội phạm trong lĩnh vực đấu thầu.
6. Phần thứ hai (Chương 8 đến Chương 16): những vấn đề cần chú ý trong đấu tranh theo từng lĩnh vực.
7. Phần thứ ba (Chương 17): phòng ngừa và kiến nghị.
8. Phụ lục A đến G.

## Lưu ý khi in

1. Mục lục là mục lục tĩnh, số trang đã được tính sẵn. Nếu sửa nội dung bản Word thì số trang trong mục lục không tự cập nhật; khi đó cần dựng lại bằng `scripts/word/build.sh TOI-PHAM-DAU-THAU` hoặc sửa tay.
2. Các sơ đồ dùng ký tự khung, cần phông **Courier New** để hiển thị đúng. Nếu máy in hoặc máy tính không có phông này, hãy in từ bản PDF.
3. Một số mẫu bảng ở Phụ lục D có nhiều cột; khi sử dụng thực tế có thể chép sang Word hoặc bảng tính và đổi sang khổ ngang.
4. Bản PDF đã nhúng sẵn phông chữ (phông tương thích kích thước với Times New Roman) nên in đúng trên mọi máy.

## Dựng lại bản in

Nguồn của bản in là các tệp Markdown trong thư mục `TOI-PHAM-DAU-THAU`, cộng phần mở đầu lấy từ `README.md` của tài liệu. Sau khi sửa nội dung, chạy:

```bash
scripts/word/build.sh TOI-PHAM-DAU-THAU
```

Dây chuyền gồm các bước: tạo tệp mẫu định dạng, ghép bản thảo (có chèn trang ngăn cách giữa các phần), chuyển sang Word, dựng mục lục với số trang tạm, dò số trang thật từ bản PDF, dựng lại mục lục và lặp đến khi số trang khớp, chuẩn hóa OOXML cho Microsoft Word. Kết quả được chép vào chính thư mục này.

Yêu cầu công cụ: `pandoc`, `python3` kèm `python-docx`, `libreoffice`, `poppler-utils`.
