from utils.joints import ARCSEC_PER_DEG, JOINTS


def repeatability(measurements, robot, master_joints, log):
    """Jog away, come back onto the pin, read again: the spread is the procedure's own repeatability."""
    first = master_joints.offsets
    diffs = []
    for joint in JOINTS:
        name = joint["name"]
        robot.release_brake(name)
        robot.jog_to_reference(name)
        second = robot.raw_joint_encoder_deg(name) * ARCSEC_PER_DEG
        robot.engage_brake(name)
        diffs.append(abs(second - float(first[name])))
    worst = max(diffs)
    log.info(f"Remaster spread per joint: {[round(d, 1) for d in diffs]} arcsec, worst {worst:.1f}\"")
    measurements.remaster_spread = {j["name"]: round(d, 1) for j, d in zip(JOINTS, diffs)}
    measurements.remaster_worst = worst / ARCSEC_PER_DEG
