import zipfile
import os
import shutil
import plyvel
import pybedrock as pb


def main():
    print("Testing Subchunk read/write...")
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

        try:
            sc = pb.readSubchunk(value)

            bits = (value[3] >> 1)
            yindex = value[2]

            print("KEY:", key.hex())
            print("ORIGINAL SIZE:", len(value))
            print("BITS:", bits)
            print("Y INDEX:", yindex)

            rebuilt = pb.writeSubchunk(sc, bits, yindex)

            print("REBUILT SIZE:", len(rebuilt))
            print("SIZE DIFFERENCE:", len(value) - len(rebuilt))

            print()
            print("ORIGINAL HEADER:", value[:4].hex())
            print("REBUILT HEADER :", rebuilt[:4].hex())

            print()
            print("FIRST 32 ORIGINAL:")
            print(value[:32].hex())

            print()
            print("FIRST 32 REBUILT:")
            print(rebuilt[:32].hex())

            break

        except Exception as e:
            print("ERROR:", repr(e))

    db.close()

    print()
    print("=" * 80)
    print("Finished.")


if __name__ == "__main__":
    main()
