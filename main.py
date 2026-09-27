import sys
import plyvel

seed = sys.argv[1]
world_size = int(sys.argv[2])

db = plyvel.DB("world/db", create_if_missing=False)

prefix = (
    (4).to_bytes(4, "little", signed=True)
    + (16).to_bytes(4, "little", signed=True)
    + bytes([0x2F])
)

for key, value in db.iterator(prefix=prefix):
    print("KEY:", key.hex())
    print("SIZE:", len(value))
    print("HEADER:", value[:4].hex())

db.close()

print("SEED:", seed)
print("WORLD SIZE:", world_size)
