# interface.py
import tkinter as tk
from tkinter import ttk

from ..controller import actions


class PrizmaToBrapaGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Conversor Prizma para Brapa")
        self.geometry("600x400")
        self.minsize(600, 400)
        self.configure(bg="#58605B")

        self.prefix_var = tk.StringVar()
        self.suffix_var = tk.StringVar()

        self.oto_df = None
        self.oto_str = None

        self.text_original = None
        self.text_converted = None

        self._create_widgets()

    def _create_widgets(self):

        self._add_prefix_suffix_frame()

        # Botão que ocupa toda a largura
        btn_select_oto = tk.Button(
            self,
            text="Selecione sua oto.ini",
            bg="#DBA244",
            relief="raised",
            fg="white",
            command=self._on_select_oto
        )
        btn_select_oto.pack(padx=10, pady=5, fill="x")

        self._add_conversion_frame()

    def _add_label(self, text, bg="#58605B", fg="white", font=("Helvetica", 9), container=None):
        if container:
            label = tk.Label(container, text=text, bg=bg, fg=fg, font=font)
            label.pack(padx=10, pady=5, anchor="w")
            return

        label = tk.Label(self, text=text, bg=bg, fg=fg, font=font)
        label.pack(padx=10, pady=5, anchor="w")

    def _add_prefix_suffix_frame(self):

        self._add_label("Insira os prefixos e sufixos de sua oto:",
                        font=("Helvetica", 12, "bold"))

        # Frame para prefixos e sufixos
        frame_inputs = tk.Frame(self, bg="#58605B")
        frame_inputs.pack(padx=10, pady=5, fill="x")

        # Entrada para Prefixos
        label_prefix = tk.Label(
            frame_inputs, text="Prefixos:", bg="#58605B", fg="white")
        label_prefix.grid(row=0, column=0, sticky="w")

        entry_prefix = tk.Entry(frame_inputs, textvariable=self.prefix_var)
        entry_prefix.grid(row=0, column=1, sticky="we", padx=(5, 20))

        # Entrada para Sufixos
        label_suffix = tk.Label(
            frame_inputs, text="Sufixos:", bg="#58605B", fg="white")
        label_suffix.grid(row=0, column=2, sticky="w")

        entry_suffix = tk.Entry(frame_inputs, textvariable=self.suffix_var)
        entry_suffix.grid(row=0, column=3, sticky="we")

        self._add_label(text="Caso sua oto não contenha, deixe em branco.")

    def _add_conversion_frame(self):
        # Frame para a grade
        frame_grid = tk.Frame(self, bg="#58605B")
        frame_grid.pack(padx=10, pady=10, fill="both", expand=True)

        # Configurar colunas e linha expansível
        frame_grid.columnconfigure(0, weight=1)
        frame_grid.columnconfigure(1, weight=1)
        # Linha das textareas expande verticalmente
        frame_grid.rowconfigure(1, weight=1)

        # (1,1) Label "Arquivo original"
        label_original = tk.Label(
            frame_grid, text="Arquivo original", bg="#58605B", fg="white"
        )
        label_original.grid(row=0, column=0, sticky="nsew", pady=5)

        # (1,2) Label "Arquivo convertido"
        label_converted = tk.Label(
            frame_grid, text="Arquivo convertido", bg="#58605B", fg="white"
        )
        label_converted.grid(
            # espaço entre colunas
            row=0, column=1, sticky="nsew", pady=5, padx=(10, 0)
        )

        # (2,1) Textarea para oto original
        self.text_original = tk.Text(frame_grid, bg="white")
        self.text_original.grid(row=1, column=0, sticky="nsew", pady=5)

        # (2,2) Textarea para oto convertido
        self.text_converted = tk.Text(frame_grid, bg="white")
        self.text_converted.grid(
            # espaço entre colunas
            row=1, column=1, sticky="nsew", pady=5, padx=(10, 0)
        )

        # (3,1) Botão "Converter"
        btn_convert = tk.Button(
            frame_grid, text="Converter",
            bg="#9744DB",
            fg="white",
            command=self._on_convert_oto
        )
        btn_convert.grid(row=2, column=0, sticky="ew", pady=5)

        # (3,2) Botão "Salvar conversão"
        btn_save = tk.Button(
            frame_grid, text="Salvar conversão",
            bg="#9744DB",
            fg="white",
        )
        btn_save.grid(
            # espaço entre colunas
            row=2, column=1, sticky="ew", pady=5, padx=(10, 0)
        )

    def _on_select_oto(self):
        oto_list = actions.get_oto_list_str()

        self.oto_str = "\n".join(oto_list)
        self.text_original.delete("1.0", "end")
        self.text_original.insert("1.0", self.oto_str)

    def _on_convert_oto(self):
        if self.oto_str is None or self.oto_str.strip() == "":
            return

        print(self.text_original.get("1.0", "end"))

        # self.text_converted.delete("1.0", "end")
        # self.text_converted.insert("1.0", self.oto_str)

    def _on_save_oto(self):
        pass
