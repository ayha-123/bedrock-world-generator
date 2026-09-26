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


def modify_subchunk(value):
    data = bytearray(value)

    bits = value[3] >> 1
    blocks_per_word = 32 // bits

    for y in range(16):
        for z in range(16):
            for x in range(16):

                index = 256 * x + 16 * z + y

                word_index = index // blocks_per_word
                block_index = index % blocks_per_word

                bit_offset = block_index * bits
                mask = (1 << bits) - 1

                offset = 4 + word_index * 4

                if offset + 4 > len(data):
                    continue

                word = int.from_bytes(
                    data[offset:offset + 4],
                    byteorder="little"
                )

                if y < 4:
                    new_id = 1
                else:
                    new_id = 0

                word &= ~(mask << bit_offset)
                word |= (new_id & mask) << bit_offset

                data[offset:offset + 4] = word.to_bytes(
                    4,
                    byteorder="little"
                )

    return bytes(data)


def main():
    print("Minecraft Island Generator")
    print("=" * 60)

    prepare_world()

    db = plyvel.DB(
        "world/db",
        create_if_missing=False
    )

    target = bytes.fromhex("02000000110000002f00")

    value = db.get(target)

    if value is None:
        print("TARGET SUBCHUNK NOT FOUND")
        db.close()
        return

    print("ORIGINAL SIZE:", len(value))

    modified = modify_subchunk(value)

    db.put(target, modified)

    print("SUBCHUNK UPDATED")
    print("NEW SIZE:", len(modified))

    db.close()

    print("=" * 60)
    print("REAL BLOCK MODIFICATION COMPLETED")


if __name__ == "__main__":
    main()
