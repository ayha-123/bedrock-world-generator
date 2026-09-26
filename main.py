import sys
import zipfile
import os
import shutil
import plyvel
import pybedrock as pb

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
    seed = int(sys.argv[1])
    world_size = int(sys.argv[2])

    print("Minecraft World Generator")
    print("=" * 60)
    print("SEED:", seed)
    print("WORLD SIZE:", world_size)

    prepare_world()

    db = plyvel.DB("world/db", create_if_missing=False)

    key = bytes.fromhex("04000000100000002f04")
    value = db.get(key)

    if value is None:
        print("TARGET SUBCHUNK NOT FOUND")
        db.close()
        return

    print("TARGET SUBCHUNK FOUND")
    print("SIZE:", len(value))
    print("HEADER:", value[:4].hex())

    blocks = pb.readSubchunk(value)

    print("BLOCK AT 73 67 256:")
    print(blocks[3][0][9])

    print("=" * 60)
    print("CHUNK READY")

    db.close()

if __name__ == "__main__":
    main()
