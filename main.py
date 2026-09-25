import os


def main():
    print("Minecraft Bedrock World Generator")
    print("Inspecting Bedrock world database...")

    world_path = "world"
    db_path = os.path.join(world_path, "db")

    print()
    print("World exists:", os.path.isdir(world_path))
    print("Level.dat exists:", os.path.isfile(os.path.join(world_path, "level.dat")))
    print("DB exists:", os.path.isdir(db_path))

    if os.path.isdir(db_path):
        print()
        print("Files inside DB:")

        for filename in os.listdir(db_path):
            full_path = os.path.join(db_path, filename)

            if os.path.isfile(full_path):
                size = os.path.getsize(full_path)
                print(f"- {filename} ({size} bytes)")
            else:
                print(f"- {filename} (directory)")

    print()
    print("Database inspection completed successfully.")


if __name__ == "__main__":
    main()
