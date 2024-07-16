#conexão com o banco de dados, sem autenticação
import pyodbc as p
class Conecta:
    def __init__(self):
            self.server = 'DESKTOP-UOHE1VE\\SQLSERVER2022'
            self.database = 'Sistema_Login'
            self.cnx = None
            self.cursor = None



    def abrir_servidor(self):
        self.cnx = p.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';Trusted_connection=yes;')
        self.cursor=self.cnx.cursor()
        
    def fechar_servidor(self):
        self.cnx.close()

    def verifica_email(self,email):
        try:
            self.abrir_servidor()
            valor = '''
            select email from Login
            '''
            self.cursor.execute(valor)
            resposta=self.cursor.fetchall()
            for linha in resposta:
                if linha[0]==email:
                    return True
                
            return False
        finally:
            if self.cnx:
                self.fechar_servidor()
                
    def atualizar_senha(self,email,senha):
        self.abrir_servidor()
        valor = "UPDATE Login SET senha = ? WHERE email = ?"
        self.cursor.execute(valor, (senha, email))
        self.cnx.commit()
                

    def verifica_senha(self, email, senha):
        try:
            self.abrir_servidor()
            valor = f'''select senha from Login where email='{email}' '''
            self.cursor.execute(valor)
            resposta=self.cursor.fetchone()
            
            if senha==resposta[0]:
                return True
            else:
                return False
        finally:
            self.fechar_servidor()
            
    def cadastrar_usuario(self,email,senha):
        try:
            self.abrir_servidor()
            valor = "INSERT INTO Login (email, senha) VALUES (?, ?)"
            self.cursor.execute(valor, (email, senha))
            self.cnx.commit()
        finally:
            if self.cnx:
                self.fechar_servidor()
        
        
        
    
