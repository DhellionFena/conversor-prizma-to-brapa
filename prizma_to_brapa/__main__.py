import utils

def main():
    oto_df = utils.get_oto(suffix="_2")

    nova_oto = []
    for linha_oto in oto_df.itertuples():
        alias : str = linha_oto.alias
        novo_alias = ""

        tem_vogal = utils.has_vowels(alias)
        tem_semivogal = utils.has_semi_vowels(alias)
        tem_consoante = utils.has_consonants(alias)

        if " " not in alias:
            # fonemas [CV] ou [CCV] ou [CC] ou [VV] ou [vV]

            if tem_vogal and tem_consoante:
                # [CV] ou [CCV]
                novo_alias = utils.extract_from_CV(alias)

            elif tem_vogal and not tem_consoante:
                # [VV] ou [vV]
                # Ignorando [VV] por enquanto. Será aproveitado o formato [V V]

                if tem_semivogal:
                    # [vV], ou seja: [yV] ou [wV]
                    novo_alias = utils.extract_from_vV(alias)

            elif not tem_vogal and tem_consoante:
                # [CC]
                novo_alias = utils.extract_from_CC(alias)
            
            else:
                raise Exception(f"Alias inválido: {linha_oto.alias}")

        else:
            # fonemas [V C] ou [V V] ou [V v] ou [Vv C] ou [- V] ou [V -]

            alias_itens = alias.split()
            if len(alias_itens) == 2:
                if tem_vogal and tem_consoante:
                    # [V C] ou [Vv C]
                    novo_alias = utils.extract_from_V_C(vogal=alias_itens[0], cons=alias_itens[1])
                    print(novo_alias)

                elif tem_vogal and not tem_consoante:
                    # [- V] ou [V V] ou [V v] ou [V -]
                    pass

                elif not tem_vogal and tem_consoante:
                    # [C -]
                    # Tratamento Ignorado
                    pass
                else:
                    raise Exception(f"Alias Inválido: {linha_oto.alias}")



if __name__ == "__main__":
    main()