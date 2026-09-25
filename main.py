import plyvel
import struct


def read_varint(data, offset=0):
    value = 0
    shift = 0

    while offset < len(data):
        byte = data[offset]
        offset += 1

        value |= (byte & 0x7F) << shift

        if not (byte & 0x80):
            return value, offset

        shift += 7

        if shift >= 35:
            return None, offset

    return None, offset


def main():
    print("Minecraft Bedrock World Generator")
    print("Inspecting one Chunk record...")

    db = plyvel.DB("world/db", create_if_missing=False)

    target_key = bytes.fromhex("03000000110000002f00")

    value = db.get(target_key)

    if value is None:
        print("Target record was not found.")
        db.close()
        return

    print()
    print("Target key:", target_key.hex())
    print("Value size:", len(value), "bytes")

    print()
    print("First 128 bytes:")
    print(value[:128].hex())

    print()
    print("Possible VarInts:")

    offset = 0

    for i in range(20):
        if offset >= len(value):
            break

        number, new_offset = read_varint(value, offset)

        if number is None:
            break

        print(
            f"{i + 1:02d}: "
            f"offset={offset:3d} "
            f"value={number}"
        )

        offset = new_offset

    db.close()

    print()
    print("Chunk record inspection completed.")


if __name__ == "__main__":
    main()
