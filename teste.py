import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
# import sys
import re
from database import conectar  # Importa a função de conexão do arquivo database.py

janela = ctk.CTk()


class Application():
    def __init__(self):
        self.janela = janela
        self.tema()
        self.tela()
        self.tela_login()
        janela.mainloop()

    def tema(self):
        # Configurações do CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

    def tela(self):
        # Configurações da janela principal
        janela.geometry("700x400")
        janela.title("Sistema de autenticação BACKUP-SWS")
        janela.iconbitmap("img/favicon.ico")
        janela.resizable(False, False)

    def tela_login(self):

        email_invalido_mostrado = False
        # Função para validar se o texto é um e-mail

        def checar_conexao():
            try:
                # Faz uma solicitação para um site confiável
                requests.get("https://www.google.com", timeout=5)
                return True
            except (requests.ConnectionError, requests.Timeout):
                return False
            # Teste
            if checar_conexao():
                print("Conectado à internet")
            else:
                messagebox.showerror(
                    "Erro", "Sem internet ou conexão com o servidor.")
            # sys.exit()  # Encerra o programa

        def redefinir_validacao_email(event=None):
            global email_invalido_mostrado
            email_invalido_mostrado = False

        def validar_email(event=None):
            global email_invalido_mostrado
            email = campo_email.get()
            padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if re.match(padrao_email, email):
                email_invalido_mostrado = False  # Reset ao ser válido
            else:
                if not email_invalido_mostrado:  # Exibe a mensagem apenas uma vez
                    messagebox.showerror(
                        "Erro", "O e-mail digitado é inválido.")
                    email_invalido_mostrado = True  # Evita repetição da mensagem
                    campo_email.delete(0, tk.END)  # Limpa o campo de email
        # Carregar imagem da tela de login
        img_login = tk.PhotoImage(file="img/login.png")
        label_img_login = ctk.CTkLabel(
            master=janela, image=img_login, text=None)
        label_img_login.place(x=50, y=80)

        label_titulo = ctk.CTkLabel(master=janela, text="Backup de banco de dados rotativo", font=(
            "Roboto", 14), text_color="#00B0F0")
        label_titulo.place(x=25, y=10)

        # Frame do lado direito
        frame_login = ctk.CTkFrame(master=janela, width=350, height=396)
        frame_login.pack(side="right")

        # widgets dentro da tela de login
        label_login = ctk.CTkLabel(
            master=frame_login, text="Login", font=("Roboto", 20))
        label_login.place(x=25, y=5)

        label_email = ctk.CTkLabel(
            master=frame_login, text="* E-mail obrigatório.", text_color="green", font=("Roboto", 10))
        label_email.place(x=25, y=50)

        # Campo de e-mail e label
        campo_email = ctk.CTkEntry(
            master=frame_login, placeholder_text="Email", width=300, font=("Roboto", 14))
        campo_email.place(x=25, y=80)
        # Redefine a validação ao editar o e-mail
        campo_email.bind("<KeyRelease>", redefinir_validacao_email)

        label_senha = ctk.CTkLabel(
            master=frame_login, text="* Senha obrigatória.", text_color="green", font=("Roboto", 10))
        label_senha.place(x=25, y=110)
        # Campo de senha e label com evento focusin
        campo_senha = ctk.CTkEntry(
            master=frame_login, placeholder_text="Senha de acesso", width=300, font=("Roboto", 14), show="*")
        campo_senha.place(x=25, y=140)
        # Evento para chamar validação ao focar no campo de senha
        campo_senha.bind("<FocusIn>", validar_email)

        campo_checkbox = ctk.CTkCheckBox(
            master=frame_login, text="Confirmar senha").place(x=25, y=180)

        # Do this:
        campo_checkbox = ctk.CTkCheckBox(
            master=frame_login, text="Confirmar senha")
        campo_checkbox.place(x=25, y=180)

        def logar():
            email = campo_email.get()
            senha = campo_senha.get()
            checkbox = campo_checkbox.get()
            # print(f'veja a caixa--------------->>>>>>>>>>>>>>>> {checkbox}')
            banco = conectar()  # Conecta ao banco de dados
            cursor = banco.cursor()

            # Consulta com parâmetros para segurança e correta formatação
            cursor.execute(
                "SELECT * FROM users WHERE email = ? AND senha = ?", (email, senha))
            # Retorna o primeiro resultado, ou None se não encontrado
            usuario_encontrado = cursor.fetchone()

            if usuario_encontrado:
                # print("Login bem-sucedido!")
                tela_cadastrar()
                messagebox.showinfo("Login bem-sucedido", "Aguarde...")

            else:
                # print("E-mail ou senha incorretos.")
                messagebox.showerror("Erro", "E-mail ou senha incorretos.")

            banco.close()  # Fecha a conexão com o banco de dados

        botao_acessar = ctk.CTkButton(
            master=frame_login, text="Altenticar", width=300, command=logar)
        botao_acessar.place(x=25, y=285)

        # Função para habilitar ou desabilitar o botão de acesso

        # imagem de sem internet
        img_sem_net = tk.PhotoImage(file="img/sem-net.png")
        posicao_img_sem_net = ctk.CTkLabel(
            master=frame_login, image=img_sem_net, text=None)

        def atualizar_botao_acesso():
            if checar_conexao():
                botao_acessar.configure(state="normal")  # Desabilita o botão
            else:
                botao_acessar.configure(state="disabled")  # Habilita o botão
                posicao_img_sem_net.place(x=10, y=50)
## TELA DE CADASTRO #################################################################

        def tela_cadastrar():
            # remover o frame_login
            frame_login.pack_forget()

            # Criando a tela de caeastro
            frame_cadastro = ctk.CTkFrame(master=janela, width=350, height=396)
            frame_cadastro.pack(side="right")
            # widgets dentro da tela de login
            label_cadastrar = ctk.CTkLabel(
                master=frame_cadastro, text="Cadastre-se.", text_color="#fff", font=("Roboto", 20))
            label_cadastrar.place(x=25, y=5)
            # Campo de nome e label
            campo_nome = ctk.CTkEntry(
                master=frame_cadastro, placeholder_text="Nome", width=300, font=("Roboto", 14))
            campo_nome.place(x=25, y=80)
            # Campo de e-mail e label
            campo_email = ctk.CTkEntry(
                master=frame_cadastro, placeholder_text="Email", width=300, font=("Roboto", 14))
            campo_email.place(x=25, y=120)
            # Campo de senha e label
            campo_senha = ctk.CTkEntry(
                master=frame_cadastro, placeholder_text="Senha", width=300, font=("Roboto", 14), show="*")
            campo_senha.place(x=25, y=160)
            # Campo de confirma senha e label
            campo_confirma_senha = ctk.CTkEntry(
                master=frame_cadastro, placeholder_text="confirme a senha", width=300, font=("Roboto", 14), show="*")
            campo_confirma_senha.place(x=25, y=200)

            checkbox = ctk.CTkCheckBox(
                master=frame_cadastro, text="Aceito todos os termos e politicas").place(x=25, y=240)

            def voltar_tela_login():
                frame_cadastro.pack_forget()  # removendo o frame de cadaastro
                frame_login.pack(side="right")  # Voltando o frame_login

            voltar_login = ctk.CTkButton(
                master=frame_cadastro, text="Voltar", width=145, fg_color="#1abc9c", text_color="#000", command=voltar_tela_login).place(x=180, y=280)

            def salvar_cadastro():
                msg = messagebox.showinfo(
                    title="Salvo com sucesso", message="Cadastro inserido")
                pass

            botao_cadastrar_usuario = ctk.CTkButton(
                master=frame_cadastro, text="Cadastrar", width=145, fg_color="#3498db", text_color="#000", command=salvar_cadastro).place(x=25, y=280)


## TELA DE CADASTRO #################################################################

      # Botão cadastrar
        label_botao_cadastrar = ctk.CTkLabel(
            master=frame_login, text="* Cadastre-se.", text_color="#fff", font=("Roboto", 10))
        label_botao_cadastrar.place(x=25, y=320)
        botao_cadastrar = ctk.CTkButton(
            master=frame_login, text="Cadastre-se", width=300, fg_color="#008000", hover_color="#000", command=tela_cadastrar)
        botao_cadastrar.place(x=25, y=350)


Application()
