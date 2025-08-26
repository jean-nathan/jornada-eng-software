# 📚 Repositório de Estudos - Engenharia de Software

Este é o meu repositório pessoal de estudos para a graduação em Engenharia de Software.

O objetivo é organizar de forma clara e escalável todo o material didático, incluindo anotações de aula, exercícios, simulados e flashcards do Anki.

-----

### 🗂️ Estrutura de Organização

A estrutura segue a analogia de uma biblioteca:

  - **Pastas de Semestre (`YYYY-N-Semestre/`)**: Estantes dedicadas a cada semestre.
  - **Pastas de Disciplina (`nome-da-disciplina/`)**: Prateleiras para cada matéria.
  - **Subpastas de Conteúdo (`anotacoes/`, `exercicios/`, etc.)**: Caixas organizadoras dentro de cada prateleira.

-----

### 🚀 Automação para Turbinar seus Estudos

Este repositório não é apenas um lugar para guardar arquivos; ele é uma **ferramenta de estudo inteligente**. Contamos com scripts poderosos para otimizar seu tempo e a qualidade do seu aprendizado.

#### 🛠️ Configuração de Semestre (`setup-semestre.sh`)

Este é o seu modelo de semestre. Ele automatiza a criação de toda a estrutura de pastas e arquivos `README.md` para um novo período letivo. Basta editar as disciplinas no script e executá-lo para que todo o seu novo semestre seja configurado em segundos.

**Para instruções completas de como usar este script, consulte o guia:**

  - [Guia de Uso do `setup-semestre.sh`](./README-Setup-Semestre.md)

#### 🗺️ Mapas Mentais (via `generate_mindmap.py`)

Pense no mapa mental como um **mapa da sua biblioteca**. Em vez de procurar em cada prateleira, você tem uma visão panorâmica de todo o seu conhecimento. Ele transforma sua hierarquia de pastas em um diagrama visual e interativo.

#### 🧠 Prompts para Flashcards (via `generate_anki_prompts.py`)

A IA é seu professor particular. Mas para que ela seja eficaz, você precisa dar as instruções certas. Este script age como um **assistente de estudo pessoal**, preparando o prompt ideal para você. Ele percorre suas anotações e exercícios, e gera um texto completo e formatado, pronto para ser copiado e colado em uma IA para criar flashcards de alta qualidade.

-----

### 🐳 Como Executar os Scripts com Docker

Para tornar a execução dos scripts ainda mais simples e universal (sem a necessidade de instalar Python e suas dependências diretamente na sua máquina), utilizamos o **Docker**.

Basta ter o Docker Desktop instalado, e todos os scripts funcionarão da mesma forma em qualquer sistema operacional (Windows, macOS ou Linux).

**Para saber como construir a imagem e executar os scripts, consulte o guia completo:**

  - [Guia de Uso do Docker](./README-Docker.md)

Com essa abordagem, seu repositório se torna um verdadeiro ambiente de estudo automatizado e portátil, pronto para te acompanhar em toda a sua jornada acadêmica.
