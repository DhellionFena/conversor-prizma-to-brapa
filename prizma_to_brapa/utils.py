import pandas as pd
from dicionario import prizma_cc, prizma_consoantes, prizma_semi, prizma_vogais

def get_oto(src : str = "input/oto.ini", prefix: str = "", suffix : str = "") -> pd.DataFrame:

    # lendo oto.ini original
    with open(src, "r") as file:
        oto = file.readlines()

    lista_oto = []
    for linha_oto in oto:
        nome_sample, params = linha_oto.split("=")
        alias, offset, consonant, cutoff, pretturance, overlap = params.split(',')
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

def save_new_oto(src : str = "output/oto.ini", oto : list = []):

    with open(src, "w") as file:
        for linha in oto:
            # print(linha)
            # u-o-e__e-a-i__i-a-u.wav=o e_2,2812.359,300,-800,200,100
            string = linha["name"] + "=" + linha["prefix"] + linha["alias"] + linha["suffix"] + "," + linha["offset"] + "," + linha["consonant"] + "," + linha["cutoff"] + "," + linha["pretturance"] + "," + linha["overlap"] + "\n"

            file.write(string)

def generate_oto_dict(alias: str, linha_oto):
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

def has_vowels(alias : str) -> (bool,str):
    for letra in prizma_vogais.keys():
        if letra in alias:
            return (True, alias.replace(letra, ""))
    return False, alias

def has_semi_vowels(alias : str) -> (bool,str):
    for letra in prizma_semi.keys():
        if letra in alias:
            alias = alias.replace(letra, "")
            return (True, alias.replace(letra, ""))
    return False, alias

def has_consonants(alias : str) -> (bool,str):
    for letra in prizma_consoantes.keys():
        if letra in alias:
            alias = alias.replace(letra, "")
            return (True, alias.replace(letra, ""))
    return False, alias

def extract_from_CV(alias : str):

    consoante = ""
    vogal = ""

    # extraindo consoantes duplas primeiro
    for cc in prizma_cc:
        if cc in alias:
            alias = alias.replace(cc, "")
            consoante = cc
            break
    
    if len(consoante) == 0:
        for c in prizma_consoantes.keys():
            if c in alias:
                alias = alias.replace(c, "")
                consoante = prizma_consoantes[c]
                break
    
    # extraindo vogais
    for v in prizma_vogais.keys():
        if v in alias:
            alias = alias.replace(v, "")
            vogal = prizma_vogais[v]
            break
    if len(consoante) > 0 and len(vogal) > 0:
        return consoante + " " + vogal
    else:
        raise Exception("Consoantes ou Vogais Inválidas para CV")

def extract_from_vV(alias : str):

    semi_vogais = "" # [y] ou [w]
    vogal = ""

    # extraindo semi_vogais
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
        raise Exception("SemiVogais ou Vogais Inválidas para CV")

def extract_from_CC(alias : str):
    alias_original = alias
    c1 = c2 = ""

    for c in prizma_consoantes.keys():
            if c in alias:
                alias = alias.replace(c, "")
                c1 = c
                break

    for c in prizma_consoantes.keys():
            if c in alias:
                alias = alias.replace(c, "")
                c2 = c
                break
    
    if len(alias) > 0:
        raise(f"Não foi possível extrair de [{alias_original}]")
    
    if alias_original.index(c1) > alias_original.index(c2):
        aux = c1
        c1 = c2
        c2 = aux
    
    return prizma_consoantes[c1] + " " + prizma_consoantes[c2]


def extract_from_V_C(vogal: str, cons:str) -> str:
    v = c = semi_v = ""

    # Verificando se vogal possui semivogais
    tem_semivogal = has_semi_vowels(vogal)
    if tem_semivogal:
        for semi in prizma_semi.keys():
            if semi in vogal:
                semi_v = prizma_semi[semi]
                vogal = vogal.replace(semi, "")
                break
    
    for vogal_prizma in prizma_vogais.keys():
        if vogal_prizma in vogal:
            v = prizma_vogais[vogal_prizma]
            vogal = vogal.replace(vogal_prizma, "")
            break
    
    for consoante_prizma in prizma_consoantes.keys():
        if consoante_prizma in cons:
            c = prizma_consoantes[consoante_prizma]
            cons = cons.replace(consoante_prizma, "")
            break

    return v + semi_v + " " + c


def extract_from_V_V(alias: str):
    result = ""
    item1, item2 = alias.split()
    if "-" in alias:
        # [- V] ou [V -]
        if item1 == "-":
            result = item1 + " " + prizma_vogais[item2]
        else:
            result = prizma_vogais[item1] + item2 
    else:
        #[V V] ou [V v]
        tem_semi, _ = has_semi_vowels(alias)
        if tem_semi:
            # [V v]
            print("TEM SEMI: ", alias)
            result = prizma_vogais[item1] + " " + prizma_semi[item2]
        else:
            # [V V]
            result = prizma_vogais[item1] + " " + prizma_vogais[item2]
    
    
    return result

def extract_from_V(vogal: str):
    result = ""

    try:
        result = prizma_vogais[vogal]
        return result
    except:
        return result

def can_add_r_or_l(alias: str):
    for fonema in prizma_cc:
        if alias[-1] in fonema[0]:
            return True
    return False