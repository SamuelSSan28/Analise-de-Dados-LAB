import pandas as pd
import calendar
import statistics
from Graphics import GraficosClass
from datetime import datetime
from datetime import timedelta

graph = GraficosClass()

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
        offsets = (0.1, 0.05, 0.1, 0.08,0.1, 0.05, 0.1, 0.08)
        graph.GeraPizza(fractions, offsets, labels)


    def bancadaCalor(self,df):
        fractions = df.loc[df["Feedback da Temperatura"] == "Quente"]["Informe a sua bancada"].value_counts()
        labels = 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'M'
        offsets = (0.1, 0.05, 0.1, 0.08,0.1, 0.05, 0.1, 0.08)
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
        data_corrente = {'Horario': [],
                     'Corrente': []
                     }
        for h in range(0, 24):
            cmd2 = "horario >= '"
            if h < 10:
                cmd2 += '0' + str(h) + ":00:00' and horario <= '" + '0' + str(h) + ":59:59'"
            else:
                cmd2 += str(h) + ":00:00' and horario <= '" + str(h) + ":59:59'"

            corrente_h_dia = corrente_por_dia.query(cmd2)

            kW = sum(corrente_h_dia['corrente']) * 220 / 1000 * 60 / 3600 #somatorio das coletas no horario * tensão / Kilo * segundos / horas

            if corrente_h_dia['corrente'].mean() > 1:
                #print(round(kW, 2), cmd2.replace('horario >=', '').replace('and', '-').replace('horario <=', ''))
                data_corrente['Horario'].append(h)
                data_corrente['Corrente'].append(round(kW, 2))

        dados = pd.DataFrame(data_corrente)
        graph.geraHistoGrama(dados, 'Horario',False)

    def kiloWatt_dia(self,dataframe):
        data_corrente = {'Data': [],
                         'Corrente': []
                         }
        for i in range(1, 13):
            quant_dias_mes = calendar.monthrange(2020, i)
            for j in range(1, quant_dias_mes[1] + 1):
                corrente_acumulada = 0
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
                result = dataframe.query(cmd)

                kW = sum(result['corrente']) * 220 / 1000 * 60 / 3600  # somatorio das coletas no horario * tensão / Kilo * segundos / horas

                if result.size > 0:
                    print(kW)
                    data_corrente['Data'].append(dia)
                    data_corrente['Corrente'].append(round(kW, 2))

                #parar se passar da data atual

        dados = pd.DataFrame(data_corrente)
        graph.geraHistoGrama(dados, 'Data', False)
        pass

    def Media_kiloWatt_horarios(self,dataframe):
        corrente = dataframe[['corrente','dia', 'horario']]
        data_corrente = {'Horario': [],
                         'Corrente': []
                         }

        cmd1 = "horario >= '06:00:00' and horario <= '12:59:59'"
        cmd2 = "horario >= '13:00:00' and horario <= '17:59:59'"
        cmd3 = "horario >= '18:00:00' and horario <= '22:59:59'"

        corrente_horarios = corrente.query(cmd1)
        kW1 = sum(corrente_horarios['corrente']) * 220 / 1000 * 60 / 3600  # somatorio das coletas no horario * tensão / Kilo * segundos / horas
        quantDias1 = corrente_horarios.drop_duplicates('dia', keep='first')['dia'].size

        corrente_horarios = corrente.query(cmd2)
        kW2 = sum(corrente_horarios[ 'corrente']) * 220 / 1000 * 60 / 3600  # somatorio das coletas no horario * tensão / Kilo * segundos / horas
        quantDias2 = corrente_horarios.drop_duplicates('dia', keep='first')['dia'].size

        corrente_horarios = corrente.query(cmd3)
        kW3 = sum(corrente_horarios[ 'corrente']) * 220 / 1000 * 60 / 3600  # somatorio das coletas no horario * tensão / Kilo * segundos / horas
        quantDias3 = corrente_horarios.drop_duplicates('dia', keep='first')['dia'].size


        data_corrente['Horario'].append("Manhã")
        data_corrente['Corrente'].append(round(kW1/quantDias1, 2)) #falta dividir pela quantidades de dias diferentes observados

        data_corrente['Horario'].append("Tarde")
        data_corrente['Corrente'].append(round(kW2/quantDias2, 2))

        data_corrente['Horario'].append('Noite')
        data_corrente['Corrente'].append(round(kW3/quantDias3, 2))

        dados = pd.DataFrame(data_corrente)
        graph.geraHistoGrama(dados, 'Horario', False,scale=[0,150])

        pass

    #controle
    def horas_ligadas_por_dia(self,dataframe):
        estado_dia_horario = dataframe[["temperatura", "estado", "dia", "horario"]]

        dia_ant = estado_dia_horario['dia'][0]
        horario_ant = estado_dia_horario['horario'][0]

        horas_dia = {}
        dif = timedelta(days=0, hours=0, minutes=0, seconds=0)
        for i in range(len(estado_dia_horario['temperatura'])):
            dia = estado_dia_horario['dia'][i]
            horario = estado_dia_horario['horario'][i]
            estado = estado_dia_horario['estado'][i]

            if dia == dia_ant:
                h1 = horario.split(":")
                h2 = horario_ant.split(":")

                h1 = timedelta(days=0, hours=int(h1[0]), minutes=int(h1[1]), seconds=int(h1[2]))
                h2 = timedelta(days=0, hours=int(h2[0]), minutes=int(h2[1]), seconds=int(h2[2]))
                if estado == 0:
                    dif += (h1 - h2)
                    dia_ant = dia
                    horario_ant = estado_dia_horario['horario'][i + 1]
            else:
                horas_dia.update({dia_ant: dif})
                dif = timedelta(days=0, hours=0, minutes=0, seconds=0)
                dia_ant = dia
                horario_ant = estado_dia_horario['horario'][i]

        data_ctrl = {'dia': [],
                     'horas_ligado': []}

        for i in horas_dia:
            data_ctrl["dia"].append(i)
            data_ctrl["horas_ligado"].append(horas_dia[i].total_seconds() / 3600)

        df_horas_ligada = pd.DataFrame(data_ctrl)
        graph.geraHistoGrama(df_horas_ligada, 'dia', False, scale=[0, df_horas_ligada['horas_ligado'].max()])
        pass

    # controle
    def horarios_que_mais_ligou(self,dataframe):
        atual = 0
        cont = -1
        anterior = -1
        ligando = []

        for i in dataframe["estado"]:
            atual = i
            if anterior == 0 and atual == 1:
                ligando.append(cont)

            if atual != anterior:
                anterior = atual

            cont += 1
        hist = [0] * 24
        for i in ligando:
            hora = dataframe['horario'][i].split(":")
            hist[int(hora[0])] += 1

        horarios = list(range(0, 24))

        cont_ligou = {"Horario": horarios, "Quantidade": hist}
        df_ligou = pd.DataFrame(cont_ligou)

        graph.geraHistoGrama(df_ligou, 'Horario', False, scale=[0, df_ligou['Quantidade'].max()+1])
        pass