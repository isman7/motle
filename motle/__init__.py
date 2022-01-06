import sys
import random
import typing as t
from pathlib import Path
from unidecode import unidecode

import click
from colorama import Back, Fore, Style


DEFAULT_MOT_SIZE = 5
COLORAMA_MAP: t.Dict[t.Tuple[bool, bool], str] = {
    (False, False): Back.WHITE + Fore.BLACK + Style.BRIGHT,
    (False, True):  Back.WHITE + Fore.BLACK + Style.BRIGHT,
    (True, False):  Back.YELLOW + Fore.BLACK + Style.BRIGHT,
    (True, True):   Back.GREEN + Fore.WHITE + Style.BRIGHT
}


def load_dict(
        path: Path = Path(__file__).resolve().parent / "dicts/ca.softcatala.txt",
        word_len: t.Optional[int] = DEFAULT_MOT_SIZE,
) -> t.List[str]:
    d = (m for m in path.read_text().split("\n") if isinstance(m, str))
    d = map(motle_normalize, d)
    d = (m for m in d if len(m) == word_len)
    return list(d)


def motle_repr(word: str, motle_result: t.List[t.Tuple[bool, bool]]) -> str:
    colors = (COLORAMA_MAP[c] for c in motle_result)
    return "".join(c + l for l, c in zip(word, colors))


def motle_normalize(word: str) -> str:
    # TODO treat ç and l·l
    word = word.lower()
    word = ''.join(filter(lambda x: not x.isdigit(), word))
    word = unidecode(word)
    return word


def motle_check( 
    word: str,
    ref_word: str,
    ref_dict: t.List[str],
) -> t.List[t.Tuple[bool, bool]]:

    norm_word = motle_normalize(word)
    norm_ref_word = motle_normalize(ref_word)
    
    assert len(norm_word) == len(norm_ref_word) == 5, f"{word} ha de tenir 5 lletres."
    assert norm_word in ref_dict, f"{word} no és al diccionari."

    check_l_in_ref_word = list(l in norm_ref_word for l in norm_word)
    check_l_in_position = list(l == r for l, r in zip(norm_word, norm_ref_word))
    return list(zip(check_l_in_ref_word, check_l_in_position))


@click.command()
def motle_cmd():
    """
    Comença un joc nou de motle!
    """
    mots = load_dict()

    mot_incognito = random.choice(mots)

    intents = 6

    while intents:
        mot = click.prompt("Paraula", type=str)
        try:
            c = motle_check(mot, mot_incognito, mots)
            print(motle_repr(''.join(filter(lambda x: not x.isdigit(), mot)), c))
            intents -= 1
            if all(all(l) for l in c):
                print(f"{Style.RESET_ALL}Molt bé! La paraula és: {Style.BRIGHT}{mot_incognito}\n")
                sys.exit()

        except AssertionError as e:
            print(Back.RED + Fore.WHITE + e.args[0])

        print(Style.RESET_ALL + "\n")

    print(f"Oh! La paraula era: {Style.BRIGHT}{mot_incognito}\n")


