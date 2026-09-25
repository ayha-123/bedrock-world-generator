import pybedrock
import inspect


def show_info(name, item):
    print()
    print("=" * 50)
    print(name)
    print("=" * 50)

    try:
        print("Signature:", inspect.signature(item))
    except Exception as e:
        print("Signature unavailable:", e)

    try:
        print("Documentation:")
        print(inspect.getdoc(item))
    except Exception as e:
        print("Documentation unavailable:", e)


def main():
    print("Minecraft Bedrock World Generator")
    print("pybedrock API inspection")
    
    show_info("loadbinary", pybedrock.loadbinary)
    show_info("writebinary", pybedrock.writebinary)
    show_info("readNBT", pybedrock.readNBT)
    show_info("writeNBT", pybedrock.writeNBT)
    show_info("readSubchunk", pybedrock.readSubchunk)
    show_info("writeSubchunk", pybedrock.writeSubchunk)


if __name__ == "__main__":
    main()
