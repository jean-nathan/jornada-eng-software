# 🐳 Executando Scripts Python com Docker

Este guia mostra como executar os scripts `generate_anki_prompts.py` e `generate_mindmap.py` usando Docker, sem precisar instalar Python na sua máquina.

## 📋 Pré-requisitos

- **Docker Desktop** instalado:
  - Windows/Mac: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
  - Linux: `sudo apt install docker.io` (Ubuntu/Debian)

## 🗂️ Estrutura dos Arquivos

Certifique-se de ter esta estrutura na raiz do seu repositório:

```
📁 Repositório/
├── Dockerfile
├── generate_anki_prompts.py
├── generate_mindmap.py
├── 2024-1-Semestre/
│   ├── Programacao/
│   │   ├── anotacoes/
│   │   └── exercicios/
│   └── Matematica/
│       ├── anotacoes/
│       └── exercicios/
└── README-Docker.md
```

## 🚀 Como Executar

### 1️⃣ **Construir a Imagem Docker**

No terminal, navegue até a pasta do repositório e execute:

```bash
# Construir a imagem (só precisa fazer uma vez)
docker build -t scripts-academicos .
```

### 2️⃣ **Executar Script de Mapas Mentais**

```bash
# Gerar mapas mentais
docker run --rm -v "$(pwd):/app" scripts-academicos python generate_mindmap.py
```

### 3️⃣ **Executar Script de Prompts Anki**

```bash
# Gerar prompts para Anki
docker run --rm -v "$(pwd):/app" scripts-academicos python generate_anki_prompts.py
```

### 4️⃣ **Executar Ambos os Scripts**

```bash
# Executar os dois scripts em sequência
docker run --rm -v "$(pwd):/app" scripts-academicos bash -c "python generate_mindmap.py && python generate_anki_prompts.py"
```

## 🖥️ Comandos por Sistema Operacional

### **Windows (PowerShell)**

```powershell
# Construir imagem
docker build -t scripts-academicos .

# Mapas mentais
docker run --rm -v "${PWD}:/app" scripts-academicos python generate_mindmap.py

# Prompts Anki
docker run --rm -v "${PWD}:/app" scripts-academicos python generate_anki_prompts.py

# Ambos
docker run --rm -v "${PWD}:/app" scripts-academicos bash -c "python generate_mindmap.py && python generate_anki_prompts.py"
```

### **Windows (Command Prompt)**

```cmd
REM Construir imagem
docker build -t scripts-academicos .

REM Mapas mentais
docker run --rm -v "%cd%:/app" scripts-academicos python generate_mindmap.py

REM Prompts Anki
docker run --rm -v "%cd%:/app" scripts-academicos python generate_anki_prompts.py
```

### **Linux/macOS**

```bash
# Construir imagem
docker build -t scripts-academicos .

# Mapas mentais
docker run --rm -v "$(pwd):/app" scripts-academicos python generate_mindmap.py

# Prompts Anki
docker run --rm -v "$(pwd):/app" scripts-academicos python generate_anki_prompts.py

# Ambos
docker run --rm -v "$(pwd):/app" scripts-academicos bash -c "python generate_mindmap.py && python generate_anki_prompts.py"
```

## 🎯 Opções Avançadas

### **Modo Interativo (Debug)**

```bash
# Entrar no container para debug
docker run --rm -it -v "$(pwd):/app" scripts-academicos bash

# Dentro do container, você pode:
python generate_mindmap.py
python generate_anki_prompts.py
ls -la  # Ver arquivos gerados
exit    # Sair do container
```

### **Executar Script Específico com Argumentos**

```bash
# Se seus scripts aceitarem argumentos
docker run --rm -v "$(pwd):/app" scripts-academicos python generate_mindmap.py --verbose
```

### **Ver Logs Detalhados**

```bash
# Executar com saída detalhada
docker run --rm -v "$(pwd):/app" scripts-academicos python -u generate_mindmap.py
```

## 📝 Script de Automação

Crie um arquivo `run-scripts.sh` (Linux/Mac) ou `run-scripts.bat` (Windows):

### **Linux/Mac (run-scripts.sh):**

```bash
#!/bin/bash

echo "🐳 Iniciando execução dos scripts com Docker..."

# Construir imagem se não existir
if [[ "$(docker images -q scripts-academicos 2> /dev/null)" == "" ]]; then
    echo "📦 Construindo imagem Docker..."
    docker build -t scripts-academicos .
fi

echo "🗺️  Gerando mapas mentais..."
docker run --rm -v "$(pwd):/app" scripts-academicos python generate_mindmap.py

echo "🎴 Gerando prompts para Anki..."
docker run --rm -v "$(pwd):/app" scripts-academicos python generate_anki_prompts.py

echo "✅ Processo concluído!"
```

### **Windows (run-scripts.bat):**

```batch
@echo off
echo 🐳 Iniciando execução dos scripts com Docker...

echo 📦 Verificando imagem Docker...
docker build -t scripts-academicos .

echo 🗺️ Gerando mapas mentais...
docker run --rm -v "%cd%:/app" scripts-academicos python generate_mindmap.py

echo 🎴 Gerando prompts para Anki...
docker run --rm -v "%cd%:/app" scripts-academicos python generate_anki_prompts.py

echo ✅ Processo concluído!
pause
```

**Para usar:**

```bash
# Linux/Mac
chmod +x run-scripts.sh
./run-scripts.sh

# Windows
run-scripts.bat
```

## ❓ Solução de Problemas

### **Erro: "docker: command not found"**
- Instale o Docker Desktop
- Certifique-se que o Docker está rodando

### **Erro de permissão no Linux**
```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
# Fazer logout e login novamente
```

### **Arquivos não são salvos**
- Certifique-se de usar `-v "$(pwd):/app"`
- Verifique se está no diretório correto

### **Container não inicia**
```bash
# Verificar se a imagem foi construída
docker images | grep scripts-academicos

# Reconstruir se necessário
docker build --no-cache -t scripts-academicos .
```

### **Ver logs de erro**
```bash
# Executar sem --rm para manter o container
docker run -v "$(pwd):/app" scripts-academicos python generate_mindmap.py

# Ver logs do último container
docker logs $(docker ps -lq)
```

## 🧹 Limpeza

### **Remover imagem criada**
```bash
docker rmi scripts-academicos
```

### **Limpeza geral do Docker**
```bash
# Remove containers parados, networks não usadas, imagens órfãs
docker system prune -f
```

## 💡 Vantagens do Docker

- ✅ **Zero instalação de Python**
- ✅ **Ambiente isolado e limpo**
- ✅ **Funciona igual em qualquer OS**
- ✅ **Fácil de compartilhar**
- ✅ **Não interfere no sistema**

---
