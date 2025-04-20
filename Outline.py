import cv2
import numpy as np

# โหลดภาพ
img = cv2.imread('img1.png')

# จุดมุมสนาม 4 จุด (ระบุจากการดูภาพแบบคร่าว ๆ หรือใช้โปรแกรมคลิกเพื่อความแม่นยำ)
# คุณสามารถแก้ไขค่าพิกัดเหล่านี้ให้ตรงกับจุดจริงในภาพได้
pts = np.array([
    [302, 54],   # A (ซ้ายบน)
    [775, 57],   # B (ขวาบน)
    [936, 727],  # D (ขวาล่าง)
    [17, 732],   # C (ซ้ายล่าง)
], np.int32)

# วาดกรอบสนาม (เชื่อม A-B-D-C กลับมา A)
pts = pts.reshape((-1, 1, 2))
cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 255), thickness=2)

# เพิ่ม Label มุม A-D (optional)
font = cv2.FONT_HERSHEY_SIMPLEX
labels = ['A', 'B', 'D', 'C']
for i, point in enumerate(pts):
    x, y = point[0]
    cv2.putText(img, labels[i], (x + 5, y - 5), font, 0.7, (0, 0, 255), 2)

# แสดงผล
cv2.imshow("Court Outline", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
