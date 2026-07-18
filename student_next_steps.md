# HƯỚNG DẪN CÁC BƯỚC TIẾP THEO CHO HỌC SINH (STUDENT MILESTONES)

Dự án **Real-time Messenger** hiện đã có sẵn bộ khung xương (Skeleton) hoàn chỉnh theo mô hình MTV của Django cùng với tích hợp Django Channels cho kết nối thời gian thực. 

Dưới đây là danh sách các nhiệm vụ cụ thể được chia theo từng giai đoạn để các em học sinh có thể tiếp tục thực hành, hoàn thiện và nâng cấp dự án này.

---

## 📅 GIAI ĐOẠN 1: KHỞI ĐỘNG & ĐỒNG BỘ CƠ SỞ DỮ LIỆU

### Bước 1: Khởi tạo và chạy Migrations cho các App Local
Vì cấu trúc cơ sở dữ liệu của các app mới (`accounts`, `chat`, `notifications`) vừa được định nghĩa mới hoàn toàn, các em cần tạo file migration riêng cho chúng và chạy đồng bộ vào cơ sở dữ liệu SQLite:

```bash
# 1. Tạo các file migrations cho 3 app mới
python manage.py makemigrations accounts chat notifications

# 2. Thực hiện đồng bộ (migrate) các bảng dữ liệu này vào database
python manage.py migrate
```

### Bước 2: Tạo tài khoản Quản trị viên (Superuser)
Tạo tài khoản quản trị để đăng nhập vào trang quản trị mặc định của Django (`http://127.0.0.1:8000/admin/`):

```bash
python manage.py createsuperuser
```
*(Hãy nhập Username, Email, và Mật khẩu theo hướng dẫn trên màn hình terminal)*.

---

## 🛠 GIAI ĐOẠN 2: CÁC NHIỆM VỤ THỰC HÀNH PHÁT TRIỂN (STUDENT TASKS)

### 📝 Nhiệm vụ 1: Đăng ký các Model vào trang quản trị Django Admin
**Mục tiêu**: Giúp học sinh có thể quản lý các tài khoản người dùng, cuộc trò chuyện, tin nhắn và thông báo trực quan từ giao diện admin.

*   **Yêu cầu**: Hãy chỉnh sửa file `admin.py` trong thư mục của từng app (`accounts/admin.py`, `chat/admin.py`, `notifications/admin.py`) để đăng ký các model tương ứng.
*   **Ví dụ gợi ý (`accounts/admin.py`)**:
    ```python
    from django.contrib import admin
    from .models import User, Contact, FriendRequest

    admin.site.register(User)
    admin.site.register(Contact)
    admin.site.register(FriendRequest)
    ```
*   **Thách thức nâng cao**: Sử dụng `admin.ModelAdmin` để hiển thị thêm các cột như `is_online`, `last_seen` của User trên danh sách admin.

---

### 👥 Nhiệm vụ 2: Thiết kế giao diện và View tạo Nhóm Chat (Group Chat)
**Mục tiêu**: Hiện tại mã nguồn đã có model `Conversation(is_group=True)`, các em cần xây dựng chức năng để người dùng tạo nhóm chat với nhiều thành viên.

*   **Yêu cầu**:
    1.  Tạo một form HTML trong giao diện danh sách bạn bè cho phép người dùng nhập "Tên nhóm" và chọn nhiều người bạn (sử dụng `<input type="checkbox">`).
    2.  Viết một Class-Based View hoặc Function-Based View nhận dữ liệu POST gửi lên, tiến hành tạo một đối tượng `Conversation` mới với `is_group=True`, sau đó lặp qua danh sách user_id được chọn để tạo các bản ghi `ConversationParticipant` tương ứng.
    3.  Chuyển hướng (Redirect) người dùng trực tiếp vào phòng chat nhóm vừa tạo.

---

### 🟢 Nhiệm vụ 3: Tích hợp và hiển thị Trạng thái "Đang nhập..." (Typing Indicator)
**Mục tiêu**: Xử lý logic hiển thị hiệu ứng ba chấm động khi đối phương đang gõ văn bản.

*   **Yêu cầu**:
    *   Mã nguồn JS trong `templates/chat/conversation_detail.html` đã có sẵn phần gửi tín hiệu WebSocket `typing` khi người dùng nhập dữ liệu vào ô chat.
    *   Học sinh cần kiểm tra khối HTML `<div id="typing-indicator-box">` trong template. Các em hãy tùy chỉnh CSS hoặc JS để khi nhận được sự kiện `typing` với trạng thái `is_typing: true` từ phía WebSocket, khối này sẽ đổi từ ẩn sang hiện (`display: block`).
    *   Hiển thị đúng tên của người đang gõ chữ bằng cách thay đổi nội dung thẻ `typing-user-text`.

---

### 👁 Nhiệm vụ 4: Cập nhật Trạng thái "Đã xem" (Seen status)
**Mục tiêu**: Khi người nhận mở tin nhắn, hệ thống cần gửi tín hiệu cập nhật trạng thái đã xem về cơ sở dữ liệu và hiển thị biểu tượng nhỏ trên màn hình người gửi.

*   **Yêu cầu**:
    *   Đọc và phân tích sự kiện `seen` trong hàm `chatSocket.onmessage` tại file `conversation_detail.html`.
    *   Tự thiết kế thêm một biểu tượng nhỏ (ví dụ: avatar thu nhỏ của người nhận hoặc chữ "Đã xem" nhạt) ở góc dưới cùng của bong bóng tin nhắn cuối cùng để báo hiệu tin nhắn đó đã được đọc thành công.

---

### 📂 Nhiệm vụ 5: Quản lý và Validate tệp đính kèm an toàn
**Mục tiêu**: Tối ưu hóa tính năng gửi file và đảm bảo an toàn cho máy chủ.

*   **Yêu cầu**:
    *   Trong `chat/models.py`, hàm `validate_file_size` đã được viết để giới hạn dung lượng tải lên.
    *   Các em hãy thử điều chỉnh tham số cấu hình `MAX_UPLOAD_SIZE` trong `config/settings/base.py` lên 20MB hoặc xuống 2MB và tải thử một tệp lớn hơn để xem thông báo lỗi hiển thị ra sao.
    *   Viết thêm hàm xử lý ở client để thông báo lỗi cho người dùng bằng thẻ alert hoặc thẻ thông báo đỏ nếu kích thước file chọn quá lớn trước khi tải lên server.

---

## 🚀 GIAI ĐOẠN 3: HƯỚNG DẪN CHẠY THỬ & ĐÁNH GIÁ (RUN & TESTING)

### Các bước chạy thử dành cho học sinh:
1.  **Chạy server phát triển**:
    ```bash
    python manage.py runserver
    ```
2.  **Đăng ký tài khoản mẫu**:
    *   Mở trình duyệt chính (ví dụ Chrome) truy cập `http://127.0.0.1:8000/accounts/register/` để đăng ký tài khoản `HocSinhA`.
    *   Mở trình duyệt ở **chế độ ẩn danh** (Incognito) hoặc một trình duyệt khác (như Firefox/Edge) đăng ký tài khoản `HocSinhB`.
3.  **Kết bạn**:
    *   Sử dụng thanh tìm kiếm trong danh sách bạn bè để tìm và kết bạn giữa hai tài khoản.
    *   Đăng nhập tài khoản đối phương để ấn "Đồng ý".
4.  **Bắt đầu nhắn tin**:
    *   Click vào nút "Nhắn tin" và thử nghiệm chat chữ thời gian thực, đính kèm hình ảnh và quan sát sự thay đổi tức thì giữa hai cửa sổ trình duyệt!
