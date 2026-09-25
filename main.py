import pybedrock


def main():
    print("Minecraft Bedrock World Generator")
    print("Inspecting pybedrock writeSubchunk...")

    print()
    print("writeSubchunk object:")
    print(pybedrock.writeSubchunk)

    print()
    print("writeSubchunk documentation:")
    print(pybedrock.writeSubchunk.__doc__)

    print()
    print("writeSubchunk attributes:")

    try:
        print(dir(pybedrock.writeSubchunk))
    except Exception as e:
        print("Could not inspect attributes:", repr(e))

    print()
    print("Inspecting related functions...")

    for name in [
        "readSubchunk",
        "writeSubchunk",
        "readNBT",
        "writeNBT",
        "loadbinary",
        "writebinary",
    ]:
        obj = getattr(pybedrock, name, None)

        print()
        print(name, "=>", obj)

        try:
            print("doc:", obj.__doc__)
        except Exception as e:
            print("doc error:", repr(e))

    print()
    print("Inspection completed.")


if __name__ == "__main__":
    main()
