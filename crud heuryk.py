import tkinter as tk
from tkinter import messagebox
from mongoengine import Document, StringField, connect

def iniciar_conexao():
    try:
        connect(
            host='mongodb+srv://alanvitor57ntc:vtrno123@alan.qz74y.mongodb.net/'
        )
        print("Conexão com MongoDB estabelecida!")
    except Exception as e:
        print(f"Erro ao conectar com MongoDB: {e}")
        messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao MongoDB. Verifique se o serviço está rodando.")
        exit(1)

class Contato(Document):
    nome = StringField(required=True, max_length=100)
    telefone = StringField(required=True, max_length=20)

def adicionar_contato():
    nome = entry_nome.get().strip()
    telefone = entry_telefone.get().strip()

    if nome and telefone:
        contato = Contato(nome=nome, telefone=telefone)
        contato.save()
        messagebox.showinfo("Sucesso", f"Contato '{nome}' adicionado!")
        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        listar_contatos()
    else:
        messagebox.showwarning("Erro", "Nome e telefone são obrigatórios.")

def listar_contatos():
    lista_contatos.delete(0, tk.END)
    contatos = Contato.objects()
    if contatos:
        for contato in contatos:
            lista_contatos.insert(tk.END, f"ID: {contato.id} - {contato.nome} : {contato.telefone}")
    else:
        lista_contatos.insert(tk.END, "Nenhum contato cadastrado ainda.")

def deletar_contato():
    try:
        selecionado = lista_contatos.get(lista_contatos.curselection())
        contato_id = selecionado.split(" - ")[0].replace("ID: ", "").strip()
        contato = Contato.objects.get(id=contato_id)
        contato.delete()
        messagebox.showinfo("Sucesso", f"Contato '{contato.nome}' deletado!")
        listar_contatos()
    except:
        messagebox.showwarning("Erro", "Selecione um contato para deletar.")

def atualizar_contato():
    try:
        selecionado = lista_contatos.get(lista_contatos.curselection())
        contato_id = selecionado.split(" - ")[0].replace("ID: ", "").strip()
        contato = Contato.objects.get(id=contato_id)
        
        novo_nome = entry_nome.get().strip()
        novo_telefone = entry_telefone.get().strip()
        
        if novo_nome:
            contato.nome = novo_nome
        if novo_telefone:
            contato.telefone = novo_telefone
        contato.save()
        messagebox.showinfo("Sucesso", f"Contato '{contato.nome}' atualizado!")
        listar_contatos()
    except:
        messagebox.showwarning("Erro", "Selecione um contato para atualizar.")

root = tk.Tk()
root.title("Aplicativo de Contatos - CRUD")
root.geometry("600x500")
root.configure(bg="#f0f2f5") 

primary_color = "#3b5998"
text_color = "#ffffff"
entry_bg = "#ffffff"
button_bg = "#4267B2"
button_fg = "#ffffff"
highlight_bg = "#f0f2f5"

lbl_title = tk.Label(root, text="Gerenciamento de Contatos", font=("Arial", 18, "bold"),
                     bg=primary_color, fg=text_color, padx=20, pady=10)
lbl_title.pack(fill=tk.X, pady=10)

lbl_nome = tk.Label(root, text="Nome:", bg="#f0f2f5", fg="#333333", font=("Arial", 12))
lbl_nome.pack()
entry_nome = tk.Entry(root, width=50, bg=entry_bg, fg="black", font=("Arial", 12))
entry_nome.pack(pady=5)

lbl_telefone = tk.Label(root, text="Telefone:", bg="#f0f2f5", fg="#333333", font=("Arial", 12))
lbl_telefone.pack()
entry_telefone = tk.Entry(root, width=50, bg=entry_bg, fg="black", font=("Arial", 12))
entry_telefone.pack(pady=5)

btn_frame = tk.Frame(root, bg="#f0f2f5")
btn_frame.pack(pady=15)

btn_add = tk.Button(btn_frame, text="Adicionar Contato", command=adicionar_contato,
                    bg=button_bg, fg=button_fg, font=("Arial", 10, "bold"), width=20, relief="flat")
btn_add.grid(row=0, column=0, padx=10)

btn_update = tk.Button(btn_frame, text="Atualizar Contato", command=atualizar_contato,
                       bg=button_bg, fg=button_fg, font=("Arial", 10, "bold"), width=20, relief="flat")
btn_update.grid(row=0, column=1, padx=10)

btn_delete = tk.Button(btn_frame, text="Deletar Contato", command=deletar_contato,
                       bg=button_bg, fg=button_fg, font=("Arial", 10, "bold"), width=20, relief="flat")
btn_delete.grid(row=0, column=2, padx=10)

lbl_contatos = tk.Label(root, text="Contatos Cadastrados:", bg="#f0f2f5", fg="#333333", font=("Arial", 12, "bold"))
lbl_contatos.pack()

lista_contatos = tk.Listbox(root, width=70, height=10, bg=highlight_bg, fg="black", font=("Arial", 12), bd=0, relief="flat", highlightthickness=1, highlightbackground="#ccc")
lista_contatos.pack(pady=10)

iniciar_conexao()

listar_contatos()

root.mainloop()
