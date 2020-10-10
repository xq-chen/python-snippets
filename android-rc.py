import cv2
import os
import time

adb = "/mnt/c/android/platform-tools/adb.exe"
# adb = "adb"

ratio = 0.3


def capture_and_load():
    if os.system(
        '%s shell screencap /sdcard/capture.png > /dev/null 2>&1' %
        adb) != 0 or os.system(
        '%s pull /sdcard/capture.png ./capture.png > /dev/null 2>&1' %
            adb) != 0:
        return None
    img = cv2.imread('capture.png')
    width = int(img.shape[1] * ratio)
    height = int(img.shape[0] * ratio)
    resized = cv2.resize(img, (width, height))
    return resized


xDown = 0
yDown = 0


def mouse_event_handler(event, x, y, flags, param):
    global xDown, yDown
    if event == cv2.EVENT_LBUTTONDOWN:
        xDown = x
        yDown = y
    elif event == cv2.EVENT_LBUTTONUP:
        if (x - xDown) > 10 or (y - yDown) > 10:
            # Swipe
            os.system('%s shell input swipe %d %d %d %d' %
                      (adb, int(xDown / ratio), int(yDown / ratio),
                       int(x / ratio), int(y / ratio)))
        else:
            os.system('%s shell input tap %d %d' %
                      (adb, int(x / ratio), int(y / ratio)))


cv2.namedWindow("Android")
cv2.setMouseCallback("Android", mouse_event_handler)

while True:
    img = capture_and_load()
    cv2.imshow("Android", img)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, break from the loop
    if key == ord("q"):
        break
    time.sleep(1)

# close all open windows
cv2.destroyAllWindows()
