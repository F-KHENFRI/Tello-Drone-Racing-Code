from parameters import RED, cv2, np
# output of subsystem


class marker_status:
    id = -1
    corners = []
    # Origin axis
    center_pt = (0, 0)
    # Horizontal axis
    top_pt = (0, 0)
    bottom_pt = (0, 0)
    # Vertical axis
    left_pt = (0, 0)
    right_pt = (0, 0)

    # Horizontal angle
    h_angle = 0
    # Vertical angle
    v_angle = 0
    # angle and distance between marker and drone
    m_angle = 0
    m_distance = 0

    height = 0
    width = 0

    @classmethod
    def reset(cls):
        cls.id = -1
        cls.corners = []
        cls.center_pt = (0, 0)
        cls.top_pt = (0, 0)
        cls.bottom_pt = (0, 0)
        cls.left_pt = (0, 0)
        cls.right_pt = (0, 0)
        cls.h_angle = 0
        cls.v_angle = 0
        cls.m_angle = 0
        cls.m_distance = 0
        cls.height = 0
        cls.width = 0

# subsystem


class SelectTargetMarker:
    @classmethod
    def setup(cls):
        marker_status.reset()

    @classmethod
    def stop(cls):
        pass

    @classmethod
    def run(cls, frame, markers, drone_pos, offset=(0, 0)):

        cls.drone_pos = drone_pos
        id, corners = cls._get_marker_with_min_id(markers)
        if id == -1:
            marker_status.reset()
            return marker_status

        br, bl, tl, tr = corners[0], corners[1], corners[2], corners[3]
        center_pt = cls._get_midpoint([br, bl, tl, tr])
        # get symmetry axes
        left_pt = cls._get_midpoint([bl, tl])
        right_pt = cls._get_midpoint([br, tr])
        bottom_pt = cls._get_midpoint([br, bl])
        top_pt = cls._get_midpoint([tl, tr])

        height = cls._length_segment(bottom_pt, top_pt)
        width = cls._length_segment(left_pt,   right_pt)

        h_angle = cls._angle_between(left_pt, right_pt)
        v_angle = cls._angle_between(top_pt, bottom_pt, vertical=True)

        cls.offset = (int(offset[0]*width), int(offset[1]*height))
        cls.marker_pos = (center_pt[0] + cls.offset[0],
                          center_pt[1] + cls.offset[1])
        m_angle = cls._angle_between(drone_pos,  cls.marker_pos, vertical=True)
        m_distance = cls._length_segment(drone_pos, cls.marker_pos)

        cls.draw(frame)

        # update output
        marker_status.id = id
        marker_status.corners = corners
        marker_status.center_pt = center_pt
        marker_status.left_pt = left_pt
        marker_status.right_pt = right_pt
        marker_status.bottom_pt = bottom_pt
        marker_status.top_pt = top_pt
        marker_status.h_angle = h_angle
        marker_status.v_angle = v_angle
        marker_status.m_angle = m_angle
        marker_status.m_distance = m_distance
        marker_status.height = height
        marker_status.width = width
        return marker_status

    @staticmethod
    def _get_marker_with_min_id(markers):
        target_id = -1
        target_corners = []

        if markers.ids is None:
            return target_id, target_corners

        for i in range(len(markers.ids)):
            id = markers.ids[i][0]
            if id < target_id or target_id == -1:
                target_id = id
                target_corners = markers.corners[i][0]

        return target_id, target_corners

    @staticmethod
    def _get_midpoint(corners):
        # corners = [p1,p2,p3,p4] with pi = (xi, yi)
        xc = yc = 0
        n = len(corners)
        for x, y in corners:
            xc += x
            yc += y
        xc = int(xc/n)
        yc = int(yc/n)
        return (xc, yc)

    @staticmethod
    def _angle_between(p1, p2, vertical=False):
        dx = p1[0]-p2[0]
        dy = p1[1]-p2[1]
        if not vertical:  # angle betwenn Horizantal axis and segment (p1,p2)
            return np.arctan(-dy/(dx+0.000001))
        else:  # angle betwenn vertical axis and segment (p1,p2)
            return np.arctan(-dx/(dy+0.000001))

    @staticmethod
    def _length_segment(p1, p2):
        return int(np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2))

    @classmethod
    def draw(cls, frame):
        if marker_status.id == -1:
            return
        cv2.aruco.drawDetectedMarkers(frame, np.array([[marker_status.corners]]), np.array([
            [marker_status.id]]), borderColor=RED)

        cv2.line(frame, marker_status.top_pt,
                 marker_status.bottom_pt, (255, 0, 0), 2)
        cv2.line(frame, marker_status.left_pt,
                 marker_status.right_pt, (255, 0, 0), 2)
        top_pt_with_offset = tuple(
            np.array(marker_status.top_pt) + np.array(cls.offset))
        bottom_pt_with_offset = tuple(
            np.array(marker_status.bottom_pt) + np.array(cls.offset))
        left_pt_with_offset = tuple(
            np.array(marker_status.left_pt) + np.array(cls.offset))
        right_pt_with_offset = tuple(
            np.array(marker_status.right_pt) + np.array(cls.offset))
        cv2.line(frame,
                 top_pt_with_offset,
                 bottom_pt_with_offset,
                 (255, 0, 0), 2)
        cv2.line(frame,
                 left_pt_with_offset,
                 right_pt_with_offset,
                 (255, 0, 0), 2)

        if cls.drone_pos[0] != 0:
            cv2.line(frame,
                     cls.drone_pos,
                     cls.marker_pos,
                     (0, 0, 255), 2)
