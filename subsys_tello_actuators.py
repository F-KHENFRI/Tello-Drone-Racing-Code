

class TelloActuators:
    TELLO = None

    @classmethod
    def setup(cls, tello):
        cls.TELLO = tello

    @classmethod
    def run(cls, rc_status):
        cls.update_rc_command(rc_status)

    @classmethod
    def update_rc_command(cls, rc_status):
        """Update routine. Send velocities to Tello.
        """
        cls.TELLO.send_rc_control(
            rc_status.a,  # left_right_velocity,
            rc_status.b,  # for_back_velocity,
            rc_status.c,  # up_down_velocity,
            rc_status.d,  # yaw_velocity,
        )
