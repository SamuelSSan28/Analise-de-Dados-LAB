from DataAnalysis import DataAnalysisClass
from BuscaBD import BancoDeDados

bd = BancoDeDados
dac = DataAnalysisClass()

bd.buscaPorDatas("registros_controle",'09/12/2019','13/12/2019')
dados_dia_16_12_2019 =  dac.ler_base_de_dados('atualfile')


dac.horarios_que_mais_ligou(dados_dia_16_12_2019)


'''
`registros_sensores`, `registros_controle`
'''

