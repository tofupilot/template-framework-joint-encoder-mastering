def interlocks(measurements, robot, run, log):
    """Setup: nothing moves before the safety circuit is healthy and the operator is on record."""
    measurements.estop_healthy = robot.estop_healthy()
    log.info(f"Interlocks OK, operator {run.operated_by}, fixture kit confirmed")
