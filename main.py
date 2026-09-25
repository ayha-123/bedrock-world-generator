import pybedrock


def main():
    print("Minecraft Bedrock World Generator")
    print("Testing world database access...")

    print()
    print("Available database functions:")

    for name in dir(pybedrock):
        if "key" in name.lower() or "db" in name.lower() or "level" in name.lower():
            print("-", name)

    print()
    print("Test completed.")


if __name__ == "__main__":
    main()
