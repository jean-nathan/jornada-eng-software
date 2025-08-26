#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gerador de Mapas Mentais para Repositórios Acadêmicos
Cria mapas mentais interativos em formato Mermaid para visualizar a estrutura de pastas.
"""

import os
import re
from pathlib import Path
import datetime

def sanitize_mermaid_label(text):
    """
    Sanitiza texto para ser usado como label no Mermaid.
    Remove caracteres especiais e formata adequadamente.
    """
    # Remove caracteres que quebram a sintaxe do Mermaid
    sanitized = re.sub(r'[^\w\s\-\.]', '', text)
    # Substitui espaços por underscores
    sanitized = re.sub(r'\s+', '_', sanitized.strip())
    # Limita o tamanho para melhor visualização
    if len(sanitized) > 30:
        sanitized = sanitized[:27] + "..."
    return sanitized if sanitized else "pasta"

def generate_mermaid_mindmap(root_path, max_depth=3):
    """
    Gera um mapa mental em formato Mermaid baseado na estrutura de pastas.
    
    Args:
        root_path (str): Caminho raiz para análise
        max_depth (int): Profundidade máxima de análise
    
    Returns:
        str: Código Mermaid para o mapa mental
    """
    def build_tree(path, current_depth=0, indent="    "):
        """Constrói recursivamente a árvore de pastas com indentação correta para mindmap."""
        if current_depth > max_depth:
            return []
        
        tree = []
        
        try:
            items = []
            # Lista todos os itens no diretório
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    # Ignora pastas ocultas e de sistema
                    if not item.startswith('.') and item not in ['__pycache__', 'node_modules', '.git']:
                        items.append((item, item_path, True))  # True = é diretório
                elif os.path.isfile(item_path) and current_depth < 2:
                    # Inclui apenas alguns tipos de arquivo importantes
                    if item.endswith(('.md', '.py', '.txt', '.pdf', '.docx', '.pptx')):
                        items.append((item, item_path, False))  # False = é arquivo
            
            # Ordena itens: pastas primeiro, depois arquivos
            items.sort(key=lambda x: (not x[2], x[0].lower()))
            
            for item_name, item_path, is_dir in items:
                sanitized_name = sanitize_mermaid_label(item_name)
                
                if is_dir:
                    # Para pastas, adiciona sem parênteses
                    tree.append(f"{indent}{sanitized_name}")
                    # Processa subdiretórios com indentação aumentada
                    subtree = build_tree(item_path, current_depth + 1, indent + "  ")
                    tree.extend(subtree)
                else:
                    # Para arquivos, adiciona com descrição entre parênteses
                    file_extension = item_name.split('.')[-1].upper() if '.' in item_name else 'FILE'
                    tree.append(f"{indent}{sanitized_name}")
                    tree.append(f"{indent}  ({file_extension})")
        
        except PermissionError:
            tree.append(f"{indent}Acesso_Negado")
            tree.append(f"{indent}  (ERRO)")
        except Exception as e:
            error_msg = str(e)[:15].replace(' ', '_')
            tree.append(f"{indent}Erro_{error_msg}")
            tree.append(f"{indent}  (ERRO)")
        
        return tree
    
    # Gera o nome raiz sanitizado
    root_name = sanitize_mermaid_label(os.path.basename(root_path) or "Repositorio")
    
    # Constrói a árvore a partir da raiz
    tree_items = build_tree(root_path)
    
    # Monta o código Mermaid final usando a sintaxe correta de mindmap
    mindmap_code = [
        "mindmap",
        f"  root(({root_name}))"
    ]
    mindmap_code.extend(tree_items)
    
    return "\n".join(mindmap_code)

def clean_old_mindmaps(root_path):
    """
    Remove mapas mentais antigos para evitar conflitos.
    
    Args:
        root_path (str): Caminho raiz para limpeza
    """
    print("Limpando mapas mentais antigos...")
    
    for root, dirs, files in os.walk(root_path):
        # Ignora a pasta .git
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            if file == "MAPA_MENTAL.md":
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"  - Removido: {file_path}")
                except OSError as e:
                    print(f"  - Erro ao remover {file_path}: {e}")

def generate_mindmap_for_path(path, output_filename):
    """
    Gera um mapa mental para um caminho específico e salva em arquivo.
    
    Args:
        path (str): Caminho para análise
        output_filename (str): Nome do arquivo de saída
    
    Returns:
        bool: True se bem-sucedido, False caso contrário
    """
    print(f"Processando: {path}")
    
    if not os.path.exists(path):
        print(f"Erro: Caminho não encontrado - {path}")
        return False
    
    mindmap_mermaid = generate_mermaid_mindmap(path)
    
    folder_name = os.path.basename(os.path.normpath(path)) or "Repositório"
    
    output_content = f"""# 🗺️ Mapa Mental - {folder_name}

Este é um mapa mental interativo da estrutura de pastas. Utilize-o para navegar facilmente pelo conteúdo.

## 📊 Estrutura do Diretório

```mermaid
{mindmap_mermaid}
```

## 📋 Informações

- **Caminho:** `{path}`
- **Gerado em:** {datetime.datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
- **Ferramenta:** Gerador de Mapas Mentais v1.4

## 🔍 Como usar

1. **Visualização:** O mapa mental mostra a hierarquia de pastas e arquivos principais.
2. **Navegação:** Use a estrutura para localizar rapidamente o conteúdo desejado.

---
*Mapa mental gerado automaticamente - Não edite manualmente este arquivo*
"""

    try:
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"  ✅ Mapa gerado: {output_filename}")
        return True
    except IOError as e:
        print(f"  ❌ Erro ao salvar o arquivo {output_filename}: {e}")
        return False

def main():
    """
    Função principal que gerencia a geração de mapas mentais.
    """
    print("🚀 Iniciando geração de mapas mentais...")
    
    try:
        root_path = Path(__file__).parent.resolve()
    except NameError:
        root_path = Path('.').resolve()
        
    print(f"📁 Caminho raiz: {root_path}")
    
    clean_old_mindmaps(root_path)
    
    maps_generated = 0
    
    print("\n📚 Gerando mapas mentais para disciplinas...")
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Ignora a pasta .git para não percorrê-la
        if '.git' in dirnames:
            dirnames.remove('.git')

        if os.path.basename(dirpath).endswith('-Semestre'):
            print(f"\n🎓 Processando semestre: {os.path.basename(dirpath)}")
            
            # Cria uma cópia da lista de diretórios para iterar, pois podemos modificá-la
            for discipline_dir in list(dirnames):
                discipline_path = os.path.join(dirpath, discipline_dir)
                output_filename = os.path.join(discipline_path, "MAPA_MENTAL.md")
                
                if generate_mindmap_for_path(discipline_path, output_filename):
                    maps_generated += 1
    
    print(f"\n🌟 Gerando mapa mental geral do repositório...")
    main_output = os.path.join(root_path, "MAPA_MENTAL.md")
    if generate_mindmap_for_path(str(root_path), main_output):
        maps_generated += 1
    
    print(f"\n✨ Processo concluído com sucesso!")
    print(f"📊 Total de mapas mentais gerados: {maps_generated}")

if __name__ == "__main__":
    main()
