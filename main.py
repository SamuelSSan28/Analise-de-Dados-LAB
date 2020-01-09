from DataAnalysis import DataAnalysisClass

dac = DataAnalysisClass()

dados_dia_16_12_2019 =  dac.ler_base_de_dados('https://raw.githubusercontent.com/SamuelSSan28/Collab_Experimento/master/corrente_dia_16_12_2019.csv')


dac.kiloWatt_hora(dados_dia_16_12_2019)

