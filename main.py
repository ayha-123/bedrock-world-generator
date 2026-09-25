import zipfile
import os
import shutil
import plyvel


def main():
    print("Reading Subchunk Palette...")
    print("=" * 80)

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

    db = plyvel.DB("world/db", create_if_missing=False)

    for key, value in db:

        if not key.endswith(b"\x2f\x00"):
            continue

        if len(value) < 100:
            continue

        print("KEY:", key.hex())
        print("SIZE:", len(value))

        # نعرف معلومات الـSubchunk من أول 4 bytes
        version = value[0]
        storage_layer = value[1]
        yindex = value[2]
        ptype = value[3]

        bits = ptype >> 1
        blocks_per_word = 32 // bits
        n32bit = (4096 + blocks_per_word - 1) // blocks_per_word

        print("VERSION:", version)
        print("STORAGE LAYER:", storage_layer)
        print("Y INDEX:", yindex)
        print("BITS PER BLOCK:", bits)
        print("WORDS:", n32bit)

        # writeSubchunk يستخدم:
        # 4 bytes header
        # packed block data
        # 4 bytes footer
        palette_start = 4 + (n32bit * 4) + 4

        print("PALETTE START:", palette_start)

        palette = value[palette_start:]

        print("PALETTE SIZE:", len(palette))

        print()
        print("PALETTE HEX:")
        print(palette.hex())

        print()
        print("PALETTE TEXT:")
        print(
            "".join(
                chr(b) if 32 <= b <= 126 else "."
                for b in palette
            )
        )

        print()
        print("=" * 80)

        break

    db.close()

    print("Finished.")


if __name__ == "__main__":
    main()
