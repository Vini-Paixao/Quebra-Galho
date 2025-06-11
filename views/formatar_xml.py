import json
import re
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import zipfile
from lxml import etree

from utilidades import resource_path, ICONS


def validar_formatar_json_xml_interface():
    class FormatadorApp:
        def __init__(self, janela):
            self.janela = janela
            self.janela.title("Formatador e Validador de XML/JSON")
            self.janela.geometry("700x590")
            self.janela.minsize(700, 590)
            self.janela.iconbitmap(resource_path("icon.ico"))

            self.formatted_parts = []
            self.current_type = "xml"
            self.criar_widgets()

        def criar_widgets(self):
            main_frame = ttk.Frame(self.janela, padding=15)
            main_frame.pack(expand=True, fill="both")

            self.criar_controles(main_frame)
            self.notebook = ttk.Notebook(main_frame)
            self.notebook.pack(expand=True, fill="both", pady=(0, 15))

            self.criar_aba_json()
            self.criar_aba_xml()

        def criar_aba_json(self):
            frame = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(frame, text=" JSON ")
            ttk.Label(
                frame, text="Cole seu JSON aqui:", font=("Segoe UI", 10, "bold")
            ).pack(pady=(0, 5), anchor="w")
            self.json_entrada = scrolledtext.ScrolledText(
                frame, width=90, height=12, wrap=tk.NONE, relief="solid", borderwidth=1
            )
            self.json_entrada.pack(fill="both", expand=True)
            ttk.Label(frame, text="Resultado:", font=("Segoe UI", 10, "bold")).pack(
                pady=5, anchor="w"
            )
            self.json_resultado = scrolledtext.ScrolledText(
                frame,
                width=90,
                height=12,
                wrap=tk.NONE,
                relief="solid",
                borderwidth=1,
                state="disabled",
            )
            self.json_resultado.pack(fill="both", expand=True)

        def criar_aba_xml(self):
            frame = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(frame, text=" XML ")
            ttk.Label(
                frame, text="Cole seu XML aqui:", font=("Segoe UI", 10, "bold")
            ).pack(pady=(0, 5), anchor="w")
            self.xml_entrada = scrolledtext.ScrolledText(
                frame, width=90, height=12, wrap=tk.NONE, relief="solid", borderwidth=1
            )
            self.xml_entrada.pack(fill="both", expand=True)
            ttk.Label(frame, text="Resultado:", font=("Segoe UI", 10, "bold")).pack(
                pady=5, anchor="w"
            )
            self.xml_resultado = scrolledtext.ScrolledText(
                frame,
                width=90,
                height=12,
                wrap=tk.NONE,
                relief="solid",
                borderwidth=1,
                state="disabled",
            )
            self.xml_resultado.pack(fill="both", expand=True)

        def inserir_separador(self):
            try:
                self.notebook.select(1)
                self.xml_entrada.focus_set()
                # CORREÇÃO: Inserir o separador correto
                self.xml_entrada.insert(tk.INSERT, "\n\n\n\n")
            except tk.TclError:
                messagebox.showerror("Erro", "Não foi possível mudar para a aba XML.")

        def criar_controles(self, parent):
            btn_frame = ttk.Frame(parent)
            btn_frame.pack(side="bottom", fill="x")
            right_frame = ttk.Frame(btn_frame)
            right_frame.pack(side="right")
            ttk.Button(
                right_frame,
                text="Fechar",
                image=ICONS.get("fechar", tk.PhotoImage()),
                compound="left",
                command=self.janela.destroy,
            ).pack(side="right", padx=(10, 0))
            ttk.Button(
                right_frame,
                text="Exportar",
                image=ICONS.get("exportar2", tk.PhotoImage()),
                compound="left",
                command=self.exportar_conteudo,
            ).pack(side="right")
            left_frame = ttk.Frame(btn_frame)
            left_frame.pack(side="left")
            ttk.Button(
                left_frame,
                text="Validar/Formatar",
                style="Accent.TButton",
                image=ICONS.get("executar", tk.PhotoImage()),
                compound="left",
                command=self.validar_formatar,
            ).pack(side="left")
            ttk.Button(
                left_frame,
                text="Inserir Separador",
                image=ICONS.get("separador", tk.PhotoImage()),
                compound="left",
                command=self.inserir_separador,
            ).pack(side="left", padx=(10, 0))

        def obter_conteudo_da_aba_selecionada(self):
            try:
                tab_selecionada = self.notebook.tab(self.notebook.select(), "text")
                self.current_type = "json" if "JSON" in tab_selecionada else "xml"
                if self.current_type == "json":
                    return self.json_entrada.get("1.0", tk.END).strip()
                return self.xml_entrada.get("1.0", tk.END).strip()
            except tk.TclError:
                return ""

        def validar_formatar(self):
            raw_input = self.obter_conteudo_da_aba_selecionada()
            if not raw_input:
                messagebox.showwarning("Aviso", "Nenhum conteúdo para formatar.")
                return

            self.formatted_parts = []
            try:
                if self.current_type == "json":
                    obj = json.loads(raw_input)
                    formatted = json.dumps(obj, indent=4, ensure_ascii=False)
                    self.formatted_parts = [formatted]
                    self.atualizar_resultado(formatted)
                else:
                    cleaned_input = raw_input.encode("utf-8-sig").decode("utf-8")

                    # separa em múltiplos XMLs usando exatamente 4 quebras de linha
                    raw_parts = cleaned_input.split("\n\n\n\n")
                    parts = [p.strip() for p in raw_parts if p.strip()]
                    
                    if not parts:
                        raise ValueError("Nenhum XML encontrado!")

                    formatted_parts = []
                    for part in parts:
                        parser = etree.XMLParser(remove_blank_text=True, recover=True)
                        element = etree.fromstring(part.encode("utf-8"), parser)
                        formatted_bytes = etree.tostring(
                            element,
                            pretty_print=True, # type: ignore
                            encoding="utf-8", # type: ignore
                            xml_declaration=True, # type: ignore
                        )
                        formatted = formatted_bytes.decode("utf-8")
                        formatted_parts.append(formatted)

                    self.formatted_parts = formatted_parts
                    # CORREÇÃO: Juntar as partes com o separador correto
                    display_text = "\n\n\n\n".join(formatted_parts)
                    self.atualizar_resultado(display_text)

                messagebox.showinfo(
                    "Sucesso",
                    f"✓ {len(self.formatted_parts)} documento(s) {self.current_type.upper()} processado(s) com sucesso!",
                )
            except json.JSONDecodeError as e:
                messagebox.showerror(
                    "Erro de JSON",
                    f"JSON inválido na linha {e.lineno}, coluna {e.colno}:\n{e.msg}",
                )
            except etree.XMLSyntaxError as e:
                messagebox.showerror("Erro de XML", f"XML inválido:\n{e.msg}")
            except Exception as e:
                messagebox.showerror(
                    "Erro Inesperado",
                    f"Ocorreu um erro ao processar a entrada:\n{str(e)}",
                )

        def atualizar_resultado(self, texto):
            widget = (
                self.json_resultado
                if self.current_type == "json"
                else self.xml_resultado
            )
            widget.config(state="normal")
            widget.delete("1.0", tk.END)
            widget.insert(tk.END, texto)
            widget.config(state="disabled")

        def exportar_conteudo(self):
            if not self.formatted_parts:
                messagebox.showwarning(
                    "Aviso",
                    "Nenhum conteúdo formatado para exportar! Valide o código primeiro.",
                )
                return
            try:
                if len(self.formatted_parts) == 1:
                    self.exportar_arquivo_unico()
                else:
                    self.exportar_zip()
            except Exception as e:
                messagebox.showerror(
                    "Erro na Exportação",
                    f"Não foi possível salvar o arquivo:\n{str(e)}",
                )

        def exportar_arquivo_unico(self):
            file_types = (
                [("JSON", "*.json")]
                if self.current_type == "json"
                else [("XML", "*.xml")]
            )
            file_path = filedialog.asksaveasfilename(
                title="Salvar arquivo",
                defaultextension=file_types[0][1],
                filetypes=file_types,
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.formatted_parts[0])
                messagebox.showinfo(
                    "Sucesso", f"Arquivo salvo com sucesso em:\n{file_path}"
                )

        def exportar_zip(self):
            file_path = filedialog.asksaveasfilename(
                title="Salvar pacote ZIP",
                defaultextension=".zip",
                filetypes=[("Arquivo ZIP", "*.zip")],
            )
            if file_path:
                with zipfile.ZipFile(file_path, "w") as zipf:
                    for i, content in enumerate(self.formatted_parts, 1):
                        ext = "json" if self.current_type == "json" else "xml"
                        zipf.writestr(f"documento_{i:03d}.{ext}", content)
                messagebox.showinfo(
                    "Sucesso",
                    f"Pacote ZIP com {len(self.formatted_parts)} arquivos salvo em:\n{file_path}",
                )

    janela = tk.Toplevel()
    FormatadorApp(janela)
    return janela
