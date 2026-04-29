import cv2
from picamera2 import Picamera2
from huskylib import *

h1 = HuskyLensLibrary("I2C", "", address=0x32)

if not h1.knock():
    print("HuskyLens not responding — check I2C wiring and address")
    exit(1)

h1.algorthim("ALGORITHM_COLOR_RECOGNITION")

picam2 = Picamera2()

main  = {"format": 'RGB888', "size": (640, 400)}
picam2.configure(picam2.create_preview_configuration(main))
picam2.set_controls({"AnalogueGain" : 7.0})   
picam2.start() 

detector = cv2.wechat_qrcode_WeChatQRCode()
padding = 30
color = ""

while True:
    img = picam2.capture_array()
    
    data, bbox = detector.detectAndDecode(img)

    if len(bbox) > 0:
        
        current_data = data[0]
        current_bbox = bbox[0]

        pt1 = tuple(current_bbox[0].astype(int))
        pt2 = tuple(current_bbox[2].astype(int))
        

        
        cv2.rectangle(img, pt1, pt2, color=(255, 0, 0), thickness=2)


        cv2.putText(img, current_data,
                    (int(current_bbox[0][0]), int(current_bbox[0][1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 250, 120), 2)


        learned = h1.learnedBlocks()
        print(learned)
        # if learned and len(learned) > 0:
        #     id = learned[0].ID
        #     if id == 1:
        #         color = "Rose"
                 
            
            

        if current_data:
            print(current_data + " " +color)

    cv2.imshow("code detector", img)

    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
picam2.stop()