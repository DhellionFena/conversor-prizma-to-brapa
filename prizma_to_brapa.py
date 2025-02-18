'''
Module with everything about the project
'''

import tkinter as tk
from tkinter import filedialog
import pandas as pd

prizma_vogais = {
    "a'": "ax",
    "e'": "eh",
    "o'": "oh",
    "a": "a",
    "e": "e",
    "i": "i",
    "o": "o",
    "u": "u",
    "An": "an",
    "Am": "an",
    "A": "an",
    "En": "en",
    "Em": "en",
    "E": "en",
    "In": "in",
    "Im": "in",
    "I": "in",
    "On": "on",
    "Om": "on",
    "O": "on",
    "Un": "un",
    "Um": "un",
    "U": "un",
}

prizma_consoantes = {
    "b": "b",
    "dj": "dj",
    "d": "d",
    "f": "f",
    "g": "g",
    "j": "j",
    "k": "k",
    "lh": "lh",
    "l": "l",
    "m": "m",
    "nh": "nh",
    "n": "n",
    "p": "p",
    "rr": "hr",  # r carioca
    "rh": "h",  # r hálito
    "r": "r",  # r tapa
    "RR": "rr",  # r trilhado
    "R": "rw",  # r caipira
    "s": "s",
    "tch": "ch",
    "t": "t",
    "v": "v",
    "x": "sh",
    "z": "z",
}

prizma_semi = {
    "yn": "y",
    "wn": "w",
    "y": "y",
    "w": "w",
}

prizma_cc = [
    "br",
    "dr",
    "fr",
    "gr",
    "kr",
    "pr",
    "tr",
    "vr",
    "bl",
    "dl",
    "fl",
    "gl",
    "kl",
    "pl",
    "tl",
    "vl"
]


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


def get_oto() -> pd.DataFrame:
    """
    Opens a file explorer to select an OTO.ini file and returns a DataFrame with the file's lines.

    :return: pd.DataFrame
        A DataFrame with the columns "name", "alias", "prefix", "suffix", "offset", "consonant", "cutoff", "pretturance" and "overlap"
    """

    root = tk.Tk()
    root.withdraw()

    # Opens a file explorer to select a file
    filepath = filedialog.askopenfilename(
        title="Select an OTO file",
        filetypes=[("OTO files", "*.ini")]
    )

    # Checks if a file was selected
    if filepath:
        if filepath.endswith('.ini'):
            prefix = input("Diga o prefixo (deixe em branco se não tiver): ")
            suffix = input("Diga o sufixo (deixe em branco se não tiver): ")
            with open(filepath, 'r', encoding='utf-8') as file:
                oto = file.readlines()
                lista_oto = []
                for linha_oto in oto:
                    nome_sample, params = linha_oto.split("=")
                    alias, offset, consonant, cutoff, pretturance, overlap = params.split(
                        ',')
                    alias = alias.replace(prefix, "").replace(suffix, "")
                    oto_dict = {
                        "name": nome_sample,
                        "alias": alias,
                        "prefix": prefix,
                        "suffix": suffix,
                        "offset": offset,
                        "consonant": consonant,
                        "cutoff": cutoff,
                        "pretturance": pretturance,
                        "overlap": overlap.replace("\n", ""),
                    }
                    lista_oto.append(oto_dict)

                return pd.DataFrame(lista_oto)


def save_new_oto(oto: [dict], src: str = "output/oto.ini"):
    """
    Saves a list of OTO entries to a specified .ini file.

    Each entry in the 'oto' list is a dictionary containing the following keys:
    "name", "alias", "prefix", "suffix", "offset", "consonant", "cutoff", 
    "pretturance", and "overlap". These values are written to the specified
    file in the format: 'name=prefixalias,suffix,offset,consonant,cutoff,
    pretturance,overlap'.

    :param src: str, default = "output/oto.ini"
        The file path where the OTO entries will be saved.
    :param oto: list, default = []
        A list of dictionaries, each representing an OTO entry.
    """

    with open(src, "w", encoding="utf-8") as file:
        for linha in oto:
            # print(linha)
            # u-o-e__e-a-i__i-a-u.wav=o e_2,2812.359,300,-800,200,100
            string = linha["name"] + "=" + linha["prefix"] + linha["alias"] + linha["suffix"] + "," + linha["offset"] + \
                "," + linha["consonant"] + "," + linha["cutoff"] + "," + \
                linha["pretturance"] + "," + linha["overlap"] + "\n"

            file.write(string)


def generate_oto_dict(alias: str, linha_oto):
    """
    Generates a dictionary representing an OTO entry.

    :param alias: str
        The alias for the OTO entry.
    :param linha_oto: object
        An object containing the other fields for the OTO entry.

    :return: dict
        A dictionary containing the fields for the OTO entry.
    """
    oto_dict = {
        "name": linha_oto.name,
        "alias": alias,
        "prefix": linha_oto.prefix,
        "suffix": linha_oto.suffix,
        "offset": linha_oto.offset,
        "consonant": linha_oto.consonant,
        "cutoff": linha_oto.cutoff,
        "pretturance": linha_oto.pretturance,
        "overlap": linha_oto.overlap,
    }
    return oto_dict


def main():
    """
    Main function for the project.

    Gets an OTO file, parses it and generates a new one with the corresponding
    aliases for each line, following the rules of the Brapra project.

    The aliases are generated by splitting the original alias into its parts and
    checking if it has a vowel, a consonant, or a semivowel. Depending on this, the
    corresponding extractor function is called to generate the new alias.

    After generating all the new aliases, the new OTO file is saved with the
    generated aliases.

    The function also handles cases where the alias has a hyphen, and adds the
    corresponding hyphen to the new alias.
    """
    oto_dataframe = get_oto()
    new_oto_entries = []

    for oto_line in oto_dataframe.itertuples():
        alias = oto_line.alias
        new_alias = ""
        add_hyphen_start = False
        add_hyphen_end = False
        add_ending_r_or_l = False

        # Check if the alias has a vowel, a semivowel, or a consonant
        alias_check = alias
        has_vowel, alias_check = has_vowels(alias_check)
        has_semivowel, alias_check = has_semi_vowels(alias_check)
        has_consonant, alias_check = has_consonants(alias_check)

        # Handle cases without spaces in the alias
        if " " not in alias:
            if has_vowel and has_consonant:
                new_alias = extract_from_consonant_vowel(alias)
                add_hyphen_start = True

            elif has_vowel and not has_consonant:
                if has_semivowel:
                    new_alias = extract_from_semivowel_vowel(alias)
                    add_hyphen_start = True
                else:
                    new_alias = extract_from_vowel(alias)

            elif not has_vowel and has_consonant:
                new_alias = extract_from_consonant_consonant(alias)

            else:
                raise Exception(f"Invalid alias: {oto_line.alias}")

        # Handle cases with spaces in the alias
        else:
            alias_parts = alias.split()
            if len(alias_parts) == 2:
                if has_vowel and has_consonant:
                    new_alias = extract_from_vowel_consonant(
                        vogal=alias_parts[0], cons=alias_parts[1])
                    add_hyphen_end = True
                    add_ending_r_or_l = can_add_r_or_l(alias_parts[1])

                elif has_vowel and not has_consonant:
                    new_alias = extract_from_vowel_vowel(alias)

                    if has_semivowel:
                        add_hyphen_end = True

                elif not has_vowel and has_consonant:
                    pass
                else:
                    raise Exception(f"Invalid alias: {oto_line.alias}")

        # Add the new alias to the list and add the corresponding hyphen
        if new_alias:
            oto_dict = generate_oto_dict(new_alias, oto_line)
            new_oto_entries.append(oto_dict)

            if add_hyphen_start:
                oto_dict = generate_oto_dict("-" + new_alias, oto_line)
                new_oto_entries.append(oto_dict)

            if add_hyphen_end:
                oto_dict = generate_oto_dict(new_alias + "-", oto_line)
                new_oto_entries.append(oto_dict)

            if add_ending_r_or_l:
                for suffix in ["r", "r-", "l", "l-"]:
                    oto_dict = generate_oto_dict(new_alias + suffix, oto_line)
                    new_oto_entries.append(oto_dict)

    # Save the new OTO file
    save_new_oto(oto=new_oto_entries)
    print("New OTO file generated.")


if __name__ == "__main__":
    main()
