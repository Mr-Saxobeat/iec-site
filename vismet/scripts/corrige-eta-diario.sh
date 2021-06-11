#!/bin/bash

# A partir das simula��es do modelo ETA que possui 30 tempos por m�s, consertam-se os dias 
# 29 e 30 de feveiro para que o CDO e depois converte os dados de bin�rio para NetCDF, e por fim, 
# junta todos os arquivos em um s�.
# Autor: Guilherme Martins - 15/03/2020. E-mail: jgmsantos@gmail.com
# https://guilherme.readthedocs.io/en/latest

# Requisitos: CDO e o arquivo tmp.ctl que servir� de modelo para criar o ct. para os bin�rios.

# O arquivo bin�rio utilizado possui a seguinte nomenclatura:
# Eta_Eta_HadGEM2-ES_5km_Historical_Diario_MXTP_YYYYMMDD.bin
# YYYY = ano, MM = m�s e DD = dia.

# A partir do tmp.ctl cria-se um ctl para cada arquivo bin�rio acima.

# Ao executar o script v�o aparecer os 2 dois erros porque o CDO n�o consegue converter as datas 29 e 30 de fevereiro.

#Syntax Error:  Invalid Date/Time value.
#  Day = 29 -- greater than 28
#Open Error:  Invalid start time in tdef card starting value
#  --> The invalid description file record is:
#  --> TDEF 1 LINEAR 29Feb2005 1dy
#  The data file was not opened.

#cdo(1) import_binary (Abort): Open failed!

#Syntax Error:  Invalid Date/Time value.
#  Day = 30 -- greater than 28
#Open Error:  Invalid start time in tdef card starting value
#  --> The invalid description file record is:
#  --> TDEF 1 LINEAR 30Feb2005 1dy
#  The data file was not opened.
#
#cdo(1) import_binary (Abort): Open failed!

for ano in {1961..2006}
do
    if [ $# -eq 0 ]
    then
        echo "Forneça o caminho dos arqivos .bin"
        echo "Exemplo: sudo ./corrige-eta-diario.sh /home/dados/eta/"
    fi

    cd $1

    for nome_arquivo in $(ls *$ano????.bin)
    do
        ## Pega o nome do arquivo sem a data,
        ## ex: Eta_Eta_HadGEM2-ES_5km_Historical_Diario_MXTP_
        nome_arquivo_variavel=$(echo $nome_arquivo | cut -d_ -f1-7)_

        # Armazena a data no formato YYYYMMDD.
        data=$(echo $nome_arquivo | cut -d_ -f8)

        mes=${data:4:2} # MM 
        dia=${data:6:2} # DD

        # Altero cada valor do m�s (01, ..., 12) para o formato string => Jan, ..., Dec.
        if [ $mes = 01 ] ; then mesc="Jan" ; fi
        if [ $mes = 02 ] ; then mesc="Feb" ; fi
        if [ $mes = 03 ] ; then mesc="Mar" ; fi
        if [ $mes = 04 ] ; then mesc="Apr" ; fi
        if [ $mes = 05 ] ; then mesc="May" ; fi
        if [ $mes = 06 ] ; then mesc="Jun" ; fi
        if [ $mes = 07 ] ; then mesc="Jul" ; fi
        if [ $mes = 08 ] ; then mesc="Aug" ; fi
        if [ $mes = 09 ] ; then mesc="Sep" ; fi
        if [ $mes = 10 ] ; then mesc="Oct" ; fi
        if [ $mes = 11 ] ; then mesc="Nov" ; fi
        if [ $mes = 12 ] ; then mesc="Dec" ; fi
        
        # Copia o ".ctl" modelo para cada arquivo ".bin".
        cp ${nome_arquivo_variavel}template.ctl $(basename $nome_arquivo .bin).ctl

        ## Corrige a primeira linha do ctl
        sed -i "/DSET/c\DSET ^$nome_arquivo" $(basename $nome_arquivo .bin).ctl

        ## Delete a terceira linha do ctl
        sed -i "3d" $(basename $nome_arquivo .bin).ctl

        ## Substitui a linha TDEF
        sed -i "/TDEF/c\TDEF 1 LINEAR ${dia}${mesc}${ano} 1dy" $(basename $nome_arquivo .bin).ctl

        # Converte de bin�rio (.ctl) para NetCDF (.nc).
        cdo -s -r -f nc -setcalendar,360_day -import_binary $(basename $nome_arquivo .bin).ctl $(basename $nome_arquivo .bin).nc
    done

    # O trecho abaixo conserta os dias 29 e 30 de feveiro.

    # Enganar o CDO para consertar os dias 29 e 30 de fevereiro de 2005 porque � sa�da do modelo com 360 dias.
    # Na linha 6 do Eta_Eta_HadGEM2-ES_5km_Historical_Diario_MXTP_20050229.ctl alterar a data para
    # TDEF 1 LINEAR 28Feb2005 1dy
    # O mesmo � feito para o dia 30 de fevereiro:
    # Na linha 6 do Eta_Eta_HadGEM2-ES_5km_Historical_Diario_MXTP_20050230.ctl alterar a data para
    # TDEF 1 LINEAR 28Feb2005 1dy
    # Depois a data e o calend�rio s�o consertados para os dias corretos. A ordem dos operadores � importante.

    #  Altera diretamente no arquivo (-i) o dia 29 para o dia 28 e o dia 30 para o dia 28.
    sed -i 's/29Feb/28Feb/' ${nome_arquivo_variavel}${ano}0229.ctl
    sed -i 's/30Feb/28Feb/' ${nome_arquivo_variavel}${ano}0230.ctl

    # Loop nos dias 29 e 30 de fevereiro.
    for dia in 29 30
    do
        cdo -r -s -f nc -settaxis,"$ano"-02-"$dia",00:00:00,1day \
                        -setcalendar,360_day \
                        -import_binary \
                        ${nome_arquivo_variavel}${ano}02${dia}.ctl \
                        ${nome_arquivo_variavel}${ano}02${dia}.nc
    done

    echo "================================================================================="

    # Junta todos os arquivos do ano em um só.
    for mes in {01..12}
    do
        echo $ano$mes
        # Junta m�s a m�s para ver se tudo est� sendo feito corretamente.
        cdo -s -O mergetime $nome_arquivo_variavel$ano$mes??.nc tmp01.$ano$mes.nc
    done

    # Junta todos arquivos (360 tempos) no arquivo final => Eta_Eta_HadGEM2-ES_5km_Historical_$ano.nc
    cdo -s -O mergetime tmp01.$ano??.nc ${nome_arquivo_variavel}${ano}.nc

    # Remove arquivos desnecess�rios.
    rm -f tmp01.??????.nc
done