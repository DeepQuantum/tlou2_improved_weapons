with open("C:/Users/damix/Documents/GitHub/TLOU2Modding/encoded.txt", encoding="utf-8") as f:
    sidbase = dict(line.split(":", 1) for line in f.readlines())
    while True:
        inp = "".join(input("> ").split())
        print(
            sidbase.get(
                result := "".join(["".join(hash_input := inp)[i : i + 2] for i in range(0, len("".join(inp)), 2)][::-1]),
                result,
            ).strip()
        )
