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

    # FIX 1: Check if bbox is not empty (length > 0) instead of "not None"
    if len(bbox) > 0:
        
        # FIX 2: Grab the first detected QR code's data and bounding box
        current_data = data[0]
        current_bbox = bbox[0]

        # Now use current_bbox instead of bbox[0]
        pt1 = tuple(current_bbox[0].astype(int))
        pt2 = tuple(current_bbox[2].astype(int))
        
        if(pt1[0] < pt2[0]):
            if(pt1[1] < pt2[1]):
                pt1Zone = ((pt1[0] - padding), (pt1[1] - padding))
                pt2Zone = ((pt2[0] + padding), (pt2[1] + padding))
            else:
                pt1Zone = ((pt1[0] - padding), (pt1[1] + padding))
                pt2Zone = ((pt2[0] + padding), (pt2[1] - padding))
        else:
            if(pt1[1] < pt2[1]):
               pt1Zone = ((pt1[0] + padding), (pt1[1] - padding))
               pt2Zone = ((pt2[0] - padding), (pt2[1] + padding))
            else:
                pt1Zone = ((pt1[0] + padding), (pt1[1] + padding))
                pt2Zone = ((pt2[0] - padding), (pt2[1] - padding))
        
        cv2.rectangle(img, pt1, pt2, color=(255, 0, 0), thickness=2)
        # print(f'pt1: {pt1}, pt2: {pt2}')
        
        cv2.rectangle(img, pt1Zone, pt2Zone, color=(0,255,0), thickness=2)
        # print(f'pt1Zone: {pt1Zone}, pt2Zone: {pt2Zone}')

        # FIX 3: Use current_data (string) for putText
        cv2.putText(img, current_data,
                    (int(current_bbox[0][0]), int(current_bbox[0][1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 250, 120), 2)

        learned = h1.learnedBlocks()
        id = learned[0].ID
        if id == 1:
            color = "Rose"
                 
            
            

        if current_data:
            print(current_data + " " +color)

    cv2.imshow("code detector", img)

    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
picam2.stop()