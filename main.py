import pybedrock
import plyvel


def main():
    print("Minecraft Bedrock World Generator")
    print("Finding Subchunk encoding parameters...")

    db = plyvel.DB("world/db", create_if_missing=False)

    target_key = bytes.fromhex("03000000110000002f00")
    original = db.get(target_key)

    if original is None:
        print("Target record not found.")
        db.close()
        return

    subchunk = pybedrock.readSubchunk(original)

    print()
    print("Original size:", len(original), "bytes")

    print()
    print("Searching for exact encoding match...")

    found = False

    for bits in range(1, 9):
        for yindex in range(0, 256):

            try:
                encoded = pybedrock.writeSubchunk(
                    subchunk,
                    bits,
                    yindex
                )

                if encoded == original:
                    print()
                    print("========================================")
                    print("EXACT MATCH FOUND!")
                    print("bitsperblock:", bits)
                    print("yindex:", yindex)
                    print("encoded size:", len(encoded))
                    print("========================================")

                    found = True

            except Exception:
                pass

    if not found:
        print()
        print("No exact match found.")

    db.close()

    print()
    print("Search completed.")


if __name__ == "__main__":
    main()
