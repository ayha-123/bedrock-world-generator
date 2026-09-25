import pybedrock
import inspect


def inspect_function(name):
    obj = getattr(pybedrock, name)

    print()
    print("=" * 50)
    print(name)
    print("=" * 50)

    print("Object:", obj)
    print("Type:", type(obj))
    print("Module:", getattr(obj, "__module__", None))
    print("Name:", getattr(obj, "__name__", None))
    print("Text signature:", getattr(obj, "__text_signature__", None))

    try:
        print("Signature:", inspect.signature(obj))
    except Exception as e:
        print("Signature unavailable:", repr(e))

    print("Doc:", getattr(obj, "__doc__", None))


def main():
    print("Minecraft Bedrock World Generator")
    print("Inspecting pybedrock native API...")

    inspect_function("readSubchunk")
    inspect_function("writeSubchunk")
    inspect_function("readNBT")
    inspect_function("writeNBT")
    inspect_function("loadbinary")
    inspect_function("writebinary")

    print()
    print("Searching pybedrock module names...")

    for name in dir(pybedrock):
        if "subchunk" in name.lower():
            print("Subchunk:", name)

    print()
    print("Inspection completed.")


if __name__ == "__main__":
    main()
