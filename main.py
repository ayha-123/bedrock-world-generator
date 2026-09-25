import struct
import plyvel


def main():
    print("Minecraft Bedrock World Generator")
    print("Detecting Minecraft chunks...")

    db_path = "world/db"
    db = plyvel.DB(db_path, create_if_missing=False)

    count = 0

    print()
    print("Possible chunk records:")
    print("--------------------------------")

    for key, value in db:

        # مفاتيح الـ chunk عادةً تحتوي على X و Z كـ int32
        if len(key) >= 8:
            x = struct.unpack("<i", key[0:4])[0]
            z = struct.unpack("<i", key[4:8])[0]

            print(
                f"X={x:6d}  Z={z:6d}  "
                f"KEY_SIZE={len(key):2d}  "
                f"VALUE_SIZE={len(value):5d}  "
                f"KEY={key.hex()}"
            )

            count += 1

        if count >= 50:
            break

    db.close()

    print("--------------------------------")
    print("Records inspected:", count)
    print("Chunk detection completed.")


if __name__ == "__main__":
    main()
