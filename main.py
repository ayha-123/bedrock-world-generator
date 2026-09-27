import sys
import plyvel

seed = sys.argv[1]
world_size = int(sys.argv[2])

db = plyvel.DB("world/db", create_if_missing=False)

key = bytes.fromhex("04000000100000002f04")
data = bytearray(db.get(key))

bits = data[3] >> 1
blocks_per_word = 32 // bits

changed = 0

for x in range(7, 12):
    for y in range(1, 6):
        for z in range(0, 3):
            index = 256 * x + 16 * z + y
            word_index = index // blocks_per_word
            position = index % blocks_per_word
            offset = 4 + word_index * 4

            word = int.from_bytes(data[offset:offset + 4], "little")
            shift = position * bits
            mask = ((1 << bits) - 1) << shift

            word = (word & ~mask) | (3 << shift)
            data[offset:offset + 4] = word.to_bytes(4, "little")

            changed += 1

db.put(key, bytes(data))
db.close()

print("SEED:", seed)
print("WORLD SIZE:", world_size)
print("BLOCKS CHANGED:", changed)
print("SUBCHUNK SIZE:", len(data))
