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

    found = False

    for key, value in db:

        if not key.endswith(b"\x2f\x00"):
            continue

        try:
            blocks = pb.readSubchunk(value)

            old = blocks[0][0][0]
            blocks[0][0][0] = old

            bits = value[3] >> 1
            yindex = value[2]

            new_subchunk = pb.writeSubchunk(
                blocks,
                bits,
                yindex
            )

            if len(new_subchunk) > 0:
                print("SUCCESS")
                print("Key:", key.hex())
                print("Original size:", len(value))
                print("New subchunk size:", len(new_subchunk))
                print("Bits:", bits)

                found = True
                break

        except Exception:
            continue

    db.close()

    print("=" * 60)

    if found:
        print("Subchunk read/write test completed.")
    else:
        print("No suitable subchunk found.")


if __name__ == "__main__":
    main()
