import cv2
from yolo import YOLO
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", default = 0, help="Path to video file")
ap.add_argument('-s', '--size', default=412, help='Size for yolo')
ap.add_argument('-c', '--confidence', default=0.75, help='Confidence for yolo')
args = ap.parse_args()

classes = ["mask", "bad mask", "no mask"]

print("loading yolov4...")
yolov4 = YOLO("models/mask-yolov4.cfg", "models/mask-yolov4.weights", classes)

print("loading yolov3-tiny-prn...")
yoloprn = YOLO("models/mask-yolov3-tiny-prn.cfg", "models/mask-yolov3-tiny-prn.weights", classes)

print("loading yolov4-tiny...")
yolotiny = YOLO("models/mask-yolov4-tiny.cfg", "models/mask-yolov4-tiny.weights", classes)

yolo = yolotiny
colors = [(0, 255, 0), (0, 165, 255), (0, 0, 255)]
yolo.size = int(args.size)
yolo.confidence = float(args.confidence)
args.video = "Stream1Recording.avi"

def main():

    print("Press 1 for pre-recorded videos, 2 for live stream: ")
    option = int(input())

    if option == 1:
        # Recorded video
        windowName1 = "Recorded Video"
        capture1 =   cv2.VideoCapture(args.video) # path to video

        # define size for recorded video frame for video 1
        width1 = int(capture1.get(3))
        height1 = int(capture1.get(4))
        size1 = (width1, height1)

        optputFile1 = cv2.VideoWriter(
            'MaskDetection.avi', cv2.VideoWriter_fourcc(*'MJPG'), 20, size1)

        # check if feed exists or not for camera 1
        if capture1.isOpened():
            ret1, frame1 = capture1.read()     
        else:
            ret1 = False

        print("Running Yolo on video")
        while ret1:
            width, height, inference_time, results = yolo.inference(frame1)
            for detection in results:
                id, name, confidence, x, y, w, h = detection
                cx = x + (w / 2)
                cy = y + (h / 2)

                # draw a bounding box rectangle and label on the image
                color = colors[id]
                cv2.rectangle(frame1, (x, y), (x + w, y + h), color, 2)
                text = "%s (%s)" % (name, round(confidence, 2))
                cv2.putText(frame1, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, 2)

            cv2.imshow(windowName1, frame1)
            optputFile1.write(frame1)
            ret1, frame1 = capture1.read()

            # escape key (27) to exit
            if cv2.waitKey(1) == 27:
                break

        print("Done")
        capture1.release()
        optputFile1.release()
        cv2.destroyAllWindows()

    elif option == 2:
        # live stream
        capture1 = cv2.VideoCapture(0)  # laptop's camera
        capture2 = cv2.VideoCapture("http://10.130.9.242:9099/video")
        capture3 = cv2.VideoCapture("http://10.130.11.182:4747/video")  

        windowName1 = "Live Stream Camera 1"
        cv2.namedWindow(windowName1)

        if capture1.isOpened():  # check if feed exists or not for camera 1
            ret1, frame1 = capture1.read()
        else:
            ret1 = False
        
        windowName2 = "Live Stream Camera 2"
        cv2.namedWindow(windowName2)

        if capture2.isOpened():  # check if feed exists or not for camera 2
            ret2, frame2 = capture2.read()
        else:
            ret2 = False
        
        windowName3 = "Live Stream Camera 3"
        cv2.namedWindow(windowName3)

        if capture3.isOpened():  # check if feed exists or not for camera 3
            ret3, frame3 = capture3.read()
        else:
            ret3 = False


        while ret1 and ret2 and ret3:
            width, height, inference_time, results = yolo.inference(frame1)
            for detection in results:
                id, name, confidence, x, y, w, h = detection
                cx = x + (w / 2)
                cy = y + (h / 2)

                # draw a bounding box rectangle and label on the image
                color = colors[id]
                cv2.rectangle(frame1, (x, y), (x + w, y + h), color, 2)
                text = "%s (%s)" % (name, round(confidence, 2))
                cv2.putText(frame1, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, 2)

            #print(windowName1)
            cv2.imshow(windowName1, frame1)
            ret1, frame1 = capture1.read()


            width2, height2, inference_time2, results2 = yolo.inference(frame2)
            for detection2 in results2:
                id2, name2, confidence2, x2, y2, w2, h2 = detection2
                cx2 = x2 + (w2 / 2)
                cy2 = y2 + (h2 / 2)

                # draw a bounding box rectangle and label on the image
                color = colors[id2]
                cv2.rectangle(frame2, (x2, y2), (x2 + w2, y2 + h2), color, 2)
                text2 = "%s (%s)" % (name2, round(confidence2, 2))
                cv2.putText(frame2, text2, (x2, y2 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, 2)
            
            #print(windowName2)
            cv2.imshow(windowName2, frame2)
            ret2, frame2 = capture2.read()


            width3, height3, inference_time3, results3 = yolo.inference(frame3)
            for detection3 in results3:
                id3, name3, confidence3, x3, y3, w3, h3 = detection3
                cx3 = x3 + (w3 / 2)
                cy3 = y3 + (h3 / 2)

                # draw a bounding box rectangle and label on the image
                color = colors[id3]
                cv2.rectangle(frame3, (x3, y3), (x3 + w3, y3 + h3), color, 2)
                text3 = "%s (%s)" % (name3, round(confidence3, 2))
                cv2.putText(frame3, text3, (x3, y3 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, 2)
            
            #print(windowName3)
            cv2.imshow(windowName3, frame3)
            ret3, frame3 = capture3.read()

            if cv2.waitKey(1) == 27:
                break

        capture1.release()
        capture2.release()
        capture3.release()
        cv2.destroyAllWindows()

    else:
        print("Invalid option entered. Exiting...")


main()
