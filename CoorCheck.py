import cv2

# โหลดภาพ
image_path = "img4.png"  # เปลี่ยนชื่อไฟล์ตามที่คุณมี
img = cv2.imread(image_path)
img_display = img.copy()

# ลิสต์เก็บพิกัด
clicked_points = []

# ฟังก์ชันคลิกเมาส์
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_points) < 4:
        clicked_points.append((x, y))
        cv2.circle(img_display, (x, y), 5, (0, 255, 0), -1)
        label = chr(ord('A') + len(clicked_points) - 1)
        cv2.putText(img_display, label, (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv2.imshow("Click 4 Points", img_display)

# เปิดหน้าต่าง
cv2.imshow("Click 4 Points", img_display)
cv2.setMouseCallback("Click 4 Points", click_event)

print("🖱 คลิก 4 จุด: A (บนซ้าย), B (บนขวา), C (ล่างซ้าย), D (ล่างขวา)")
cv2.waitKey(0)
cv2.destroyAllWindows()

# พิมพ์พิกัดที่คลิก
print("\n== พิกัดที่คลิกได้ (pixel) ==")
for i, pt in enumerate(clicked_points):
    print(f"{chr(ord('A') + i)}: {pt}")
