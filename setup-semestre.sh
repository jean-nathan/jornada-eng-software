#!/bin/bash

# ==========================================================
# Script de Configuração de Novo Semestre
# Versão: 1.0
# Descrição: Cria a estrutura de pastas e arquivos para um
# novo semestre de estudos de Engenharia de Software.
# ==========================================================

# ==========================================================
# ⚙️  CONFIGURAÇÕES DO SEMESTRE (EDITAR AQUI!)
# ==========================================================
YEAR="2025"
SEMESTER="2"

DISCIPLINES=(
    "Introdução à Programação de Computadores"
    "Arquitetura de Computadores"
    "Requisitos de Sistemas"
    "Desenv. Web em Html5, Css, Javascript e Php"
    "Paradigmas de Linguagens de Programação em Python"
)
# ==========================================================

SEMESTER_FOLDER="${YEAR}-${SEMESTER}-Semestre"

SUBFOLDERS=(
    "anotacoes"
    "exercicios"
    "simulados"
    "anki"
)

# ==========================================================
# Funções Auxiliares
# ==========================================================

# Converte o nome da disciplina para kebab-case
slugify_discipline_name() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -d '()'
}

# Cria o README do semestre
create_semester_readme() {
    local semester_path=$1
    cat << EOF > "${semester_path}/README.md"
# ${YEAR}-${SEMESTER}-Semestre

Repositório de estudos e materiais do ${SEMESTER}º Semestre de ${YEAR} da faculdade de Engenharia de Software.

---

### 📝 Disciplinas

$(for d in "${DISCIPLINES[@]}"; do slugged_name=$(slugify_discipline_name "$d"); echo "- [\`$d\`](./$slugged_name/)"; done)

---

### 💡 Lembrete

Use as subpastas para manter a organização: \`anotacoes/\`, \`exercicios/\`, \`simulados/\` e \`anki/\`.

Bons estudos!
EOF
}

# Cria o README da disciplina
create_discipline_readme() {
    local discipline_path=$1
    local discipline_name=$2
    cat << EOF > "${discipline_path}/README.md"
# 📝 Anotações de ${discipline_name}

Material de estudo para a disciplina de **${discipline_name}** do ${SEMESTER}º Semestre.

---

### 📂 Conteúdo

- [Anotações e Resumos](anotacoes/)
- [Listas e Exercícios](exercicios/)
- [Simulados e Provas](simulados/)
- [Decks do Anki](anki/)

---

### 🎯 Objetivo

Manter todo o material da disciplina organizado para facilitar a revisão e o aprendizado contínuo.
EOF
}

# ==========================================================
# 🚀 Execução do Script
# ==========================================================

echo "=========================================================="
echo "    Iniciando a criação da estrutura de pastas para o"
echo "        ${SEMESTER}º Semestre de ${YEAR}"
echo "=========================================================="

if [ -d "$SEMESTER_FOLDER" ]; then
    read -p "A pasta '$SEMESTER_FOLDER' já existe. Deseja continuar? (Isso pode sobrescrever arquivos) [s/N] " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Operação cancelada."
        exit 1
    fi
fi

# Cria a pasta do semestre
mkdir -p "${SEMESTER_FOLDER}"
echo "📦 Pasta do semestre criada: ${SEMESTER_FOLDER}/"

# Cria as pastas de disciplinas e subpastas
for discipline in "${DISCIPLINES[@]}"; do
    slugged_name=$(slugify_discipline_name "$discipline")
    DISCIPLINE_PATH="${SEMESTER_FOLDER}/${slugged_name}"
    mkdir -p "${DISCIPLINE_PATH}"
    echo "  └─ Criando disciplina: ${slugged_name}/"
    
    create_discipline_readme "${DISCIPLINE_PATH}" "$discipline"
    
    for subfolder in "${SUBFOLDERS[@]}"; do
        SUBFOLDER_PATH="${DISCIPLINE_PATH}/${subfolder}"
        mkdir -p "${SUBFOLDER_PATH}"
        touch "${SUBFOLDER_PATH}/.gitkeep"
    done
done

# Cria o README principal do semestre
create_semester_readme "${SEMESTER_FOLDER}"

echo "✅ Estrutura criada com sucesso!"
echo "Agora você pode começar a adicionar seus estudos neste semestre."
