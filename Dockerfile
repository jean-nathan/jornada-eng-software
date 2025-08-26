# Dockerfile para Scripts Python Acadêmicos
# Imagem base com Python otimizada e leve
FROM python:3.11-slim

# Metadados do container
LABEL maintainer="seu-email@exemplo.com"
LABEL description="Container para executar scripts de geração de mapas mentais e prompts Anki"
LABEL version="1.0"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Atualiza sistema e instala dependências necessárias
RUN apt-get update && apt-get install -y \
  --no-install-recommends \
  git \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean

# Define diretório de trabalho
WORKDIR /app

# Copia apenas os scripts necessários primeiro (otimização de cache)
COPY generate_anki_prompts.py generate_mindmap.py ./

# Copia todo o conteúdo do repositório
COPY . .

# CORREÇÃO: Não criar usuário específico para evitar problemas de permissão
# O container rodará como root, mas isso é seguro pois é isolado

# Define permissões corretas
RUN chmod +x generate_anki_prompts.py generate_mindmap.py

# Comando padrão (pode ser sobrescrito)
CMD ["python", "--version"]
