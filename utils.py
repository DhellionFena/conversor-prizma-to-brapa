def get_vogais(alias : str) -> list[str]:
    for i in range(len(2)):
        for prizma_v in prizma_vogais.keys():
            if prizma_v in alias:
                alias.count(prizma_v)
                alias = alias.replace(prizma_v, "")
                vogais.append(prizma_vogais[prizma_v])
                break
    return []