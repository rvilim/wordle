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

    # Loop through the old dictionary word by word and constrcut a new dictionary that is pruned with the excluded letters, the letters
    # we know must exist (and know where they cannot be) and the letters which we know exist (and know where they must be)

    # Recall our dictionary is mapping a set of letters to a list of words which is composed from those letters
    for letters, words in dictionary.items():

        #  a word must have all the letters which we know exist AND it can't have any excluded letters
        if not set(exists.keys()) - letters and not excluded.intersection(letters):

            # Check that each of the words we form from our set of letters has the right letters in the right positions, and
            # letters NOT in the positions we know they can't be.
            new_words = [
                word for word in words if letter_in_position(word, positions) and letters_not_in_position(word, exists)
            ]

            if new_words:
                new_dictionary[letters] = new_words

    return new_dictionary


def parse(guess: str, exists) -> Tuple[Dict[int, str], Dict[str, List[int]]]:
    # This parses an input string (capitals = right letter in right position, lowercase = right letter in wrong position)

    # the positions dict tells us characters which must be in a position
    # the exists dictionary tells us, for a given character where it can NOT be
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
    # Construct a guess string, capital letters are the correct letter in the correct position,
    # Lowercase letters are the correct letter in the wrong position
    # Periods are a total miss.

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
    # For a given word, calculate the number of guesses required to solve it (to a max of 15)
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

        # The letters we exclude are the ones we've guessed minus the ones we have either found positions for, or know exist
        excluded = guessed - set(positions.values()) - set(exists.keys())

        dictionary = subset_words(dictionary, positions, exists, excluded)

        best_word, n_candidates = score_dictionary(dictionary)
        result = dictionary[best_word]

        if n_candidates == 1:
            print(f"🔮🔮🔮 {result[0].upper()} 🔮🔮🔮")
            return

        print(f"Guess {result[0].upper()}, {n_candidates} candidates remaining")
        guessed = guessed.union(result[0])


if __name__ == "__main__":
    # solve_all()
    interactive()
