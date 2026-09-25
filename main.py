import os
import pybedrock
import plyvel


def main():
    print("Minecraft Bedrock World Generator")
    print("Testing pybedrock subchunk reader...")

    db = plyvel.DB("world/db", create_if_missing=False)

    target_key = bytes.fromhex("03000000110000002f00")
    value = db.get(target_key)

    if value is None:
        print("Target record not found.")
        db.close()
        return

    print()
    print("Record found")
    print("Key:", target_key.hex())
    print("Value size:", len(value), "bytes")

    print()
    print("Testing pybedrock.readSubchunk...")

    try:
        result = pybedrock.readSubchunk(value)

        print()
        print("SUCCESS!")
        print("Result type:", type(result))
        print("Result:", result)

    except Exception as e:
        print()
        print("readSubchunk failed.")
        print("Error type:", type(e).__name__)
        print("Error:", str(e))

    db.close()

    print()
    print("Test completed.")


if __name__ == "__main__":
    main()
