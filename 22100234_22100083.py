import cv2

def main():

    print("Press 1 for pre-recorded videos, 2 for live stream: ")
    option = int(input())

    capture2 = cv2.VideoCapture("http://192.168.61.235:9099/video")
    capture3 = cv2.VideoCapture("http://192.168.61.208:8080/video")   # sample code for mobile camera video capture using IP camera

    if option == 1:
        # Record video
        windowName1 = "Sample Feed from Camera 1"
        windowName2 = "Sample Feed from Camera 2"
        windowName3 = "Sample Feed from Camera 3"
        capture1 = cv2.VideoCapture(0)  # laptop's camera

        # define size for recorded video frame for video 1
        width1 = int(capture1.get(3))
        height1 = int(capture1.get(4))
        size1 = (width1, height1)

        width2 = int(capture2.get(3))
        height2 = int(capture2.get(4))
        size2 = (width2, height2)

        width3 = int(capture3.get(3))
        height3 = int(capture3.get(4))
        size3 = (width3, height3)

        # frame of size is being created and stored in .avi file
        optputFile1 = cv2.VideoWriter(
            'Stream1Recording.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, size1)

        optputFile2 = cv2.VideoWriter(
            'Stream2Recording.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, size2)
        
        optputFile3 = cv2.VideoWriter(
          'Stream3Recording.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, size3)

        # check if feed exists or not for camera 1
        if capture1.isOpened():
            ret1, frame1 = capture1.read()     
        else:
            ret1 = False

        if capture2.isOpened():
            ret2, frame2 = capture2.read()     
        else:
            ret2 = False
        
        if capture3.isOpened():
            ret3, frame3 = capture3.read()     
        else:
            ret3 = False

        while ret1 and ret2 and ret3:
            ret1, frame1 = capture1.read()
            ret2, frame2 = capture2.read()
            ret3, frame3 = capture3.read()

            # sample feed display from cameras
            cv2.imshow(windowName1, frame1)
            cv2.imshow(windowName2, frame2)
            cv2.imshow(windowName3, frame3)

            # saves the frame from cameras
            optputFile1.write(frame1)
            optputFile2.write(frame2)
            optputFile3.write(frame3)

            # escape key (27) to exit
            if cv2.waitKey(1) == 27:
                break

        capture1.release()
        optputFile1.release()
        capture2.release()
        optputFile2.release()
        capture3.release()
        optputFile3.release()
        cv2.destroyAllWindows()

    elif option == 2:
        # live stream

        windowName1 = "Live Stream Camera 1"
        cv2.namedWindow(windowName1)

        capture1 = cv2.VideoCapture(0)  # laptop's camera

        if capture1.isOpened():  # check if feed exists or not for camera 1
            ret1, frame1 = capture1.read()
            ret2, frame2 = capture2.read()
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
            ret1, frame1 = capture1.read()
            cv2.imshow(windowName1, frame1)

            ret2, frame2 = capture2.read()
            cv2.imshow(windowName2, frame2)

            ret3, frame3 = capture3.read()
            cv2.imshow(windowName3, frame3)

            if cv2.waitKey(1) == 27:
                break

        capture1.release()
        capture2.release()
        capture3.release()
        cv2.destroyAllWindows()

    else:
        print("Invalid option entered. Exiting...")


main()
