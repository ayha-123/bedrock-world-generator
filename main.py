import sys
import plyvel
import pybedrock as pb

seed = sys.argv[1]
world_size = int(sys.argv[2])

db = plyvel.DB("world/db", create_if_missing=False)

key = bytes.fromhex("04000000100000002f04")
data = db.get(key)

subchunk = pb.readSubchunk(data)

x = 9
y = 3
z = 0

old_id = subchunk[y][z][x]
subchunk[y][z][x] = 3

new_data = pb.writeSubchunk(subchunk, 3, 4)

db.put(key, new_data)

check = pb.readSubchunk(db.get(key))

print("SEED:", seed)
print("WORLD SIZE:", world_size)
print("OLD BLOCK ID:", old_id)
print("NEW BLOCK ID:", check[y][z][x])
print("SUBCHUNK SIZE:", len(new_data))

db.close()
