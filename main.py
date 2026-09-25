import zipfile
import os
import shutil
import plyvel
import pybedrock as pb


def main():
    print("Reading real Minecraft world...")
    print("=" * 80)

    if os.path.exists("world"):
        shutil.rmtree("world")

    os.makedirs("world", exist_ok=True)

    with zipfile.ZipFile("template.zip", "r") as z:
        z.extractall("world")

    # إذا كان الـZIP يحتوي مجلدًا داخليًا
    if not os.path.exists("world/db"):
        folders = [
            x for x in os.listdir("world")
            if os.path.isdir(os.path.join("world", x))
        ]

        if folders and os.path.exists(
            os.path.join("world", folders[0], "db")
        ):
            old = os.path.join("world", folders[0])
            for item in os.listdir(old):
                shutil.move(
                    os.path.join(old, item),
                    os.path.join("world", item)
                )
            os.rmdir(old)

    db = plyvel.DB("world/db", create_if_missing=False)

    found = 0

    for key, value in db:

        # Subchunk records تنتهي بـ 2f00
        if not key.endswith(b"\x2f\x00"):
            continue

        if len(value) < 8:
            continue

        try:
            # pybedrock يستطيع قراءة الـSubchunk نفسه
            sc = pb.readSubchunk(value)

            print()
            print("=" * 80)
            print("KEY:", key.hex())
            print("VALUE SIZE:", len(value))
            print("SUBCHUNK SIZE:", len(sc))
            print("DIMENSIONS:", [len(sc), len(sc[0]), len(sc[0][0])])

            # أول 16 بلوك من أول طبقة
            print()
            print("FIRST LAYER:")
            for row in sc[0]:
                print(" ".join(map(str, row)))

            found += 1

            # نكتفي بأول سجل صالح
            break

        except Exception as e:
            continue

    db.close()

    print()
    print("=" * 80)
    print("Valid subchunks found:", found)
    print("Finished.")


if __name__ == "__main__":
    main()
