#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gerador de Mapas Mentais para Repositórios Acadêmicos
Cria mapas mentais interativos em formato Mermaid para visualizar a estrutura de pastas.
"""

import os
import re
from pathlib import Path

def sanitize_mermaid_label(text):
    """
    Sanitiza texto para ser usado como label no Mermaid.
    Remove caracteres especiais e formata adequadamente.
    """
    # Remove caracteres especiais que podem quebrar o Mermaid
    sanitized = re.sub(r'[^\w\s\-\.]', '', text)
    # Substitui espaços por underscores e remove espaços extras
    sanitized = re.sub(r'\s+', '_', sanitized.strip())
    # Limita o tamanho do label
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
    def build_tree(path, current_depth=0):
        """Constrói recursivamente a árvore de pastas."""
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
                    tree.append(f"  {sanitized_name}")
                    # Recursivamente adiciona subpastas
                    subtree = build_tree(item_path, current_depth + 1)
                    for subtree_item in subtree:
                        tree.append(f"  {subtree_item}")
                else:
                    # Adiciona arquivos com ícone diferente
                    file_icon = "📄" if item_name.endswith('.md') else "📁"
                    tree.append(f"  {file_icon} {sanitized_name}")
        
        except PermissionError:
            tree.append("  [Acesso Negado]")
        except Exception as e:
            tree.append(f"  [Erro: {str(e)[:20]}...]")
        
        return tree
    
    # Gera o nome raiz sanitizado
    root_name = sanitize_mermaid_label(os.path.basename(root_path) or "Repositório")
    
    # Constrói a árvore
    tree_items = build_tree(root_path)
    
    # Monta o código Mermaid
    mindmap_code = ["mindmap", f"  root(({root_name}))"]
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
    
    # Verifica se o caminho existe
    if not os.path.exists(path):
        print(f"Erro: Caminho não encontrado - {path}")
        return False
    
    # Gera o mapa mental em formato Mermaid
    mindmap_mermaid = generate_mermaid_mindmap(path)
    
    # Cria o conteúdo do arquivo Markdown
    folder_name = os.path.basename(path) or "Repositório"
    
    output_content = f"""# 🗺️ Mapa Mental - {folder_name}

Este é um mapa mental interativo da estrutura de pastas. Utilize-o para navegar facilmente pelo conteúdo.

## 📊 Estrutura do Diretório

```mermaid
{mindmap_mermaid}
```

## 📋 Informações

- **Caminho:** `{path}`
- **Gerado em:** {__import__('datetime').datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
- **Ferramenta:** Gerador de Mapas Mentais v1.0

## 🔍 Como usar

1. **Visualização:** O mapa mental mostra a hierarquia de pastas e arquivos principais
2. **Navegação:** Use a estrutura para localizar rapidamente o conteúdo desejado
3. **Arquivos importantes:** Documentos Markdown (📄) e outros arquivos relevantes são destacados

## 💡 Dicas

- Pastas são representadas por nós no mapa mental
- Arquivos importantes (.md, .py, .pdf, etc.) são mostrados com ícones específicos
- A profundidade máxima de visualização é limitada para melhor legibilidade

---
*Mapa mental gerado automaticamente - Não edite manualmente este arquivo*
"""

    # Salva o arquivo
    try:
        # Garante que o diretório existe
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
    
    # Define o caminho raiz do repositório
    root_path = os.path.dirname(os.path.abspath(__file__))
    
    print(f"📁 Caminho raiz: {root_path}")
    
    # Limpa mapas mentais antigos
    clean_old_mindmaps(root_path)
    
    # Contador de mapas gerados
    maps_generated = 0
    
    # Gera mapa mental para cada disciplina
    print("\n📚 Gerando mapas mentais para disciplinas...")
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Percorre apenas as pastas de semestre (padrão: YYYY-N-Semestre)
        if dirpath != root_path and os.path.basename(dirpath).endswith('-Semestre'):
            print(f"\n🎓 Processando semestre: {os.path.basename(dirpath)}")
            
            for discipline_dir in dirnames:
                # Estando em uma pasta de semestre, entra em cada disciplina
                discipline_path = os.path.join(dirpath, discipline_dir)
                output_filename = os.path.join(discipline_path, "MAPA_MENTAL.md")
                
                if generate_mindmap_for_path(discipline_path, output_filename):
                    maps_generated += 1
    
    # Gera o mapa mental principal na raiz
    print(f"\n🌟 Gerando mapa mental geral do repositório...")
    main_output = os.path.join(root_path, "MAPA_MENTAL.md")
    if generate_mindmap_for_path(root_path, main_output):
        maps_generated += 1
    
    # Relatório final
    print(f"\n✨ Processo concluído com sucesso!")
    print(f"📊 Total de mapas mentais gerados: {maps_generated}")
    print(f"📁 Arquivo principal: {main_output}")
    
    # Instruções de uso
    print(f"\n💡 Para visualizar os mapas mentais:")
    print(f"   1. Abra os arquivos MAPA_MENTAL.md em um visualizador Markdown")
    print(f"   2. Use extensões como 'Markdown Preview' no VS Code")
    print(f"   3. Ou visualize no GitHub/GitLab que suportam Mermaid")

if __name__ == "__main__":
    main()
