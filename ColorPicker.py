import cv2
import numpy as np

# เปิดกล้อง
cap = cv2.VideoCapture(0)

cv2.namedWindow("HSV Mask")

# สร้าง Trackbars สำหรับปรับค่า HSV
def nothing(x):
    pass

cv2.createTrackbar("LowH", "HSV Mask", 20, 179, nothing)
cv2.createTrackbar("HighH", "HSV Mask", 35, 179, nothing)
cv2.createTrackbar("LowS", "HSV Mask", 100, 255, nothing)
cv2.createTrackbar("HighS", "HSV Mask", 255, 255, nothing)
cv2.createTrackbar("LowV", "HSV Mask", 100, 255, nothing)
cv2.createTrackbar("HighV", "HSV Mask", 255, 255, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ย่อภาพเพื่อให้แสดงเร็วขึ้น (ถ้าต้องการ)
    # frame = cv2.resize(frame, (640, 480))

    # แปลงเป็น HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # อ่านค่าจาก trackbar
    lh = cv2.getTrackbarPos("LowH", "HSV Mask")
    hh = cv2.getTrackbarPos("HighH", "HSV Mask")
    ls = cv2.getTrackbarPos("LowS", "HSV Mask")
    hs = cv2.getTrackbarPos("HighS", "HSV Mask")
    lv = cv2.getTrackbarPos("LowV", "HSV Mask")
    hv = cv2.getTrackbarPos("HighV", "HSV Mask")

    lower = np.array([lh, ls, lv])
    upper = np.array([hh, hs, hv])

    # ทำ mask
    mask = cv2.inRange(hsv, lower, upper)

    # วัตถุที่ detect แล้ว
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # แสดงผล
    cv2.imshow("Webcam", frame)
    cv2.imshow("HSV Mask", mask)
    cv2.imshow("Detected", result)

    if cv2.waitKey(1) & 0xFF == 27:  # Esc เพื่อออก
        break

cap.release()
cv2.destroyAllWindows()
