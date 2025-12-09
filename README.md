# 🏋️‍♂️ VisionFit - AI Personal Trainer

> **Đồ án cuối kỳ môn Computer Vision**
>
> **Đề tài:** Ứng dụng Pose Estimation hỗ trợ tập luyện thể dục tại nhà.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose-green)

## 📖 Giới thiệu
**VisionFit** là ứng dụng sử dụng Thị giác máy tính (Computer Vision) để theo dõi và phân tích động tác tập luyện của người dùng trong thời gian thực.

Ứng dụng sử dụng **MediaPipe** để phát hiện các khớp xương cơ thể và tính toán góc độ, từ đó đếm số lần tập (Reps) và cảnh báo tư thế đúng/sai.

### ✨ Tính năng chính
- 📷 **Real-time Tracking:** Nhận diện tư thế qua Webcam.
- 🔢 **Auto Counter:** Tự động đếm số lần tập (Ví dụ: Bicep Curls).
- 📊 **Visual Feedback:** Hiển thị biểu đồ và thanh tiến trình độ gập của cơ.
- ⚙️ **Tùy chỉnh:** Cài đặt mục tiêu (Target Reps) và độ nhạy của thuật toán.

---

## 🛠 Cài đặt và Chạy ứng dụng (Local)

Để đảm bảo hiệu năng tốt nhất và độ trễ thấp nhất (Low Latency), khuyến khích chạy ứng dụng trực tiếp trên máy tính cá nhân thay vì trên Cloud.

### Bước 1: Clone dự án về máy
Mở Terminal hoặc Command Prompt (CMD) và chạy lệnh:

```bash
git clone https://github.com/tranhuudat2004/VisionFit-App.git
cd REPO-NAME
```


### Bước 2: Cài đặt các thư viện cần thiết
Đảm bảo bạn đã cài đặt Python. Chạy lệnh sau để cài các gói phụ thuộc:

```bash
pip install -r requirements.txt
```

> **Lưu ý:** Nếu gặp lỗi cài đặt, bạn có thể thử cài thủ công từng món:
> `pip install streamlit mediapipe opencv-python numpy`

### Bước 3: Chạy ứng dụng
Khởi chạy server Streamlit bằng lệnh:

```bash
streamlit run app.py
```

Sau khi chạy lệnh, trình duyệt sẽ tự động mở ra tại địa chỉ: `http://localhost:8501/`

---

## 📂 Cấu trúc thư mục

```text
VisionFit-App/
├── app.py              # Source code chính của ứng dụng
├── requirements.txt    # Danh sách thư viện cần cài đặt
├── README.md           # Hướng dẫn sử dụng
└── ...
```

## 🧩 Công nghệ sử dụng
*   **Ngôn ngữ:** Python 3
*   **Giao diện (UI):** Streamlit
*   **Xử lý ảnh:** OpenCV
*   **Mô hình AI:** Google MediaPipe Pose

## 👥 Nhóm thực hiện
1.  [Tên Thành Viên 1] - [MSSV]
2.  [Tên Thành Viên 2] - [MSSV]

---
*Dự án phục vụ mục đích học tập môn Computer Vision - Năm học 202X.*
