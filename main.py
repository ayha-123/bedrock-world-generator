import sys
import plyvel

seed = sys.argv[1]
world_size = int(sys.argv[2])

db = plyvel.DB("world/db", create_if_missing=False)

x = 4
z = 16
y = 4

for layer in range(8):
    key = (
        x.to_bytes(4, "little", signed=True)
        + z.to_bytes(4, "little", signed=True)
        + bytes([0x2F, y])
    )

    data = db.get(key)

    if data is not None:
        print("FOUND")
        print("KEY:", key.hex())
        print("SIZE:", len(data))
        print("HEADER:", data[:8].hex())
        print("LAYER BYTE:", data[1])

db.close()

print("SEED:", seed)
print("WORLD SIZE:", world_size)
