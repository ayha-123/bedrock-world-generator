import sys
import plyvel
import pybedrock as pb

seed = sys.argv[1]
world_size = int(sys.argv[2])

db = plyvel.DB("world/db", create_if_missing=False)

key = bytes.fromhex("04000000100000002f04")
data = db.get(key)

bits = data[3] >> 1
blocks_per_word = 32 // bits
word_count = (4096 + blocks_per_word - 1) // blocks_per_word

palette_offset = 4 + word_count * 4
palette_size = int.from_bytes(
    data[palette_offset:palette_offset + 4],
    "little"
)

print("SEED:", seed)
print("WORLD SIZE:", world_size)
print("RAW SIZE:", len(data))
print("BITS:", bits)
print("BLOCKS PER WORD:", blocks_per_word)
print("WORD COUNT:", word_count)
print("PALETTE OFFSET:", palette_offset)
print("PALETTE SIZE:", palette_size)

db.close()
