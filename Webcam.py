import cv2
import numpy as np

# === STEP 0: สร้างกล้อง webcam ===
cap = cv2.VideoCapture(0)

# ขนาดสนามจริง (เมตร)
width_m = 0.6
height_m = 0.6
scale_px_per_m = 500
output_size = (int(width_m * scale_px_per_m), int(height_m * scale_px_per_m))

# พิกัดสนามจริง (เมตร)
pts_top = np.array([
    [0, 0],
    [width_m, 0],
    [0, height_m],
    [width_m, height_m]
], dtype=np.float32) * scale_px_per_m  # Convert to pixel

# === STEP 1: ให้คลิก 4 จุดมุมสนามจากกล้อง ===
clicked_points = []

def click_points(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_points) < 4:
        clicked_points.append((x, y))
        print(f"Point {len(clicked_points)}: ({x}, {y})")

print("คลิก 4 จุดมุมสนาม (ตามลำดับ: A, B, C, D)")

# รอคลิก 4 จุดจาก webcam
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # แสดงจุดที่คลิกไว้
    for pt in clicked_points:
        cv2.circle(frame, pt, 5, (0, 0, 255), -1)

    cv2.imshow("Click 4 Points", frame)
    cv2.setMouseCallback("Click 4 Points", click_points)

    if len(clicked_points) == 4:
        cv2.destroyWindow("Click 4 Points")
        break

    if cv2.waitKey(1) & 0xFF == 27:
        break

pts_image = np.array(clicked_points, dtype=np.float32)

# === STEP 2: คำนวณ Homography ===
H, _ = cv2.findHomography(pts_image, pts_top)

# === STEP 3: ฟังก์ชันแสดงตำแหน่งเมาส์ใน top view ===
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        xm = x / scale_px_per_m
        ym = y / scale_px_per_m
        print(f"[Top View] x = {xm:.2f} m, y = {ym:.2f} m")

cv2.namedWindow("Top View")
cv2.setMouseCallback("Top View", mouse_callback)

# === STEP 4: เริ่มทำงานแบบ Real-time ===
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ทำ Perspective Transform
    warped = cv2.warpPerspective(frame, H, output_size)

    # แสดงผล
    cv2.imshow("Webcam (Original)", frame)
    cv2.imshow("Top View", warped)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
