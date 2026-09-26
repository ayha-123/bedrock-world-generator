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
        for folder in os.listdir("world"):
            path = os.path.join("world", folder, "db")

            if os.path.exists(path):
                old = os.path.join("world", folder)

                for item in os.listdir(old):
                    shutil.move(
                        os.path.join(old, item),
                        os.path.join("world", item)
                    )

                os.rmdir(old)
                break

def main():
    prepare_world()

    db = plyvel.DB("world/db", create_if_missing=False)

    key = bytes.fromhex("04000000100000002f04")
    value = db.get(key)

    if value is None:
        print("TARGET NOT FOUND")
        db.close()
        return

    print("TARGET FOUND")
    print("SIZE:", len(value))
    print("HEADER:", value[:4].hex())

    blocks = pb.readSubchunk(value)

    x = 73 % 16
    y = 67 % 16
    z = 256 % 16

    print("LOCAL:", x, y, z)
    print("BLOCK ID:", blocks[y][z][x])

    print("SAMPLE BLOCK IDS:")

    ids = {}

    for yy in range(16):
        for zz in range(16):
            for xx in range(16):
                block_id = blocks[yy][zz][xx]
                ids[block_id] = ids.get(block_id, 0) + 1

    for block_id, count in sorted(ids.items()):
        print(block_id, count)

    db.close()

if __name__ == "__main__":
    main()
