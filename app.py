import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av

# --- CẤU HÌNH MEDIA PIPE ---
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# --- HÀM TÍNH TOÁN GÓC ---
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
    return angle

# --- GIAO DIỆN STREAMLIT ---
st.set_page_config(layout="wide", page_title="AI Fitness Trainer")

st.title("💪 AI Personal Trainer - Cloud Version")
st.write("Phiên bản Web: Đứng xa camera để thấy toàn bộ cơ thể.")

# --- CLASS XỬ LÝ VIDEO CHO WEBRTC ---
# Khác với Local, trên Web ta phải dùng Class này để xử lý từng frame ảnh
class PoseDetector:
    def __init__(self):
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.counter = 0
        self.stage = None

    def recv(self, frame):
        # 1. Chuyển đổi format ảnh từ WebRTC sang OpenCV
        img = frame.to_ndarray(format="bgr24")
        
        # 2. Xử lý ảnh (giống hệt code local)
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.pose.process(image)
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 3. Logic đếm (Tính toán góc)
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Lấy tọa độ (Vai - Khuỷu - Cổ tay trái)
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            angle = calculate_angle(shoulder, elbow, wrist)
            
            # Hiển thị số đo góc ngay cạnh khuỷu tay
            cv2.putText(image, str(int(angle)), 
                           tuple(np.multiply(elbow, [image.shape[1], image.shape[0]]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Logic đếm Reps
            if angle > 160:
                self.stage = "down"
            if angle < 30 and self.stage == 'down':
                self.stage = "up"
                self.counter += 1
                
        except Exception as e:
            pass

        # 4. Vẽ thông số trực tiếp lên Video (Vì Streamlit Metric không update realtime qua WebRTC dễ dàng được)
        # Vẽ hộp chứa thông tin
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        
        # Hiện số Reps
        cv2.putText(image, 'REPS', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(self.counter), (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Hiện trạng thái Stage
        cv2.putText(image, 'STAGE', (65,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(self.stage), (60,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

        # Vẽ xương
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
        
        # 5. Trả ảnh về cho Web hiển thị
        return av.VideoFrame.from_ndarray(image, format="bgr24")

# --- CHẠY WEBRTC ---
# Đây là component thay thế cho cv2.VideoCapture(0)
webrtc_streamer(
    key="example", 
    video_processor_factory=PoseDetector,
    media_stream_constraints={"video": True, "audio": False}, # Tắt âm thanh cho nhẹ
    rtc_configuration={ # Cấu hình Server STUN (quan trọng để chạy trên mạng)
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)