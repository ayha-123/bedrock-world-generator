import zipfile
import os
import shutil
import random
import math


def prepare_world():
    if os.path.exists("world"):
        shutil.rmtree("world")

    os.makedirs("world", exist_ok=True)

    with zipfile.ZipFile("template.zip", "r") as z:
        z.extractall("world")

    if not os.path.exists("world/db"):
        folders = [
            x for x in os.listdir("world")
            if os.path.isdir(os.path.join("world", x))
        ]

        for folder in folders:
            candidate = os.path.join("world", folder, "db")

            if os.path.exists(candidate):
                old = os.path.join("world", folder)

                for item in os.listdir(old):
                    shutil.move(
                        os.path.join(old, item),
                        os.path.join("world", item)
                    )

                os.rmdir(old)
                break


def generate_islands(seed):
    rng = random.Random(seed)

    islands = []

    for i in range(30):
        angle = rng.uniform(0, math.pi * 2)
        distance = rng.uniform(200, 5000)

        x = int(math.cos(angle) * distance)
        z = int(math.sin(angle) * distance)

        size_type = rng.random()

        if size_type < 0.55:
            radius = rng.randint(12, 35)
            island_type = "small"
        elif size_type < 0.88:
            radius = rng.randint(36, 90)
            island_type = "medium"
        else:
            radius = rng.randint(100, 220)
            island_type = "large"

        height = rng.randint(4, 25)

        islands.append({
            "x": x,
            "z": z,
            "radius": radius,
            "height": height,
            "type": island_type
        })

    return islands


def main():
    print("Minecraft Open World Generator")
    print("=" * 60)

    seed = 123456789

    prepare_world()

    islands = generate_islands(seed)

    print("SEED:", seed)
    print("ISLANDS:", len(islands))
    print("=" * 60)

    for number, island in enumerate(islands, 1):
        print(
            "ISLAND",
            number,
            "X:",
            island["x"],
            "Z:",
            island["z"],
            "RADIUS:",
            island["radius"],
            "HEIGHT:",
            island["height"],
            "TYPE:",
            island["type"]
        )

    print("=" * 60)
    print("ISLAND GENERATION COMPLETED")


if __name__ == "__main__":
    main()
