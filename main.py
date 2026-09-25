import pybedrock


def main():
    print("Minecraft Bedrock World Generator")
    print("pybedrock imported successfully!")
    print()
    print("Available pybedrock items:")

    items = [name for name in dir(pybedrock) if not name.startswith("_")]

    for item in items:
        print("-", item)


if __name__ == "__main__":
    main()