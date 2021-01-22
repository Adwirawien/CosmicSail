import math
from simulation.Vector2D import Vector2D, vector_from_heading


class Simulation:

    motors = {}
    motor_types = {}
    sensors = {}
    sensor_types = {}

    def __init__(self, motors, motor_types, sensors, sensor_types) -> None:
        self.motors = motors
        self.motor_types = motor_types
        self.sensors = sensors
        self.sensor_types = sensor_types

    def start(self) -> None:
        # TODO: set all hardware into simulation mode

        return None

    def update(self) -> None:
        sail_area = 0.366  # in m**2
        wind_speed = 1  # in m/s
        wind_force = (sail_area ** 2) * (1.229 ** 3) * wind_speed ** 2  # results in Newton
        wind_direction = 10  # degrees
        heading = 300  # degrees
        sail = 40  # degrees of elongation from middle of boat

        # find smallest possible angle from wind_dir to heading
        gamma = math.radians(360 - abs(wind_direction - heading) if abs(wind_direction - heading) > 180 else abs(wind_direction - heading))

        alpha = gamma - math.radians(sail)

        wind_vector = vector_from_heading(wind_direction)  # TODO: relative to boat direction?
        wind_vector = wind_vector * wind_force

        sail_elongation = (sail + heading) % 360

        f3 = vector_from_heading((sail_elongation + 90) % 360)

        f3 *= alpha * math.radians(90)
        print(math.degrees(math.atan2(f3.y, f3.x)))
        print(abs(f3))

        return None
