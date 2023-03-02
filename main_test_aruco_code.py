import time
from parameters import run_status, FPS, DRONE_POS, RAD2DEG
from subsys_display_view import Display
from subsys_read_cam import ReadCAM
from subsys_read_keyboard import ReadKeyboard
from subsys_markers_detected import MarkersDetected
from subsys_select_target_marker import SelectTargetMarker


def setup():

    ReadCAM.setup()
    Display.setup()
    ReadKeyboard.setup()
    MarkersDetected.setup()
    SelectTargetMarker.setup()


def run():
    # run keyboard subsystem

    rc_status_1, key_status, mode_status = ReadKeyboard.run(rc_threshold=40)
    frame = ReadCAM.run()

    markers_status, frame = MarkersDetected.run(frame)
    marker_status = SelectTargetMarker.run(
        frame, markers_status, DRONE_POS, offset=(0, 0))

    Display.run(frame,
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
    ReadCAM.stop()
    MarkersDetected.stop()
    SelectTargetMarker.stop()


if __name__ == "__main__":
    setup()

    while run_status.value:
        run()

    stop()
