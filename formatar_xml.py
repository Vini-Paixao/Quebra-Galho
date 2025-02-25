import json
import re
import xml.dom.minidom
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from tkinter.font import Font
from xml.parsers.expat import ExpatError
import zipfile

from utilidades import resource_path

def validar_formatar_json_xml_interface():
    class FormatadorApp:
        def __init__(self, janela):
            self.janela = janela
            self.janela.title("Formatar XML e JSON")
            self.janela.geometry('700x590')
            self.janela.minsize(700, 590)
            self.janela.configure(bg='#7acbe6')
            self.janela.iconbitmap(resource_path('icon.ico'))
            self.formatted_parts = []
            self.current_type = 'xml'
            self.criar_widgets()
            self.configurar_estilos()

        def configurar_estilos(self):
            self.style = ttk.Style()
            self.style.theme_use('clam')
            self.style.configure('TNotebook', background='#7acbe6')
            self.style.configure('TFrame', background='#7acbe6')
            self.style.map('TNotebook.Tab', 
                         background=[('selected', '#7acbe6')], 
                         foreground=[('selected', 'black')])
            
            self.style.configure('Validar.TButton',
                                 background='#4CAF50',
                                 foreground='white',
                                 font=('Verdana', 9, 'bold'),
                                 borderradius=5)
            
            self.style.configure('Exportar.TButton',
                                 background='#2196F3',
                                 foreground='white',
                                 font=('Verdana', 9, 'bold'))
            
            self.style.configure('Fechar.TButton',
                                 background='#dc3545',
                                 foreground='white',
                                 font=('Verdana', 9, 'bold'))
            
            self.style.map('Validar.TButton', background=[('active', '#67d167')])
            self.style.map('Exportar.TButton', background=[('active', '#2196F3')])
            self.style.map('Fechar.TButton', background=[('active', '#dc3545')])


        def criar_widgets(self):
            main_frame = ttk.Frame(self.janela)
            main_frame.pack(padx=15, pady=15, expand=True)

            # Notebook (abas)
            self.notebook = ttk.Notebook(main_frame)
            self.notebook.pack(fill='both', expand=True)
            
            # Abas
            self.criar_aba_json()
            self.criar_aba_xml()
            
            # Controles
            self.criar_controles(main_frame)

        def criar_aba_json(self):
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=' JSON ', padding=5)
            
            tk.Label(frame, text="Cole seu JSON aqui:", font=('Verdana', 10), 
                   bg='#7acbe6').pack(pady=5, anchor='w')
            
            self.json_entrada = scrolledtext.ScrolledText(
                frame, width=90, height=12, wrap=tk.NONE,
                font=('Consolas', 10), bg='white', padx=10, pady=10
            )
            self.json_entrada.pack(fill='both', expand=True)
            
            tk.Label(frame, text="Resultado formatado:", font=('Verdana', 10), 
                   bg='#7acbe6').pack(pady=5, anchor='w')
            
            self.json_resultado = scrolledtext.ScrolledText(
                frame, width=90, height=12, wrap=tk.NONE,
                font=('Consolas', 10), bg='#f8f9fa', padx=10, pady=10, 
                state='disabled'
            )
            self.json_resultado.pack(fill='both', expand=True)

        def criar_aba_xml(self):
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=' XML ', padding=5)
            
            tk.Label(frame, 
                   text="Cole seu XML aqui (use <!-- SEPARADOR --> para múltiplos):", 
                   font=('Verdana', 10), bg='#7acbe6').pack(pady=5, anchor='w')
            
            self.xml_entrada = scrolledtext.ScrolledText(
                frame, width=90, height=12, wrap=tk.NONE,
                font=('Consolas', 10), bg='white', padx=10, pady=10
            )
            self.xml_entrada.pack(fill='both', expand=True)
            
            tk.Label(frame, text="Resultado formatado:", font=('Verdana', 10), 
                   bg='#7acbe6').pack(pady=5, anchor='w')
            
            self.xml_resultado = scrolledtext.ScrolledText(
                frame, width=90, height=12, wrap=tk.NONE,
                font=('Consolas', 10), bg='#f8f9fa', padx=10, pady=10, 
                state='disabled'
            )
            self.xml_resultado.pack(fill='both', expand=True)

        def criar_controles(self, parent):
            btn_frame = ttk.Frame(parent, style='TFrame')
            btn_frame.pack(pady=10)
            
            style = ttk.Style()
            style.configure('TButton', font=('Verdana', 9))
            
            ttk.Button(btn_frame, text="Validar/Formatar", style='Validar.TButton', 
                      command=self.validar_formatar).pack(side='left', padx=5)
            
            ttk.Button(btn_frame, text="Exportar", style='Exportar.TButton',
                      command=self.exportar_conteudo).pack(side='left', padx=5)
            
            ttk.Button(btn_frame, text="Fechar", style='Fechar.TButton',
                      command=self.janela.destroy).pack(side='left', padx=5)

        def obter_conteudo(self):
            tab = self.notebook.tab(self.notebook.select(), 'text').strip()
            self.current_type = 'json' if tab == 'JSON' else 'xml'
            
            if self.current_type == 'json':
                return self.json_entrada.get('1.0', tk.END).strip()
            return self.xml_entrada.get('1.0', tk.END).strip()

        def validar_formatar(self):
            raw_input = self.obter_conteudo()
            self.formatted_parts = []
            
            try:
                if self.current_type == 'json':
                    obj = json.loads(raw_input)
                    formatted = json.dumps(obj, indent=4, ensure_ascii=False)
                    self.formatted_parts = [formatted]
                    self.atualizar_resultado(formatted)
                else:
                    # Divisão robusta considerando diferentes formatos de separador
                    parts = [p.strip() for p in re.split(r'<!--\s*SEPARADOR\s*-->', raw_input, flags=re.IGNORECASE) if p.strip()]
                    
                    if not parts:
                        raise ValueError("Nenhum XML encontrado!")
                    
                    formatted_parts = []
                    for idx, part in enumerate(parts, 1):
                        try:
                            # Pré-processamento e validação
                            clean_part = part.strip()
                            if not clean_part:
                                continue
                                
                            if not clean_part.startswith(('<?xml', '<')):
                                raise ValueError(f"XML {idx} não inicia com tag válida")
                            
                            # Parsing e formatação
                            dom = xml.dom.minidom.parseString(clean_part)
                            formatted = dom.toprettyxml(indent="  ")
                            
                            # Pós-processamento
                            formatted = '\n'.join([line.rstrip() for line in formatted.split('\n') if line.strip()])
                            formatted_parts.append(formatted)
                            
                        except ExpatError as e:
                            error_msg = f"XML {idx} inválido\nLinha {e.lineno}: {e.args[0]}"
                            raise ValueError(error_msg)
                        except Exception as e:
                            raise ValueError(f"Erro no XML {idx}:\n{str(e)}")
                    
                    self.formatted_parts = formatted_parts
                    display = "\n\n" + "═"*50 + " SEPARADOR " + "═"*50 + "\n\n".join(formatted_parts)
                    self.atualizar_resultado(display)
                
                messagebox.showinfo("Sucesso", 
                    f"✓ {len(self.formatted_parts)} documento(s) processado(s) com sucesso!")
            
            except json.JSONDecodeError as e:
                messagebox.showerror("Erro JSON", 
                    f"Erro na linha {e.lineno}:\n{e.msg}\n\nDica: Verifique vírgulas faltantes ou chaves desbalanceadas")
            except ValueError as e:
                messagebox.showerror("Erro de Formatação", str(e))
            except Exception as e:
                messagebox.showerror("Erro Inesperado", 
                    f"Ocorreu um erro não esperado:\n{str(e)}\n\nPor favor, verifique a entrada e tente novamente")

        def atualizar_resultado(self, texto):
            widget = self.json_resultado if self.current_type == 'json' else self.xml_resultado
            widget.config(state='normal')
            widget.delete('1.0', tk.END)
            widget.insert(tk.END, texto)
            widget.config(state='disabled')

        def exportar_conteudo(self):
            if not self.formatted_parts:
                messagebox.showwarning("Aviso", "Nenhum conteúdo formatado para exportar!")
                return
            
            try:
                if len(self.formatted_parts) == 1:
                    self.exportar_unico()
                else:
                    self.exportar_zip()
            except Exception as e:
                messagebox.showerror("Erro na Exportação", 
                    f"Não foi possível salvar o arquivo:\n{str(e)}")

        def exportar_unico(self):
            file_types = [('JSON', '*.json')] if self.current_type == 'json' else [('XML', '*.xml')]
            default_ext = file_types[0][1][1:]
            
            file_path = filedialog.asksaveasfilename(
                title="Salvar arquivo",
                defaultextension=default_ext,
                filetypes=file_types + [('Todos arquivos', '*.*')]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.formatted_parts[0])
                messagebox.showinfo("Sucesso", 
                    f"Arquivo salvo com sucesso em:\n{file_path}")

        def exportar_zip(self):
            file_path = filedialog.asksaveasfilename(
                title="Salvar pacote ZIP",
                defaultextension='.zip',
                filetypes=[('Arquivo ZIP', '*.zip')]
            )
            
            if file_path:
                with zipfile.ZipFile(file_path, 'w') as zipf:
                    for i, content in enumerate(self.formatted_parts, 1):
                        ext = 'json' if self.current_type == 'json' else 'xml'
                        filename = f"documento_{i:03d}.{ext}"
                        zipf.writestr(filename, content)
                
                messagebox.showinfo("Sucesso", 
                    f"Pacote ZIP contendo {len(self.formatted_parts)} arquivos\nsalvo em:\n{file_path}")

    janela = tk.Toplevel()
    FormatadorApp(janela)
    return janela