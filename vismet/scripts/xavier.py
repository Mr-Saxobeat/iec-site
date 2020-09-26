from vismet.models import XavierStation, XavierStationData
from datetime import datetime
import os
import csv


## Este script lê os arquivos csv de dados coletados por Xavier
## e salva nos modelos de estações Xavier.
def run():

    # Estas variáveis é apenas para controle de limite de dados
    finish = -999
    limite_mes = 1 #Quantidade de meses a rodar

    print("Verifique se se os caminhos dos arquivos e o limite de dados a serem rodados estão corretos antes de continuar.")
    resposta = input("S para continuar\nN para cancelar: ")

    if resposta.upper() == 'N':
        return print("Script cancelado.")

    # Pasta raíz dos arquivos que serão abertos
    path = "/home/weiglas/Documents/iec/dados/1. Dados de Estações Historicas/Xavier/Xavier Time Series1980-2017 CSV/"

    # Nomes dos arquivos que serão abertos
    fileET0 = open(path + "Xavier_ET0_1980-2017.csv", 'r')
    fileRelHum = open(path + "Xavier_RelHum_1980-2017.csv", 'r')
    fileRs = open(path + "Xavier_Rs_1980-2017.csv", 'r')
    fileTempMax = open(path + "Xavier_TempMax_1980-2017.csv", 'r')
    fileTempMin = open(path + "Xavier_TempMin_1980-2017.csv", 'r')
    fileU2 = open(path + "Xavier_u2_1980-2017.csv", 'r')

    # Leitor dos arquivos csv
    readerET0 = csv.reader(fileET0)
    readerRelHum = csv.reader(fileRelHum)
    readerRs = csv.reader(fileRs)
    readerTempMax = csv.reader(fileTempMax)
    readerTempMin = csv.reader(fileTempMin)
    readerU2 = csv.reader(fileU2)

    # Na primeira linha do .csv o programa vai pegar todas as datas
    # e armazená-las nesta lista.
    dates  = []

    # Inicialização com false para caso o programa pegue uma célula
    # vazia, ele não salva um model.
    inmet_code = False

    # Loop pelas linhas
    for i, rowET0 in enumerate(readerET0):
        rowRelHum = next(readerRelHum)
        rowRs = next(readerRs)
        rowTempMax = next(readerTempMax)
        rowTempMin = next(readerTempMin)
        rowU2 = next(readerU2)

        # Loop pelas colunas da linha
        for j, valueET0 in enumerate(rowET0):
            valueRelHum = rowRelHum[j]
            valueRs = rowRs[j]
            valueTempMax = rowTempMax[j]
            valueTempMin = rowTempMin[j]
            valueU2 = rowU2[j]

            # Essa conversão é feita para que no banco de daods
            # o armazenamento seja feita de forma correta para
            # serialização entre formatos como json, onde "None"
            # é convertido para "null" para csv é um valor vazio.
            if valueET0 == "NaN":
                valueET0 = None
            if valueRelHum == "NaN":
                valueRelHum = None
            if valueRs == "NaN":
                valueRs = None
            if valueTempMax == "NaN":
                valueTempMax = None
            if valueTempMin == "NaN":
                valueTempMin = None
            if valueU2 == "NaN":
                valueU2 = None

            # Se está na primeira linha, mas não na primeira coluna,
            # pois esta é apenas legenda.
            if i == 0 and j != 0:
                dt = datetime.strptime(valueET0, '%d/%m/%Y')
                dates.append(dt)

                # Este pequeno bloco serve única e exclusivamente
                # para limitar a quantidade de dias que o loop vai iterar.
                # Dessa forma consegue-se fazer um pequeno teste do programa.
                if dt.month > limite_mes:
                    finish = j
                    break

            # A partir da segunda linha, começam os dados
            elif i > 0:
                # A primeira coluna corresponde ao code_inmet da estação
                if j == 0:
                    inmet_code = valueET0

                # Se foi pego um inmet_code e já passou da primeira coluna
                elif inmet_code and j > 0:
                    obj, created = XavierStationData.objects.get_or_create(
                        date = dates[j - 1],
                        station = XavierStation.objects.get(inmet_code=inmet_code),
                        defaults = {
                            'evapo': valueET0,
                            'relHum': valueRelHum,
                            'solarIns': valueRs,
                            'maxTemp': valueTempMax,
                            'minTemp': valueTempMin,
                            'windSpeed': valueU2,
                        }
                    )

                    if not created:
                        obj.evapo = valueET0
                        obj.relHum = valueRelHum
                        obj.solarIns = valueRs
                        obj.maxTemp = valueTempMax
                        obj.minTemp = valueTempMin
                        obj.windSpeed = valueU2
                        obj.save()

                    print(obj)

            # Este pequeno bloco serve única e exclusivamente
            # para limitar a quantidade de dias que o loop vai iterar.
            # Dessa forma consegue-se fazer um pequeno teste do programa.
            if j == finish:
                break

    fileET0.close()
    fileRelHum.close()
    fileRs.close()
    fileTempMax.close()
    fileTempMin.close()
    fileU2.close()
    print("acabou")
