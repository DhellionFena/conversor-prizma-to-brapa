import pandas as pd

# lendo oto.ini original
with open("input/oto.ini", "r") as file:
    oto = file.readlines()

prefix = ""
suffix = "_2"

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

oto_df = pd.DataFrame(lista_oto)

prizma_vogais = {
    "a'" : ["ax"],
    "e'" : ["eh", "ae"],
    "o'" : ["oh"],
    "a" : ["a"],
    "e": ["e"],
    "i": ["i"],
    "o": ["o"],
    "u": ["u"],
    "An" : ["an"],
    "Am" : ["an"],
    "A" : ["an"],
    "En" : ["en"],
    "Em" : ["en"],
    "E" : ["en"],
    "In" : ["in"],
    "Im" : ["in"],
    "I" : ["in"],
    "On" : ["on"],
    "Om" : ["on"],
    "O" : ["on"],
    "Un" : ["un"],
    "Um" : ["un"],
    "U" : ["un"],
}

prizma_consoantes = {
    "b": ["b"],
    "dj": ["dj"],
    "d": ["d"],
    "f": ["f"],
    "g": ["g"],
    "j": ["j"],
    "k": ["k"],
    "lh": ["lh"],
    "l": ["l"],
    "m": ["m"],
    "nh": ["nh"],
    "n": ["n"],
    "p": ["p"],
    "rr": ["hr"], # r carioca
    "rh": ["h"], # r hálito
    "r": ["r"], # r tapa
    "RR": ["rr"], # r trilhado
    "R": ["rw"], # r caipira
    "s": ["s"],
    "tch": ["ch"],
    "t": ["t"],
    "v": ["v"],
    "x": ["sh"],
    "z": ["z"],
}

prizma_semic = {
    "yn": ["y"],
    "wn": ["w"],
    "y": ["y"],
    "w": ["w"],
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


# prizma_cc = {
#     "br": ["br","b r"],
#     "dr": ["dr", "d r"],
#     "fr": ["fr","f r"],
#     "gr": ["gr","g r"],
#     "kr": ["kr","k r"],
#     "pr": ["pr","p r"],
#     "tr": ["tr","t r"],
#     "vr": ["vr","v r"],

#     "bl": ["bl","b l"],
#     "dl": ["dl", "d l"],
#     "fl": ["fl","f l"],
#     "gl": ["gl","g l"],
#     "kl": ["kl","k l"],
#     "pl": ["pl","p l"],
#     "tl": ["tl","t l"],
#     "vl": ["vl","v l"],
# }

# print(oto_df)

nova_oto = []
for linha_oto in oto_df.itertuples():
    alias : str = linha_oto.alias
    original = alias
    novas_linhas = []

    if " " not in alias:
        # fonema CV ou CCV ou CC ou VV
        consoantes = []
        vogais = []

        # coletando Vogais
        for i in range(2):
            for prizma_v in prizma_vogais.keys():
                if prizma_v in alias:
                    count = alias.count(prizma_v)
                    alias = alias.replace(prizma_v, "")

                    if count > 1:
                        vogais.append(prizma_vogais[prizma_v])
                        vogais.append(prizma_vogais[prizma_v])
                    else:
                        vogais.append(prizma_vogais[prizma_v])
                    break

        match len(vogais):
            case 0:
                # CC
                for i in range(2):
                    for prizma_c in prizma_consoantes.keys():
                        if prizma_c in alias:
                            count = alias.count(prizma_c)
                            alias = alias.replace(prizma_c, "")

                            if count > 1:
                                consoantes.append(prizma_consoantes[prizma_c])
                                consoantes.append(prizma_consoantes[prizma_c])
                            else:
                                consoantes.append(prizma_consoantes[prizma_c])
                            break

                # adicionando alias convertidos
                for itens_c1 in consoantes[0]:
                    for c1 in itens_c1:
                        for itens_c2 in consoantes[1]:
                            for c2 in itens_c2:
                                novo_alias = c1 +  " " + c2
                                novas_linhas.append(novo_alias)
                                print(original, novo_alias)

            case 1:
                # CCV ou CV
                for cc in prizma_cc:
                    if cc in alias:
                        alias = alias.replace(cc, "")
                        consoantes.append([cc])
                        break

                if len(consoantes) == 0:
                    # CV
                    for prizma_c in prizma_consoantes.keys():
                        if prizma_c in alias:
                            alias = alias.replace(prizma_c, "")
                            consoantes.append(prizma_consoantes[prizma_c])
                            break
                
                if len(consoantes) == 0:
                    # (y ou w)
                    for prizma_c in prizma_semic.keys():
                        if prizma_c in alias:
                            alias = alias.replace(prizma_c, "")
                            consoantes.append(prizma_semic[prizma_c])
                            break
                

                # adicionando alias convertidos
                for itens_c in consoantes:
                    for c in itens_c:
                        for itens_v in vogais:
                            for v in itens_v:
                                novo_alias = c +  " " + v
                                novas_linhas.append(novo_alias)

            case 2:
                # VV, nesse caso será usado o "V V" então essas samples serão descartadas
                pass
            
            case _:
                raise Exception("DEU RUIM")


        if len(alias) > 0:
            #casos extraordinarios
            print(f"original: {original} | diferente: {alias}")

    else:
        # fonema "V C" ou "V V"
        # print("VC: ", alias)
        pass

