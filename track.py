import cv2
import sys
import numpy as np

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


tracker_type = "CSRT"


def screen_init(frame):
    pts = []

    # def draw_circle(event, x, y, flags, param):
    #     if event == cv2.EVENT_LBUTTONDBLCLK:
    #         cv2.circle(frame, (x, y), 5, (0, 255, 255), -1)
    #         pts.append([x, y])

    # cv2.namedWindow('image')
    # cv2.setMouseCallback('image', draw_circle)  #<=====here

    # while (1):
    #     cv2.imshow('image', frame)
    #     if cv2.waitKey(20) & 0xFF == 27:
    #         break
    # cv2.destroyAllWindows()

    bbox = cv2.selectROI(frame, False)
    pts = [(bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1]),
           (bbox[0], bbox[1] + bbox[3]),
           (bbox[0] + bbox[2], bbox[1] + bbox[3])]
    nummer = 9

    x_01 = np.linspace(pts[0][0], pts[1][0], num=nummer, dtype=np.int)
    y_01 = np.linspace(pts[0][1], pts[1][1], num=nummer, dtype=np.int)

    x_02 = np.linspace(pts[0][0], pts[2][0], num=nummer, dtype=np.int)
    y_02 = np.linspace(pts[0][1], pts[2][1], num=nummer, dtype=np.int)

    x_23 = np.linspace(pts[2][0], pts[3][0], num=nummer, dtype=np.int)
    y_23 = np.linspace(pts[2][1], pts[3][1], num=nummer, dtype=np.int)

    x_13 = np.linspace(pts[1][0], pts[3][0], num=nummer, dtype=np.int)
    y_13 = np.linspace(pts[1][1], pts[3][1], num=nummer, dtype=np.int)

    rect_pts = []
    for (x1, y1), (x2, y2) in zip(zip(x_01, y_01), zip(x_23, y_23)):
        xx = np.linspace(x1, x2, num=nummer, dtype=np.int)
        yy = np.linspace(y1, y2, num=nummer, dtype=np.int)
        for x, y in zip(xx, yy):
            cv2.circle(frame, (x, y), 2, (0, 255, 255), 2)
            rect_pts.append((x, y))

    rect_pts = np.array(rect_pts)
    init = np.array([0, 1, nummer, nummer + 1])
    nixs = [ix - 1 for ix in range(0, nummer * nummer, nummer)]
    ixs = np.array([
        init + ix
        for ix in range(nummer * nummer - nummer - 1) if ix not in nixs
    ],
                   dtype=np.int)
   
    return ixs, rect_pts, pts


def track_init(frame):
    tracker_type = "CSRT"
    tracker = cv2.TrackerCSRT_create()

    # Create a black image, a window and bind the function to window

    bbox = cv2.selectROI(frame, False)
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    return bbox, tracker


def fill_matches(frame, ixs, rect_pts, bbox, color=(255, 0, 255)):
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    p = (int((p1[0] + p1[0]) / 2), int((p1[1] + p1[1]) / 2))

    d_ret = [-1,rect_pts[ixs[0]]]
    for i, ix in enumerate(ixs):
        d = [i,rect_pts[ix]]
        cv2.rectangle(frame, tuple(d[1][0]), tuple(d[1][-1]), (0, 255, 255), 2)
        cv2.putText(frame, str(i), (d[1][0][0],d[1][-1][1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)

        result1 = cv2.pointPolygonTest(d[1], p, False)
        if (result1 >= 0):
            cv2.fillPoly(frame, pts=[d[1]], color=(0, 255, 255))
            cv2.rectangle(frame, tuple(d[1][0]), tuple(d[1][-1]), color, -1)
            d_ret = d
    return frame, d_ret


# def track(frame,lines,bbox,tracker):
def track(frame, ixs, rect_pts, bbox, tracker):
    timer = cv2.getTickCount()

    # Update tracker
    ok, bbox = tracker.update(frame)

    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    # Draw bounding box
    screen_box = (-1, bbox)
    if ok:
        
        frame, screen_box = fill_matches(frame, ixs, rect_pts, bbox)
      
        screen_box = (screen_box[0], cv2.boundingRect(np.array(screen_box[1])))
    else:
        # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Display tracker type on frame
    cv2.putText(frame, tracker_type + " Tracker", (100, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    # Display FPS on frame
    cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    return frame, bbox, screen_box


if __name__ == '__main__':

    tracker_type = "CSRT"
    tracker = cv2.TrackerCSRT_create()
    video = cv2.VideoCapture(1)
    if not video.isOpened():
        print("Video Capture Failed: Connect MYNTEYE S STEREO CAMERA")
        sys.exit()

    # Read first frame.
    for i in range(50):
        ok, frame = video.read()
    # lines,screen_pts = screen_init(frame)
    ixs, rect_pts, screen_pts = screen_init(frame)

   
    bbox, tracker = track_init(frame)
   

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        frame, bbox, screen_box = track(frame, ixs, rect_pts, bbox, tracker)

        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27: break
