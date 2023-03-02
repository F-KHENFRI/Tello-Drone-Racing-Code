from parameters import DEG2RAD, RAD2DEG
import numpy as np

# output of subsystem


class rc_status:
    a = 0
    b = 0
    c = 0
    d = 0

# subsystem


class VisualControl:
    KP_LR_CTRL = 0.2
    KP_YAW_CTRL = 0.5
    cmp = 0

    @classmethod
    def setup(cls):
        pass

    @classmethod
    def run(cls, target_marker, drone_status):
        if target_marker.id == -1:
            rc_status.c = 0
            rc_status.d = int(0.99*rc_status.d)    # yaw_velocity
            rc_status.a = int(0.99*rc_status.a)    # left_right_velocity
            # wait for the drone to pass the last Gate
            if cls.cmp > 10:
                rc_status.b = int(0.99*rc_status.b)  # for_back_velocity

            cls.cmp = cls.cmp + 1
            return rc_status
        cls.cmp = 0
        # Get the angle and the distance between the marker and the drone
        phi = int(target_marker.m_angle * RAD2DEG)
        distance = target_marker.m_distance

        # Yaw velocity control
        rc_status.d = int(cls.KP_YAW_CTRL * phi)

        # Left/Right velocity control
        DX = distance * np.sin(phi*DEG2RAD)
        rc_status.a = int(cls.KP_LR_CTRL * DX)

        # Forward/Backward velocity control
        rb_threshold = 40
        rc_status.b = rb_threshold - int(rb_threshold * abs(phi)/70)

        # Up/Down velocity control
        rc_status.c = 0

        return rc_status

    @classmethod
    def stop(cls):
        pass
