import sys

def main():
    if len(sys.argv) < 3:
        print("Missing arguments")
        return

    seed = int(sys.argv[1])
    world_size = int(sys.argv[2])

    print("Minecraft World Generator")
    print("=" * 60)
    print("SEED:", seed)
    print("WORLD SIZE:", world_size)
    print("=" * 60)

if __name__ == "__main__":
    main()
