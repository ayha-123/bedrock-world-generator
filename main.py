import os
import pybedrock


def main():
    print("Minecraft Bedrock World Generator")
    print("Testing Bedrock LevelDB access...")

    db_path = "world/db"

    print()
    print("DB path:", db_path)
    print("DB exists:", os.path.exists(db_path))

    if os.path.exists(db_path):
        print("DB contents:")
        for item in os.listdir(db_path)[:10]:
            print("-", item)

    print()
    print("Testing listkeys...")

    try:
        result = pybedrock.listkeys(db_path)
        print("listkeys succeeded!")
        print("Result type:", type(result))
        print("Result:", result)
    except Exception as e:
        print("listkeys failed:")
        print(type(e).__name__, ":", e)

    print()
    print("Test completed.")


if __name__ == "__main__":
    main()
