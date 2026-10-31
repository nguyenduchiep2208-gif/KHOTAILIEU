#!/usr/bin/env python3
"""Cau hinh cac bo tai lieu trong kho, dung chung cho ban HTML va ban in.

Chon bo tai lieu bang bien moi truong BO (mac dinh: SO-TAY-DIEU-TRA-VIEN).
Script bash doc mot gia tri cau hinh bang lenh:
    python3 -I scripts/bo_tai_lieu.py <BO> <khoa>
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAC_DINH = "SO-TAY-DIEU-TRA-VIEN"

CAU_HINH = {
    # ------------------------------------------------------------------
    "SO-TAY-DIEU-TRA-VIEN": {
        "ten_tep": "SO TAY DIEU TRA VIEN",
        "meta": "meta.yaml",
        # Trang ngan cach chen truoc tep co tien to tuong ung trong ban in
        "ngan_cach": [],
        "html": {
            "title": "Sổ tay Điều tra viên",
            "description": "Sổ tay Điều tra viên: {n_pages} phần và phụ lục, {n_sec} mục tra cứu, "
                           "cập nhật pháp luật tố tụng hình sự đến ngày 28/10/2026.",
            "h1": "Sổ tay Điều tra viên",
            "sub": "Tài liệu nghiệp vụ tra cứu, áp dụng pháp luật tố tụng hình sự",
            "badges": ["Phiên bản 1.0", "Biên soạn 28/10/2026", "Cập nhật pháp luật đến 28/10/2026",
                       "23 phần và 6 phụ lục", "{n_sec} mục tra cứu"],
            "warn": (
                "    <b>Cảnh báo sử dụng.</b> Đây là tài liệu tham khảo nghiệp vụ, không phải văn bản\n"
                "    quy phạm pháp luật và không thay thế văn bản quy phạm pháp luật. Trước khi ban hành\n"
                "    bất kỳ quyết định tố tụng nào, phải đối chiếu văn bản gốc trên Công báo hoặc Cơ sở\n"
                "    dữ liệu quốc gia về pháp luật và kiểm tra tình trạng hiệu lực. Các nội dung đánh dấu\n"
                "    <span class=\"tag tag-check\">CẦN ĐỐI CHIẾU</span> là nội dung bắt buộc phải kiểm tra lại\n"
                "    văn bản gốc trước khi áp dụng."
            ),
            "placeholder": "Tra cứu theo mục, ví dụ: thời hạn tạm giam, khám xét, kê biên, "
                           "tài sản mã hóa, xử lý chuyển hướng",
            "footer": (
                "    Tài liệu được biên soạn và lưu trữ phục vụ công tác nghiên cứu, tra cứu nghiệp vụ cá nhân.\n"
                "    Bản Markdown gốc nằm cùng thư mục để đọc trực tiếp trên GitHub."
            ),
            "groups": [
                ("Phần mở đầu", ["00"]),
                ("Khối A. Nền tảng pháp lý và tổ chức", ["01", "02", "03", "04"]),
                ("Khối B. Quy trình tố tụng", ["05", "06", "07", "08", "09", "10", "11", "12", "13"]),
                ("Khối C. Chuyên đề điều tra", ["14", "15", "16", "17", "18"]),
                ("Khối D. Kỹ năng và kỷ luật nghiệp vụ", ["19", "20", "21", "22"]),
                ("Phụ lục tra cứu", ["PL"]),
            ],
            "quick": [
                ("Vừa tiếp nhận tin báo, chưa rõ thẩm quyền", "05-tiep-nhan-giai-quyet-nguon-tin.html"),
                ("Sắp hết thời hạn, cần tra mốc gia hạn", "phu-luc/PL-A-bang-tra-cuu-thoi-han.html"),
                ("Việc phải làm trong 24 giờ đầu", "phu-luc/PL-C-checklist-tac-nghiep.html"),
                ("Cần giữ người trong trường hợp khẩn cấp", "07-bien-phap-ngan-chan.html"),
                ("Chuẩn bị khởi tố bị can", "06-khoi-to-vu-an-khoi-to-bi-can.html"),
                ("Cần tạm giam, tra căn cứ Điều 119", "07-bien-phap-ngan-chan.html"),
                ("Cần khám xét, tra thành phần bắt buộc", "09-cac-hoat-dong-dieu-tra.html"),
                ("Cần phong tỏa tài khoản, kê biên tài sản", "08-bien-phap-cuong-che-ke-bien-phong-toa.html"),
                ("Thu giữ điện thoại, máy tính, dữ liệu", "15-chuyen-de-chung-cu-dien-tu-tai-san-so.html"),
                ("Phát hiện ví tài sản mã hóa", "15-chuyen-de-chung-cu-dien-tu-tai-san-so.html"),
                ("Cần trưng cầu giám định, yêu cầu định giá", "11-giam-dinh-dinh-gia.html"),
                ("Bị can là người dưới 18 tuổi", "17-chuyen-de-nguoi-chua-thanh-nien.html"),
                ("Doanh nghiệp có dấu hiệu phạm tội", "16-chuyen-de-phap-nhan-thuong-mai.html"),
                ("Tài sản, đối tượng ở nước ngoài", "18-thu-hoi-tai-san-hop-tac-quoc-te.html"),
                ("Chuẩn bị kết thúc điều tra", "12-ket-thuc-dieu-tra.html"),
                ("Viện kiểm sát trả hồ sơ điều tra bổ sung", "21-sai-sot-thuong-gap-phong-ngua.html"),
                ("Bị can kêu oan, tố cáo bức cung", "22-dao-duc-nghe-nghiep-trach-nhiem-phap-ly.html"),
                ("Tra văn bản đã bị thay thế", "phu-luc/PL-D-danh-muc-van-ban-phap-luat.html"),
                ("Tra biểu mẫu theo giai đoạn", "phu-luc/PL-B-danh-muc-bieu-mau.html"),
                ("Xem sơ đồ quy trình tố tụng", "phu-luc/PL-F-so-do-quy-trinh.html"),
            ],
        },
    },
    # ------------------------------------------------------------------
    "TOI-PHAM-DAU-THAU": {
        "ten_tep": "TOI PHAM DAU THAU",
        "meta": "meta-toi-pham-dau-thau.yaml",
        "ngan_cach": [
            ("01", "PHẦN THỨ NHẤT. NHẬN THỨC CHUNG VỀ ĐẤU THẦU VÀ TỘI PHẠM TRONG LĨNH VỰC ĐẤU THẦU",
             "Gồm Chương 1 đến Chương 7: tổng quan về đấu thầu; hệ thống pháp luật; quy trình lựa chọn "
             "nhà thầu và các điểm rủi ro; hành vi bị cấm và chế tài; tội phạm theo Bộ luật Hình sự; "
             "phương thức, thủ đoạn và lỗ hổng sai phạm; thực trạng ở Việt Nam và Thành phố Hồ Chí Minh."),
            ("08", "PHẦN THỨ HAI. NHỮNG VẤN ĐỀ CẦN CHÚ Ý TRONG ĐẤU TRANH THEO TỪNG LĨNH VỰC",
             "Gồm Chương 8 đến Chương 16: phương pháp chung phát hiện, xác minh, điều tra; các lĩnh vực "
             "y tế; giáo dục và đào tạo; du lịch, thể dục, thể thao; bảo hiểm; đầu tư xây dựng, giao "
             "thông; công nghệ thông tin; dịch vụ công ích đô thị, môi trường; lựa chọn nhà đầu tư, "
             "dự án PPP, dự án có sử dụng đất."),
            ("17", "PHẦN THỨ BA. PHÒNG NGỪA VÀ KIẾN NGHỊ",
             "Gồm Chương 17: phòng ngừa tội phạm trong lĩnh vực đấu thầu và kiến nghị hoàn thiện "
             "pháp luật, cơ chế quản lý, nhất là trên địa bàn Thành phố Hồ Chí Minh."),
        ],
        "html": {
            "title": "Tội phạm trong lĩnh vực đấu thầu",
            "description": "Tài liệu chuyên sâu về tội phạm trong lĩnh vực đấu thầu: {n_pages} chương và "
                           "phụ lục, {n_sec} mục tra cứu, cập nhật pháp luật đến ngày 31/10/2026.",
            "h1": "Tội phạm trong lĩnh vực đấu thầu",
            "sub": "Tài liệu chuyên sâu: nhận thức, pháp luật, lỗ hổng sai phạm và những vấn đề "
                   "cần chú ý trong đấu tranh theo từng lĩnh vực",
            "badges": ["Phiên bản 1.0", "Biên soạn 31/10/2026", "Cập nhật pháp luật đến 31/10/2026",
                       "18 chương và 7 phụ lục", "{n_sec} mục tra cứu"],
            "warn": (
                "    <b>Cảnh báo sử dụng.</b> Đây là tài liệu tham khảo nghiệp vụ, không phải văn bản\n"
                "    quy phạm pháp luật và không thay thế văn bản quy phạm pháp luật. Pháp luật về đấu thầu\n"
                "    thay đổi rất nhanh trong giai đoạn 2025 đến 2026; trước khi ban hành bất kỳ quyết định\n"
                "    tố tụng nào phải đối chiếu văn bản gốc và xác định đúng văn bản có hiệu lực tại thời điểm\n"
                "    xảy ra hành vi. Các nội dung đánh dấu <span class=\"tag tag-check\">CẦN ĐỐI CHIẾU</span>\n"
                "    là nội dung bắt buộc phải kiểm tra lại văn bản gốc trước khi áp dụng."
            ),
            "placeholder": "Tra cứu theo mục, ví dụ: thông thầu, quân xanh, giá gói thầu, thiết bị y tế, "
                           "chỉ định thầu, thiệt hại, Điều 222",
            "footer": (
                "    Tài liệu được biên soạn và lưu trữ phục vụ công tác nghiên cứu, tra cứu nghiệp vụ cá nhân.\n"
                "    Bản Markdown gốc nằm cùng thư mục để đọc trực tiếp trên GitHub."
            ),
            "groups": [
                ("Chương mở đầu", ["00"]),
                ("Phần thứ nhất. Nhận thức chung về đấu thầu và tội phạm trong lĩnh vực đấu thầu",
                 ["01", "02", "03", "04", "05", "06", "07"]),
                ("Phần thứ hai. Những vấn đề cần chú ý trong đấu tranh theo từng lĩnh vực",
                 ["08", "09", "10", "11", "12", "13", "14", "15", "16"]),
                ("Phần thứ ba. Phòng ngừa và kiến nghị", ["17"]),
                ("Phụ lục tra cứu", ["PL"]),
            ],
            "quick": [
                ("Mới tiếp cận lĩnh vực đấu thầu, cần hiểu từ gốc", "01-tong-quan-ve-dau-thau.html"),
                ("Không rõ văn bản nào áp dụng cho hành vi đã xảy ra", "02-he-thong-phap-luat-ve-dau-thau.html"),
                ("Cần biết khâu nào trong quy trình dễ bị lợi dụng", "03-quy-trinh-lua-chon-nha-thau-va-diem-rui-ro.html"),
                ("Phân định vi phạm hành chính với tội phạm", "04-hanh-vi-bi-cam-va-che-tai.html"),
                ("Định tội danh: Điều 222 hay tham ô, nhận hối lộ", "05-toi-pham-trong-linh-vuc-dau-thau.html"),
                ("Nhận diện quân xanh, quân đỏ, nhóm lợi ích", "06-phuong-thuc-thu-doan-va-lo-hong.html"),
                ("Vì sao nhiều vụ việc chưa làm rõ được", "07-thuc-trang-viet-nam-va-tphcm.html"),
                ("Có đơn tố giác thông thầu, cần hướng xác minh", "08-phuong-phap-chung-phat-hien-dieu-tra.html"),
                ("Gói thầu thiết bị y tế, vật tư, thuốc", "09-linh-vuc-y-te.html"),
                ("Thiết bị dạy học, sách giáo khoa, sửa chữa trường", "10-linh-vuc-giao-duc-dao-tao.html"),
                ("Sự kiện, lễ hội, xúc tiến du lịch, thể thao", "11-linh-vuc-du-lich-the-duc-the-thao.html"),
                ("Quỹ bảo hiểm y tế, mua sắm ngành bảo hiểm", "12-linh-vuc-bao-hiem.html"),
                ("Công trình xây dựng, giao thông, khối lượng khống", "13-linh-vuc-dau-tu-xay-dung-giao-thong.html"),
                ("Phần mềm, thiết bị công nghệ thông tin", "14-linh-vuc-cong-nghe-thong-tin.html"),
                ("Thu gom rác, chiếu sáng, cây xanh, chống ngập", "15-linh-vuc-dich-vu-cong-ich-moi-truong.html"),
                ("Dự án có sử dụng đất, PPP, BT", "16-lua-chon-nha-dau-tu-ppp-dat-dai.html"),
                ("Cần xác định thiệt hại, trưng cầu giám định", "08-phuong-phap-chung-phat-hien-dieu-tra.html"),
                ("Tra nhanh dấu hiệu nghi vấn theo từng khâu", "phu-luc/PL-B-bo-chi-bao-nghi-van.html"),
                ("Lập danh mục tài liệu cần thu thập", "phu-luc/PL-C-danh-muc-tai-lieu-can-thu-thap.html"),
                ("Chuẩn bị câu hỏi lấy lời khai", "phu-luc/PL-E-cau-hoi-lay-loi-khai.html"),
                ("Xem vụ án điển hình và bài học", "phu-luc/PL-F-vu-an-dien-hinh.html"),
            ],
        },
    },
}


def ten_bo() -> str:
    return os.environ.get("BO", MAC_DINH)


def lay(bo: str = "") -> dict:
    bo = bo or ten_bo()
    if bo not in CAU_HINH:
        sys.exit(f"Bo tai lieu khong xac dinh: {bo}. Cac bo hien co: {', '.join(CAU_HINH)}")
    return CAU_HINH[bo]


def thu_muc(bo: str = "") -> Path:
    bo = bo or ten_bo()
    lay(bo)
    return ROOT / bo


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Cach dung: bo_tai_lieu.py <BO> <khoa>")
    print(lay(sys.argv[1])[sys.argv[2]])
