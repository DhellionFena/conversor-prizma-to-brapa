'''
Module with oto validators
'''
from prizma_to_brapa.utils.dictionary import prizma_cc, prizma_consoantes, prizma_semi, prizma_vogais


def has_vowels(alias: str) -> (bool, str):
    """
    Checks if the given alias contains any vowels defined in `prizma_vogais`.

    :param alias: str
        The string to be checked for vowels.

    :return: tuple
        A tuple where the first element is a boolean indicating whether a vowel
        was found, and the second element is the alias with the first found
        vowel removed.
    """

    for letra in prizma_vogais.keys():
        if letra in alias:
            return (True, alias.replace(letra, ""))
    return False, alias


def has_semi_vowels(alias: str) -> (bool, str):
    """
    Checks if the given alias contains any semi-vowels defined in `prizma_semi`.

    :param alias: str
        The string to be checked for semi-vowels.

    :return: tuple
        A tuple where the first element is a boolean indicating whether a 
        semi-vowel was found, and the second element is the alias with the 
        first found semi-vowel removed.
    """

    for letra in prizma_semi.keys():
        if letra in alias:
            alias = alias.replace(letra, "")
            return (True, alias.replace(letra, ""))
    return False, alias


def has_consonants(alias: str) -> (bool, str):
    """
    Checks if the given alias contains any consonants defined in `prizma_consoantes`.

    :param alias: str
        The string to be checked for consonants.

    :return: tuple
        A tuple where the first element is a boolean indicating whether a consonant
        was found, and the second element is the alias with the first found
        consonant removed.
    """
    for letra in prizma_consoantes.keys():
        if letra in alias:
            alias = alias.replace(letra, "")
            return (True, alias.replace(letra, ""))
    return False, alias


def can_add_r_or_l(alias: str):
    """
    Checks if the given alias ends with a consonant that can accept
    a 'r' or 'l' suffix, as defined in `prizma_cc`.

    :param alias: str
        The string to be checked.

    :return: bool
        A boolean indicating whether the alias ends with a consonant that
        can accept a 'r' or 'l' suffix.
    """
    for fonema in prizma_cc:
        if alias[-1] in fonema[0]:
            return True
    return False
