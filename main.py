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


def inspect_chunks(db):
    chunks = {}

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

        position = (x, z)

        if position not in chunks:
            chunks[position] = 0

        chunks[position] += 1

    print("CHUNKS FOUND:", len(chunks))

    for position, records in list(chunks.items())[:10]:
        print(
            "CHUNK:",
            position[0],
            position[1],
            "RECORDS:",
            records
        )


def main():
    print("Minecraft Open World Generator")
    print("=" * 60)

    prepare_world()

    db = plyvel.DB(
        "world/db",
        create_if_missing=False
    )

    inspect_chunks(db)

    db.close()

    print("=" * 60)
    print("CHUNK SYSTEM INSPECTION COMPLETED")


if __name__ == "__main__":
    main()
