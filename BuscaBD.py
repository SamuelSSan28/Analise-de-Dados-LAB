# Importamos a biblioteca:
import pymysql
import csv
import sys

class BancoDeDados:
    def conexaoBD(self): #retorna uma conexao com o BD
        return pymysql.connect(db='sensores_2', user='temperatura', passwd='DisnelLab2019',port=3360)

    def buscaPorDatas(self,tabela,data1,data2):  # insere dados na tabela registros
        # Abrimos uma conexão com o banco de dados:
        c = self.conexaoBD()

        # Cria um cursor:
        cursor = c.cursor()

        # O comando:
        sql = "SELECT * from {} where str_to_date(dia, '%d/%m/%Y') >= str_to_date('{}', '%d/%m/%Y')  and  str_to_date(dia, '%d/%m/%Y') <= str_to_date('{}', '%d/%m/%Y')". \
            format(tabela, data1, data2)
        print(sql)
        # Executa o comando:
        cursor.execute(sql)

        # Salva o resultado numa matriz:
        rows = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        if rows:
            fp = open('atualfile.csv', 'w')
            myFile = csv.writer(fp)
            myFile.writerow(column_names)
            myFile.writerows(rows)
            fp.close()

        # fecha conexao
        c.close()




