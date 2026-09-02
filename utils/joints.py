"""Joint table of the mock arm: gearbox type sets the motor-vs-joint delta limit."""

JOINTS = [
    {"name": "J1", "gearbox": "cycloidal", "ratio": 121, "delta_limit_arcmin": 0.5},
    {"name": "J2", "gearbox": "cycloidal", "ratio": 121, "delta_limit_arcmin": 0.5},
    {"name": "J3", "gearbox": "harmonic", "ratio": 101, "delta_limit_arcmin": 1.0},
    {"name": "J4", "gearbox": "harmonic", "ratio": 101, "delta_limit_arcmin": 1.0},
    {"name": "J5", "gearbox": "harmonic", "ratio": 101, "delta_limit_arcmin": 1.0},
    {"name": "J6", "gearbox": "harmonic", "ratio": 101, "delta_limit_arcmin": 1.0},
]

ARCSEC_PER_DEG = 3600.0
