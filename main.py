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
    print("Minecraft Bedrock World Generator")
    print("=" * 60)

    prepare_world()

    db = plyvel.DB("world/db", create_if_missing=False)

    target = bytes.fromhex("02000000110000002f00")

    for key, value in db:

        if key != target:
            continue

        print("KEY:", key.hex())
        print("SIZE:", len(value))
        print("HEADER:", value[:4].hex())
        print("FIRST 32 BYTES:", value[:32].hex())

        bits = value[3] >> 1
        blocks_per_word = 32 // bits

        print("BITS:", bits)
        print("BLOCKS PER WORD:", blocks_per_word)

        blocks = pb.readSubchunk(value)

        print("MATRIX:", len(blocks), len(blocks[0]), len(blocks[0][0]))

        print("FIRST 16 BLOCK IDS:")

        for i in range(16):
            print(i, blocks[0][0][i])

        print("=" * 60)
        print("RAW WORDS:")

        for i in range(4):
            offset = 4 + i * 4
            word = int.from_bytes(
                value[offset:offset + 4],
                byteorder="little"
            )

            ids = []

            for j in range(blocks_per_word):
                ids.append(
                    (word >> (j * bits)) & ((1 << bits) - 1)
                )

            print(
                "WORD",
                i,
                "HEX:",
                value[offset:offset + 4].hex(),
                "IDS:",
                ids
            )

        db.close()

        print("=" * 60)
        print("RAW DATA TEST COMPLETED.")
        return

    db.close()

    print("TARGET RECORD NOT FOUND.")


if __name__ == "__main__":
    main()
