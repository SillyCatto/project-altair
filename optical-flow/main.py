import cv2
import numpy as np

# === CONFIGURATION ===
STREAM_URL = "http://192.168.0.104:4747/video" # video stream
initial_rect = (200, 150, 100, 100)  # (x, y, width, height)

# === INITIAL SETUP ===
cap = cv2.VideoCapture(STREAM_URL)

# Wait for first valid frame
while True:
    ret, old_frame = cap.read()
    if ret:
        break
    print("Waiting for the first frame...")
    cv2.waitKey(100)

old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

# Rectangle setup
x, y, w, h = initial_rect
roi = old_gray[y:y+h, x:x+w]

# Detect good feature points inside the initial rectangle
p0 = cv2.goodFeaturesToTrack(roi, mask=None, maxCorners=100, qualityLevel=0.3, minDistance=7)

# Adjust to full frame coordinates
if p0 is not None:
    p0[:, 0, 0] += x
    p0[:, 0, 1] += y

# Lucas-Kanade parameters
lk_params = dict(
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
)

# === MAIN LOOP ===
while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame not received, skipping...")
        continue

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if p0 is None or len(p0) == 0:
        print("No tracking points. Reinitializing...")
        roi = frame_gray[y:y+h, x:x+w]
        p0 = cv2.goodFeaturesToTrack(roi, mask=None, maxCorners=100, qualityLevel=0.3, minDistance=7)
        if p0 is not None:
            p0[:, 0, 0] += x
            p0[:, 0, 1] += y
        continue

    # Optical flow tracking
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    if p1 is not None and st is not None:
        good_new = p1[st == 1]
        good_old = p0[st == 1]

        if len(good_new) == 0 or len(good_old) == 0:
            print("All points lost. Reinitializing...")
            roi = frame_gray[y:y+h, x:x+w]
            p0 = cv2.goodFeaturesToTrack(roi, mask=None, maxCorners=100, qualityLevel=0.3, minDistance=7)
            if p0 is not None:
                p0[:, 0, 0] += x
                p0[:, 0, 1] += y
            continue

        # Movement vector
        movement = good_new - good_old
        avg_movement = np.mean(movement, axis=0)

        if np.isnan(avg_movement).any():
            print("Movement NaN detected. Skipping frame.")
            continue

        # Update rectangle center
        center_x = x + w // 2 + int(avg_movement[0])
        center_y = y + h // 2 + int(avg_movement[1])

        # Update top-left corner of rectangle
        x = center_x - w // 2
        y = center_y - h // 2

        # Draw updated rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw tracked points
        for pt in good_new:
            cv2.circle(frame, tuple(pt.astype(int)), 3, (0, 0, 255), -1)

        # Update for next frame
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)

        # Reinitialize if too few points
        if len(p0) < 10:
            print("Too few points. Reinitializing...")
            roi = frame_gray[y:y+h, x:x+w]
            new_p = cv2.goodFeaturesToTrack(roi, mask=None, maxCorners=100, qualityLevel=0.3, minDistance=7)
            if new_p is not None:
                new_p[:, 0, 0] += x
                new_p[:, 0, 1] += y
                p0 = new_p

    # cv2.resizeWindow("Optical Flow Tracking", 800, 600)
    cv2.imshow("Optical Flow Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
