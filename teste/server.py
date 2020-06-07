from bs4 import BeautifulSoup 
import requests
import time 
import threading
import socket
import sys 

tempo = 0
UC = {
      }
Comandos = {
        'atualiza',
        'sair',
        'baixar',
        'comandos',
#        'cadastra uc',
#        'deleta uc'
        }

def get_boleto_num(lista):
    boleto = str(lista[3]).split('=')
    boleto = str(boleto[2]).split(' ')
    boleto = str(boleto[0]).split('"')
    return boleto[1]


def get_data(html):
    html_data = []
    for td in html:
        tds = td.find_all('td')
    for i in range(len(tds)):
        html_data += tds[i]
        print('ta dando certo',html_data)
    print('Deu certo get data html data')
    boleto = get_boleto_num(html_data)
    print('Deu certo get data boleto')
    return html_data,boleto

def add_hist(param):
    data_list = []  
    for i in range(len(param)):
        data_list += str(param[i]).split('<')
    return data_list

def atualiza_pagina_inicial(link,param):
    page = requests.post(link, param)
    soup = BeautifulSoup(page.text,'html.parser')
    pg = soup.find_all(class_='content differ')
    data,boleto = get_data(pg)
    print('Deu certo get data')
    data_list = add_hist(data)
    print('Deu certo data list')
    vencimento = data_list[3]
    valor_fatura = data_list[4]
    open('Atualiza_bot.html','a+').write(str('<br />'))
    open('Atualiza_bot.html','a+').write(str(vencimento))
    open('Atualiza_bot.html','a+').write(str('<br />'))
    open('Atualiza_bot.html','a+').write(str(valor_fatura))
    open('Atualiza_bot.html','a+').write(str('<br />'))
    return data_list,boleto
      
def bot_ie(conn,addr):
    url = 'http://agencia.ienergia.com.br:8085/'
    uc = str(conn.recv(10))
    senha = 'ie'+ uc
    data = {'UC':uc, 'Senha':senha}
    while True :
        com = str(conn.recv(20),'utf-8').lower()
        if(com in Comandos):
            if (com=='sair'):
                conn.close()
            elif (com=='atualiza'):
                data_list,boleto = atualiza_pagina_inicial(url,data)
                print('Dados Atualizados com Sucesso!')
            elif(com=='comandos'):
                print(Comandos)
            elif(com=='uc'):
                pass
#                print('Digite a UC atualizada: ')
#                data = {'UC':uc, 'Senha':senha}
#                print('Atualizado!')
            else:
                url_boleto = 'http://agencia.ienergia.com.br:8085/?ReturnUrl=%2FFaturas%2FEmiteFatura%2F'+boleto
                page_boleto = requests.post(url_boleto,data)
                soup_boleto = BeautifulSoup(page_boleto.text,'html.parser')
                print(soup_boleto)
#                open('boleto.pdf','w').write(str(soup_boleto))
    
        else:
            print('comando errado irmao \n')
            conn.close()
        
Port = 8081

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # AF_INET = IPv4 SOCK_STREAM = TCP

try:
    sock.bind(('0.0.0.0',Port))
except:
    print('### Bind Error, closing session ###')
    time.sleep(2)
    sys.exit()

sock.listen(10)
print('Aguardando conexoes em: ',Port)

while True :
    conn, addr = sock.accept()
    print('Conexao estabelecida com: ',addr)
    t = threading.Thread(target=bot_ie,args=(conn,addr))
    t.start() 
    
    
print('A Sessao com: ',addr,' foi encerrada')
sock.close()

# COISAS a FAZER 
# ver como baixar pdf via pyhton
# data da proximo leitura 
#  mes corrente da ftura             
    
    
