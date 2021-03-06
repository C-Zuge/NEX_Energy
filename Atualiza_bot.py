from bs4 import BeautifulSoup 
import requests
import time 

print('Digite a UC: ')
uc = str(input())
senha = 'ie'+ uc
data = {'UC':uc, 'Senha':senha}
url = 'http://agencia.ienergia.com.br:8085/'
tempo = 0
UC = {
      }
Comandos = {
        'atualiza',
        'sair',
        'baixar',
        'comandos',
        'cadastra uc',
#        'deleta uc'
        }

#def Cadastra(uc):
#    global UC
#    tam = len(UC)+1 
#    if not uc in UC:
#        UC.keys = str(tam)
#        UC[str(tam)] = str(uc)
#        print('UC criada com sucesso',UC)
#    else:
#        print('Essa UC ja existe')
        
def get_boleto_num(lista):
#    Esta função serve para tirar o Numero de identificação do boleto que esta no html fonte
    boleto = str(lista[3]).split('=')
    boleto = str(boleto[2]).split(' ')
    boleto = str(boleto[0]).split('"')
    return boleto[1]

def baixa_boleto(url_boleto,data):
#   Esta função serve somente para baixar o pdf da uc fornecida pelo usuario por meio de requests
    page_boleto = requests.post(url_boleto,data)
    filename = 'boleto UC_'+str(uc)+'.pdf'
    with open(filename, "wb") as code:
        code.write(page_boleto.content) # Gera pdf com nome 'filename' e conteudo de 'page_boleto'
        
def atualiza_pagina_inicial(link,param):
#    Atualiza a pagina da UC caso nao tenha dado problema de requisição e gera um html com os dados obtidos
#    função responsavel pelo scraping de todo dado necessario da pagina inicial do Iguaçu Energia
    page = requests.post(link, param)
    soup = BeautifulSoup(page.text,'html.parser')
    pg = soup.find_all(class_='content differ') # class_='content differ' é classe dentro de td do html bruto
    data,boleto = get_data(pg)
    data_list = add_hist(data)
    vencimento = data_list[3]
    valor_fatura = data_list[4]
#   processo de gerar html com os dados obtidos do scraping || a+ -> append 
    open('Atualiza_bot.html','a+').write(str('<br />'))
    open('Atualiza_bot.html','a+').write(str(vencimento))
    open('Atualiza_bot.html','a+').write(str('<br />'))
    open('Atualiza_bot.html','a+').write(str(valor_fatura))
    open('Atualiza_bot.html','a+').write(str('<br />'))
    return data_list,boleto


def get_data(html):
#   Função responsavel por afunilar o html bruto em somente a parte do html que possui os dados que nos interessam
    html_data = []
    for td in html:
        tds = td.find_all('td')
    for i in range(len(tds)):
         html_data += (tds[i])
    boleto = get_boleto_num(html_data)
    return html_data,boleto

def add_hist(param):
#   Função que gera uma lista de todos os valores importantes do html afunilado para extração posterior
    data_list = []  
    for i in range(len(param)):
        data_list += str(param[i]).split('<')
    return data_list
#Cadastra(uc)
while True :
    if (tempo == 0):
        data_list,boleto = atualiza_pagina_inicial(url,data)
        tempo = time.localtime().tm_min
        print('Dados Atualizados com Sucesso!',tempo)
    elif (tempo >= tempo + 1):
        data_list,boleto = atualiza_pagina_inicial(url,data)
        print('Dados Atualizados com Sucesso!')
    else:
        print('\nDigite COMANDOS para ver os comandos possiveis \n')
        print('Digite o comando: ')
        com = str(input()).lower()
        if(com in Comandos):
            if (com=='sair'):
                break
            elif (com=='atualiza'):
                data_list,boleto = atualiza_pagina_inicial(url,data)
                print('Dados Atualizados com Sucesso!')
            elif(com=='comandos'):
                print(Comandos)
            elif(com=='cadastra uc'):
                print('Digite a nova UC: ')
                uc = input()
#                Cadastra(uc)
                data = {'UC':uc, 'Senha':senha}
                print('Atualizado!')
            else:
                url_boleto = 'http://agencia.ienergia.com.br:8085/?ReturnUrl=%2FFaturas%2FEmiteFatura%2F'+boleto
                baixa_boleto(url_boleto,data)
    
        else:
            print('Comando errado irmao \n')
            break

# COISAS a FAZER 
# Data da proximo leitura 
# Mês corrente da fatura  
# Gerar arquivo xls a partir dos dados obtidos em configuração {UC, Mes corrente, Vencimento, Valor da Fatura}
            
