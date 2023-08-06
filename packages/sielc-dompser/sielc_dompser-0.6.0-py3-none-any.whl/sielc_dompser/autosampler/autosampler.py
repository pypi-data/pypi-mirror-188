import atexit
import time
import logging

from enum import IntEnum

from ftdi_serial import Serial


class AutosamplerError(Exception):
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg


class ProtocolError(AutosamplerError):
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg


class CommandStateValues(IntEnum):
    """command state values"""
    GETTING_READY = 0
    INJECTION = 1
    WASHING = 2
    SHAKING = 3


class CommandStateResponses(IntEnum):
    """command state responses"""
    READY = 0
    INJECTION = 1
    WASHING = 2
    SHAKING = 3
    GETTING_READY = 4
    ERROR = 5  # WHY IS ERROR NOT NEGATIVE?!?!?!


class AutosamplerProtocol:
    # variables [letter][int] to send to the autosampler to updated (write) or read parameters
    # protocol A - system
    RESET_MCU = 'A1'
    FIRMWARE_VERSION = 'A3'
    PROTOCOL_VERSION = 'A4'
    DEVICE_SERIAL_NUMBER_VERSION = 'A10'
    # protocol B
    COMMAND_STATE = 'B1'
    COMMAND_STATE_VALUES = {
        0: 'Getting ready',
        1: 'Injection',
        2: 'Washing',
        3: 'Shaking',
    }
    COMMAND_STATE_RESPONSES = {
        0: 'Ready',
        1: 'Injection',
        2: 'Washing',
        3: 'Shaking',
        4: 'Getting ready',
        5: 'Error',

    }
    INJECTION_CONTROL = 'B3'
    VIAL_NUMBER = 'B4'
    SAMPLE_VOLUME = 'B5'  # amount of sample to get from a vial in microliters
    SYRINGE_REFILL_SPEED = 'B7'  # in uL/min
    SYRINGE_DRAW_SPEED = 'B8'  # in uL/min
    # protocol C - arm
    ARM_ANGLE = 'C2'  # arm position, angle of rotation in int
    ARM_ANGLE_VALUES = {
        1000100: "Recalibrate arm angle of rotation",
        1000200: "Abort moving the arm angle of rotation",
    }  # also values between 0 and 9000 will move the arm angle to that degree/100 (0.00 - 90.00 degrees)
    ARM_ANGLE_RESPONSES = {
        -100: "Arm rotation position unknown",
        -200: "Finding the arm rotation position (in progress)"
        # if the value is between 0-9000, arm is not moving, position is 0-90.00 degrees
        # if the value is 200XXXX, then the arm is moving (increasing angle) to XX.XX (XXXX/100) real arm position
        # if the value is 300XXXX, then the arm is moving (decreasing angle) to XX.XX (XXXX/100) real arm position
    }
    # protocol D - tray
    SHAKING_MODE = 'D2'
    SHAKING_MODE_RESPONSES = {
        0: 'No shaking',
        1: 'Shaking mode 1',
        2: 'Shaking mode 2',
        3: 'Shaking mode 3',
    }
    SHAKING_TIME = 'D3'
    TRAY_ANGLE = 'D4'
    TRAY_ANGLE_VALUES = {
        1000100: 'Recalibrate tray angle',
        1000200: 'Abort tray move'
    }  # get/set the tray angle, takes value 0 - 35999, where the value is the tray position in angle * 100 (degrees)
    TRAY_ANGLE_RESPONSES = {
        # a response of 20XXXXX, means the tray is moving to position XXXXX = XXX.XX degrees
        # a response of 0-35999, means the tray is at that position in degrees
        -100: 'Lost tray position',
        -200: 'Finding tray position (in progress)',
        -300: 'Tray shaking',
    }
    # protocol E - arm and tray
    MOVE_TRAY_AND_ARM = 'E1'
    MOVE_TRAY_AND_ARM_VALUES = {
        0: "Move tray and arm home (injection port)",
        10001: "Recalibrate tray and arm move",
        10002: "Abort tray and arm move",
    }
    for i in range(1, 49):
        MOVE_TRAY_AND_ARM_VALUES[i] = f"Move tray and arm to position {i}"
    MOVE_TRAY_AND_ARM_RESPONSES = {
        0: 'Tray and arm not moving, at home',
        20000: 'Moving tray and arm to home',  # doesnt appear in protocol list but encountered?
        -1: "Vial positioning error",
    }
    for i in range(1, 49):
        MOVE_TRAY_AND_ARM_RESPONSES[i] = f"Tray and arm not moving and vial is {i}"
        MOVE_TRAY_AND_ARM_RESPONSES[20000 + i] = f"Moving tray and arm home or to vial number {i}"
    # protocol F - needle
    NEEDLE_Y = 'F2'
    NEEDLE_Y_VALUES = {  # can move needle between 0 and n*100 mm
        1000100: "Recalibrate needle Y",
        1000200: "Abort needle Y move",
    }
    NEEDLE_Y_RESPONSES = {
        2000000: 'Needle moving to upper position',  # doesnt appear in protocol list but encountered? todo double check
        -100: "Needle Y position unknown",
        -200: 'Needle Y - Finding a sensor (in progress)',
    }
    for i in range(0, 5001):
        NEEDLE_Y_VALUES[i] = f"Move needle to {i / 100} mm. 0 is the bottom of the vial, 50 for upper position, " \
                             f"top of vial position ~ 38 mm"
        NEEDLE_Y_RESPONSES[i] = f"Needle not moving and position is {i / 100} mm"
        NEEDLE_Y_RESPONSES[2000000 + i] = f'Needle moving up, {i / 100} mm current position'
        NEEDLE_Y_RESPONSES[3000000 + i] = f'Needle moving down, {i / 100} mm current position'
        NEEDLE_Y_RESPONSES[600000 + i] = f'Needle in injection port, {i / 100} mm position'
        NEEDLE_Y_RESPONSES[700000 + i] = f'Needle in upper position, {i / 100} mm position'
    WASHING = 'F3'
    WASHING_VALUES = {
        0: 'Start washing',
        1: 'Stop washing'
    }
    WASHING_RESPONSES = {
        0: "Washing not started",
        1: 'Washing in progress',
    }
    # protocol G - valve
    VALVE_POSITION = 'G1'
    VALVE_POSITION_VALUES = {
        1: 'Valve move to position 1',
        2: 'Valve move to position 2',
        3: 'Valve move to position 3',
        4: 'Valve move to position 4',
        5: 'Valve move to position 5',
        10001: 'Recalibrate valve',
        10002: 'Abort valve movement',
    }
    VALVE_POSITION_RESPONSES = {
        -2: 'Valve finding sensor (in progress)',
        -1: 'Valve position unknown',
        1: 'Valve not moving, at position 1',
        2: 'Valve not moving, at position 2',
        3: 'Valve not moving, at position 3',
        4: 'Valve not moving, at position 4',
        5: 'Valve not moving, at position 5',
        20001: 'Valve moving to position 1',
        20002: 'Valve moving to position 2',
        20003: 'Valve moving to position 3',
        20004: 'Valve moving to position 4',
        20005: 'Valve moving to position 5',
    }
    # protocol H - syringe
    # set plunger position in uL. between 0-4100 (0-4100 uL) for large syringe (low pressure) or 0-1000 (0.1-100 uL)
    # for small syringe (high pressure)
    PLUNGER_POSITION = 'H1'
    PLUNGER_POSITION_VALUES = {
        10001: 'Recalibrate zero (go to find zero, position will be 0)',
        10002: 'Abort (Stop doing anything with syringe)'
    }
    PLUNGER_POSITION_RESPONSES = {
        -2: 'Unknown plunger position and calibrating',
        -1: 'Unknown plunger position and not moving',
    }
    for i in range(0, 4101):
        PLUNGER_POSITION_VALUES[i] = f"Move plunger position to {i}"
        PLUNGER_POSITION_RESPONSES[i] = f"Current plunger position {i} (1, 2, 3...)"
        PLUNGER_POSITION_RESPONSES[20000 + i] = f"Refilling plunger to {20000 + i} (1, 2, 3...)"
        PLUNGER_POSITION_RESPONSES[30000 + i] = f"Drawing plunger to {30000 + i} (3, 2, 1...)"
    PLUNGER_DRAW_FLOW_RATE = 'H2'  # draw flow rate in uL/min, value bw 1-48000
    PLUNGER_REFILL_FLOW_RATE = 'H3'  # refill flow rate in uL/min, value bw 1-48000
    # protocol I - fan
    INTERNAL_FAN_SPEED = 'I1'  # fan speed in %, bw 0-100. good range is 50-100%


class Autosampler:
    def __init__(self,
                 port: str
                 ):
        self.logger = logging.getLogger(__name__)
        self._port = port
        self._baudrate = 115200
        self.ser: Serial = None
        self._waste_port_location: float = 8.0  # from testing, 8 degrees seemed good
        self._wash_line_volume: int = 0
        self.connect()

    @property
    def bottom_of_injection_port_height(self) -> float:
        """Found to be 3 mm; found by reading the needle position after power cycling the autosampler"""
        return 3.0

    @property
    def above_vial_height(self) -> float:
        """Height (mm) for the arm to move the needle so it is above a vial. ~38 mm"""
        return 38.0

    @property
    def top_of_vial_height(self) -> float:
        """Height (mm) for the arm to move the needle so it is at the top of a vial; if there is a cap on the vial
        the needle should be low enough to pierce it. ~25 mm"""
        return 25.0

    @property
    def bottom_of_waste_port_height(self) -> float:
        """From testing, seems like heigh (mm) for the needle to be at the bottom/in the waste port is ~ 25 mm"""
        return 25.0

    @property
    def waste_port_location(self) -> float:
        """The arm angle in degrees (possible values 0.00 - 90.00) so that the needle is above the waste port"""
        return self._waste_port_location

    @waste_port_location.setter
    def waste_port_location(self, value: float):
        """Value must be between 0.00 - 90.00"""
        if value is not None:
            if 0.00 <= round(value, 2) <= 90.00:
                self._waste_port_location = round(value, 2)

    @property
    def wash_line_volume(self) -> int:
        """The volume (uL) of the line between the plunger and the wash port; the volume to move liquid in the
        plunger from the plunger to the wash port"""
        return self._wash_line_volume

    @wash_line_volume.setter
    def wash_line_volume(self, value: int):
        """Wash line volume in uL"""
        if value is not None:
            self._wash_line_volume = int(value)

    def connect(self):
        try:
            if self.ser is None:
                ser = Serial(self._port,
                             baudrate=self._baudrate,
                             )
                self.ser = ser
            else:
                self.ser.connect()
            # Ensure that the serial port is closed on system exit
            atexit.register(self.disconnect)
        except Exception as e:
            raise e

    def disconnect(self):
        self.ser.disconnect()

    def firmware_version(self):
        response = self.read(AutosamplerProtocol.FIRMWARE_VERSION)
        self.logger.debug(f'Firmware version: {response}')
        return response

    # todo figure out what this really does
    def command_state(self):
        response = self.read(AutosamplerProtocol.COMMAND_STATE)
        self.logger.debug(f'Command state: {response}')
        return response

    # todo figure out what this really does
    def command_state_get_ready(self):
        response = self.update(AutosamplerProtocol.COMMAND_STATE, 0)
        self.logger.debug(f'Set command state {AutosamplerProtocol.COMMAND_STATE_VALUES[0]} response: {response}')
        return response

    # todo figure out what this really does
    def command_state_injection(self):
        response = self.update(AutosamplerProtocol.COMMAND_STATE, 1)
        self.logger.debug(f'Set command state {AutosamplerProtocol.COMMAND_STATE_VALUES[1]} response: {response}')
        return response

    # todo figure out what this really does
    def command_state_wash(self):
        response = self.update(AutosamplerProtocol.COMMAND_STATE, 2)
        self.logger.debug(f'Set command state {AutosamplerProtocol.COMMAND_STATE_VALUES[2]} response:  {response}')
        return response

    # todo, add wait, check works
    # def command_state_shake(self, duration: int = None, shaking_mode: [0, 1, 2, 3] = None):
    #     """
    #
    #     :param duration: seconds to shake for. if none, use the current shaking duration
    #     :param int, shaking_mode: 0 for no shaking, 1-3 to enable shaking modes 1-3, or leave as None to use the
    #         current shaking mode
    #     :return:
    #     """
    #     if shaking_mode is not None:
    #         self.shaking_mode(shaking_mode)
    #     response = self.update(AutosamplerProtocol.COMMAND_STATE, 3)
    #     self.logger.debug(f'Set command state {AutosamplerProtocol.COMMAND_STATE_VALUES[3]}')
    #     self.logger.debug(f'Shake for {duration} seconds')
    #     return response
    #
    # todo, add wait, check works
    # def shaking_mode(self, mode: [0, 1, 2, 3] = None):
    #     """
    #     Set shaking mode, or
    #     :param mode:
    #     :return:
    #     """
    #     if mode is not None:
    #         response = self.update(AutosamplerProtocol.SHAKING_MODE, mode)
    #         self.logger.debug(f'Set shaking mode to: {AutosamplerProtocol.SHAKING_MODE_RESPONSES[mode]}')
    #         # self.logger.debug(f'Set shaking mode response: {response}')
    #     response = self.read(AutosamplerProtocol.SHAKING_MODE)
    #     self.logger.debug(f'Current shaking mode: {AutosamplerProtocol.SHAKING_MODE_RESPONSES[response]}')
    #     return response
    #
    # todo, add wait, check works
    # def shaking_duration(self, duration: int = None):
    #     """
    #     Set shaking duration in seconds if duration is passed, and return current shaking time
    #
    #     :param duration: value between 0 and 10000 in seconds
    #     :return:
    #     """
    #     if duration is not None:
    #         if 0 > duration > 10000:
    #             raise ProtocolError(f'Shaking duration must be an int between 0 and 10000')
    #         response = self.update(AutosamplerProtocol.SHAKING_TIME, duration)
    #         self.logger.debug(f'Set shaking duration: {response} seconds')
    #         # self.logger.debug(f'Set shaking time response: {response}')
    #     response = self.read(AutosamplerProtocol.SHAKING_TIME)
    #     self.logger.debug(f'Current shaking duration: {response} seconds')
    #     return response

    # # todo, add wait, check works
    # def washing(self) -> bool:
    #     """
    #     False if washing not started, true if washing in progress
    #     :return:
    #     """
    #     response = self.read(AutosamplerProtocol.WASHING)
    #     self.logger.debug(f'{AutosamplerProtocol.WASHING_VALUES[response]}')
    #     return bool(response)
    #
    # # todo, add wait, check works
    # def start_washing(self):
    #     response = self.update(AutosamplerProtocol.WASHING, 1)
    #     self.logger.debug(f'{AutosamplerProtocol.WASHING_VALUES[1]}')
    #     self.logger.debug(f'Washing response: {response}')
    #     is_washing = self.washing()
    #     return is_washing
    #
    # # todo, add wait, check works
    # def stop_washing(self):
    #     response = self.update(AutosamplerProtocol.WASHING, 0)
    #     self.logger.debug(f'{AutosamplerProtocol.WASHING_VALUES[0]}')
    #     self.logger.debug(f'Washing response: {response}')
    #     is_washing = self.washing()
    #     return is_washing

    def recalibrate_needle(self, wait=True):
        if self.needle_in_injection_port() is False:
            self.home_tray_arm()
        response = self.move_needle(1000100, wait)
        # add hardcoded sleep because it seems like when recalibrating the needle the autosampler cant tell that the
        # needle is moving
        time.sleep(13)
        return response

    def needle_to_max_y_if_arm_near_tray(self):
        """
        Check if the arm is anywhere near the tray/vials; consider this the waste port location (angle) plus a fudge
        factor 0.5 degree. If it is then move the needle to the maximum y position. This might be necessary for some
        autosampler movements that might move the tray or arm, and its important that the needle by at the maximum y
        position so it doesnt get clipped by anything moving
        :return:
        """
        if self._arm_angle() > (self.waste_port_location + 0.5):
            # force the arm to be in the maximum y position
            if self.needle_in_upper_position() is False:
                self.needle_to_max_y()

    def needle_to_max_y(self):
        """
        Move needle to the upper position - 50.00 mm
        :return:
        """
        response = self.move_needle(50, wait=True)
        return response

    def needle_to_min_y(self):
        """
        Move needle to the bottom of the vial - 0.00 mm
        :return:
        """
        response = self.move_needle(0, wait=True)
        return response

    def needle_to_above_a_vial(self, n=None):
        """
        Move needle to the above a vial (38.0 mm). If n is passed in, then move to vial number n

        :param n: vial number, between 1 and 48
        :return:
        """
        if n is not None:
            if 1 <= n <= 48:
                self.move_tray_arm(n)
            else:
                raise ProtocolError(f'Cannot move to vial number {n}, value must be between 1 - 48')
        response = self.move_needle(self.above_vial_height, wait=True)
        return response

    def needle_to_top_of_vial(self, n=None):
        """
        Move needle to the top of the vial (25 mm). If there is a cap on the vial the needle
        should be low enough to pierce it. If n is passed in, then move to vial number n.

        :param n: vial number, between 1 and 48
        :return:
        """
        if n is not None:
            if 1 <= n <= 48:
                self.move_tray_arm(n)
            else:
                raise ProtocolError(f'Cannot move to vial number {n}, value must be between 1 - 48')
        response = self.move_needle(self.top_of_vial_height, wait=True)
        return response

    def needle_to_bottom_of_vial(self, n=None):
        """
        Move needle to the bottom of the vial (0.0 mm). If n is passed in, then move to vial number n

        :param n: vial number, between 1 and 48
        :return:
        """
        if n is not None:
            if 1 <= n <= 48:
                self.move_tray_arm(n)
            else:
                raise ProtocolError(f'Cannot move to vial number {n}, value must be between 1 - 48')
        response = self.needle_to_min_y()
        return response

    def needle_to_top_of_injection_port(self):
        """Move the needle so it is above the waste port; go to the max y height"""
        self.arm_to_injection_port()
        response = self.needle_to_max_y()
        return response

    def needle_to_bottom_of_injection_port(self):
        """Move the needle so it is above the waste port; """
        self.arm_to_injection_port()
        response = self.move_needle(self.bottom_of_injection_port_height)
        return response

    def needle_to_top_of_waste_port(self):
        """Move the needle so it is above the waste port; go to the max y height"""
        self.arm_to_waste_port()
        response = self.needle_to_max_y()
        return response

    def needle_to_bottom_of_waste_port(self):
        """From testing it seems like the bottom of the waste port is at height 25.0 mm, so move to that height"""
        self.needle_to_top_of_waste_port()
        response = self.move_needle(self.bottom_of_waste_port_height)
        return response

    def move_needle(self, y: float, wait: bool = True):
        """
        Move needle to the Y position in mm. Range can be 0-50.00 mm. Or send 1000100 to recalibrate or 1000200 to
        abort Y movement. 0 is the bottom of the vial and 50 is the upper position. Top of the vial is ~38 mm

        :param wait:
        :param y:
        :return:
        """
        if y == 1000100 or y == 1000200:
            y_formatted_for_protocol = y
        else:
            if 0 > y > 50:
                raise ProtocolError(f'Needle Y value must be 0 < y < 50.00 (mm)')
            y_formatted_for_protocol = int(y * 100)
        response = self.update(AutosamplerProtocol.NEEDLE_Y, y_formatted_for_protocol)
        if wait:
            while self._needle_moving():
                time.sleep(0.01)
            time.sleep(0.1)  # extra wait just in case things are still moving
        self.logger.debug(AutosamplerProtocol.NEEDLE_Y_VALUES[y_formatted_for_protocol])
        response = self.read(AutosamplerProtocol.NEEDLE_Y)
        return response

    def needle_position(self) -> int:
        response = self.read(AutosamplerProtocol.NEEDLE_Y)
        response = int(response)
        self.logger.debug(AutosamplerProtocol.NEEDLE_Y_RESPONSES[response])
        if response == -100:
            raise AutosamplerError('Needle position unknown')
        return response

    def needle_in_injection_port(self) -> bool:
        """
        True if needle is in the injection port
        :return:
        """
        response = self.needle_position()
        if 605000 >= response >= 600000:
            return True
        else:
            return False

    def needle_in_upper_position(self) -> bool:
        """
        True if needle is in the upper position (50.00 mm)
        :return:
        """
        response = self.needle_position()
        if 705000 >= response >= 700000:
            return True
        else:
            return False

    def _needle_moving(self) -> bool:
        response = self.needle_position()
        if 2005000 >= response >= 2000000 or 3005000 >= response >= 3000000:
            self.logger.debug('Needle moving')
            return True
        else:
            return False

    def arm_to_injection_port(self, wait=True) -> float:
        """
        Moves the arm so that it is above the injection port
        :param wait: if True, wait until all arm and needle movements have stopped before allowing this method to
            return. recommended to use True
        :return:
        """
        response = self.arm_angle(0, wait)
        return response

    def arm_to_waste_port(self, wait=True):
        """
        Moves the arm so that it is above the waste port
        :param wait: if True, wait until all arm and needle movements have stopped before allowing this method to
            return. recommended to use True
        :return:
        """
        response = self.arm_angle(self.waste_port_location, wait)
        return response

    def recalibrate_arm(self):
        """
        Recalibrate the arm angle position
        :return:
        """
        response = self.arm_angle(1000100, True)
        return response

    def abort_moving_arm(self):
        """
        Abort moving the arm
        :return:
        """
        response = self._arm_angle(1000200, True)
        return response

    def arm_angle(self, angle: float = None, wait: bool = True) -> float:
        """
        Get/set the position (angle in degrees of the arm), between 0.00 - 90.00 degrees. Force the needle to go to
        the maximum height if the arm will move

        :param angle: angle to move the arm to
        :param wait: if should wait for the movement to complete
        :return:
        """
        if angle is not None:
            if self.needle_in_upper_position() is False:
                self.needle_to_max_y()
        response = self._arm_angle(angle, wait)
        return response

    def _arm_moving(self) -> bool:
        """
        Return true if the arm is moving
        :return:
        """
        response = self._arm_angle()
        if 20000 <= response <= 30090:
            return True
        else:
            return False

    def _arm_angle(self, n: float = None, wait: bool = True) -> float:
        """
        Get/set the position (angle in degrees) of the arm. See AutosamplerProtocol.ARM_ANGLE_VALUES and
        self.ARM_ANGLE_RESPONSES for more details
        Warning. the needle must be in the upper position before calling this to move the arm

        :param n: angle to move to, or the code to recalibrate or abort arm movement
        :param wait: if should wait for the movement to complete
        :return:
        """
        if n is not None:
            if 0 <= n <= 90.00:
                # move arm angle position to XX.XX degrees
                n = int(round(n, 2) * 100)
            elif n == 1000100 or n == 1000200:
                # recalibration or abort arm movement
                n = int(n)
            else:
                raise ProtocolError(f'Move arm angle input must be one of '
                                    f'{list(AutosamplerProtocol.ARM_ANGLE_VALUES.keys())} or a value between 0.00 '
                                    f'and 90.00')
            self.update(AutosamplerProtocol.ARM_ANGLE, n)
            if AutosamplerProtocol.ARM_ANGLE_RESPONSES.keys().__contains__(n):
                self.logger.debug(AutosamplerProtocol.ARM_ANGLE_VALUES[n])
            else:
                self.logger.debug(f'Moving arm angle of rotation to {n/100} degrees')
            if wait:
                while self._arm_moving():
                    time.sleep(0.01)
                time.sleep(1)
            while self.read(AutosamplerProtocol.ARM_ANGLE) == -200:
                # while reading the arm angle is in progress, wait
                time.sleep(0.01)
        response = self.read(AutosamplerProtocol.ARM_ANGLE)
        if 0 <= response <= 9000:
            response = round(response / 100, 2)
            self.logger.debug(f'Arm not moving, angle is {response} degrees')
        elif 2000000 <= response <= 2009000:
            response = round(response / 100, 2)
            self.logger.debug(f'Arm angle is at {response - 20000} degrees and is increasing (moving away from '
                              f'injection port)')
        elif 3000000 <= response <= 3009000:
            response = round(response / 100, 2)
            self.logger.debug(f'Arm angle is at {response - 30000} degrees and is decreasing (moving towards injection '
                              f'port)')
        elif response == -100:
            # todo raise error or not?
            raise AutosamplerError('Arm angle position unknown')
        elif response == -200:
            self.logger.debug('Finding the arm angle position')
        return response

    def recalibrate_tray_arm(self, wait=True):
        """
        :return:
        """
        return
        # todo check why this doesnt work?
        response = self.move_tray_arm(10001, wait)
        return response

    def _tray_moving(self) -> bool:
        """
        Return true if the tray is moving
        :return:
        """
        response = self.tray_angle()
        if 20000 <= response <= 20359.99:
            return True
        else:
            return False

    def recalibrate_tray(self):
        """
        Recalibrate the tray. Force the needle to go to the maximum height in case it is in a vial
        :return:
        """
        self.needle_to_max_y_if_arm_near_tray()
        response = self._tray_angle(n=1000100)
        time.sleep(1)  # extra time to make sure tray isnt moving
        return response

    def tray_angle(self, angle: float = None, wait=True):
        """
        Get/set the tray rotation angle (angle in degrees), between 0.00 - 359.99 degrees. Force the needle to go to
        the maximum height if the tray is going to move

        :param angle: angle to move to
        :param wait: if should wait for the movement to complete
        :return:
        """
        if angle is not None:
            self.needle_to_max_y_if_arm_near_tray()
        response = self._tray_angle(angle, wait)
        return response

    def _tray_angle(self, n: float = None, wait: bool = True):
        """
        Get/set the tray rotation angle (angle in degrees). See AutosamplerProtocol.TRAY_ANGLE_VALUES and
        AutosamplerProtocol.TRAY_ANGLE_RESPONSES for more details

        :param n: angle to move to, or the code to recalibrate or abort arm movement
        :param wait: if should wait for the movement to complete
        :return:
        """
        if n is not None:
            if 0 <= n <= 359.99:
                # move tray angle position to XXX.XX degrees
                n = int(round(n, 2) * 100)
            elif n == 1000100:
                # recalibrate tray
                n = int(n)
            elif n == 1000200:
                # abort tray movement
                n = int(n)
            else:
                raise ProtocolError(f'Tray angle input must be a value between 0-10000 or one of '
                                    f'{list(AutosamplerProtocol.TRAY_ANGLE_VALUES.keys())}, given {n}')
            self.update(AutosamplerProtocol.TRAY_ANGLE, n)
            if AutosamplerProtocol.TRAY_ANGLE_VALUES.keys().__contains__(n):
                self.logger.debug(AutosamplerProtocol.TRAY_ANGLE_VALUES[n])
            else:
                self.logger.debug(f'Moving tray angle to {n/100} degrees')
            if wait:
                while self._tray_moving():
                    time.sleep(0.01)
                time.sleep(1)
            while self.read(AutosamplerProtocol.TRAY_ANGLE) == -200:
                # while reading the tray angle is in progress, wait
                time.sleep(0.01)
        response = self.read(AutosamplerProtocol.TRAY_ANGLE)
        if 0 <= response <= 35999:
            response = round(response / 100, 2)
            self.logger.debug(f'Tray not moving, angle is {response} degrees')
        elif 2000000 <= response <= 2035999:
            response = round(response / 100, 2)
            self.logger.debug(f'Tray is moving to angle {round(response - 20000, 2)} degrees')
        elif response == -100:
            # todo raise error or not?
            raise AutosamplerError('Tray angle position lost')
        elif response == -200 or response == -300:
            self.logger.debug(AutosamplerProtocol.TRAY_ANGLE_RESPONSES[response])
        return response

    def disable_tray_shaking(self):
        """
        Set the tray shaking mode to No shaking
        :return: the current set shaking mode
        """
        response = self.tray_shaking_mode(n=0)
        return response

    def tray_shaking_mode(self, n: int = None):
        """
        If n is set, then set the tray shaking mode to n. Return the current set shaking mode
        n can be:
            0 - no shaking
            1 - shaking mode 1
            2 - shaking mode 2
            3 - shaking mode 3

        :param n: the shaking mode to set
        :return: the current set shaking mode
        """
        response = self._tray_shaking_mode(n=n)
        return response

    def _tray_shaking_mode(self, n: int = None):
        """
        If n is set, then set the tray shaking mode to n. Return the current set shaking mode
        n can be:
            0 - no shaking
            1 - shaking mode 1
            2 - shaking mode 2
            3 - shaking mode 3

        :param n: the shaking mode to set
        :return: the current set shaking mode
        """
        if n is not None:
            if 0 > n > 3:
                raise ProtocolError(f'Shaking mode number should be 0-3, given {n}')
            self.update(AutosamplerProtocol.SHAKING_MODE, n)
            self.logger.debug(f'Set shaking mode to number to {AutosamplerProtocol.SHAKING_MODE_RESPONSES[n]}')
        response = self.read(AutosamplerProtocol.SHAKING_MODE)
        self.logger.debug(f'Current shaking mode is: {AutosamplerProtocol.SHAKING_MODE_RESPONSES[response]}')
        return response

    def _tray_shaking(self) -> bool:
        """
        Return True if the tray is shaking
        :return:
        """
        response = self.tray_angle()
        if response == -300:
            return True
        else:
            return False

    def shake_tray(self, t: int, wait=True):
        """
        Shake the tray in the currently set shaking mode for t seconds.
        While shaking, the autosampler LED is blue.
        Seems like after shaking the tray, the tray encounters an error (maybe tray angle position unknown) and the
        autosampler LED flashes orange/red, and the tray looks like it performs a recalibration automatically
        afterwards (tray does at least a 360 rotation). Therefore, force the needle to be in the maximum height to
        ensure it doesnt get hit by the needle

        :param int, t: seconds, 0-10000 for the tray to shake
        :param bool, wait: whether the script should wait until the tray finishes shaking or not
        :return:
        """
        self.needle_to_max_y_if_arm_near_tray()
        response = self._shake_tray(t=t, wait=wait)
        return response

    def _shake_tray(self, t: int, wait=True):
        """
        Shake the tray in the currently set shaking mode for t seconds

        :param int, t: seconds, 0-10000 for the tray to shake
        :param bool, wait: whether the script should wait until the tray finishes shaking or not
        :return:
        """
        self._tray_shaking_time(t=t)
        self.logger.debug(f'Set command state {AutosamplerProtocol.COMMAND_STATE_VALUES[3]}')
        response = self.update(AutosamplerProtocol.COMMAND_STATE, 3)
        self.logger.debug(f'Set command state is: {AutosamplerProtocol.COMMAND_STATE_RESPONSES[response]}')
        if response == 3:
            self.logger.debug(f'Shake for {t} seconds')
            if wait:
                time.sleep(t)
            while self._tray_shaking():
                # just in case the tray is still shaking, wait to make sure it isnt before returning
                time.sleep(0.1)
        else:
            # todo raise an error? or not?
            self.logger.error('Unable to set mode to shake')
        return response

    def _tray_shaking_time(self, t: int = None):
        """
        Get/set the time (s) that the tray should shake for

        :param int, t: seconds, 0-10000 for the tray to shake
        :return:
        """
        if t is not None:
            if 0 <= t <= 10000:
                pass
            else:
                raise ProtocolError(f'Tray shaking time must be between 0-10000, given {t}')
            self.update(AutosamplerProtocol.SHAKING_TIME, t)
            self.logger.debug(f'Set tray shaking time to {t} seconds')
        response = self.read(AutosamplerProtocol.SHAKING_TIME)
        self.logger.debug(f'Curent tray shaking time is {response} seconds')
        return response

    def home_tray_arm(self, wait=True):
        """
        Moves the tray and arm to the injection port home position.
        Warning, needle must be in the upper position before calling this
        :return:
        """
        response = self.move_tray_arm(0, wait)
        return response

    def move_tray_arm(self, n, wait=True):
        """
        Move the tray and arm to a position. Force the needle tothe maximum y position before moving so the needle
        doesn't get clipped by anything during movements

        For valid positions and descriptions see AutosamplerProtocol.MOVE_TRAY_AND_ARM_VALUES
        :param n: one of the keys of AutosamplerProtocol.MOVE_TRAY_AND_ARM_VALUES
        :param wait: if should wait for movement to complete
        :return:
        """
        if self.needle_in_upper_position() is False:
            self.needle_to_max_y()
        response = self._move_tray_arm(n, wait)
        return response

    def _move_tray_arm(self, n: int, wait=True):
        """
        Move the tray and arm to a position.
        Warning, needle must be in the upper position before calling this

        For valid positions and descriptions see AutosamplerProtocol.MOVE_TRAY_AND_ARM_VALUES
        :param n: one of the keys of AutosamplerProtocol.MOVE_TRAY_AND_ARM_VALUES
        :param wait: if should wait for movement to complete

        :return:
        """
        if AutosamplerProtocol.MOVE_TRAY_AND_ARM_VALUES.keys().__contains__(n) is False:
            raise ProtocolError(f'Move tray arm input must be one of '
                                f'{list(AutosamplerProtocol.MOVE_TRAY_AND_ARM_VALUES.keys())}, given {n}')
        self.update(AutosamplerProtocol.MOVE_TRAY_AND_ARM, n)
        if wait:
            while self._tray_arm_moving():
                time.sleep(0.01)
            time.sleep(0.1)  # extra wait just in case things are still moving
        self.logger.debug(AutosamplerProtocol.MOVE_TRAY_AND_ARM_VALUES[n])
        response = self._tray_arm_position()
        return response

    def _tray_arm_moving(self) -> bool:
        response = self._tray_arm_position()
        if 49 >= response >= 0:
            return False
        else:
            self.logger.debug('Tray and arm moving')
            return True

    def _tray_arm_position(self):
        """
        Check if the tray and arm are moving and the position of the tray and arm
        :return:
        """
        response = self.read(AutosamplerProtocol.MOVE_TRAY_AND_ARM)
        self.logger.debug(AutosamplerProtocol.MOVE_TRAY_AND_ARM_RESPONSES[response])
        if response == -1:
            raise AutosamplerError('Vial positioning error')
        return response

    def vial_number(self, n: int = None):
        """
        Get or set the vial number
        :param n: int, 1-48
        :return:
        """
        if n is not None:
            if 1 > n > 48:
                raise ProtocolError(f'Vial number should be 1-48, given {n}')
            self.update(AutosamplerProtocol.VIAL_NUMBER, n)
            self.logger.debug(f'Set vial number to {n}')
        response = self.read(AutosamplerProtocol.VIAL_NUMBER)
        self.logger.debug(f'Vial number is {response}')
        return response

    def recalibrate_valve(self, wait=True):
        response = self.valve_position(10001, wait)
        time.sleep(2)
        return response

    def valve_position(self, position: int = None, wait: bool = True):
        """
        Get/set the position of the valve,
        :param position:
        :param wait:
        :return:
        """
        response = self._valve_position(position, wait)
        return response

    def _valve_moving(self) -> bool:
        response = self.valve_position()
        if 20005 >= response >= 20001:
            self.logger.debug('Valve moving')
            return True
        else:
            return False

    def _valve_position(self, n: int = None, wait: bool = True):
        """
        Get/set the position of the valve, or recalibrate it. See AutosamplerProtocol.VALVE_POSITION_VALUES and
        self.VALVE_POSITION_RESPONSES

        :param n:
        :param wait:
        :return:
        """
        if n is not None:
            if AutosamplerProtocol.VALVE_POSITION_VALUES.keys().__contains__(n) is False:
                raise ProtocolError(f'Valve position input must be one of '
                                    f'{list(AutosamplerProtocol.VALVE_POSITION_VALUES.keys())}, given {n}')
            self.update(AutosamplerProtocol.VALVE_POSITION, n)
            self.logger.debug(AutosamplerProtocol.VALVE_POSITION_VALUES[n])
            if wait:
                while self._valve_moving():
                    time.sleep(0.01)
                time.sleep(0.1)  # extra wait just in case things are still moving
        response = self.read(AutosamplerProtocol.VALVE_POSITION)
        self.logger.debug(AutosamplerProtocol.VALVE_POSITION_RESPONSES[response])
        if response == -1:
            raise AutosamplerError('Valve position unknown')
        return response

    def recalibrate_plunger(self):
        response = self._plunger_position(10001)
        time.sleep(7)
        return response

    def stop_plunger(self):
        response = self._plunger_position(10002)
        return response

    def zero_plunger(self, wait: bool = True):
        response = self.plunger_position(0, wait)
        return response

    def plunger_position(self, n: int = None, wait: bool = True):
        """
        Get/set the plunger position in uL. between 0-4100 (0-4100 uL) for large syringe (low pressure) or
        0-1000 (0.1-100 uL) for small syringe (high pressure)

        :param n: plunger position in uL between 0-4100 (0-4100 uL) for large syringe (low pressure) or
            0-1000 (0.1-100 uL) for small syringe (high pressure)
        :param wait:
        :return:
        """
        response = self._plunger_position(n, wait)
        return response

    def _plunger_moving(self):
        response = self._plunger_position()
        if response >= 20000:
            self.logger.debug('Plunger moving')
            return True
        else:
            return False

    def _plunger_position(self, n: int = None, wait: bool = True):
        """
        Get/set the plunger position in uL. between 0-4100 (0-4100 uL) for large syringe (low pressure) or
        0-1000 (0.1-100 uL) for small syringe (high pressure). send 10001 to recalibrate zero, 10002 to abort anything
        to do with the syringe.

        :param n: plunger position in uL between 0-4100 (0-4100 uL) for large syringe (low pressure) or
            0-1000 (0.1-100 uL) for small syringe (high pressure), or 10001 to recalibrate zero or 10002 to abort
            anything to do with the plunger
        :param wait:
        :return:
        """
        if n is not None:
            if AutosamplerProtocol.PLUNGER_POSITION_VALUES.keys().__contains__(n) is False:
                raise ProtocolError(f'Plunger position input must be a value between 0 and 4100, or 10001 or 10002, '
                                    f'but was given {n}')
            response = self.update(AutosamplerProtocol.PLUNGER_POSITION, n)
            self.logger.debug(AutosamplerProtocol.PLUNGER_POSITION_VALUES[n])
            if wait:
                while self._plunger_moving():
                    time.sleep(0.01)
                time.sleep(0.1)  # extra wait just in case things are still moving
        response = self.read(AutosamplerProtocol.PLUNGER_POSITION)
        self.logger.debug(AutosamplerProtocol.PLUNGER_POSITION_RESPONSES[response])
        # if response == -1:  # todo raise error or not?
        #     raise AutosamplerError(AutosamplerProtocol.PLUNGER_POSITION_RESPONSES[response])
        return response

    def plunger_draw_flow_rate(self, n: int = None):
        """
        Get/set the plunger draw flow rate in uL/min. n is a value between 1 and 48000

        :param n: flow rate in uL/min, value between 1 - 48000
        """
        return self._plunger_draw_flow_rate(n=n)

    def _plunger_draw_flow_rate(self, n: int = None):
        """
        Get/set the plunger draw flow rate in uL/min. n is a value between 1 and 48000

        :param n: flow rate in uL/min, value between 1 - 48000
        :return:
        """
        if n is not None:
            n = int(n)
            if n > 48000 or n < 1:
                raise ProtocolError(f'Plunger draw flow rate must be a value between 1 and 4800, but was given {n}')
            response = self.update(AutosamplerProtocol.PLUNGER_DRAW_FLOW_RATE, n)
            self.logger.debug(f'Set plunger draw flow rate to {n} uL/min')
        response = self.read(AutosamplerProtocol.PLUNGER_DRAW_FLOW_RATE)
        self.logger.debug(f'Plunger draw flow rate is {response} uL/min')
        return response

    def plunger_refill_flow_rate(self, n: int = None):
        """
        Get/set the plunger refill flow rate in uL/min. n is a value between 1 and 48000

        :param n: flow rate in uL/min, value between 1 - 48000
        """
        return self._plunger_refill_flow_rate(n=n)

    def _plunger_refill_flow_rate(self, n: int = None):
        """
        Get/set the plunger refill flow rate in uL/min. n is a value between 1 and 48000

        :param n: flow rate in uL/min, value between 1 - 48000
        :return:
        """
        if n is not None:
            n = int(n)
            if n > 48000 or n < 1:
                raise ProtocolError(f'Plunger refill flow rate must be a value between 1 and 4800, but was given {n}')
            response = self.update(AutosamplerProtocol.PLUNGER_REFILL_FLOW_RATE, n)
            self.logger.debug(f'Set plunger refill flow rate to {n} uL/min')
        response = self.read(AutosamplerProtocol.PLUNGER_REFILL_FLOW_RATE)
        self.logger.debug(f'Plunger refill flow rate is {response} uL/min')
        return response

    def fan_speed(self, n=None):
        """
        Set fan speed to n% or get the fan speed. Range 50-100% is good
        :param n: % to set speed to.  Range 50-100% is good
        :return:
        """
        if n is not None:
            if 0 > n > 100:
                raise ProtocolError(f'Fan speed must be set between 0-100%, but was given {n}%')
            self.update(AutosamplerProtocol.INTERNAL_FAN_SPEED, n)
        response = self.read(AutosamplerProtocol.INTERNAL_FAN_SPEED)
        self.logger.debug(f'Internal fan speed: {response}%')
        return response

    def update(self, protocol: str, value: int):
        """
        To update parameters:
        Send >1 [letter][number:int]=[value:int]
        Receive on success <1 [letter][number:int]=[value:int]
        Receive on error <1 [letter][number:int]![error:str]

        :param str, protocol: protocol to request in format [letter][int]
        :param int, value:
        :return:
        """
        protocol_formatted = protocol + '=' + str(value)
        response = self._request(protocol_formatted)
        return response

    def read(self, protocol: str):
        """

        :param protocol: protocol to request in format [letter][int]
        :return:
        """
        protocol_formatted = protocol + "?"
        response = self._request(protocol_formatted)
        return response

    def _request(self, protocol: str):
        """
        To update parameters:
        Send >1 [letter][number:int]=[value:int]
        Receive on success <1 [letter][number:int]=[value:int]
        Receive on error <1 [letter][number:int]![error:str]

        To read information parameters:
        Send >1 [letter][number:int]?
        Receive <1 [letter][number:int]=[value:int]

        :param protocol: either ">1 [letter][int]=[int]" or ">1 [letter][int]?" depending on if updating or reading
            parameters
        :return:
        """
        if protocol[0:3] != ">1 ":  # add ">1 " to protocol
            protocol = ">1 " + protocol
        protocol += "\x0D" + "\x0A"
        response = str(self.ser.request(protocol.encode()).decode())
        response = response[3:]  # remove "<1 " from response
        # response contains ! if there is an error
        if response.count("!") > 0:
            error_protocol = response.split("!")[0]
            error_string = response.split("!")[1]
            error_msg = f'Error response from protocol {error_protocol}: {error_string}'
            raise ProtocolError(error_msg)
        response = self.str_after_equals_sign(response)
        if self.is_int(response):  # response might be a negative number
            return int(response)
        return response

    def str_after_equals_sign(self, s):
        """Return the string after the equals sign"""
        return s.split("=")[-1]

    def is_int(self, s):
        try:
            int(s)
            return True
        except ValueError as e:
            return False
