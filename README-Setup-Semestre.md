### 🛠️ Guia de Uso: `setup-semestre.sh`

Este script é uma poderosa ferramenta de automação para configurar a estrutura de pastas do seu repositório a cada novo semestre. Pense nele como uma **fábrica de organização** que, com um único comando, monta toda a estrutura para você.

#### Por que usar?

  - **Zero Repetição:** Cansado de criar as mesmas pastas e arquivos `README.md` a cada semestre? Este script faz isso por você em segundos.
  - **Consistência Garantida:** Ele assegura que todas as pastas e arquivos sigam o padrão de nomeação `kebab-case` e a estrutura de subpastas que definimos.
  - **Totalmente Personalizável:** Você só precisa editar a lista de disciplinas no topo do arquivo. O resto é automático.

-----

### Como Usar

O processo é rápido e só precisa ser feito uma vez por semestre.

1.  **Edite as Configurações:** Abra o arquivo `setup-semestre.sh` e vá até a seção **`⚙️ CONFIGURAÇÕES DO SEMESTRE`**. Altere o ano, o número do semestre e a lista de disciplinas para as matérias que você irá cursar.

    ```bash
    # Exemplo:
    YEAR="2026"
    SEMESTER="1"

    DISCIPLINES=(
        "Estruturas de Dados Avançadas"
        "Banco de Dados II"
        "Engenharia de Software III"
        "Sistemas Operacionais"
    )
    ```

2.  **Dê Permissão de Execução:** Se for a primeira vez que você está usando o script, abra seu terminal na raiz do repositório e execute o comando abaixo para torná-lo executável:

    ```bash
    chmod +x setup-semestre.sh
    ```

3.  **Execute o Script:** Agora, para gerar toda a estrutura do novo semestre, basta rodar:

    ```bash
    ./setup-semestre.sh
    ```

Pronto\! O script criará a pasta do semestre, todas as pastas de disciplinas e as subpastas necessárias com os arquivos `README.md` e `.gitkeep` em cada uma.
