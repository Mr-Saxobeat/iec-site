import json
import requests
import datetime
import time
from rest_framework import status
from vismet.models import Pixel


# Utilizando a api do SERVI:
# https://climateserv.readthedocs.io/en/latest/api.html
def retrieveChirpsData(pixel, startDate, finalDate):
    # Recupera dados de pixel da api SERVI para o modelo CHIRPS

    validation = validateInputs(pixel, startDate, finalDate)
    if validation['status'] == status.HTTP_400_BAD_REQUEST:
        return validation

    # Geometria do pixel para ser passado como parâmetro no request
    geometry = pixel.geom.json

    data = {
        'datatype': 0, # Global CHIRPS 	0 	Daily from 1981 to present
        'begintime': startDate.strftime('%m/%d/%Y'), # MM/DD/YYYY
        'endtime': finalDate.strftime('%m/%d/%Y'), # MM/DD/YYYY
        'intervaltype': 1, # 0-daly, 1-montly, 2-yearly 
        'operationtype': 5, # 0-max, 1-min, 2-median, 3-range, 4-sum, 5-average, 6-download
        'geometry': geometry
        # 'dateType_Category': 'default',
        # 'isZip_CurrentDataType': 'false',
        # 'layerid'
        # 'featureids'
        # 'isZip_CurrentDataType'
    }

    response_of_submit_request = requests.get(
                                    'https://climateserv.servirglobal.net/chirps/submitDataRequest/',
                                    params=data
                                )

    # Se o request de dados foi sucesso
    if response_of_submit_request.status_code == status.HTTP_200_OK:
        request_id = response_of_submit_request.json()[0]
        count_tries = 0

        # Verifica o progresso do processamento do
        # request a cada 1 segundo por 10 vezez.
        while True:
            time.sleep(1)
            request_progress = requests.get(
                                    'https://climateserv.servirglobal.net/chirps/getDataRequestProgress/',
                                    params={'id': request_id}
                                    )

            if request_progress.status_code == 200:
                progress = request_progress.json()[0]

                if progress == 100.0:
                    request_data = requests.get(
                                        'http://climateserv.servirglobal.net/chirps/getDataFromRequest/',
                                        params={'id': request_id}
                                    )

                    if request_data.status_code == status.HTTP_200_OK:
                        chirps_data = request_data.json()

                        try:
                            verifyData = chirps_data.json()['data']
                        except KeyError:
                            return {'message': 'O SERV Chirps não retornou dados.',
                                    'status': status.HTTP_400_BAD_REQUEST}

                        chirps_data['status'] = status.HTTP_200_OK
                        return chirps_data
                    else:
                        return request_data.json()
                elif progress == -1:
                    return {
                                'message': 'Houve algum erro no processamento do request. Verifique os argumentos passados.',
                                'status': status.HTTP_400_BAD_REQUEST
                            }
            else:
                return {'progress': request_progress.json(), 'status': request_progress}
            
            count_tries += 1

            if count_tries == 10:
                return {
                            'message': 'O servidor SERV CHIRPS demorou a responder.',
                            'status': status.HTTP_408_REQUEST_TIMEOUT
                        }
    else:
        return {
                    'message': 'Erro no servidor SERV CHIRPS',
                    'data': response_of_submit_request.json(),
                    'status': response_of_submit_request.status_code
            }


def validateInputs(pixel, startDate, finalDate):
    if type(pixel) is not Pixel:
        return {
                    'message': 'O primeiro argumento (pixel) deve ser do tipo vismet.models.Pixel',
                    'status': status.HTTP_400_BAD_REQUEST
            }
    elif type(startDate) is not datetime.date:
        return {
                    'message': 'O segundo argumento (startTime) deve ser do tipo datetime.date',
                    'status': status.HTTP_400_BAD_REQUEST
            }
    elif type(finalDate) is not datetime.date:
        return {
                    'message': 'O terceiro argumento (finalTime) deve ser do tipo datetime.date',
                    'status': status.HTTP_400_BAD_REQUEST
            }
    elif finalDate < startDate:
        return {
                    'message': 'A data final deve ser maior que a data inicial.',
                    'status': status.HTTP_400_BAD_REQUEST
            }
    else:
        return {'status': status.HTTP_200_OK}
        



    
    
