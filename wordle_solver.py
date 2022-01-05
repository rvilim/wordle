from collections import defaultdict
from typing import FrozenSet, Dict, List, Set, Tuple
from functools import lru_cache
import operator
import time


def read_dictionary(filename: str) -> Dict[FrozenSet, List[str]]:
    dictionary = defaultdict(list)

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            if len(line) != 5:
                continue

            dictionary[frozenset(line)].append(line)
        return dictionary


def letter_in_position(word: str, positions: Dict[int, str]) -> bool:
    return all(word[position] == letter for position, letter in positions.items())


def letters_not_in_position(word: str, exists: Dict[str, List[int]]) -> bool:
    return not any(word[position] == letter for letter, positions in exists.items() for position in positions)


def subset_words(
    dictionary: Dict[FrozenSet[str], List[str]], positions: Dict[str, int], exists: Dict[str, List[int]], excluded: Set[str]
) -> Dict[FrozenSet[str], List[str]]:

    new_dictionary = defaultdict(list)

    for letters, words in dictionary.items():
        if not set(exists.keys()) - letters and not excluded.intersection(letters):
            new_words = [
                word for word in words if letter_in_position(word, positions) and letters_not_in_position(word, exists)
            ]

            if new_words:
                new_dictionary[letters] = new_words

    return new_dictionary


def parse(guess: str, exists) -> Tuple[Dict[int, str], Dict[str, List[int]]]:
    positions = {}

    for position, char in enumerate(guess):
        if char.isupper():
            positions[position] = char.lower()

        if char.islower():
            exists[char].append(position)

    return positions, exists


def score_dictionary(dictionary: Dict[FrozenSet[str], List[str]]) -> Tuple[int, int]:
    scores: Dict[FrozenSet[str], int] = defaultdict(int)

    keys = list(dictionary.keys())
    for i, chosen in enumerate(keys):
        for guess in keys[: i + 1]:
            scores[chosen] += len(chosen.intersection(guess))

    scores_sorted = list(sorted(scores, key=scores.get, reverse=True))

    return max(scores.items(), key=operator.itemgetter(1))[0], sum(len(dictionary[w]) for w in scores_sorted)


def make_guess(word, guess):
    response = ""
    for w, g in zip(word.lower(), guess.lower()):
        if w == g:
            response += w.upper()
        elif g.lower() in word.lower():
            response += g.lower()
        else:
            response += "."

    return response


def solve(dictionary, word: str):
    guess = make_guess(word, "arose")
    guessed = set(guess.lower().replace(".", ""))
    excluded = set()
    exists = defaultdict(list)

    for steps in range(15):
        guessed = guessed.union(set(guess.lower().replace(".", "")))

        positions, exists = parse(guess, exists)

        excluded = guessed - set(exists.keys()) - set(positions.values())

        dictionary = subset_words(dictionary, positions, exists, excluded)

        best_word, n_candidates = score_dictionary(dictionary)

        guess_word = dictionary[best_word][0]

        if n_candidates == 1:
            return steps

        guessed = guessed.union(guess_word)

        guess = make_guess(word, guess_word)


def solve_all():
    dictionary = read_dictionary("dictionary.txt")

    for words in dictionary.values():
        for word in words:
            start = time.time()

            steps = solve(dictionary, word)
            print(f"Solved for {word} in {steps} guesses in {time.time() - start:.3f}s")


def interactive():
    dictionary = read_dictionary("dictionary.txt")

    guessed = set("arose")
    excluded = set()
    exists = defaultdict(list)

    print("Guess AROSE")

    for _ in range(5):
        guess = input()

        guessed = guessed.union(set(guess.lower().replace(".", "")))

        positions, exists = parse(guess, exists)

        excluded = guessed - set(positions.values()) - set(exists.keys())

        dictionary = subset_words(dictionary, positions, exists, excluded)
        best_word, n_candidates = score_dictionary(dictionary)
        result = dictionary[best_word]
        print(f"Guess {result[0].upper()}, {n_candidates} candidates remaining")
        guessed = guessed.union(result[0])


if __name__ == "__main__":
    # solve_all()
    interactive()
