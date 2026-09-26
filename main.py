import zipfile
import os
import shutil
import math
import random
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


def change_raw_palette(value, x, y, z, new_id):
    bits = value[3] >> 1
    blocks_per_word = 32 // bits

    index = 256 * x + 16 * z + y
    word_index = index // blocks_per_word
    block_index = index % blocks_per_word

    bit_offset = block_index * bits
    mask = (1 << bits) - 1

    offset = 4 + word_index * 4

    if offset + 4 > len(value):
        return value

    word = int.from_bytes(
        value[offset:offset + 4],
        byteorder="little"
    )

    word &= ~(mask << bit_offset)
    word |= (new_id & mask) << bit_offset

    data = bytearray(value)

    data[offset:offset + 4] = word.to_bytes(
        4,
        byteorder="little"
    )

    return bytes(data)


def generate_test_world(db, seed):
    random.seed(seed)

    target = bytes.fromhex("02000000110000002f00")

    value = db.get(target)

    if value is None:
        print("TARGET RECORD NOT FOUND")
        return

    data = value

    for z in range(16):
        for x in range(16):
            distance = math.sqrt(
                (x - 7.5) ** 2 +
                (z - 7.5) ** 2
            )

            if distance < 5:
                palette = 1
            else:
                palette = 0

            data = change_raw_palette(
                data,
                x,
                0,
                z,
                palette
            )

    db.put(target, data)

    print("TEST ISLAND GENERATED")
    print("SEED:", seed)


def main():
    print("Minecraft Bedrock World Generator")
    print("=" * 60)

    prepare_world()

    seed = 123456789

    db = plyvel.DB(
        "world/db",
        create_if_missing=False
    )

    generate_test_world(db, seed)

    db.close()

    print("=" * 60)
    print("WORLD GENERATION COMPLETED")


if __name__ == "__main__":
    main()
