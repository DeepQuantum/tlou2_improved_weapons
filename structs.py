import struct

sidbase = {}
with open("C:/Users/damix/Documents/GitHub/TLOU2Modding/encoded.txt", encoding="utf-8") as f:
    sidbase = dict(line.split(":", 1) for line in f.readlines())

with open("C:/Dark Games/The Last of Us Part II Remastered/build/pc/main/bin_unpacked/dc1/weapon-gameplay.bin", "rb") as f:
    orig_data = f.read()

with open("./improved_weapons/bin/dc1/weapon-gameplay.bin", "rb") as f:
    data = f.read()

size = int.from_bytes(data[0x1C0:0x1C4], "little")
symbol_array_start = 0x07B8
struct_array_start = 0x01F8
struct_size = 144

for i in range(0, size):
    symbol = data[symbol_array_start + i * 0x8 : symbol_array_start + i * 0x8 + 0x8]
    symbol_string = symbol.hex().upper()
    symbol_string = "".join(["".join(symbol_string)[i : i + 2] for i in range(0, len("".join(symbol_string)), 2)][::-1])
    symbol_name = sidbase.get(symbol_string, symbol_string).strip()

    weapon_gameplay_definition_pointer = int.from_bytes(data[struct_array_start + i * 0x8 : struct_array_start + i * 0x8 + 0x4], "little")
    if not weapon_gameplay_definition_pointer:
        continue
    firearm_gameplay_definition_pointer = int.from_bytes(
        data[weapon_gameplay_definition_pointer + 16 : weapon_gameplay_definition_pointer + 20], "little"
    )
    gun_data = data[firearm_gameplay_definition_pointer : firearm_gameplay_definition_pointer + 0x2E8]
    if not gun_data:
        continue

    mag_size_pointer = firearm_gameplay_definition_pointer + 0x98

    mag_size_orig = int.from_bytes(orig_data[mag_size_pointer : mag_size_pointer + 0x4], "little")
    mag_size = int.from_bytes(data[mag_size_pointer : mag_size_pointer + 0x4], "little")

    fire_rate_pointer = firearm_gameplay_definition_pointer + 20
    fire_rate_orig = struct.unpack("<f", orig_data[fire_rate_pointer : fire_rate_pointer + 0x4])[0]
    fire_rate = struct.unpack("<f", data[fire_rate_pointer : fire_rate_pointer + 0x4])[0]

    search_terms: list[str] = ["glock"]
    if not search_terms or any(search in symbol_name for search in search_terms):
        print(f"{symbol_name} @ {hex(weapon_gameplay_definition_pointer)}")
        print(f"   -> weapon_pointer: " + hex(firearm_gameplay_definition_pointer))
        print(f"   -> mag_size @ {hex(mag_size_pointer)}: {mag_size} (+ {mag_size - mag_size_orig})")
        print(f"   -> mag_size_orig @ {hex(mag_size_pointer)}: {mag_size_orig}")
        fire_rate_percent = round((fire_rate_orig - fire_rate) / fire_rate * 100, 2)
        print(f"   -> fire_rate @ {hex(fire_rate_pointer)}: {round(fire_rate, 2)} ({round((1 / fire_rate) * 60, 2)}) (+ {fire_rate_percent}%)")
        print(f"   -> fire_rate_orig @ {hex(fire_rate_pointer)}: {round(fire_rate_orig, 2)}")
