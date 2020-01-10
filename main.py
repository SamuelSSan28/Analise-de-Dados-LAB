from DataAnalysis import DataAnalysisClass

dac = DataAnalysisClass()

dados_dia_16_12_2019 =  dac.ler_base_de_dados('https://raw.githubusercontent.com/SamuelSSan28/Collab_Experimento/master/controle_csv.csv')


dac.horarios_que_mais_ligou(dados_dia_16_12_2019)

