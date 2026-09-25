import os


def main():
    print("Minecraft Bedrock World Generator")
    print("Inspecting LevelDB files safely...")

    db_path = "world/db"

    print()
    print("DB files:")

    for filename in os.listdir(db_path):
        path = os.path.join(db_path, filename)

        if os.path.isfile(path):
            size = os.path.getsize(path)

            print()
            print("File:", filename)
            print("Size:", size, "bytes")

            with open(path, "rb") as f:
                data = f.read(64)

            print("First 64 bytes:", data.hex())

    print()
    print("Safe inspection completed.")


if __name__ == "__main__":
    main()
