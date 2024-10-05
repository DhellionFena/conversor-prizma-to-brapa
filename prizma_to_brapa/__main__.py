import utils

def main():
    oto_df = utils.get_oto(suffix="_1")

    nova_oto = []
    for linha_oto in oto_df.itertuples():
        alias : str = linha_oto.alias
        novo_alias = ""
        add_hifen_start = False
        add_hifen_end = False
        add_ending_r_l = False

        alias_check = alias
        tem_vogal, alias_check = utils.has_vowels(alias_check)
        tem_semivogal, alias_check = utils.has_semi_vowels(alias_check)
        tem_consoante, alias_check = utils.has_consonants(alias_check)

        if " " not in alias:
            # fonemas [CV] ou [CCV] ou [CC] ou [VV] ou [vV] ou [V]

            if tem_vogal and tem_consoante:
                # [CV] ou [CCV]
                novo_alias = utils.extract_from_CV(alias)
                add_hifen_start = True

            elif tem_vogal and not tem_consoante:
                # [VV] ou [vV] ou [V]

                if tem_semivogal:
                    # [vV], ou seja: [yV] ou [wV]
                    novo_alias = utils.extract_from_vV(alias)
                else:
                    # [V] ou [VV]
                    # Ignorando [VV] por enquanto. Será aproveitado o formato [V V]
                    novo_alias = utils.extract_from_V(alias)

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
                    add_hifen_end = True
                    add_ending_r_l = utils.can_add_r_or_l(alias_itens[1])

                elif tem_vogal and not tem_consoante:
                    # [- V] ou [V V] ou [V v] ou [V -]
                    novo_alias = utils.extract_from_V_V(alias)

                    if tem_semivogal:
                        add_hifen_end = True

                elif not tem_vogal and tem_consoante:
                    # [C -]
                    # Tratamento Ignorado
                    pass
                else:
                    raise Exception(f"Alias Inválido: {linha_oto.alias}")
        
        if len(novo_alias) > 0:
            oto_dict = utils.generate_oto_dict(novo_alias, linha_oto)
            nova_oto.append(oto_dict)

            if add_hifen_start:
                oto_dict = utils.generate_oto_dict("-"+novo_alias, linha_oto)
                nova_oto.append(oto_dict)

            if add_hifen_end:
                oto_dict = utils.generate_oto_dict(novo_alias+"-", linha_oto)
                nova_oto.append(oto_dict)
            
            if add_ending_r_l:

                oto_dict = utils.generate_oto_dict(novo_alias+"r", linha_oto)
                nova_oto.append(oto_dict)

                oto_dict = utils.generate_oto_dict(novo_alias+"r-", linha_oto)
                nova_oto.append(oto_dict)

                oto_dict = utils.generate_oto_dict(novo_alias+"l", linha_oto)
                nova_oto.append(oto_dict)

                oto_dict = utils.generate_oto_dict(novo_alias+"l-", linha_oto)
                nova_oto.append(oto_dict)
    
    utils.save_new_oto(oto=nova_oto)
    print("NOVA OTO GERADA.")


if __name__ == "__main__":
    main()