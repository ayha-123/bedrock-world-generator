import os
import plyvel


def main():
    print("Minecraft Bedrock World Generator")
    print("Opening Bedrock LevelDB...")

    db_path = "world/db"

    print()
    print("Opening:", db_path)

    db = plyvel.DB(db_path, create_if_missing=False)

    print("LevelDB opened successfully!")
    print()

    count = 0

    for key, value in db:
        print("KEY:", key[:80].hex())
        print("VALUE SIZE:", len(value), "bytes")
        print()

        count += 1

        if count >= 20:
            break

    db.close()

    print("Keys inspected:", count)
    print("LevelDB inspection completed successfully.")


if __name__ == "__main__":
    main()
