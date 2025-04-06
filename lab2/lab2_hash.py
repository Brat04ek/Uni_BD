
ENCODING_DICTIONARY = [
    ("аб", 1),
    ("вгд", 2),
    ("еєжз", 3),
    ("иіїй", 4),
    ("клмн", 5),
    ("опр", 6),
    ("сту", 7),
    ("фхцчшщь", 8),
    ("юя", 9),
]

DICTIONARY = {letter: value for letters, value in ENCODING_DICTIONARY for letter in letters}
MAX_NAME_LENGTH = 20

def hash_name(name: str) -> int:
    if len(name) > MAX_NAME_LENGTH:
        raise KeyError(f"Name length is greater than max name lenght {MAX_NAME_LENGTH}")

    trailing_zeros = [0] * (MAX_NAME_LENGTH - len(name))
    lenght_name = str(len(name))
    lenght_name = "0" + lenght_name if len(lenght_name) == 1 else lenght_name

    try:
        hash_parts = [DICTIONARY[letter] for letter in name.lower()]
    except KeyError as e:
        raise KeyError(f"Name contains unknown letter '{e.args[0]}'")

    full_hash = hash_parts + trailing_zeros + [lenght_name]
    return int("".join(map(str, full_hash)))