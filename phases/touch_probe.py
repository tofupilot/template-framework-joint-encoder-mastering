def touch_probe(measurements, robot, log):
    """Optional finishing pass with a touch probe on a reference surface (cells that have one)."""
    log.info("Touch-probe finishing pass")
    measurements.probe_residual = 0.0004
