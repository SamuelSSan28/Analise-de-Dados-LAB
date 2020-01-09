import pandas as pd
import calendar
import statistics
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


    def bancadaFrio(self,df):
        fractions = df.loc[df["Feedback da Temperatura"] == "Frio"]["Informe a sua bancada"].value_counts()
        labels = 'B1', 'B2', 'B3', 'B4','B5','B6','B7','M'
        offsets = (0.1, 0.05, 0.1, 0.08)
        graph.GeraPizza(fractions, offsets, labels)


    def bancadaCalor(self,df):
        fractions = df.loc[df["Feedback da Temperatura"] == "Quente"]["Informe a sua bancada"].value_counts()
        labels = 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'M'
        offsets = (0.1, 0.05, 0.1, 0.08)
        graph.GeraPizza(fractions, offsets, labels)


    def sensasacaoM(self,df):
        labels = 'Frio', 'Agradavel', 'Quente', 'Muito Frio'
        fractions = df.query("Hora > '08:00:00' and Hora < '12:00:00'")["Feedback da Temperatura"].value_counts()
        offsets = (0.1, 0.05, 0.1, 0.08)
        graph.GeraPizza(fractions, offsets, labels)

    def sensasacaoT(self,df):
        labels = 'Frio', 'Agradavel', 'Quente', 'Muito Frio'
        fractions = df.query("Hora > '12:00:00' and Hora < '18:00:00'")["Feedback da Temperatura"].value_counts()
        offsets = (0.1, 0.05, 0.1, 0.08)
        graph.GeraPizza(fractions, offsets, labels)


    def sensasacaoN(self,df):
        labels = 'Frio', 'Agradavel', 'Quente', 'Muito Frio'
        fractions = df.query("Hora > '18:00:00' and Hora < '20:00:00'")["Feedback da Temperatura"].value_counts()
        offsets = (0.1, 0.05, 0.1, 0.08)
        graph.GeraPizza(fractions, offsets, labels)

    def temperaturaMedia_Dia(self,df_sensores):
        data_temp = {'Data': [],
                     'Temperatura_Max': [],
                     'Temperatura_Min': [],
                     'Temperatura_Med': []
                     }

        for i in range(1, 13):
            quant_dias_mes = calendar.monthrange(2019, i)
            for j in range(1, quant_dias_mes[1] + 1):
                d = j
                m = i
                dia = "2019"

                if m < 10:
                    dia = "0" + str(m) + "/" + dia
                else:
                    dia = str(m) + "/" + dia

                if d < 10:
                    dia = "0" + str(d) + "/" + dia
                else:
                    dia = str(d) + "/" + dia

                cmd = "dia == '" + dia + "'"
                result = df_sensores.query(cmd)
                temp_dia = []
                temp_min = []

                for j in result["temperatura"]:
                    if len(temp_min) < 5:
                        temp_min.append(j)

                    if len(temp_min) == 4:
                        med = sum(temp_min) / len(temp_min)
                        temp_dia.append(med)
                        temp_min = []

                result["temperatura"].replace(temp_dia)
                if len(result) > 0:
                    max_temp_dia = result["temperatura"].max()
                    min_temp_dia = result["temperatura"].min()
                    med_temp_dia = result["temperatura"].mean()

                    data_temp['Data'].append(dia[0:2] + "/10/2019")#ver isso aqui
                    data_temp['Temperatura_Max'].append(round(max_temp_dia))
                    data_temp['Temperatura_Min'].append(round(min_temp_dia))
                    data_temp['Temperatura_Med'].append(round(med_temp_dia))

        dados = pd.DataFrame(data_temp)
        graph.geraHistoGrama(dados[['Data', 'Temperatura_Max', 'Temperatura_Med','Temperatura_Min']],'Data')


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