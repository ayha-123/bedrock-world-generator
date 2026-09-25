import pybedrock
import plyvel


def main():
    print("Minecraft Bedrock World Generator")
    print("Testing Subchunk encoding...")

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
    print("Testing bitsperblock values...")

    for bits in [1, 2, 3, 4, 5, 6, 7, 8]:

        try:
            encoded = pybedrock.writeSubchunk(
                subchunk,
                bits,
                0
            )

            print(
                f"bits={bits}: "
                f"SUCCESS, size={len(encoded)} bytes"
            )

            if encoded == original:
                print(
                    f"  >>> EXACT MATCH with original!"
                )

        except Exception as e:
            print(
                f"bits={bits}: FAILED - {repr(e)}"
            )

    db.close()

    print()
    print("Encoding test completed.")


if __name__ == "__main__":
    main()
