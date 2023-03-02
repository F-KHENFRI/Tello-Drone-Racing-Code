import time
from parameters import ENV, run_status, FPS, DRONE_POS, RAD2DEG
from subsys_display_view import Display
from subsys_read_keyboard import ReadKeyboard
from subsys_markers_detected import MarkersDetected
from subsys_select_target_marker import SelectTargetMarker
from subsys_tello_sensors import TelloSensors
from subsys_tello_actuators import TelloActuators


def setup():
    ENV.status = ENV.SIMULATION
    TelloSensors.setup()
    TelloActuators.setup(TelloSensors.TELLO)
    Display.setup()
    ReadKeyboard.setup()
    MarkersDetected.setup()
    SelectTargetMarker.setup()


def run():
    # run keyboard subsystem
    rc_status, key_status, mode_status = ReadKeyboard.run(rc_threshold=40)
    frame, drone_status = TelloSensors.run(mode_status)
    markers_status, frame = MarkersDetected.run(frame)
    marker_status = SelectTargetMarker.run(
        frame, markers_status, DRONE_POS, offset=(-4, 0))

    TelloActuators.run(rc_status)

    Display.run(frame,
                Battery=drone_status.battery,
                Roll=drone_status.roll,
                Pitch=drone_status.pitch,
                Yaw=drone_status.yaw,
                X=drone_status.x,
                Y=drone_status.y,
                Z=drone_status.z,
                Mode=mode_status.value,
                LeftRight=rc_status.a,
                ForBack=rc_status.b,
                UpDown=rc_status.c,
                YawRC=rc_status.d,
                id=marker_status.id,
                H_angle=int(marker_status.h_angle * RAD2DEG),
                v_angle=int(marker_status.v_angle * RAD2DEG),
                m_angle=int(marker_status.m_angle * RAD2DEG),
                m_distance=marker_status.m_distance,
                m_height=marker_status.height,
                m_width=marker_status.width,
                )

    time.sleep(1 / FPS)


def stop():
    Display.stop()
    TelloSensors.stop()
    TelloActuators.stop()
    ReadKeyboard.stop()
    MarkersDetected.stop()
    SelectTargetMarker.stop()


if __name__ == "__main__":
    setup()

    while run_status.value:
        run()

    stop()
