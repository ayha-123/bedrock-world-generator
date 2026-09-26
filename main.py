import zipfile
import os
import shutil
import plyvel


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


def main():
    print("Minecraft Chunk Locator")
    print("=" * 60)

    prepare_world()

    db = plyvel.DB(
        "world/db",
        create_if_missing=False
    )

    target_x = 73 // 16
    target_z = 256 // 16

    print("BLOCK X:", 73)
    print("BLOCK Z:", 256)
    print("CHUNK X:", target_x)
    print("CHUNK Z:", target_z)
    print("=" * 60)

    found = 0

    for key, value in db:
        if len(key) < 8:
            continue

        x = int.from_bytes(
            key[0:4],
            byteorder="little",
            signed=True
        )

        z = int.from_bytes(
            key[4:8],
            byteorder="little",
            signed=True
        )

        if x == target_x and z == target_z:
            print("MATCH")
            print("KEY:", key.hex())
            print("SIZE:", len(value))
            print("LAST BYTES:", value[-16:].hex())
            print()

            found += 1

    db.close()

    print("=" * 60)
    print("MATCHING RECORDS:", found)


if __name__ == "__main__":
    main()
