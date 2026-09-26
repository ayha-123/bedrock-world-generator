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


def change_raw_palette(value, x, y, z, new_id):
    bits = value[3] >> 1
    blocks_per_word = 32 // bits

    index = 256 * x + 16 * z + y
    word_index = index // blocks_per_word
    block_index = index % blocks_per_word

    bit_offset = block_index * bits
    mask = (1 << bits) - 1

    offset = 4 + word_index * 4

    word = int.from_bytes(
        value[offset:offset + 4],
        byteorder="little"
    )

    old_id = (word >> bit_offset) & mask

    word &= ~(mask << bit_offset)
    word |= (new_id & mask) << bit_offset

    data = bytearray(value)
    data[offset:offset + 4] = word.to_bytes(
        4,
        byteorder="little"
    )

    return bytes(data), old_id


def main():
    print("Minecraft Bedrock World Generator")
    print("=" * 60)

    prepare_world()

    db = plyvel.DB("world/db", create_if_missing=False)

    target = bytes.fromhex("02000000110000002f00")

    value = db.get(target)

    if value is None:
        print("TARGET RECORD NOT FOUND")
        db.close()
        return

    print("ORIGINAL SIZE:", len(value))
    print("ORIGINAL WORD:", value[4:8].hex())

    modified, old_id = change_raw_palette(
        value,
        0,
        0,
        0,
        1
    )

    print("OLD RAW PALETTE ID:", old_id)
    print("NEW RAW PALETTE ID:", 1)
    print("NEW WORD:", modified[4:8].hex())

    if modified[4:8] != value[4:8]:
        db.put(target, modified)
        print("BLOCK DATA CHANGED")
        print("LEVELDB UPDATED")
    else:
        print("BLOCK DATA WAS NOT CHANGED")

    db.close()

    print("=" * 60)
    print("RAW BLOCK TEST COMPLETED.")


if __name__ == "__main__":
    main()
