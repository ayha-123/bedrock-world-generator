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

    key = bytes.fromhex("04000000100000002f04")
    value = db.get(key)

    if value is None:
        print("TARGET NOT FOUND")
        db.close()
        return

    print("TARGET FOUND")
    print("SIZE:", len(value))
    print("HEADER:", value[:4].hex())

    print("RAW DATA:")
    print(value[4:].hex())

    blocks = pb.readSubchunk(value)

    print("=" * 60)
    print("PALETTE IDS")

    ids = {}

    for y in range(16):
        for z in range(16):
            for x in range(16):
                block_id = blocks[y][z][x]
                ids[block_id] = ids.get(block_id, 0) + 1

    for block_id, count in sorted(ids.items()):
        print("ID:", block_id, "COUNT:", count)

    print("=" * 60)
    print("TARGET BLOCK ID:", blocks[3][0][9])

    db.close()

if __name__ == "__main__":
    main()
