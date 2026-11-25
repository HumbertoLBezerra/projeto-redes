from scapy.all import sniff
from utils import *

quantia = int(input("Insira a quantia de pacotes a ser analisada: "))

pacotes = sniff(count=quantia)

condicao = True

while condicao:
    print("Selecione informações resumidas ou detalhadas:")
    opc =int(input("1-Informações Resumidas \n2-Informações Detalhadas\n"))
    
    if opc == 1:
        for pacote in pacotes:
            print(pacote.summary())
        break
    elif opc == 2:
        for pacote in pacotes:
            pacote.show()
        break
    else:
        limpar_tela()
        print("Opção inválida informada! Insira novamente!")

