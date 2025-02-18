'''
Module with fonems extractors
'''
from prizma_to_brapa.utils.dictionary import prizma_cc, prizma_consoantes
from prizma_to_brapa.utils.dictionary import prizma_semi, prizma_vogais
from prizma_to_brapa.utils.validators import has_semi_vowels


def extract_from_consonant_vowel(alias: str):
    """
    Extracts a consonant and a vowel from the given alias, and returns
    a string with the extracted consonant followed by the extracted vowel.

    :param alias: str
        The alias to be extracted from.

    :return: str
        A string with the extracted consonant followed by the extracted vowel.

    :raises:
        Exception
            If the alias does not contain a valid consonant and a valid vowel.
    """
    consoante = ""
    vogal = ""

    # extraindo consoantes duplas primeiro
    for cc in prizma_cc:
        if cc in alias:
            alias = alias.replace(cc, "")
            consoante = cc
            break

    if len(consoante) == 0:
        # pylint: disable=consider-using-dict-items consider-iterating-dictionary
        for c in prizma_consoantes.keys():
            if c in alias:
                alias = alias.replace(c, "")
                consoante = prizma_consoantes[c]
                break

    # extraindo vogais
    # pylint: disable=consider-using-dict-items consider-iterating-dictionary
    for v in prizma_vogais.keys():
        if v in alias:
            alias = alias.replace(v, "")
            vogal = prizma_vogais[v]
            break
    if len(consoante) > 0 and len(vogal) > 0:
        return consoante + " " + vogal
    else:
        # pylint: disable=broad-exception-raised
        raise Exception("Consoantes ou Vogais Inválidas para CV")


def extract_from_semivowel_vowel(alias: str):
    """
    Extracts a semivowel and a vowel from a given alias.

    This function takes an alias and extracts a semivowel and a vowel from it.
    It returns a string with the extracted semivowel followed by the extracted
    vowel.

    :param alias: str
        The string to be extracted from.

    :return: str
        A string with the extracted semivowel followed by the extracted vowel.

    :raises:
        Exception
            If the alias does not contain a valid semivowel and a valid vowel.
    """
    semi_vogais = ""  # [y] ou [w]
    vogal = ""

    # extraindo semi_vogais
    # pylint: disable=consider-using-dict-items consider-iterating-dictionary
    for semi in prizma_semi.keys():
        if semi in alias:
            alias = alias.replace(semi, "")
            semi_vogais = prizma_semi[semi]
            break

    # extraindo vogais
    for v in prizma_vogais.keys():
        if v in alias:
            alias = alias.replace(v, "")
            vogal = prizma_vogais[v]
            break

    if len(semi_vogais) > 0 and len(vogal) > 0:
        return semi_vogais + " " + vogal
    else:
        # pylint: disable=broad-exception-raised
        raise Exception("SemiVogais ou Vogais Inválidas para CV")


def extract_from_consonant_consonant(alias: str):
    """
    Extracts two consonants from the given alias and returns them in order.

    This function identifies and extracts two consonants from the provided alias.
    If the alias contains more than two consonants or is invalid, an exception is raised.
    The consonants are returned in the order they appear in the original alias.

    :param alias: str
        The alias from which consonants are to be extracted.

    :return: str
        A string with the two extracted consonants, separated by a space.

    :raises:
        Exception
            If the alias does not allow extraction of exactly two consonants.
    """

    alias_original = alias
    c1 = c2 = ""

    # pylint: disable=consider-iterating-dictionary
    for c in prizma_consoantes.keys():
        if c in alias:
            alias = alias.replace(c, "")
            c1 = c
            break

    # pylint: disable=consider-iterating-dictionary
    for c in prizma_consoantes.keys():
        if c in alias:
            alias = alias.replace(c, "")
            c2 = c
            break

    if len(alias) > 0:
        # pylint: disable=broad-exception-raised
        raise Exception(f"Não foi possível extrair de [{alias_original}]")

    if alias_original.index(c1) > alias_original.index(c2):
        aux = c1
        c1 = c2
        c2 = aux

    return prizma_consoantes[c1] + " " + prizma_consoantes[c2]


def extract_from_vowel_consonant(vogal: str, cons: str) -> str:
    """
    Extracts a vowel, a semivowel (if present) and a consonant from the given strings.

    :param vogal: str
        The string from which a vowel is to be extracted.

    :param cons: str
        The string from which a consonant is to be extracted.

    :return: str
        A string with the extracted vowel, semivowel (if present) and consonant, separated by spaces.

    :raises:
        Exception
            If the strings do not allow extraction of a vowel and a consonant, or if a semivowel is present in the vowel string.
    """
    v = c = semi_v = ""

    # Verificando se vogal possui semivogais
    tem_semivogal = has_semi_vowels(vogal)
    if tem_semivogal:
        # pylint: disable=consider-using-dict-items consider-iterating-dictionary
        for semi in prizma_semi.keys():
            if semi in vogal:
                semi_v = prizma_semi[semi]
                vogal = vogal.replace(semi, "")
                break

    # pylint: disable=consider-using-dict-items consider-iterating-dictionary
    for vogal_prizma in prizma_vogais.keys():
        if vogal_prizma in vogal:
            v = prizma_vogais[vogal_prizma]
            vogal = vogal.replace(vogal_prizma, "")
            break

    # pylint: disable=consider-using-dict-items consider-iterating-dictionary
    for consoante_prizma in prizma_consoantes.keys():
        if consoante_prizma in cons:
            c = prizma_consoantes[consoante_prizma]
            cons = cons.replace(consoante_prizma, "")
            break

    return v + semi_v + " " + c


def extract_from_vowel_vowel(alias: str):
    """
    Extracts a combination of vowels or a vowel and a semivowel from the given alias.

    This function analyzes the provided alias to determine if it contains a sequence of
    two vowels or a vowel and a semivowel. It returns a string with the extracted components 
    in the appropriate format. Handles cases where the alias may contain a hyphen, indicating
    a special structure.

    :param alias: str
        The alias to extract the vowel or vowel-semivowel combination from.

    :return: str
        A string with the extracted components, separated by spaces.
    """

    result = ""
    item1, item2 = alias.split()
    if "-" in alias:
        # [- V] ou [V -]
        if item1 == "-":
            result = item1 + " " + prizma_vogais[item2]
        else:
            result = prizma_vogais[item1] + " " + item2
    else:
        # [V V] ou [V v]
        tem_semi, _ = has_semi_vowels(alias)
        if tem_semi:
            # [V v]
            # print("TEM SEMI: ", alias)
            result = prizma_vogais[item1] + " " + prizma_semi[item2]
        else:
            # [V V]
            result = prizma_vogais[item1] + " " + prizma_vogais[item2]

    return result


def extract_from_vowel(vogal: str):
    """
    Extracts a vowel from the given string.

    :param vogal: str
        The string from which a vowel is to be extracted.

    :return: str
        The extracted vowel.

    :raises:
        Exception
            If the string does not contain a valid vowel.
    """
    result = ""

    try:
        result = prizma_vogais[vogal]
        return result
    except Exception:  # pylint: disable=broad-except
        return result
