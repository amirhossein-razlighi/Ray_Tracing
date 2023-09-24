import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

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
        {
            "center": np.array([-0.2, 0, -1]),
            "radius": 0.7,
            "ambient": np.array([0.1, 0, 0]),
            "diffuse": np.array([0.7, 0, 0]),
            "specular": np.array([1, 1, 1]),
            "shininess": 100,
        },
        {
            "center": np.array([0.1, -0.3, 0]),
            "radius": 0.1,
            "ambient": np.array([0.1, 0, 0.1]),
            "diffuse": np.array([0.7, 0, 0.7]),
            "specular": np.array([1, 1, 1]),
            "shininess": 100,
        },
        {
            "center": np.array([-0.3, 0, 0]),
            "radius": 0.15,
            "ambient": np.array([0, 0.1, 0]),
            "diffuse": np.array([0, 0.6, 0]),
            "specular": np.array([1, 1, 1]),
            "shininess": 100,
        },
    ]

    # Define the light source
    light = {
        "position": np.array([5, 5, 5]),
        "ambient": np.array([1, 1, 1]),
        "diffuse": np.array([1, 1, 1]),
        "specular": np.array([1, 1, 1]),
    }

    image = np.zeros((height, width, 3))

    for i, y in tqdm(enumerate(np.linspace(screen[1], screen[3], height))):
        for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
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

            # find the normal to the intersection point
            normal_to_surface = intersection - nearest_object["center"]
            normal_to_surface /= np.linalg.norm(normal_to_surface)  # normalize

            # find the unit direction vector from the intersection point to the light source
            light_direction = light["position"] - intersection
            light_direction /= np.linalg.norm(light_direction)  # normalize

            _, min_distance = nearest_intersected_object(
                objects, intersection, light_direction
            )
            intersect_to_light_dist = np.linalg.norm(light["position"] - intersection)
            is_shadowed = min_distance < intersect_to_light_dist

            if is_shadowed:
                continue

            # RGB using Blenn-Phong model
            illumination = np.zeros((3))

            # add ambient
            illumination += nearest_object["ambient"] * light["ambient"]

            # add diffuse
            illumination += (
                nearest_object["diffuse"]
                * light["diffuse"]
                * np.dot(light_direction, normal_to_surface)
            )

            # add specular
            intersect_to_camera = camera - intersection
            intersect_to_camera /= np.linalg.norm(intersect_to_camera)  # normalize

            H = intersect_to_camera + light_direction
            H /= np.linalg.norm(H)  # normalize

            illumination += (
                nearest_object["specular"]
                * light["specular"]
                * np.dot(normal_to_surface, H) ** (nearest_object["shininess"] / 4)
            )

            # set the pixel color
            image[i, j] = np.clip(illumination, 0, 1)

    plt.imshow(image)
    plt.show()


if __name__ == "__main__":
    main()
