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

def set_block(value, x, y, z, new_id):
    data = bytearray(value)

    bits = data[3] >> 1
    blocks_per_word = 32 // bits

    index = 256 * x + 16 * z + y
    word_index = index // blocks_per_word
    position = index % blocks_per_word

    offset = 4 + word_index * 4

    word = int.from_bytes(
        data[offset:offset + 4],
        byteorder="little"
    )

    shift = position * bits
    mask = ((1 << bits) - 1) << shift

    word = (word & ~mask) | ((new_id & ((1 << bits) - 1)) << shift)

    data[offset:offset + 4] = word.to_bytes(
        4,
        byteorder="little"
    )

    return bytes(data)

def main():
    prepare_world()

    db = plyvel.DB("world/db", create_if_missing=False)

    key = bytes.fromhex("04000000100000002f04")
    value = db.get(key)

    if value is None:
        print("TARGET NOT FOUND")
        db.close()
        return

    x = 73 % 16
    y = 67 % 16
    z = 256 % 16

    before = pb.readSubchunk(value)

    print("BEFORE:", before[y][z][x])
    print("BITS:", value[3] >> 1)

    new_value = set_block(
        value,
        x,
        y,
        z,
        3
    )

    after = pb.readSubchunk(new_value)

    print("AFTER:", after[y][z][x])

    if after[y][z][x] != 3:
        print("BLOCK CHANGE FAILED")
        db.close()
        return

    db.put(key, new_value)

    print("BLOCK CHANGED TO STONE")
    print("X:", 73)
    print("Y:", 67)
    print("Z:", 256)

    db.close()

if __name__ == "__main__":
    main()
