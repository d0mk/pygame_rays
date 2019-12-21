import random
import math


def cast_rays(origin, obstacles, screen_width, screen_height):
    num_of_rays = 200
    angle_increment = 2 * math.pi / num_of_rays
    max_ray_length = math.sqrt(screen_width ** 2 + screen_height ** 2)

    x3, y3 = origin
    current_angle = 0
    rays = []

    def normalize(v_x, v_y):
        v_magnitude = math.sqrt(v_x ** 2 + v_y ** 2)
        v_x /= v_magnitude
        v_y /= v_magnitude
        return v_x, v_y

    def line_length(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    for _ in range(num_of_rays):
        dir_vector = math.cos(current_angle), math.sin(current_angle)
        candidates = []

        x4 = x3 + dir_vector[0] * max_ray_length
        y4 = y3 + dir_vector[1] * max_ray_length

        for p1, p2 in obstacles:
            x1, y1, x2, y2 = *p1, *p2

            if (denominator := (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)) == 0:
                continue
            else:
                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
                u = ((y1 - y2) * (x1 - x3) - (x1 - x2) * (y1 - y3)) / denominator

                if 0 < t < 1 and u > 0:
                    intersection_x = int(x1 + t * (x2 - x1))
                    intersection_y = int(y1 + t * (y2 - y1))
                    candidates.append((intersection_x, intersection_y))

        if candidates:
            rays.append((origin, min(candidates, key=lambda x: line_length(*origin, *x))))

        current_angle += angle_increment

    return rays