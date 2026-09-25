import os


def main():
    print("Minecraft Bedrock World Generator")
    print("Checking world template...")

    world_path = "world"

    print()
    print("World exists:", os.path.isdir(world_path))
    print("Level.dat exists:", os.path.isfile(os.path.join(world_path, "level.dat")))
    print("DB exists:", os.path.isdir(os.path.join(world_path, "db")))

    if os.path.isdir(os.path.join(world_path, "db")):
        files = os.listdir(os.path.join(world_path, "db"))
        print("DB items:", len(files))

    print()
    print("Template check completed successfully.")


if __name__ == "__main__":
    main() 
