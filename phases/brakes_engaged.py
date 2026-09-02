def brakes_engaged(measurements, robot, log):
    """Teardown: every brake back on before the fixture is removed."""
    measurements.all_brakes_engaged = robot.brakes_engaged()
    log.info("All brakes engaged")
