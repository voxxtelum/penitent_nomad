import math
from typing import List, Tuple
import great_circle_calculator.great_circle_calculator as gcc


def _miles_to_meters(miles):
    return math.floor(miles * 1609.344)


def _intermediate_ratio(r1: int, r2: int):
    if r1 > r2:
        return r1 / (r1 + r2)
    else:
        return r2 / (r1 + r2)


def _intermediate_points(df1, rad1: int, df2, rad2: int):
    int_points = []
    if rad1 >= rad2:
        for df1_row in df1:
            for df2_row in df2:
                loc_1 = (df1_row[0], df1_row[1])
                loc_2 = (df2_row[0], df2_row[1])
                center_dist = gcc.distance_between_points(loc_1, loc_2, unit="miles")
                # print(center_dist)

                if center_dist < (rad1 + rad2):
                    int_point = gcc.intermediate_point(
                        loc_1, loc_2, _intermediate_ratio(rad1, rad2)
                    )
                    # print(int_point)
                    int_points.append((int_point[1], int_point[0]))

    # if rad1 < rad2:
    #   for df1_row in df1:
    #     for df2_row in df2:
    #       loc_1 = (df2_row[0], df2_row[1])
    #       loc_2 = (df1_row[0], df1_row[1])
    #       center_dist = gcc.distance_between_points(loc_1, loc_2, unit='miles')

    #       if center_dist < (rad1 + rad2):
    #         int_point = gcc.intermediate_point(loc_1, loc_2, _intermediate_ratio(rad1, rad2))
    #         int_points.append((int_point[1], int_point[0]))

    return int_points


def _cent_points(points: List[Tuple[float, float]]):

    num_points = len(points)

    x = 0.0
    y = 0.0
    z = 0.0

    for point in points:
        lat = point[0] * math.pi / 180
        lon = point[1] * math.pi / 180

        a = math.cos(lat) * math.cos(lon)
        b = math.cos(lat) * math.sin(lon)
        c = math.sin(lat)

        x += a
        y += b
        z += c

    x /= num_points
    y /= num_points
    z /= num_points

    n_lon = math.atan2(y, x)
    n_hyp = math.sqrt(x * x + y * y)
    n_lat = math.atan2(z, n_hyp)

    o_lat = n_lat * 180 / math.pi
    o_lon = n_lon * 180 / math.pi

    return (o_lat, o_lon)
