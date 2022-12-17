from utils.utils import load_input
import re


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def distance_in_taxicab_geometry(self, other: 'Point') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def get_tuning_frequency(self) -> int:
        return self.x * 4_000_000 + self.y


class Beacon(Point):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)


class Sensor(Point):
    def __init__(self, x, y, beacon: Beacon) -> None:
        super().__init__(x, y)
        self.beacon = beacon
        self.distance_to_beacon = self.distance_in_taxicab_geometry(self.beacon)


def main() -> None:
    _input = load_input(day=15)
    sensors = prepare_sensors_list(_input)
    print(f"Part one: {get_taken_coords_no_in_specific_y(sensors, 2_000_000)}")
    print(f"Part two: {get_distress_beacon(sensors, 4_000_000, 4_000_000).get_tuning_frequency()}")


def prepare_sensors_list(_input: list[str]) -> list[Sensor]:
    sensors = []
    for line in _input:
        sensor_x, sensor_y, beacon_x, beacon_y = map(int, (re.findall(r'(-?\d+)', line)))
        sensors.append(Sensor(sensor_x, sensor_y, Beacon(beacon_x, beacon_y)))
    return sensors


def get_taken_coords_no_in_specific_y(sensors: list[Sensor], y_of_interest: int) -> int:
    min_x = min(sensor.x - sensor.distance_to_beacon for sensor in sensors)
    max_x = max(sensor.x + sensor.distance_to_beacon for sensor in sensors)
    beacons = [(sensor.beacon.x, sensor.beacon.y) for sensor in sensors]

    taken_count = 0

    for x in range(min_x, max_x + 1):
        point_of_interest = Point(x, y_of_interest)

        if (point_of_interest.x, point_of_interest.y) in beacons:
            continue

        for sensor in sensors:
            if point_of_interest.distance_in_taxicab_geometry(sensor) > sensor.distance_to_beacon:
                continue

            if point_of_interest.distance_in_taxicab_geometry(sensor) <= sensor.distance_to_beacon:
                taken_count += 1
                break

    return taken_count


def get_distress_beacon(sensors: list[Sensor], max_x: int, max_y: int):
    def max_y_at_x(_sensor: Sensor, _x: int) -> int:
        """
        Credits to a Reddit user myhf for this optimization.
        https://www.reddit.com/user/myhf/
        """
        return _sensor.y + _sensor.distance_to_beacon - abs(_sensor.x - x)

    for x in range(max_x + 1):
        y = 0

        while y <= max_y:
            candidate_point = Point(x, y)
            is_candidate_point_valid = True

            for sensor in sensors:
                if candidate_point.distance_in_taxicab_geometry(sensor) <= sensor.distance_to_beacon:
                    is_candidate_point_valid = False
                    y = max_y_at_x(sensor, x)
                    break

            if is_candidate_point_valid:
                return candidate_point

            y += 1


if __name__ == '__main__':
    main()
