import cv2


cam = cv2.VideoCapture(0)

while True:
    try:
        flag, res = cam.read() # 640 x 480
        if not flag:
            continue

        res = cv2.cvtColor(res, cv2.COLOR_RGB2GRAY)
        cv2.resize(res, (640//5))
        print(res.shape)
    except Exception as e:
        print(e)
        break

cam.release()