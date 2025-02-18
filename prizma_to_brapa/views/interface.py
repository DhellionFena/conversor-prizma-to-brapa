import tkinter as tk
from tkinter import filedialog

# Criar a janela principal
root = tk.Tk()
root.title("Minha Primeira Interface")
root.geometry("400x300")  # Define o tamanho da janela
root.configure(background="#FAFAFA")

# Criar um rótulo
label = tk.Label(root, text="🎵 Conversor PRIZMA para BRAPA 🎵",
                 font=("Helvetica", 16, "bold"), background="#FAFAFA")
label.pack(pady=10)

# Criar um botão para abrir o arquivo OTO


def abrir_oto():
    filepath = filedialog.askopenfilename(
        title="Selecione um arquivo OTO",
        filetypes=[("OTO files", "*.ini")]
    )
    if filepath:
        label.config(text=f"Arquivo selecionado: {filepath}")


botao_oto = tk.Button(root, text="Abrir arquivo OTO", command=abrir_oto)
botao_oto.pack(pady=10)


# Criar um botão


def clicar():
    label.config(text="Botão clicado!")


botao = tk.Button(root, text="Clique aqui", command=clicar)
botao.pack(pady=10)

# Iniciar o loop principal
root.mainloop()
