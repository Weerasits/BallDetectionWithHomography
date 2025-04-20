import cv2
import numpy as np

# ---------- CONFIG ----------
width_m = 0.9
height_m = 0.9
scale_px_per_m = 300  # 300 px = 1 m
output_size = (int(width_m * scale_px_per_m), int(height_m * scale_px_per_m))

# พิกัดสนามใน top view (เมตร -> px)
pts_top = np.array([
    [0, 0],
    [width_m, 0],
    [0, height_m],
    [width_m, height_m]
], dtype=np.float32) * scale_px_per_m

# ---------- STEP 1: Webcam + คลิก 4 จุด ----------
cap = cv2.VideoCapture(0)
clicked_points = []

def click_points(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_points) < 4:
        clicked_points.append((x, y))
        print(f"Point {len(clicked_points)}: ({x}, {y})")

print("คลิก 4 จุดมุมสนามในภาพจากกล้อง: A → B → C → D")

while True:
    ret, frame = cap.read()
    if not ret:
        break

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

# ---------- STEP 2: Homography ----------
H, _ = cv2.findHomography(pts_image, pts_top)

# ---------- STEP 3: Detect Yellow Ball ----------
def detect_yellow_ball(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # ปรับช่วงสีให้กว้างขึ้น
    lower_yellow = np.array([28, 69, 0])
    upper_yellow = np.array([45, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # เพิ่ม blur และ morphological filter
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest)
        if radius > 3:
            return int(x), int(y)
    return None


# ---------- STEP 4: Real-time Loop ----------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # หา centroid ลูกบอล
    center = detect_yellow_ball(frame)

    # แปลงมุมมองเป็น Top View
    warped = cv2.warpPerspective(frame, H, output_size)

    # แสดงตำแหน่งใน top view (แปลงตำแหน่งผ่าน Homography)
    if center:
        # แปลงจุดด้วย homography
        pts = np.array([[center]], dtype=np.float32)
        dst = cv2.perspectiveTransform(pts, H)
        cx, cy = dst[0][0]
        x_meter = cx / scale_px_per_m
        y_meter = cy / scale_px_per_m

        # วาดบนภาพ top view
        cv2.circle(warped, (int(cx), int(cy)), 10, (0, 0, 255), -1)
        cv2.putText(warped, f"x={x_meter:.2f}m y={y_meter:.2f}m",
                    (int(cx)+10, int(cy)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        print(x_meter,y_meter)
    cv2.imshow("Webcam", frame)
    cv2.imshow("Top View", warped)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
