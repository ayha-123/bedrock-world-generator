import pybedrock


def main():
    print("Minecraft Bedrock World Generator")
    print("Testing pybedrock binary functions...")

    print()
    print("loadbinary:")
    print(pybedrock.loadbinary.__doc__)

    print()
    print("writebinary:")
    print(pybedrock.writebinary.__doc__)

    print()
    print("Binary API test completed.")


if __name__ == "__main__":
    main()
