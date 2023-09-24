import numpy as np
import matplotlib.pyplot as plt

width = 300
height = 200


def get_sphere_intersect(sphere_center, sphere_radius, ray_origin, ray_direction):
    """
    Return the closest intersection point between the ray and the sphere
    """
    a = np.linalg.norm(ray_direction) ** 2  # if normalized, this is 1
    b = 2 * np.dot(ray_direction, ray_origin - sphere_center)
    c = np.linalg.norm(ray_origin - sphere_center) ** 2 - sphere_radius**2
    delta = b**2 - 4 * a * c

    if delta > 0:
        t1 = (-b - np.sqrt(delta)) / (2 * a)
        t2 = (-b + np.sqrt(delta)) / (2 * a)

        if t1 > 0 and t2 > 0:  # check if the intersection is in front of the camera
            return min(t1, t2)  # return the closest intersection point

    return None


def nearest_intersected_object(objects, ray_origin, ray_direction):
    """
    Return the nearest object and its intersection point with the ray
    """
    distances = [
        get_sphere_intersect(obj["center"], obj["radius"], ray_origin, ray_direction)
        for obj in objects
    ]
    nearest_object = None
    min_distance = np.inf

    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = objects[index]

    return nearest_object, min_distance


def main():
    camera = np.array([0, 0, 1])
    ratio = 1.0 * width / height
    screen = (-1, 1.0 / ratio, 1, -1.0 / ratio)  # left, top, right, bottom

    # Define the objects present in the scene
    objects = [
        {"center": np.array([-0.2, 0, 1]), "radius": 0.7},
        {"center": np.array([0.1, -0.3, 0]), "radius": 0.1},
        {"center": np.array([-0.3, 0, 0]), "radius": 0.15},
    ]

    image = np.zeros((height, width, 3))

    x_ax, y_ax = np.meshgrid(
        np.linspace(screen[0], screen[2], width),
        np.linspace(screen[1], screen[3], height),
    )

    for i, y in enumerate(y_ax):
        for j, x in enumerate(x_ax):
            pixel = np.array([x, y, 0])
            direction = pixel - camera
            direction /= np.linalg.norm(direction)  # normalize

            # Find the nearest intersection
            nearest_object, min_distance = nearest_intersected_object(
                objects, camera, direction
            )

            if nearest_object is None:
                continue

            intersection = camera + min_distance * direction
            
        print("progress: %d/%d" % (i + 1, height))

    plt.imshow(image)
    plt.show()
