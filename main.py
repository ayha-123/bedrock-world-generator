import plyvel


DB_PATH = "world/db"

TARGETS = [
    bytes.fromhex("02000000110000002f00"),
    bytes.fromhex("03000000110000002f00"),
    bytes.fromhex("03000000120000002f00"),
]


def main():
    print("Minecraft Bedrock World Generator")
    print("READ-ONLY Palette Inspector")
    print("=" * 70)

    db = plyvel.DB(DB_PATH, create_if_missing=False)

    try:
        for key in TARGETS:
            value = db.get(key)

            if value is None:
                print("Not found:", key.hex())
                continue

            print()
            print("-" * 70)
            print("KEY:", key.hex())
            print("TOTAL SIZE:", len(value))

            # أول 4 بايت هي header
            bits = value[3] >> 1

            if bits == 0:
                print("Invalid bits_per_block")
                continue

            blocks_per_word = 32 // bits
            n32bit = (4096 // blocks_per_word) + 1

            block_data_size = n32bit * 4

            palette_offset = 4 + block_data_size

            print("BITS PER BLOCK:", bits)
            print("BLOCK DATA SIZE:", block_data_size)
            print("PALETTE OFFSET:", palette_offset)

            # نطبع 100 بايت بعد block data
            start = palette_offset
            end = min(start + 100, len(value))

            print()
            print("BYTES AFTER BLOCK DATA:")
            print(value[start:end].hex(" "))

            print()
            print("BYTES WITH OFFSETS:")

            for i in range(start, end, 16):
                chunk = value[i:min(i + 16, end)]
                print(f"{i:04X}: {chunk.hex(' ')}")

    finally:
        db.close()

    print()
    print("=" * 70)
    print("Finished.")
    print("No files were modified.")


if __name__ == "__main__":
    main()
