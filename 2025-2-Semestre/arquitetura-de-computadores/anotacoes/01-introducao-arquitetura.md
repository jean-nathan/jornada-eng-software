# Introdução à Arquitetura de Computadores

### O que é Arquitetura?

A arquitetura de computadores é o projeto conceitual e a estrutura operacional fundamental de um sistema de computador. É a "planta" que define como o hardware e o software interagem.

### Modelo de Von Neumann

* **Definição:** Um modelo de arquitetura de computador que se baseia em uma unidade de processamento central (CPU) e uma memória de armazenamento única.
* **Componentes Principais:**
    * **CPU (Unidade Central de Processamento):** Cérebro do computador. Contém a Unidade Lógica e Aritmética (ULA) e a Unidade de Controle (UC).
    * **Memória:** Armazena dados e instruções.
    * **Barramentos:** Canais de comunicação entre os componentes (dados, endereço e controle).
* **Ciclo de Instrução (Fetch-Decode-Execute):**
    1.  **Fetch (Busca):** A UC busca a próxima instrução da memória.
    2.  **Decode (Decodificação):** A UC interpreta a instrução.
    3.  **Execute (Execução):** A ULA executa a instrução.

### Arquitetura Harvard

* **Diferença:** Possui memórias separadas para instruções e para dados, permitindo que a busca e a execução de instruções ocorram simultaneamente.
* **Vantagem:** Aumento de performance devido ao paralelismo.
* **Uso:** Microcontroladores, processadores de sinais digitais.
