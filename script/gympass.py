#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime

def entrada():
   return tipo_dados([i.split() for i in [x for x in sys.stdin][1:]])


def tipo_dados(entrada):
    try:
        y = [[datetime.datetime.strptime(x[0], '%H:%M:%S.%f').time(), x[1], x[3], int(x[4]),x[5],float(x[6].replace(",","."))] for x in entrada]
        return y
    except IndexError:
        print("Erro: Faltam colunas no arquivo de entrada")
        sys.exit(1)
    except ValueError:
        print("Erro: Coluna com valor inesperado ")
        sys.exit(1)



def agrupamento_voltas_pilotos(lista_linhas):
    pilotos =  set([i[1] for i in lista_linhas])
    lista_linhas.sort(key=lambda x: x[1])
    agrupamento_total = []
    for i in pilotos:
        agrupamento_pilotos = []
        for k in lista_linhas:
            if k[1] == i:
                agrupamento_pilotos.append(k)
        agrupamento_total.append(agrupamento_pilotos)
    return(agrupamento_total)

def somar_tempos(tempos):
    tempo_final = [formatar_tempo_minuto_segundo(i[4]) for i in tempos]
    segundos = sum(i.total_seconds() for i in tempo_final)
    return formatar_tempo_string(segundos)

def formatar_tempo_minuto_segundo (tempo):
    try:
        m, s = tempo.split(":")
        return datetime.timedelta(minutes=int(m), seconds=float(s))
    except ValueError:
        print("Erro: Coluna Tempo da Volta com formato errado")
        sys.exit(1)

def formatar_tempo_hora_minuto_segundo (tempo):
    h, m, s = tempo.split(":")
    return datetime.timedelta(hours=int(h), minutes=int(m), seconds=float(s))

def formatar_tempo_string(tempo):
    segundos = tempo % 60
    minutos = (tempo - segundos) / 60
    segundos = round(segundos, 3)
    return str(int(minutos)) + ":" + str(segundos)


def campeao(melhores_voltas):
    possiveis_primeiros = []
    ultimos = []
    for i in melhores_voltas:
        if i[3] == 4:
            possiveis_primeiros.append(i)
        else:
            ultimos.append(i)

    possiveis_primeiros.sort(key=lambda x: x[0])
    ultimos.sort(key=lambda x: x[0])
    posicao = 0
    for i in range(len(possiveis_primeiros)):
        posicao += 1
        possiveis_primeiros[i].append(posicao)

    for i in range(len(ultimos)):
        posicao += 1
        ultimos[i].append(posicao)
    classificacao = possiveis_primeiros+ultimos
    classificacao.sort(key= lambda x: x[len(x)-1])
    return classificacao


def tempo_diff_campeao(classificacao):
    tempo_campeao = formatar_tempo_minuto_segundo(classificacao[0][4]).total_seconds()
    diffs = []
    for i in classificacao:
        diffs.append(formatar_tempo_string(formatar_tempo_minuto_segundo(i[4]).total_seconds() - tempo_campeao))
    return diffs

def melhor_volta(voltas):
    tempos = [formatar_tempo_minuto_segundo(i[4]) for i in voltas]
    index = tempos.index(min(tempos))
    return index

def media_velocidade (velocidades):
    return round(sum([i[5] for i in velocidades ])/len(velocidades),3)

def melhor_volta_corrida(melhores_voltas):
    index = melhor_volta(melhores_voltas)
    return melhores_voltas[index][2], melhores_voltas[index][6]

def resumo_pilotos(voltas_pilotos):
    resumo = []
    for i in voltas_pilotos:
        i.sort(key = lambda x: x[3])
        tempo_total = somar_tempos(i)
        index = melhor_volta(i)
        resumo.append([i[-1][0],i[-1][1],i[-1][2],i[-1][3], tempo_total, media_velocidade(i), i[index][3], i[index][4]])
    result = campeao(resumo)
    return result


def formatar_saida(resumo):
    diffs_tempo = tempo_diff_campeao(resumo)
    with open('../output/resultado_simples.txt', 'w') as the_file:
        the_file.write('Posição Chegada; Código Piloto; Nome Piloto; Qtde Voltas Completadas; Tempo Total de Prova\n')
        for i in resumo:
            the_file.write(str(i[8])+";"+str(i[1])+";"+str(i[2])+";"+str(i[3])+";"+str(i[4])+"\n")

    with open('../output/resultado_completo.txt', 'w') as the_file:
        the_file.write('Posição Chegada; Código Piloto; Nome Piloto; Qtde Voltas Completadas; Tempo Total de Prova; Melhor Volta; Velocidade Média; Tempo Apos Vencendor\n')
        index = 0
        for i in resumo:
            the_file.write(str(i[8])+";"+str(i[1])+";"+str(i[2])+";"+str(i[3])+";"+str(i[4])+";"+str(i[6])+";"+str(i[5])+";"+str(diffs_tempo[index])+"\n")
            index+=1

if __name__ == "__main__":
    tratamento_entrada = entrada()
    if len(tratamento_entrada) > 0:
        resumo = resumo_pilotos(agrupamento_voltas_pilotos(tratamento_entrada))
        formatar_saida(resumo)
    else:
        print("Erro: Arquivo sem dados")