from collections import defaultdict
import tqdm


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

    for chosen in tqdm.tqdm(wordlist.keys()):

        for guess in wordlist.keys():
            scores[guess] += len(guess.intersection(chosen))

    for w in sorted(scores, key=scores.get, reverse=True):
        print(f"{wordlist[w]}:{scores[w]}")
