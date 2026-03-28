import mediapipe as mp
import cv2
import numpy as np
import time
import os

# contants
ml = 150
max_x, max_y = 250 + ml, 50
curr_tool = "select tool"
time_init = True
rad = 40
var_inits = False
thick = 4
prevx, prevy = 0, 0


# get tools function
def getTool(x):
    if x < 50 + ml:
        return "line"

    elif x < 100 + ml:
        return "rectangle"

    elif x < 150 + ml:
        return "draw"

    elif x < 200 + ml:
        return "circle"

    else:
        return "erase"


def index_raised(yi, y9):
    if (y9 - yi) > 40:
        return True

    return False


from mediapipe.tasks.python import BaseOptions, vision

base_options = BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1, min_hand_detection_confidence=0.6, min_hand_presence_confidence=0.6, min_tracking_confidence=0.6)
hand_landmark = vision.HandLandmarker.create_from_options(options)
# draw = mp.solutions.drawing_utils

# drawing tools
tools_path = os.path.join(os.path.dirname(__file__), "tools.png")
tools = cv2.imread(tools_path)

mask = None
'''
tools = np.zeros((max_y+5, max_x+5, 3), dtype="uint8")
cv2.rectangle(tools, (0,0), (max_x, max_y), (0,0,255), 2)
cv2.line(tools, (50,0), (50,50), (0,0,255), 2)
cv2.line(tools, (100,0), (100,50), (0,0,255), 2)
cv2.line(tools, (150,0), (150,50), (0,0,255), 2)
cv2.line(tools, (200,0), (200,50), (0,0,255), 2)
'''

cap = cv2.VideoCapture(0)
while True:
    ret, frm = cap.read()
    if not ret or frm is None:
        break

    frame_h, frame_w = frm.shape[:2]
    if mask is None or mask.shape != (frame_h, frame_w):
        mask = np.ones((frame_h, frame_w), dtype=np.uint8) * 255
    frm = cv2.flip(frm, 1)

    rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = hand_landmark.detect(mp_image)

    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            # draw.draw_landmarks(frm, hand_landmarks, hands.HAND_CONNECTIONS)
            x, y = int(hand_landmarks[8].x * frame_w), int(hand_landmarks[8].y * frame_h)

            if x < max_x and y < max_y and x > ml:
                if time_init:
                    ctime = time.time()
                    time_init = False
                ptime = time.time()

                cv2.circle(frm, (x, y), rad, (0, 255, 255), 2)
                rad -= 1

                if (ptime - ctime) > 0.8:
                    curr_tool = getTool(x)
                    print("your current tool set to : ", curr_tool)
                    time_init = True
                    rad = 40

            else:
                time_init = True
                rad = 40

            if curr_tool == "draw":
                xi, yi = int(hand_landmarks[12].x * frame_w), int(hand_landmarks[12].y * frame_h)
                y9 = int(hand_landmarks[9].y * frame_h)

                if index_raised(yi, y9):
                    cv2.line(mask, (prevx, prevy), (x, y), 0, thick)
                    prevx, prevy = x, y

                else:
                    prevx = x
                    prevy = y



            elif curr_tool == "line":
                xi, yi = int(hand_landmarks[12].x * frame_w), int(hand_landmarks[12].y * frame_h)
                y9 = int(hand_landmarks[9].y * frame_h)

                if index_raised(yi, y9):
                    if not (var_inits):
                        xii, yii = x, y
                        var_inits = True

                    cv2.line(frm, (xii, yii), (x, y), (50, 152, 255), thick)

                else:
                    if var_inits:
                        cv2.line(mask, (xii, yii), (x, y), 0, thick)
                        var_inits = False

            elif curr_tool == "rectangle":
                xi, yi = int(hand_landmarks[12].x * frame_w), int(hand_landmarks[12].y * frame_h)
                y9 = int(hand_landmarks[9].y * frame_h)

                if index_raised(yi, y9):
                    if not (var_inits):
                        xii, yii = x, y
                        var_inits = True

                    cv2.rectangle(frm, (xii, yii), (x, y), (0, 255, 255), thick)

                else:
                    if var_inits:
                        cv2.rectangle(mask, (xii, yii), (x, y), 0, thick)
                        var_inits = False

            elif curr_tool == "circle":
                xi, yi = int(hand_landmarks[12].x * frame_w), int(hand_landmarks[12].y * frame_h)
                y9 = int(hand_landmarks[9].y * frame_h)

                if index_raised(yi, y9):
                    if not (var_inits):
                        xii, yii = x, y
                        var_inits = True

                    cv2.circle(frm, (xii, yii), int(((xii - x) ** 2 + (yii - y) ** 2) ** 0.5), (255, 255, 0), thick)

                else:
                    if var_inits:
                        cv2.circle(mask, (xii, yii), int(((xii - x) ** 2 + (yii - y) ** 2) ** 0.5), (0, 255, 0), thick)
                        var_inits = False

            elif curr_tool == "erase":
                xi, yi = int(hand_landmarks[12].x * frame_w), int(hand_landmarks[12].y * frame_h)
                y9 = int(hand_landmarks[9].y * frame_h)

                if index_raised(yi, y9):
                    cv2.circle(frm, (x, y), 30, (0, 0, 0), -1)
                    cv2.circle(mask, (x, y), 30, 255, -1)

    op = cv2.bitwise_and(frm, frm, mask=mask)
    frm[:, :, 1] = op[:, :, 1]
    frm[:, :, 2] = op[:, :, 2]

    tool_left = min(ml, frame_w)
    tool_right = min(max_x, frame_w)
    tool_top = 0
    tool_bottom = min(max_y, frame_h)
    if tool_right > tool_left and tool_bottom > tool_top:
        roi_h = tool_bottom - tool_top
        roi_w = tool_right - tool_left
        if tools is None:
            tool_img = np.zeros((roi_h, roi_w, 3), dtype=np.uint8)
        else:
            tool_img = cv2.resize(tools, (roi_w, roi_h), interpolation=cv2.INTER_AREA)
        frm[tool_top:tool_bottom, tool_left:tool_right] = cv2.addWeighted(
            tool_img, 0.7, frm[tool_top:tool_bottom, tool_left:tool_right], 0.3, 0
        )

    cv2.putText(frm, curr_tool, (270 + ml, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("paint app", frm)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break
