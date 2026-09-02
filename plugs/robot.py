"""Robot controller service interface (mock).

Six joints with a joint-side absolute encoder and a motor-side encoder. Each
joint carries a real assembly offset between encoder zero and mechanical zero
(what mastering measures) and a gearbox lost motion (what the motor-vs-joint
delta measures). Swap for the vendor service API (UR dashboard, KUKA
Sunrise, ABB RobotWare, FANUC KAREL); the phases stay unchanged.
"""

import numpy as np

from utils.joints import ARCSEC_PER_DEG, JOINTS


class RobotController:
    def __init__(self):
        self._rng = np.random.default_rng(6)
        # true encoder-zero to mechanical-zero offset per joint, degrees
        self._true_offset = {j["name"]: self._rng.normal(0.0, 0.05) for j in JOINTS}
        self._true_offset["J4"] = -0.08   # encoder seated slightly rotated on J4
        self._lost_motion = {j["name"]: abs(self._rng.normal(0.25, 0.08)) for j in JOINTS}  # arcmin
        self._brakes = {j["name"]: True for j in JOINTS}
        self._offset_written = {}
        print("Controller service mode, all brakes engaged")

    def estop_healthy(self):
        return True

    def release_brake(self, joint):
        self._brakes[joint] = False
        return True

    def engage_brake(self, joint):
        self._brakes[joint] = True
        return True

    def brakes_engaged(self):
        return all(self._brakes.values())

    def jog_to_reference(self, joint):
        """Drive the joint until the witness pin engages; returns True when at reference."""
        return True

    def raw_joint_encoder_deg(self, joint):
        """Joint-side encoder reading at the mechanical reference: the offset plus pin clearance."""
        return self._true_offset[joint] + self._rng.normal(0.0, 0.0008)

    def motor_encoder_deg(self, joint):
        """Motor-side reading divided by the gear ratio, at the same reference."""
        ratio = next(j["ratio"] for j in JOINTS if j["name"] == joint)
        lost = self._lost_motion[joint] / 60.0 * self._rng.choice([-1.0, 1.0])
        return self._true_offset[joint] + lost + self._rng.normal(0.0, 0.0005 / ratio)

    def write_offset(self, joint, offset_deg):
        self._offset_written[joint] = float(offset_deg)
        return True

    def read_offset(self, joint):
        return self._offset_written.get(joint)

    def multiturn_valid(self, joint):
        return True
