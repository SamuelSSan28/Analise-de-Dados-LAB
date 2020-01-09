import pandas as pd
import calendar
from Graphics import GraficosClass as graph
from datetime import datetime
from datetime import timedelta


class DataAnalysisClass:
    def __init__(self):
        pass

    def ler_base_de_dados(self,url):
        '''
        funcão responsavel por ler os arquivos csv
        :param url: link do csv
        :return: retorna um dataframe com dados encontrados
        '''
        try:
            return pd.read_csv(url)
        except Exception as ex:
            print('ERRO: ',ex)

    def feedbackTemperatura(self,dataframe):
        labels = 'Frio', 'Agradavel', 'Quente', 'Muito Frio'
        fractions = dataframe["Feedback da Temperatura"].value_counts()
        offsets = (0.1, 0.05, 0.1, 0.08)
        graph.GeraPizza(fractions,offsets,labels)


    def bancadaFrio(self):
        pass

    def bancadaCalor(self):
        pass

    def sensasacaoM(self):
        pass

    def sensasacaoT(self):
        pass

    def sensasacaoN(self):
        pass

    def temperaturaMedia_Dia(self):
        pass

    def kiloWatt_hora(self,df):
        corrente_por_dia = df[['corrente', 'horario']]

        for h in range(0, 24):
            cmd2 = "horario >= '"
            if h < 10:
                cmd2 += '0' + str(h) + ":00:00' and horario <= '" + '0' + str(h) + ":59:59'"
            else:
                cmd2 += str(h) + ":00:00' and horario <= '" + str(h) + ":59:59'"

            corrente_h_dia = corrente_por_dia.query(cmd2)

            kW = sum(corrente_h_dia['corrente']) * 220 / 1000 * 60 / 3600 #somatorio das coletas no horario * tensão / Kilo * segundos / horas

            if corrente_h_dia['corrente'].mean() > 1:
                print(round(kW, 2), cmd2.replace('horario >=', '').replace('and', '-').replace('horario <=', ''))

        pass

    def kiloWatt_dia(self):
        pass

    def Media_kiloWatt_horarios(self):
        pass