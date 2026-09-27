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
        for folder in os.listdir("world"):
            source = os.path.join("world", folder)

            if os.path.exists(os.path.join(source, "db")):
                for item in os.listdir(source):
                    shutil.move(
                        os.path.join(source, item),
                        os.path.join("world", item)
                    )

                os.rmdir(source)
                break

def main():
    prepare_world()

    db = plyvel.DB("world/db", create_if_missing=False)

    found = 0

    for key, value in db:
        if len(key) < 9:
            continue

        if key[8] != 0x2f:
            continue

        if b"minecraft:water" in value:
            print("WATER SUBCHUNK FOUND")
            print("KEY:", key.hex())
            print("SIZE:", len(value))
            print("HEADER:", value[:4].hex())
            print()
            found += 1

    print("=" * 60)
    print("WATER SUBCHUNKS:", found)

    db.close()

if __name__ == "__main__":
    main()
