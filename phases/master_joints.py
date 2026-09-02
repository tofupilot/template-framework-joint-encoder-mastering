from utils.joints import ARCSEC_PER_DEG, JOINTS


def master_joints(measurements, robot, ui, log):
    """Per joint: brake off, jog to the witness pin, read both encoders, write the offset, brake on."""
    offsets_arcsec, deltas_arcmin, worst_ratio = [], [], 0.0
    for i, joint in enumerate(JOINTS):
        name = joint["name"]
        robot.release_brake(name)
        robot.jog_to_reference(name)
        joint_deg = robot.raw_joint_encoder_deg(name)
        motor_deg = robot.motor_encoder_deg(name)
        robot.write_offset(name, joint_deg)
        robot.engage_brake(name)

        offset_arcsec = joint_deg * ARCSEC_PER_DEG
        delta_arcmin = abs(motor_deg - joint_deg) * 60.0
        offsets_arcsec.append(offset_arcsec)
        deltas_arcmin.append(delta_arcmin)
        worst_ratio = max(worst_ratio, delta_arcmin / joint["delta_limit_arcmin"])
        log.info(f"{name}: offset {offset_arcsec:+.0f}\" ({joint_deg:+.4f} deg), motor-vs-joint {delta_arcmin:.2f}' (limit {joint['delta_limit_arcmin']}')")
        ui.mastering_progress = int(100 * (i + 1) / len(JOINTS))

    measurements.mastering.x_axis = list(range(1, len(JOINTS) + 1))
    measurements.mastering.y_axis.offset = offsets_arcsec
    measurements.mastering.y_axis.delta = deltas_arcmin
    measurements.mastering.y_axis.offset.aggregations.max_abs_deg = max(abs(o) for o in offsets_arcsec) / ARCSEC_PER_DEG
    measurements.mastering.y_axis.delta.aggregations.worst_vs_limit = worst_ratio
    measurements.offsets = {j["name"]: round(o, 1) for j, o in zip(JOINTS, offsets_arcsec)}
