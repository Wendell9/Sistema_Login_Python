import Conexao
import os
import random
from mailjet_rest import Client
from dotenv import load_dotenv
letraminuscula='abcdefghijklmnopqrstuvwxyz'
letramaiuscula='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numeros='0123456789'
caracter_especial='!@#$%^&*?:'

conexao=Conexao.Conecta()

def verifica_forca_senha(senha):
    senhaForte=True
    mensagem='Senha Fraca\n'
    contNumero = 0
    contletraminuscula = 0
    contletramaiuscula = 0
    contsimbolo = 0
    for letra in senha:
        if letra in letraminuscula:
            contletraminuscula+=1
        elif letra in letramaiuscula:
            contletramaiuscula+=1
        elif letra in caracter_especial:
            contsimbolo+=1
        elif letra in numeros:
            contNumero+=1
    
    if contNumero==0:
        mensagem+='A senha precisa conter ao menos um número\n'
        senhaForte=False
    if contletramaiuscula==0:
        mensagem+='A senha precisa conter ao menos uma letra maiuscula\n'
        senhaForte=False
    if contletraminuscula==0:
        mensagem+='A senha precisa conter ao menos uma letra minuscula\n'
        senhaForte=False
    if contsimbolo==0:
        mensagem+='A senha precisa conter ao menos um dos simbolos {!@#$%^&*?:}\n'
        senhaForte=False
    if len(senha)<8:
        mensagem+='A senha precisa conter ao menos 8 caracteres'
        senhaForte=False
    if mensagem=='Senha Fraca\n':
        mensagem='Senha Forte'
        
    print(mensagem)
    return senhaForte

def enviar_email(email,nova_senha):
    try:
        load_dotenv()
        print(os.getenv('MAILJET_API_KEY'))
        print(os.getenv('MAILJET_API_SECRET'))
        api_key = os.getenv('MAILJET_API_KEY')
        api_secret = os.getenv('MAILJET_API_SECRET')
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
                'Messages': [
                    {
                        "From": {
                            "Email": "wgamer66@gmail.com",
                            "Name": "SISTEMA_LOGIN"
                        },
                        "To": [
                            {
                                "Email": email,
                                "Name": "You"
                            }
                        ],
                        "Subject": "Recuperação de Senha",
                        "TextPart": f"Olá,\nSegue abaixo sua nova senha\nSenha: {nova_senha}\nApós logar, favor alterar a senha\nAtenciosamente",
                        "HTMLPart": f"""
                        <h1>Recuperação de Senha</h1>
                        <p>Olá,</p>
                        <p>Segue abaixo sua nova senha:</p>
                        <p><strong>Senha: {nova_senha}</strong></p>
                        <p>Após logar, favor alterar a senha.</p>
                        <p>Atenciosamente,</p>
                        """
                    }
                ]
            }
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())
        print('O email de redefinição de senha foi enviado com sucesso')
    except ValueError as e:
        print(f'Erro: {e}')

def limpa_tela():
    os.system('cls')

def tela_opcoes_1():
    print('''
██╗░░░░░░█████╗░░██████╗░██╗███╗░░██╗
██║░░░░░██╔══██╗██╔════╝░██║████╗░██║
██║░░░░░██║░░██║██║░░██╗░██║██╔██╗██║
██║░░░░░██║░░██║██║░░╚██╗██║██║╚████║
███████╗╚█████╔╝╚██████╔╝██║██║░╚███║
╚══════╝░╚════╝░░╚═════╝░╚═╝╚═╝░░╚══╝''')
    print('Bem vindo ao sistema',"Escolha uma das opções abaixo:",'1. Cadastro','2. Login','3. Redefinir Senha',sep='\n')
    
def tela_opcoes_2():
    print('Tela de Login','1.Redefinir senha','2.Voltar',sep='\n')

def pressione_tecla():
    input('Pressione qualquer tecla para voltar\n')

def Login():
    print('Login:')
    email=input('Email:')
    
    senha=input('Senha:')
    
    existencia_email=conexao.verifica_email(email)   
    if existencia_email:
        if conexao.verifica_senha(email, senha):
            Area_de_Login(email)
            main()
        else:
            print('Senha incorreta! Favor tentar o login novamente')
            pressione_tecla()
            Login()
    else:
        print('Email inexistente, favor inserir um email valido')
        main()
        
def Area_de_Login(email):
    tela_opcoes_2()
    resposta=int(input())
    match resposta:
        case 1:
            Redefinir_Senha_Login(email)
        case 2:
            limpa_tela()
            main()
                      
def Redefinir_Senha_Login(email):
    print('Redefinir Senha')
    senha_antiga=input('Senha anterior:')
    senha=input('Senha Nova:')
    senha2=input('Digite a senha nova novamente para confirmar:')
    
    if conexao.verifica_senha(email,senha_antiga):
        if senha==senha2:
            if verifica_forca_senha(senha):
                conexao.atualizar_senha(email,senha2)
                print('Operação realizada com sucesso')
                pressione_tecla()
                limpa_tela()
                Area_de_Login(email)
            else:
                pressione_tecla()
                limpa_tela()
                Redefinir_Senha_Login(email)
        else:
            print('As duas senhas novas devem ser iguais')
            pressione_tecla()
            limpa_tela()
            Redefinir_Senha_Login(email)
    else:
        print('Senha incorreta')
        pressione_tecla()
    
    conexao.atualizar_senha(email,senha2)
    
def Cadastro():
    print('Cadastro')
    email=input('Email:')
    print('A senha precisa conter ao menos um número',
          'A senha precisa conter ao menos uma letra maiuscula',
          'A senha precisa conter ao menos uma letra minuscula',
          'A senha precisa conter ao menos um dos simbolos {!@#$%^&*?:}',
          'A senha deve conter ao menos 8 caracteres',sep='\n')
    senha=input('Senha:') 
    if email=='':
        print('Email inválido')
        pressione_tecla()
        limpa_tela()
        Cadastro()
    elif conexao.verifica_email(email):
        print('Email ja existente na nossa base de dados, favor se dirigir a área de login para logar ou recuperar a senha')
        pressione_tecla()
        limpa_tela()
        main()
    elif senha=='':
        print('Senha invalida')
        pressione_tecla()
        Cadastro()
    elif not verifica_forca_senha(senha):
        pressione_tecla()
        limpa_tela()
        Cadastro()
    conexao.cadastrar_usuario(email,senha)
    print('Cadastro Realizado com sucesso')
    pressione_tecla()
    limpa_tela()
    main()

def Gerar_Senha_Aleatoria():

   resposta=''
   for i in range(3):
    resposta+=random.choice(letraminuscula)
    resposta+=random.choice
    resposta+=random.choice(numeros)
    resposta+=random.choice(caracter_especial)
   return resposta

def Esqueci_Senha():
    print('Esqueci a Senha')
    print('1.Redefinir Senha')
    print('2.Voltar')
    try:
        resposta=int(input())
        match resposta:
            case 1:
                print('Redefinir Senha')
                email=input('Insira email para recuperar a senha:')
                
                if conexao.verifica_email(email):
                    nova_senha=Gerar_Senha_Aleatoria()
                    conexao.atualizar_senha(email,nova_senha)
                    enviar_email(email,nova_senha)
                    pressione_tecla()
                    limpa_tela()
                    main()
                else:
                    print('Email inexistente. Favor inserir um email valido')
                    limpa_tela()
                    Esqueci_Senha()
            case 2:
                limpa_tela()
                main()
    except:
        print('Insira uma opção válida')
        pressione_tecla()
        Esqueci_Senha()
    
      
def main():
    tela_opcoes_1()
    resposta=int(input())
    match resposta:
        case 1:
            Cadastro()
        case 2:
            Login()
        case 3:
            Esqueci_Senha()
    
if __name__ == "__main__":
    main()
           
