#Importação de Bibliotecas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style='darkgrid')

class GraficosClass:
    def __init__(self):
        pass

    def GeraPizza(self,fractions,labels,offsets=(0.1, 0.05,0.1, 0.08)):
        '''
        função que gera graficos no formato de Pizza/Setores
        :param fractions: vetor com a frequencia de cada item
        :param offsets: vetor com o valor de afastamento de cada fração em relação as outras
        :param labels: vetor com o nome de cada fração de
        :return: Não tem retorno, apenas apresenta o grafico em uma janela
        '''
        plt.pie(fractions, explode=offsets, labels=labels,
                autopct='%1.1f%%', rotatelabels=True, shadow=True, startangle=180,
                colors=sns.color_palette('muted'))
        plt.axis('equal')
        plt.show()


    def geraHistoGrama(self,dataframe,classe,ordem):
        '''
        função que gera gráficos no formato de histograma onde o eixo x contém a frequencia dos dados e o eixo y as classes
        :param dataframe: dataframe com os dados
        :param classe: a coluna do dataframe que vai conter as classes
        :param ordem: crescente se True ou decrescente se False
        :return:
        '''
        (dataframe
         .groupby(classe).mean()
         .sort_values(by=classe, ascending=ordem)
         .plot.barh(figsize=(15, 10), width=.7))
        plt.xlim(left=0, right=25)
        plt.show()