import json

from utils.joints import JOINTS


def verify_written(measurements, robot, unit, attach, master_joints, log):
    """Read every offset back from the controller and attach the mastering file to the run."""
    readback = {j["name"]: robot.read_offset(j["name"]) for j in JOINTS}
    measurements.offsets_written = all(v is not None for v in readback.values())
    measurements.multiturn_valid = all(robot.multiturn_valid(j["name"]) for j in JOINTS)
    mastering_file = {"serial_number": unit.serial_number, "offsets_deg": readback, "offsets_arcsec": master_joints.offsets}
    attach.data(json.dumps(mastering_file, indent=2).encode(), f"{unit.serial_number}_mastering.json")
    unit.metadata["mastered"] = True
    log.info("Offsets read back and mastering file attached")
