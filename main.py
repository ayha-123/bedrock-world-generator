import pybedrock
import plyvel


def get_shape(data):
    shape = []

    current = data

    while isinstance(current, list):
        shape.append(len(current))

        if not current:
            break

        current = current[0]

    return shape


def main():
    print("Minecraft Bedrock World Generator")
    print("Analyzing decoded Subchunk structure...")

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
    print("Result type:", type(result))
    print("Structure:", get_shape(result))

    print()
    print("Top-level elements:", len(result))

    for i, item in enumerate(result):
        if isinstance(item, list):
            print(f"Element {i}: {len(item)} rows")

            if len(item) > 0 and isinstance(item[0], list):
                print(f"Element {i}: {len(item[0])} columns")

    db.close()

    print()
    print("Structure analysis completed.")


if __name__ == "__main__":
    main()
