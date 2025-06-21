# actions.py
# from ..utils import extractors, oto_operations, validators
import tkinter as tk
from tkinter import filedialog

import pandas as pd

from prizma_to_brapa.utils.validators import has_semi_vowels, has_vowels
from prizma_to_brapa.utils.validators import has_consonants
from prizma_to_brapa.utils.validators import can_add_r_or_l
from prizma_to_brapa.utils.extractors import extract_from_consonant_vowel
from prizma_to_brapa.utils.extractors import extract_from_semivowel_vowel
from prizma_to_brapa.utils.extractors import extract_from_vowel
from prizma_to_brapa.utils.extractors import extract_from_vowel_vowel
from prizma_to_brapa.utils.extractors import extract_from_vowel_consonant
from prizma_to_brapa.utils.extractors import extract_from_consonant_consonant


def get_oto_list_str() -> list[str]:

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
            with open(filepath, 'r', encoding='utf-8') as file:
                oto = file.readlines()
                return oto


def get_oto_df_from_str(oto_str: str, prefix="", suffix="") -> pd.DataFrame:
    oto_str = oto_str.strip()
    oto = oto_str.split("\n")
    oto = [linha for linha in oto if "=" in linha]

    prefix = prefix.strip()
    suffix = suffix.strip()

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


def get_oto_str_from_list_dict(oto: list[dict]) -> str:
    string = ""
    for linha in oto:
        # u-o-e__e-a-i__i-a-u.wav=o e_2,2812.359,300,-800,200,100
        string += linha["name"] + "=" + linha["prefix"] + linha["alias"] + linha["suffix"] + "," + linha["offset"] + \
            "," + linha["consonant"] + "," + linha["cutoff"] + "," + \
            linha["pretturance"] + "," + linha["overlap"] + "\n"

    return string


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


def run_conversion(oto_str: str, oto_prefix: str, oto_suffix: str) -> str:
    oto_dataframe = get_oto_df_from_str(oto_str, oto_prefix, oto_suffix)
    new_oto_entries = []

    for oto_line in oto_dataframe.itertuples():
        alias = oto_line.alias
        new_alias = ""
        add_hyphen_start = False
        add_hyphen_end = False
        add_ending_r_or_l = False
        add_ending_x = False

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
                    if " h" == new_alias[-2:]:
                        add_ending_x = True

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

            if add_ending_x:

                ending_rotica = new_alias.replace("h", "x")
                oto_dict = generate_oto_dict(ending_rotica, oto_line)
                new_oto_entries.append(oto_dict)

                oto_dict = generate_oto_dict(ending_rotica+"-", oto_line)
                new_oto_entries.append(oto_dict)

    return get_oto_str_from_list_dict(new_oto_entries)


def save_new_oto(new_oto: str) -> None:

    file_path = filedialog.asksaveasfilename(
        defaultextension=".ini", filetypes=[("OTO Files", "*.ini")])

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_oto)
