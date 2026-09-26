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
    print("Minecraft Stone Block Test")
    print("=" * 60)

    prepare_world()

    db = plyvel.DB("world/db", create_if_missing=False)

    key = bytes.fromhex("04000000100000002f04")
    value = db.get(key)

    if value is None:
        print("TARGET SUBCHUNK NOT FOUND")
        db.close()
        return

    print("TARGET SUBCHUNK FOUND")
    print("KEY:", key.hex())
    print("SIZE:", len(value))

    blocks = pb.readSubchunk(value)

    local_x = 73 % 16
    local_y = 67 % 16
    local_z = 256 % 16

    print("LOCAL X:", local_x)
    print("LOCAL Y:", local_y)
    print("LOCAL Z:", local_z)

    old_id = blocks[local_y][local_z][local_x]

    print("OLD BLOCK PALETTE ID:", old_id)

    print("=" * 60)
    print("SUBCHUNK READ SUCCESSFULLY")
    print("TARGET BLOCK LOCATED")
    print("=" * 60)

    db.close()

if __name__ == "__main__":
    main()
