from collections import defaultdict


def read_dict(filename: str):
    words = defaultdict(list)

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            if len(line) != 5:
                continue

            words[frozenset(line)].append(line)
        return words


if __name__ == "__main__":
    wordlist = read_dict("dictionary.txt")
    scores = defaultdict(int)

    for i, chosen in enumerate(wordlist.keys()):

        if i % 1000 == 0:
            print(f"{i}/{len(wordlist)}")

        for guess in wordlist.keys():
            scores[guess] += len(guess.intersection(chosen))

    print("\nTop and bottom scoring words")

    scores_sorted = sorted(scores, key=scores.get, reverse=True)
    for w in scores_sorted[:15]:
        print(f"{wordlist[w]}: {scores[w]}")
    print("\n...\n")
    for w in scores_sorted[-15:]:
        print(f"{wordlist[w]}: {scores[w]}")
