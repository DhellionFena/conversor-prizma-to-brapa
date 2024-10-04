import utils

def main():
    oto_df = utils.get_oto(suffix="_2")

    nova_oto = []
    for linha_oto in oto_df.itertuples():
        alias : str = linha_oto.alias
        novo_alias = ""

        consoantes = []
        vogais = []

        if " " not in alias:
            # fonemas [CV] ou [CCV] ou [CC] ou [VV] ou [vV]

            tem_vogal = utils.has_vowels(alias)
            tem_consoante = utils.has_consonants(alias)

            if tem_vogal and tem_consoante:
                # [CV] ou [CCV]
                novo_alias = utils.extract_from_CV(alias)

            elif tem_vogal and not tem_consoante:
                # [VV] ou [vV]
                # Ignorando [VV] por enquanto. Será aproveitado o formato [V V]

                if utils.has_semi_vowels(alias):
                    # [vV], ou seja: [yV] ou [wV]
                    novo_alias = utils.extract_from_vV(alias)
                    print(alias)
                    print(novo_alias)

            elif not tem_vogal and tem_consoante:
                # [CC]
                novo_alias = utils.extract_from_CC(alias)
            
            else:
                raise(Exception(f"Alias inválido: {linha_oto.alias}"))

        else:
            # fonema [V C] ou [V V] ou [Vv C]
            # print("VC: ", alias)
            pass



if __name__ == "__main__":
    main()