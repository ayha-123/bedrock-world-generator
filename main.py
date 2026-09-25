import pybedrock


def show_doc(name, item):
    print()
    print("=" * 50)
    print(name)
    print("=" * 50)
    print("Documentation:")
    print(item.__doc__)


def main():
    print("Minecraft Bedrock World Generator")
    print("Inspecting database API...")

    show_doc("listkeys", pybedrock.listkeys)
    show_doc("loadbinary", pybedrock.loadbinary)
    show_doc("rmkey", pybedrock.rmkey)

    print()
    print("Inspection completed.")


if __name__ == "__main__":
    main()
