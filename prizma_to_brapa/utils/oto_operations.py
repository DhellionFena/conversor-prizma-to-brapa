'''
File with operations related to oto.ini
'''
import tkinter as tk
from tkinter import filedialog

import pandas as pd


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
