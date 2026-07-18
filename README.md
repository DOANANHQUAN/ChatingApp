# 🚀 HƯỚNG DẪN KHỞI CHẠY DỰ ÁN (RUNNING GUIDE)

Tài liệu này hướng dẫn cách cài đặt môi trường, cấu hình cơ sở dữ liệu và khởi chạy ứng dụng nhắn tin thời gian thực **Django Real-Time Messenger** trên máy tính cá nhân.

---

## 📋 1. YÊU CẦU TIỀN ĐỀ (PREREQUISITES)
*   **Python**: Phiên bản `3.10` trở lên (Khuyến nghị `3.11` hoặc `3.12`).
*   **Cơ sở dữ liệu**: SQLite (mặc định cho môi trường phát triển - không cần cài đặt thêm).
*   **Hệ điều hành**: Hỗ trợ tốt trên Linux, macOS, và Windows.

---

## 🛠️ 2. CÁC BƯỚC THIẾT LẬP BAN ĐẦU (SETUP STEPS)

Mở Terminal (hoặc Command Prompt) tại thư mục gốc của dự án (`/home/dctrng/Documents/Teky_12_Chat`) và thực hiện lần lượt các bước sau:

### Bước 2.1: Tạo và Kích hoạt Môi trường ảo (Virtual Environment)
Môi trường ảo giúp cô lập các thư viện của dự án, tránh xung đột hệ thống.

*   **Trên Linux / macOS**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
*   **Trên Windows (PowerShell / Command Prompt)**:
    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1   # PowerShell
    # hoặc: .\venv\Scripts\activate.bat # CMD
    ```

### Bước 2.2: Cài đặt các thư viện cần thiết (Dependencies)
Nâng cấp `pip` và cài đặt các thư viện định nghĩa sẵn trong `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Bước 2.3: Sao chép hình ảnh mặc định (Default Assets)
Chạy script helper để sao chép hình ảnh đại diện mặc định và hình ảnh nhóm mặc định vào đúng thư mục `static/` và `media/`:

```bash
python copy_assets.py
```

### Bước 2.4: Khởi tạo cơ sở dữ liệu (Database Migrations)
Tạo cấu trúc bảng dữ liệu cho các tính năng Chat, Tài khoản và Thông báo, sau đó đồng bộ vào cơ sở dữ liệu:

```bash
# Tạo tệp tin ánh xạ cơ sở dữ liệu cho các app nội bộ
python manage.py makemigrations accounts chat notifications

# Đồng bộ (Tạo bảng dữ liệu) vào file db.sqlite3
python manage.py migrate
```

### Bước 2.5: Tạo tài khoản Quản trị viên (Superuser)
Tạo tài khoản quản trị để kiểm tra dữ liệu từ trang Admin:

```bash
python manage.py createsuperuser
```
*(Lưu ý: Khi nhập mật khẩu trên terminal, các ký tự sẽ được ẩn đi vì lý do bảo mật. Hãy gõ bình thường và nhấn Enter).*

---

## 🎬 3. KHỞI CHẠY ỨNG DỤNG (RUNNING THE APP)

Khởi động máy chủ phát triển ASGI (sử dụng Daphne được tích hợp sẵn để xử lý kết nối WebSocket):

```bash
python manage.py runserver
```

Khi màn hình hiển thị như bên dưới tức là ứng dụng đã khởi chạy thành công:
```text
Starting ASGI/Daphne version 4.2.2 development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

*   **Giao diện ứng dụng chat**: Truy cập địa chỉ [http://127.0.0.1:8000/](http://127.0.0.1:8000/) trên trình duyệt.
*   **Giao diện quản trị Admin**: Truy cập địa chỉ [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) và đăng nhập bằng tài khoản Superuser vừa tạo.

---

## 🧪 4. HƯỚNG DẪN KIỂM THỬ TÍNH NĂNG CHAT THỜI GIAN THỰC

Để trải nghiệm trọn vẹn luồng gửi nhận tin nhắn, hình ảnh và trạng thái online thời gian thực:

1.  **Mở cửa sổ ẩn danh**: 
    *   Mở trình duyệt thông thường (ví dụ: Google Chrome) và truy cập trang đăng ký: `http://127.0.0.1:8000/accounts/register/`. Đăng ký tài khoản `userA`.
    *   Mở một cửa sổ **Trình duyệt ẩn danh (Incognito)** (hoặc một trình duyệt khác như Edge, Firefox) truy cập cùng link và đăng ký tài khoản `userB`.
2.  **Kết bạn chéo**:
    *   Tại tài khoản `userA`, gõ tìm kiếm `@userB` ở thanh tìm kiếm, gửi lời mời kết bạn.
    *   Tại tài khoản `userB`, truy cập danh sách bạn bè, bấm **Chấp nhận kết bạn**.
3.  **Nhắn tin và Gửi ảnh**:
    *   Mở phòng chat giữa hai người. Thử gõ chữ để thấy **Typing Indicator** (đang nhập...) hiện lên ở màn hình người kia.
    *   Nhắn tin và nhấn Gửi -> Tin nhắn xuất hiện ngay lập tức bên tài khoản đối phương.
    *   Đính kèm hình ảnh và gửi -> Ảnh sẽ được tải lên và hiển thị thumbnail tức thì!
    *   Bên tài khoản nhận đọc tin nhắn -> Bên người gửi sẽ thấy nhãn `(Đã xem)` xuất hiện bên cạnh tin nhắn cuối cùng.
