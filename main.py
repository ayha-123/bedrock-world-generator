import os
import struct
import plyvel


DB_PATH = "world/db"


def read_u32(data, offset):
    if offset + 4 > len(data):
        return None
    return struct.unpack_from("<I", data, offset)[0]


def inspect_subchunk(key, value):
    if len(value) < 8:
        return None

    version = value[0]
    storage_layer = value[1]
    yindex = value[2]
    ptype = value[3]

    savetype = ptype & 1
    bits_per_block = ptype >> 1

    if bits_per_block == 0:
        blocks_per_word = 0
    else:
        blocks_per_word = 32 // bits_per_block

    # عدد كلمات 32-bit التي يقرأها pybedrock
    if blocks_per_word:
        n32bit = (4096 // blocks_per_word) + 1
        data_size = n32bit * 4
    else:
        n32bit = 0
        data_size = 0

    palette_offset = 4 + data_size

    palette_size = None

    if palette_offset + 4 <= len(value):
        palette_size = read_u32(value, palette_offset)

    return {
        "key": key.hex(),
        "value_size": len(value),
        "version": version,
        "storage_layer": storage_layer,
        "yindex": yindex,
        "ptype": ptype,
        "savetype": savetype,
        "bits_per_block": bits_per_block,
        "blocks_per_word": blocks_per_word,
        "n32bit": n32bit,
        "data_size": data_size,
        "palette_offset": palette_offset,
        "palette_size": palette_size,
    }


def main():
    print("Minecraft Bedrock World Generator")
    print("READ-ONLY Subchunk Inspector")
    print("=" * 70)

    if not os.path.isdir(DB_PATH):
        print("ERROR: world/db not found.")
        return

    print("Opening LevelDB...")
    print("Database:", DB_PATH)
    print()

    db = plyvel.DB(DB_PATH, create_if_missing=False)

    found = 0

    try:
        for key, value in db:
            # سجلات الـSubchunk التي نريد فحصها
            # نركز على المفاتيح التي تنتهي بـ 2f00
            if not key.endswith(bytes.fromhex("2f00")):
                continue

            info = inspect_subchunk(key, value)

            if info is None:
                continue

            found += 1

            print("-" * 70)
            print("SUBCHUNK", found)

            for name, val in info.items():
                print(f"{name:20}: {val}")

            # نوقف بعد أول 20 سجل حتى يبقى الناتج صغيراً
            if found >= 20:
                print()
                print("Stopped after 20 subchunks.")
                break

    finally:
        db.close()

    print()
    print("=" * 70)
    print("Finished.")
    print("No files were modified.")


if __name__ == "__main__":
    main()
