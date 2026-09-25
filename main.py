import pybedrock
import plyvel


def main():
    print("Minecraft Bedrock World Generator")
    print("Inspecting Subchunk values...")

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
    print("Structure:", len(result), "x", len(result[0]), "x", len(result[0][0]))

    # جمع كل القيم الموجودة
    values = set()

    for y in range(16):
        for z in range(16):
            for x in range(16):
                values.add(result[y][z][x])

    values = sorted(values)

    print()
    print("Unique values:", len(values))
    print("Values:")
    print(values)

    # عرض الطبقة الوسطى فقط
    y = 8

    print()
    print("Layer Y=8:")
    print()

    for z in range(16):
        row = []

        for x in range(16):
            row.append(result[y][z][x])

        print(" ".join(f"{v:3}" for v in row))

    db.close()

    print()
    print("Inspection completed.")


if __name__ == "__main__":
    main()
