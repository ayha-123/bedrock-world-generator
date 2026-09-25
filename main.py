import pybedrock
import plyvel


def main():
    print("Minecraft Bedrock World Generator")
    print("Inspecting Subchunk palette...")

    db = plyvel.DB("world/db", create_if_missing=False)

    target_key = bytes.fromhex("03000000110000002f00")
    value = db.get(target_key)

    if value is None:
        print("Target record not found.")
        db.close()
        return

    result = pybedrock.readSubchunk(value)

    print()
    print("Record size:", len(value), "bytes")
    print("Decoded structure: 16 x 16 x 16")

    print()
    print("Searching for palette information...")

    # اطبع نوع ومحتويات العناصر العليا فقط
    for i, item in enumerate(result):
        print(
            f"Layer {i}: type={type(item).__name__}, "
            f"rows={len(item)}, "
            f"columns={len(item[0]) if item else 0}"
        )

    print()
    print("Testing writeSubchunk compatibility...")

    try:
        encoded = pybedrock.writeSubchunk(result)

        print("writeSubchunk SUCCESS!")
        print("Encoded size:", len(encoded), "bytes")

        if encoded == value:
            print("Encoded data is IDENTICAL to original record.")
        else:
            print("Encoded data differs from original record.")
            print("This is useful information, but we will NOT write it to the world yet.")

    except Exception as e:
        print("writeSubchunk FAILED")
        print("Error:", repr(e))

    db.close()

    print()
    print("Palette/write analysis completed.")


if __name__ == "__main__":
    main()
