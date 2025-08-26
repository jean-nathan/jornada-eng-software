#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gerador de Prompts para Flashcards do Anki - Versão Aprimorada
Gera prompts personalizados incluindo automaticamente o conteúdo dos arquivos .md
das disciplinas acadêmicas (anotações, exercícios e simulados).
"""

import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

def clean_old_prompts(prompts_dir):
    """
    Remove todos os arquivos .txt do diretório de prompts, se ele existir.
    
    Args:
        prompts_dir (str): Caminho para o diretório de prompts
    """
    if os.path.exists(prompts_dir):
        print(f"🧹 Iniciando a limpeza dos prompts antigos em '{prompts_dir}'...")
        removed_count = 0
        
        for filename in os.listdir(prompts_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(prompts_dir, filename)
                try:
                    os.remove(file_path)
                    print(f"  ✅ Removido: {filename}")
                    removed_count += 1
                except OSError as e:
                    print(f"  ❌ Erro ao remover {file_path}: {e}")
        
        print(f"📊 Total de arquivos removidos: {removed_count}")
    else:
        print(f"📁 O diretório '{prompts_dir}' não existe, será criado.")

def read_markdown_file(file_path):
    """
    Lê o conteúdo de um arquivo Markdown.
    
    Args:
        file_path (str): Caminho para o arquivo
        
    Returns:
        str: Conteúdo do arquivo ou mensagem de erro
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return content if content else "[Arquivo vazio]"
    except UnicodeDecodeError:
        try:
            # Tenta com encoding alternativo
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read().strip()
                return content if content else "[Arquivo vazio]"
        except Exception as e:
            return f"[Erro ao ler arquivo: {str(e)}]"
    except Exception as e:
        return f"[Erro ao ler arquivo: {str(e)}]"

def extract_discipline_content(discipline_path):
    """
    Extrai todo o conteúdo dos arquivos .md das pastas anotacoes, exercicios e simulados.
    
    Args:
        discipline_path (str): Caminho da disciplina
        
    Returns:
        dict: Conteúdo organizado por categoria
    """
    content = {
        'anotacoes': [],
        'exercicios': [],
        'simulados': [],
        'total_files': 0,
        'total_characters': 0
    }
    
    # Pastas a serem escaneadas
    folders_to_scan = ['anotacoes', 'exercicios', 'simulados']
    
    for folder_name in folders_to_scan:
        folder_path = os.path.join(discipline_path, folder_name)
        
        if os.path.exists(folder_path):
            print(f"  📂 Escaneando pasta: {folder_name}")
            
            try:
                files = [f for f in os.listdir(folder_path) if f.endswith('.md') and not f.startswith('.')]
                files.sort()  # Ordena alfabeticamente
                
                for filename in files:
                    file_path = os.path.join(folder_path, filename)
                    
                    if os.path.isfile(file_path):
                        print(f"    📄 Lendo: {filename}")
                        
                        file_content = read_markdown_file(file_path)
                        
                        content[folder_name].append({
                            'filename': filename,
                            'content': file_content,
                            'path': file_path
                        })
                        
                        content['total_files'] += 1
                        content['total_characters'] += len(file_content)
                        
            except PermissionError as e:
                print(f"    ⚠️  Sem permissão para acessar {folder_path}: {e}")
            except Exception as e:
                print(f"    ❌ Erro ao escanear {folder_path}: {e}")
        else:
            print(f"  📂 Pasta não encontrada: {folder_name}")
    
    return content

def format_content_for_prompt(content, discipline_name):
    """
    Formata o conteúdo extraído para inclusão no prompt.
    
    Args:
        content (dict): Conteúdo extraído da disciplina
        discipline_name (str): Nome da disciplina
        
    Returns:
        str: Conteúdo formatado para o prompt
    """
    if content['total_files'] == 0:
        return "⚠️ **Nenhum arquivo .md encontrado nas pastas especificadas.**"
    
    formatted_sections = []
    
    # Mapeamento de nomes de pastas para títulos
    section_titles = {
        'anotacoes': '📝 Anotações de Aula',
        'exercicios': '🔧 Exercícios e Práticas',
        'simulados': '🎯 Simulados e Avaliações'
    }
    
    for section_key, section_title in section_titles.items():
        if content[section_key]:
            formatted_sections.append(f"\n## {section_title}")
            formatted_sections.append(f"*Total de {len(content[section_key])} arquivo(s)*\n")
            
            for file_info in content[section_key]:
                filename = file_info['filename']
                file_content = file_info['content']
                
                # Adiciona separador visual
                formatted_sections.append(f"### 📄 {filename}")
                formatted_sections.append("```")
                formatted_sections.append(file_content)
                formatted_sections.append("```\n")
    
    # Adiciona estatísticas
    stats_section = f"""
## 📊 Resumo do Conteúdo Disponível
- **Total de arquivos processados:** {content['total_files']}
- **Total de caracteres:** {content['total_characters']:,}
- **Arquivos por categoria:**
  - Anotações: {len(content['anotacoes'])}
  - Exercícios: {len(content['exercicios'])}
  - Simulados: {len(content['simulados'])}
"""
    
    return stats_section + "\n" + "\n".join(formatted_sections)

def generate_enhanced_prompt(discipline_name, semester_name, discipline_path, content):
    """
    Gera um prompt completo com todo o conteúdo da disciplina incluído.
    
    Args:
        discipline_name (str): Nome da disciplina
        semester_name (str): Nome do semestre
        discipline_path (str): Caminho da disciplina
        content (dict): Conteúdo extraído da disciplina
        
    Returns:
        str: Prompt completo formatado
    """
    
    # Formata o conteúdo para inclusão no prompt
    formatted_content = format_content_for_prompt(content, discipline_name)
    
    # Gera sugestões de tópicos
    topic_suggestions = get_topic_suggestions(discipline_name)
    
    prompt_content = f"""# 🎴 Prompt Completo para Geração de Flashcards Anki

## 🎯 Objetivo
Você é um especialista em educação e flashcards do Anki. Sua tarefa é criar um conjunto completo de flashcards de alta qualidade para a disciplina de **"{discipline_name}"**, do **{semester_name.replace('-', ' ').replace('Semestre', 'semestre').capitalize()}**.

## 📚 Informações da Disciplina
- **Disciplina:** {discipline_name}
- **Período:** {semester_name.replace('-', ' ').capitalize()}
- **Total de arquivos processados:** {content['total_files']}
- **Total de conteúdo:** {content['total_characters']:,} caracteres
- **Gerado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}

## 🎯 Instruções Específicas

### 📋 Formato dos Flashcards
Use EXATAMENTE este formato para cada flashcard:

```
Pergunta: [Sua pergunta clara e concisa]
Resposta: [Resposta objetiva e completa]

---
```

### 🔍 Critérios de Qualidade
1. **Clareza:** Cada pergunta deve focar em UM conceito específico
2. **Concisão:** Respostas diretas, sem redundâncias
3. **Relevância:** Baseado exclusivamente no conteúdo fornecido abaixo
4. **Progressividade:** Do básico ao avançado
5. **Aplicabilidade:** Inclua exemplos práticos quando disponíveis no material

### 📊 Quantidade e Estratégia
- **Meta:** 20-40 flashcards no total (baseado na quantidade de conteúdo)
- **Priorize:** Conceitos que aparecem múltiplas vezes no material
- **Inclua:** Definições, procedimentos, comparações e aplicações práticas
- **Evite:** Perguntas muito específicas ou decorativas

### 🎲 Tipos de Perguntas
- **Definições:** "O que é...?", "Defina...", "Qual o conceito de...?"
- **Comparações:** "Qual a diferença entre X e Y?", "Compare..."
- **Procedimentos:** "Como fazer...?", "Quais os passos para...?"
- **Aplicações:** "Quando usar...?", "Em que situação...?", "Para que serve...?"
- **Análise:** "Por que...?", "Qual a consequência de...?", "Qual a importância de...?"

## 💡 Sugestões de Tópicos
{topic_suggestions}

## 📝 Instruções Críticas de Saída
1. **APENAS FLASHCARDS:** Forneça SOMENTE a lista de flashcards, nada mais
2. **SEM TEXTO ADICIONAL:** Não inclua introduções, explicações ou comentários
3. **FORMATO EXATO:** Use exatamente o formato especificado acima
4. **SEPARAÇÃO CLARA:** Use "---" entre cada flashcard
5. **BASE NO CONTEÚDO:** Use APENAS as informações fornecidas abaixo

---

# 📖 CONTEÚDO COMPLETO DA DISCIPLINA

{formatted_content}

---

# ⚡ INSTRUÇÕES FINAIS

Com base em TODO o conteúdo acima, crie agora os flashcards seguindo rigorosamente:
- O formato especificado
- Apenas informações do conteúdo fornecido
- Foco em conceitos principais e aplicações práticas
- Perguntas claras e respostas completas

**IMPORTANTE:** Responda APENAS com os flashcards no formato especificado, sem qualquer texto adicional."""
    
    return prompt_content

def get_topic_suggestions(discipline_name):
    """
    Gera sugestões de tópicos automaticamente baseadas no nome da disciplina.
    
    Args:
        discipline_name (str): Nome da disciplina
        
    Returns:
        str: Lista formatada de sugestões de tópicos
    """
    # Tópicos genéricos que se aplicam a qualquer disciplina
    generic_topics = [
        f'Conceitos fundamentais de {discipline_name}',
        f'Definições e terminologias importantes',
        f'Métodos e técnicas principais',
        f'Aplicações práticas e exemplos',
        f'Resolução de problemas e exercícios',
        f'Casos especiais e situações excepcionais'
    ]
    
    # Formata a lista
    formatted_topics = "\n".join([f"  - {topic}" for topic in generic_topics])
    return formatted_topics

def generate_anki_prompts(root_path):
    """
    Gera prompts completos para criar flashcards do Anki, incluindo todo o conteúdo
    dos arquivos .md das disciplinas encontradas.
    
    Args:
        root_path (str): Caminho raiz do repositório
    """
    if not os.path.exists(root_path):
        print(f"❌ Erro: O caminho '{root_path}' não existe.")
        return

    output_dir = os.path.join(root_path, "anki_prompts")
    
    # 1. Limpa os prompts antigos antes de gerar os novos
    clean_old_prompts(output_dir)

    # Garante que a pasta de prompts exista
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n🚀 Iniciando a geração de prompts completos para flashcards do Anki...")
    print(f"📁 Diretório base: {root_path}")
    print(f"🔍 Buscando pastas: anotacoes, exercicios, simulados")

    disciplines_found = 0
    prompts_generated = 0
    total_files_processed = 0

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Ignora pastas ocultas e a pasta de prompts
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != "anki_prompts"]

        # Verifica se é uma pasta de disciplina (tem pelo menos uma das pastas esperadas)
        expected_folders = ['anotacoes', 'exercicios', 'simulados']
        has_expected_folders = any(folder in dirnames for folder in expected_folders)
        
        if has_expected_folders:
            disciplines_found += 1
            
            discipline_name = os.path.basename(dirpath).replace('-', ' ').replace('_', ' ').title()
            semester_name = os.path.basename(os.path.dirname(dirpath))
            
            print(f"\n📚 Processando: {discipline_name}")
            print(f"🎓 Semestre: {semester_name}")
            
            # Extrai todo o conteúdo da disciplina
            content = extract_discipline_content(dirpath)
            total_files_processed += content['total_files']
            
            print(f"📊 Arquivos processados: {content['total_files']}")
            print(f"📏 Total de caracteres: {content['total_characters']:,}")
            
            if content['total_files'] > 0:
                # Gera o prompt completo com conteúdo
                prompt_content = generate_enhanced_prompt(
                    discipline_name, 
                    semester_name, 
                    dirpath, 
                    content
                )
                
                # Cria o arquivo com o prompt
                safe_filename = "".join(c for c in os.path.basename(dirpath) if c.isalnum() or c in ('-', '_'))
                output_filename = os.path.join(output_dir, f"{safe_filename}_anki_prompt_completo.txt")
                
                try:
                    with open(output_filename, 'w', encoding='utf-8') as f:
                        f.write(prompt_content)
                    
                    print(f"  ✅ Prompt gerado: {os.path.basename(output_filename)}")
                    print(f"  📄 Tamanho do arquivo: {len(prompt_content):,} caracteres")
                    prompts_generated += 1
                    
                except IOError as e:
                    print(f"  ❌ Erro ao criar arquivo: {e}")
            else:
                print(f"  ⚠️  Nenhum arquivo .md encontrado - prompt não gerado")
    
    # Relatório final
    print(f"\n{'='*60}")
    print(f"🎉 PROCESSO CONCLUÍDO!")
    print(f"{'='*60}")
    print(f"📚 Disciplinas encontradas: {disciplines_found}")
    print(f"📝 Prompts gerados com sucesso: {prompts_generated}")
    print(f"📄 Total de arquivos .md processados: {total_files_processed}")
    
    if prompts_generated > 0:
        print(f"📁 Localização dos prompts: {output_dir}")
        print(f"\n💡 COMO USAR:")
        print(f"   1. Abra os arquivos '_anki_prompt_completo.txt' na pasta 'anki_prompts'")
        print(f"   2. Copie TODO o conteúdo do arquivo")
        print(f"   3. Cole em sua IA preferida (ChatGPT, Claude, etc.)")
        print(f"   4. A IA criará os flashcards baseados no conteúdo real da disciplina")
        print(f"   5. Importe os flashcards gerados no Anki")
        
        print(f"\n🎯 VANTAGENS:")
        print(f"   ✅ Conteúdo completo incluído automaticamente")
        print(f"   ✅ Não precisa copiar/colar manualmente")
        print(f"   ✅ Flashcards baseados no material real")
        print(f"   ✅ Prompts otimizados para cada disciplina")
    else:
        print(f"\n⚠️  NENHUM PROMPT FOI GERADO")
        print(f"   Verifique se a estrutura está correta:")
        print(f"   📁 YYYY-N-Semestre/disciplina/anotacoes/*.md")
        print(f"   📁 YYYY-N-Semestre/disciplina/exercicios/*.md")
        print(f"   📁 YYYY-N-Semestre/disciplina/simulados/*.md")

def main():
    """
    Função principal do programa.
    """
    print("🎴 Gerador de Prompts Completos para Flashcards do Anki")
    print("📖 Versão Aprimorada - Inclui conteúdo automático dos arquivos .md")
    print("=" * 70)
    
    # Detecta o diretório atual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        generate_anki_prompts(current_dir)
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Processo interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print(f"💡 Dica: Verifique se há arquivos .md corrompidos ou com encoding especial")
        sys.exit(1)

if __name__ == "__main__":
    main()
