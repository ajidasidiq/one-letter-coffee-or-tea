"""One Letter: Coffee or Tea.

Picks exactly one letter -- A for coffee, B for tea -- and writes it, alone,
to /output/entry.txt. Nothing else goes in the file: no word, no explanation,
no punctuation, not even a trailing newline. The file must be exactly one
character long, or the gate refuses the entry.

How the pick is made: the judge weighs three things, most important first --
vivid, funny, true. So this program scores both drinks on those three
criteria, each on a 0-10 scale built from concrete, checkable observations
about the drink, and sends the higher total. The scores are argued in code,
not asserted: every sub-score names the observation behind it.

The verdict: coffee wins, and it is not close on the criterion that matters
most.

Vividness -- coffee 9, tea 5.
    Coffee hits every sense at once: the smell fills a room before the cup
    reaches you, the first sip is bitter enough to wake your face up, and the
    caffeine jolt is a physical event you can feel in your chest within
    minutes. Tea is pleasant and warm, but it whispers; coffee shouts. A
    letter that stands for coffee carries that shout in a single character.

Funniness -- coffee 8, tea 4.
    Coffee owns the joke. "Don't talk to me before my coffee" is a
    personality, a mug slogan, a whole genre of morning memes. Nobody has
    ever made a meme about being dangerously un-tea-ed. Tea is too polite to
    be funny; coffee is the drink of people who are barely functioning, and
    barely functioning is funny because it is honest.

Truth -- coffee 9, tea 6.
    Ask a room of builders, couriers, night-shift workers and students what
    got them through the morning and the honest answer is coffee. Tea is the
    answer people give when they want to sound calm and balanced; coffee is
    the answer they give when they are telling the truth. The letter A is
    also the truer shape for the choice: first, blunt, no hedging -- the
    same way a black coffee has nothing to hide behind.

Totals: coffee 26, tea 15. The program sends A.
"""

from __future__ import annotations

import os
import sys

# Criterion weights follow the judge's brief: vivid first, then funny, then
# true. The weights only break near-ties; here the gap is wide on every axis.
WEIGHTS = {"vivid": 3, "funny": 2, "true": 1}

# Each sub-score is (score out of 10, the observation it rests on).
DRINKS = {
    "A": {
        "name": "coffee",
        "scores": {
            "vivid": (9, "bitter first sip, room-filling aroma, a jolt you feel"),
            "funny": (8, "the before-coffee meme is a whole personality"),
            "true": (9, "the honest fuel of mornings, deadlines and night shifts"),
        },
    },
    "B": {
        "name": "tea",
        "scores": {
            "vivid": (5, "warm and pleasant, but it whispers where coffee shouts"),
            "funny": (4, "too polite to be a joke; nobody fears the un-tea-ed"),
            "true": (6, "the calm answer people give when they want to sound balanced"),
        },
    },
}


def weighted_total(drink: dict) -> int:
    """Weighted sum of a drink's criterion scores."""
    return sum(
        WEIGHTS[criterion] * score
        for criterion, (score, _note) in drink["scores"].items()
    )


def pick_letter() -> str:
    """Return the letter of the highest-scoring drink.

    Ties are impossible here (26 vs 15), but if the scores ever did tie the
    tie-break is vividness first, matching the judge's order of criteria.
    """
    ranked = sorted(
        DRINKS.items(),
        key=lambda item: (
            weighted_total(item[1]),
            item[1]["scores"]["vivid"][0],
        ),
        reverse=True,
    )
    return ranked[0][0]


def main() -> int:
    letter = pick_letter()
    drink = DRINKS[letter]

    for other_letter, other in DRINKS.items():
        if other_letter != letter:
            print(
                f"{drink['name']} ({letter}): {weighted_total(drink)}  vs  "
                f"{other['name']} ({other_letter}): {weighted_total(other)}"
            )
    for criterion, (score, note) in drink["scores"].items():
        print(f"  {criterion}: {score}/10 -- {note}")
    print(f"Verdict: send {letter} ({drink['name']}).")

    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    # Exactly one character: no newline, no space, nothing else.
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(letter)

    with open(out_path, "rb") as handle:
        raw = handle.read()
    assert raw == letter.encode("utf-8"), f"entry must be exactly {letter!r}"
    print(f"Wrote {out_path}: {raw!r} ({len(raw)} byte)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
