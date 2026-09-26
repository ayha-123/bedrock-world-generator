import sys
import math

def main():
    if len(sys.argv) < 3:
        print("Missing arguments")
        return

    seed = int(sys.argv[1])
    world_size = int(sys.argv[2])

    chunks_per_side = math.ceil(world_size / 16)
    total_chunks = chunks_per_side * chunks_per_side

    print("Minecraft World Generator")
    print("=" * 60)
    print("SEED:", seed)
    print("WORLD SIZE:", world_size)
    print("CHUNKS PER SIDE:", chunks_per_side)
    print("TOTAL CHUNKS:", total_chunks)
    print("=" * 60)

if __name__ == "__main__":
    main()
