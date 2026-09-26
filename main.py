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
    print("Minecraft Block Test")
    print("=" * 60)

    prepare_world()

    db = plyvel.DB("world/db", create_if_missing=False)

    key = bytes.fromhex("04000000100000002f04")
    value = db.get(key)

    if value is None:
        print("TARGET SUBCHUNK NOT FOUND")
        db.close()
        return

    print("TARGET FOUND")
    print("KEY:", key.hex())
    print("SIZE:", len(value))

    data = bytearray(value)

    old_byte = data[4]
    data[4] = old_byte ^ 0x10

    db.put(key, bytes(data))

    print("BLOCK DATA CHANGED")
    print("OLD BYTE:", hex(old_byte))
    print("NEW BYTE:", hex(data[4]))

    db.close()

    print("=" * 60)
    print("DONE")

if __name__ == "__main__":
    main()
