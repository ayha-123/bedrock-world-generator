import sys
import plyvel
import pybedrock as pb

seed = sys.argv[1]
world_size = int(sys.argv[2])

db = plyvel.DB("world/db", create_if_missing=False)

key = bytes.fromhex("04000000100000002f04")
data = db.get(key)

subchunk = pb.readSubchunk(data)

print("SEED:", seed)
print("WORLD SIZE:", world_size)
print("RAW SIZE:", len(data))
print("HEADER:", data[:4].hex())
print("BITS:", data[3] >> 1)
print("BLOCK 73 67 256:", subchunk[3][0][9])
print("BLOCK 0 0 0:", subchunk[0][0][0])

db.close()
