from parameters import cv2

# output of subsystem


class markers_status:
    corners = []
    ids = []


# subsystem
class MarkersDetected:

    PARAM_DRAW_MARKERS = True

    @classmethod
    def setup(cls):
        pass

    @classmethod
    def run(cls, frame):
        cp_frame = frame.copy()
        corners, ids = cls.__find_markers(cp_frame)
        if cls.PARAM_DRAW_MARKERS and ids is not None:
            cls.__draw_markers(cp_frame, corners, ids)

        markers_status.ids = ids
        markers_status.corners = corners
        return markers_status, cp_frame

    @classmethod
    def stop(cls):
        pass

    @classmethod
    def __find_markers(cls, frame):
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_100)
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, _ = cv2.aruco.detectMarkers(
            gray, aruco_dict, parameters=parameters
        )

        return corners, ids

    @classmethod
    def __draw_markers(cls, frame, corners, ids):
        cv2.aruco.drawDetectedMarkers(
            frame, corners, ids, borderColor=(100, 0, 240))
