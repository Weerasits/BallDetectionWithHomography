import cv2
import numpy as np

# === STEP 0: Load and Resize the Image ===
img = cv2.imread('img4.png')
scale_percent = 50
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
img_resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

# === STEP 1: Define Points ===
# Points in resized image
pts_image = np.array([
    [549 * 0.5, 450 * 0.5],    # A
    [751 * 0.5, 445 * 0.5],    # B
    [467 * 0.5, 847 * 0.5],    # C
    [878 * 0.5, 841 * 0.5],   # D
], dtype=np.float32)

# Points in real-world (meters)
pts_top = np.array([
    [0, 0],        # A
    [1.5, 0],      # B
    [0, 2.7],      # C
    [1.5, 2.7],    # D
], dtype=np.float32)

# === STEP 2: Homography and Warp ===
output_size_m = (1.5, 2.7)  # meters
scale_px_per_m = 300  # ปรับตามความคมชัดที่ต้องการ (300 px ต่อเมตร)

output_res = (int(output_size_m[0] * scale_px_per_m),
              int(output_size_m[1] * scale_px_per_m))

# Convert top view points to pixels
pts_top_px = pts_top * scale_px_per_m

# Compute homography
H, _ = cv2.findHomography(pts_image, pts_top_px)
warped = cv2.warpPerspective(img_resized, H, output_res)

# === STEP 3: Mouse Callback (แสดงตำแหน่งเป็นเมตร) ===
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        xm = x / scale_px_per_m
        ym = y / scale_px_per_m
        print(f"Position: x = {xm:.2f} m, y = {ym:.2f} m")

# === STEP 4: Draw court outline on resized image ===
pts = np.array([
    [549 * 0.5, 450 * 0.5],    # A
    [751 * 0.5, 445 * 0.5],    # B
    [878 * 0.5, 841 * 0.5],   # D
    [467 * 0.5, 847 * 0.5],    # C
], np.int32).reshape((-1, 1, 2))

cv2.polylines(img_resized, [pts], isClosed=True, color=(0, 255, 255), thickness=2)
font = cv2.FONT_HERSHEY_SIMPLEX
labels = ['A', 'B', 'D', 'C']
for i, point in enumerate(pts):
    x, y = point[0]
    cv2.putText(img_resized, labels[i], (x + 5, y - 5), font, 0.6, (0, 0, 255), 2)

# === STEP 5: Show and run ===
cv2.namedWindow('Top View')
cv2.setMouseCallback('Top View', mouse_callback)

while True:
    cv2.imshow("Court Outline", img_resized)
    cv2.imshow("Top View", warped)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cv2.destroyAllWindows()
