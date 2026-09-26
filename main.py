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


def change_block(value, x, y, z, new_palette_id):
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

    word &= ~(mask << bit_offset)
    word |= (new_palette_id & mask) << bit_offset

    data = bytearray(value)
    data[offset:offset + 4] = word.to_bytes(
        4,
        byteorder="little"
    )

    return bytes(data)


def main():
    print("Minecraft Bedrock World Generator")
    print("=" * 60)

    prepare_world()

    db = plyvel.DB("world/db", create_if_missing=False)

    for key, value in db:

        if key != bytes.fromhex("02000000110000002f00"):
            continue

        try:
            blocks = pb.readSubchunk(value)

            old_id = blocks[0][0][0]

            new_id = old_id

            for candidate in range(16):
                if candidate != old_id:
                    new_id = candidate
                    break

            modified = change_block(
                value,
                0,
                0,
                0,
                new_id
            )

            test_blocks = pb.readSubchunk(modified)

            print("SUCCESS")
            print("Key:", key.hex())
            print("Old palette ID:", old_id)
            print("New palette ID:", test_blocks[0][0][0])

            db.put(key, modified)

            print("WORLD DATABASE UPDATED")
            print("Original size:", len(value))
            print("New size:", len(modified))

            break

        except Exception as e:
            print("ERROR:", e)

    db.close()

    print("=" * 60)
    print("World modification test completed.")


if __name__ == "__main__":
    main()
