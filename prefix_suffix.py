import argparse, inf, sys
from pathlib import Path

def overlap_max_len(a: str, b: str) -> int: # суффикс А = префикс В
    l = min(len(a), len(b))
    for k in range(l, 0, -1):
        if a[-k:] == b[:k]:
            return k
    return 0


def overlap_min_len(a: str, b: str) -> int: # суффикс B = префикс A
    l = min(len(a), len(b))
    for k in range(1, l + 1):
        if a[-k:] == b[:k]:
            return k
    return 0


def best_overlaps(words):
    best_max = (0, None, None)
    best_min = (inf, None, None)

    n = len(words)
    for i in range(n):
        a = words[i].strip()
        for j in range(n):
            if i == j:
                continue
            b = words[j].strip()

            k_max = overlap_max_len(a, b)
            if k_max > best_max[0]:
                best_max = (k_max, i, j)

            k_min = overlap_min_len(a, b)
            if 0 < k_min < best_min[0]:
                best_min = (k_min, i, j)

    maxk, i, j = best_max
    mink, p, q = best_min

    max_pair = (words[i], words[j]) if i is not None else None
    min_pair = (words[p], words[q]) if p is not None else None
    if mink is inf:
        mink = 0

    return (maxk, max_pair), (mink, min_pair)


def read_words(source):
    return [line.rstrip("\n") for line in source if line.strip()]


if __name__ == "__main__":
    ap = argparse.ArgumentParser("Поиск пары слов с макс/мин перекрытием")
    ap.add_argument("-f", "--file", help="Path to file")
    args = ap.parse_args()

    if args.file and args.file != "-":
        path = Path(args.file)
        if not path.exists():
            ap.error(f"File not found: {path}")
        with path.open("r", encoding="utf-8") as file:
            words = read_words(file)

    else:
        words = read_words(sys.stdin)

    (max_k, max_pair), (min_k, min_pair) = best_overlaps(words)
    print("Max:", max_k, "->", max_pair)
    print("Min:", min_k, "->", min_pair)
