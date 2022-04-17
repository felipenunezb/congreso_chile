from zeep import Client
import pandas as pd
from collections import defaultdict
from zeep.helpers import serialize_object
from tqdm.auto import tqdm
import json
import os


def getVotacionesDiputados(periods, save_path: str = None):
    '''
    Obtener listado de votaciones por anyo, junto con los resultados de las votaciones individuales de cada diputado.
    
    Resultados:
    0: Rechaza, 1: Aprueba, 2: Abstencion
    '''

    #check if integer or list. If not, break.
    if not isinstance(periods, (int, list)):
        print("Input should be a year or a list of years.")
        return None

    #connect zeep client
    soap_url = 'http://opendata.camara.cl/camaradiputados/WServices/WSLegislativo.asmx?WSDL'
    client = Client(soap_url)

    #if integer, cast to list
    if isinstance(periods, int):
        periods = [periods]

    #set outputs
    votaciones_x_year = defaultdict() # year -> voting info
    diputado_x_votacion = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: list()))) # year -> id dip -> id voting -> vote

    #iterate over periods, return list of votaciones along with result details
    for year in tqdm(periods, desc = 'Years'):

        votacion_response = client.service.retornarVotacionesXAnno(year)
        votaciones_x_year[year] = [serialize_object(votacion) for votacion in votacion_response] #cast to ordered dict

        votaciones_id = [votacion['Id'] for votacion in votacion_response] #get list of voting IDs, to iterate

        for voto_id in tqdm(votaciones_id, desc='Votaciones'):

            votacion_detalle_response = client.service.retornarVotacionDetalle(voto_id)
            votacion_detalle_dict = serialize_object(votacion_detalle_response) #cast to ordered dict

            #iterate over list of dips and store their vote
            for dip in votacion_detalle_dict['Votos']['Voto']:
                diputado_x_votacion[year][dip['Diputado']['Id']][voto_id] = dip['OpcionVoto']['Valor']

    #if a save path is provided, save json files
    if save_path:

        #format dates, to avoid serialization issue with JSON (datetime -> yyyymmdd)
        _ = [votacion.update({'Fecha': votacion['Fecha'].strftime("%Y%m%d")}) for key, val in votaciones_x_year.items() for votacion in val]

        #get years, to saved filename
        min_yr, max_yr = min(periods), max(periods)
        if min_yr == max_yr:
            out_yr = min_yr
        else:
            out_yr = f"{min_yr}_{max_yr}"

        #save both files
        with open(os.path.join(save_path, f'info_votaciones_{out_yr}.json'), 'w') as outfile:
            json.dump(votaciones_x_year, outfile, indent=4)
        with open(os.path.join(save_path, f'votaciones_diputados_{out_yr}.json'), 'w') as outfile:
            json.dump(diputado_x_votacion, outfile, indent=4)

    return votaciones_x_year, diputado_x_votacion