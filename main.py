import sys
import plyvel
import pybedrock as pb

seed = sys.argv[1]
world_size = int(sys.argv[2])

db = plyvel.DB("world/db", create_if_missing=False)

key = bytes.fromhex("04000000100000002f04")
data = bytearray(db.get(key))

bits = data[3] >> 1
blocks_per_word = 32 // bits

x = 9
y = 3
z = 0

index = 256 * x + 16 * z + y
word_index = index // blocks_per_word
position = index % blocks_per_word
offset = 4 + word_index * 4

word = int.from_bytes(data[offset:offset + 4], "little")
shift = position * bits
mask = ((1 << bits) - 1) << shift

old_id = (word >> shift) & ((1 << bits) - 1)

word = (word & ~mask) | (3 << shift)
data[offset:offset + 4] = word.to_bytes(4, "little")

db.put(key, bytes(data))

check = pb.readSubchunk(db.get(key))

print("SEED:", seed)
print("WORLD SIZE:", world_size)
print("OLD ID:", old_id)
print("NEW ID:", check[y][z][x])
print("SIZE BEFORE:", 2682)
print("SIZE AFTER:", len(data))

db.close()
