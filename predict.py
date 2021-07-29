import cv2


cam = cv2.VideoCapture(0)

while True:
    try:
        flag, res = cam.read()
        if not flag:
            continue

        res = cv2.cvtColor(res, cv2.COLOR_RGB2GRAY)
        print(res.shape)
    except Exception as e:
        print(e)
        break

cam.release()