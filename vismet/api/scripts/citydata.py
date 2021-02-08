import os
import geopandas
import csv
import requests
import datetime

def get_cities_fid(shp_file_dir):
    shp_file = geopandas.read_file(os.path.join(shp_file_dir, 'ES_Municipios.shp'))
    fids = list(shp_file.FID)
    return fids


# Script para carregar dados de municípios via rest
def run(base_dir='/home/weiglas/Documents/iec/dados/3. Dados de Cenários Futuros/Media por Munucipios --- Eta 5km HADGEM2-ES /',
        shp_file_dir = 'esmunicpios/',
        data_file_dir = 'dados-municipios/',
        url='http://127.0.0.1:8000/api2/citydata/'):

    fids = get_cities_fid(os.path.join(base_dir, shp_file_dir))

    evtp_dir = os.path.join(base_dir, data_file_dir, 'EVTP/')
    mntp_dir = os.path.join(base_dir, data_file_dir, 'MNTP/')
    mxtp_dir = os.path.join(base_dir, data_file_dir, 'MXTP/')
    ocis_dir = os.path.join(base_dir, data_file_dir, 'OCIS/')
    prec_dir = os.path.join(base_dir, data_file_dir, 'PREC/')
    tp2m_dir = os.path.join(base_dir, data_file_dir, 'TP2M/')

    for model_name in os.listdir(evtp_dir):

        # remover isso depois !K!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        if model_name != 'RCP 4.5':
            continue

        evtp_files = os.listdir(os.path.join(evtp_dir, model_name))
        mntp_files = os.listdir(os.path.join(mntp_dir, model_name))
        mxtp_files = os.listdir(os.path.join(mxtp_dir, model_name))
        ocis_files = os.listdir(os.path.join(ocis_dir, model_name))
        prec_files = os.listdir(os.path.join(prec_dir, model_name))
        tp2m_files = os.listdir(os.path.join(tp2m_dir, model_name))

        data_model_name = model_name
        if data_model_name == 'Historical':
            data_model_name = 'Histórico'

        for i_file, data_file in enumerate(evtp_files):
            evtp_f = open(os.path.join(evtp_dir, model_name, evtp_files[i_file]), 'r')
            mntp_f = open(os.path.join(mntp_dir, model_name, mntp_files[i_file]), 'r')
            mxtp_f = open(os.path.join(mxtp_dir, model_name, mxtp_files[i_file]), 'r')
            ocis_f = open(os.path.join(ocis_dir, model_name, ocis_files[i_file]), 'r')
            prec_f = open(os.path.join(prec_dir, model_name, prec_files[i_file]), 'r')
            tp2m_f = open(os.path.join(tp2m_dir, model_name, tp2m_files[i_file]), 'r')

            evtp = list(csv.reader(evtp_f))
            mntp = list(csv.reader(mntp_f))
            mxtp = list(csv.reader(mxtp_f))
            ocis = list(csv.reader(ocis_f))
            prec = list(csv.reader(prec_f))
            tp2m = list(csv.reader(tp2m_f))

            for i_row, row in enumerate(evtp):
                evtp_row = evtp[i_row]
                mntp_row = mntp[i_row]
                mxtp_row = mxtp[i_row]
                ocis_row = ocis[i_row]
                prec_row = prec[i_row]
                tp2m_row = tp2m[i_row]

                if len(evtp_row[0]) > 4:
                    date = datetime.date(int(evtp_row[0][1:]), int(evtp_row[1]), 1)
                else:
                    date = datetime.date(int(evtp_row[0]), int(evtp_row[1]), 1)

                # remover isso depois !K!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
                if date.year < 2082:
                    print(date.year)
                    continue

                for i_col, col in enumerate(evtp_row[2:]):
                    i_col = i_col + 2
                    evtp_value = evtp_row[i_col]
                    mntp_value = mntp_row[i_col]
                    mxtp_value = mxtp_row[i_col]
                    ocis_value = ocis_row[i_col]
                    prec_value = prec_row[i_col]
                    tp2m_value = tp2m_row[i_col]
                    fid = fids[i_col - 2]

                    data = {
                        'evapo': evtp_value,
                        'minTemp': mntp_value,
                        'maxTemp': mxtp_value,
                        'ocis': ocis_value,
                        'precip': prec_value,
                        'tp2m': tp2m_value,
                        'city_fid': fid,
                        'data_model': data_model_name,
                        'date': date.strftime('%Y-%m-%d')
                    }

                    response = requests.post(url, data=data, verify=False)

                    if response.status_code == 201:
                        print(data_model_name + ' ' + str(fid) + ' ' + date.strftime('%d/%m/%Y'))
                    else:
                        print('STATUS CODE: ' + str(response.status_code))
                        print('i_col = ' + str(i_col))
                        print(response.text)
                        print(data)
                        return 0

            evtp_f.close()
            mntp_f.close()
            mxtp_f.close()
            ocis_f.close()
            prec_f.close()
            tp2m_f.close()


    print("ACABOU")


                    