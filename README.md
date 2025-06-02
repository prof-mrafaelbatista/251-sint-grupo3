# Projeto para conclusão do P1 de messias

## Descrição do Projeto

Este projeto foi desenvolvido como trabalho final do 1º Período para a disciplina de Introdução à Programação com Python com professor Messias do curso de Sistemas para Internet da Uniesp. O objetivo foi criar um site informativo e interativo utilizando Python, Flask e o Bootstrap para o frontend. O site aborda os fundamentos da programação em Python, inclui uma seção sobre a equipe de desenvolvimento, um dicionário de termos técnicos gerenciável e uma funcionalidade de "Tira-Dúvidas" integrada com a API do Google Gemini.

## Membros da Euquipe

*   **Nome:** Hrasam
    *   **GitHub:** [https://github.com/hrasam01](https://github.com/hrasam01)

## Funcionalidades Principais

1.  **Conteúdo Educacional:**
    *   Apresentação de conceitos, aplicações e exemplos de código para os seguintes tópicos de Python:
        *   Estruturas de Seleção
        *   Estruturas de Repetição
        *   Vetores e Matrizes
        *   Funções e Procedimentos
        *   Tratamentos de Exceção
2.  **Página da Equipe:**
    *   Informações sobre os desenvolvedores do projeto.
3.  **Dicionário de Termos:**
    *   **Visualização:** Lista todos os termos e suas definições.
    *   **Adicionar:** Permite inserir novos termos e definições.
    *   **Alterar:** Permite modificar termos e definições existentes.
    *   **Deletar:** Permite remover termos do dicionário.
    *   Os dados são persistidos em um arquivo `dicionario.json`.
4.  **Tira-Dúvidas com IA (Gemini API):**
    *   Seção onde os usuários podem submeter perguntas sobre Python e receber respostas geradas pela API do Google Gemini.
5.  **Navegação e Interface:**
    *   Interface de usuário clara e amigável, construída com Bootstrap 5.
    *   Navegação intuitiva entre as seções do site.

## Tecnologias Utilizadas

*   **Backend:**
    *   Python 3.x
    *   Flask (Microframework web)
*   **Frontend:**
    *   HTML5
    *   CSS3 (com Bootstrap 5)
    *   Bootstrap 5
*   **Persistência de Dados:**
    *   Arquivo JSON (`dicionario.json`) para o Dicionário de Termos.
*   **APIs Externas:**
    *   Google Gemini API (para a funcionalidade "Tirar Dúvidas")
*   **Outras bibliotecas Python:**
    *   `google-generativeai` (para interagir com a API do Gemini)
    *   `python-dotenv` (para gerenciamento de variáveis de ambiente)

## Estrutura do Projeto

.
├── app.py
├── dicionario.json 
├── README.md
├── requirements.txt
├── static
│   ├── css
│   │   └── style.css
│   ├── img
│   │   └── bomb.jpg
│   └── js
└── templates
    ├── adicionar_termo.html
    ├── alterar_termo.html
    ├── base.html
    ├── dicionario.html
    ├── equipe.html
    ├── index.html
    └── tira_duvidas.html


## Configuração e Instalação

1.  **Pré-requisitos:**
    *   Python 3.7 ou superior
    *   pip (gerenciador de pacotes Python)

2.  **Clonar o Repositório (se aplicável):**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO_GIT]
    cd [NOME_DA_PASTA_DO_PROJETO]
    ```
    Ou simplesmente baixe e descompacte os arquivos do projeto.

3.  **Criar e Ativar um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv .venv
    # No Windows:
    .\.venv\Scripts\activate
    # No macOS/Linux:
    source .venv/bin/activate
    ```

4.  **Instalar as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configurar Variáveis de Ambiente:**
    *   Crie um arquivo `.env`:
        ```bash
        touch .env
        ```
    *   Edite o arquivo `.env` e adicione sua API Key do Google Gemini:
        ```
        GEMINI_API_KEY="SUA_API_KEY_AQUI"
        ```
    *   **IMPORTANTE:** Não inclua seu arquivo `.env` com a chave real em repositórios Git públicos. O arquivo `.gitignore` (se você usar Git) deve listar `.env`.

## Como Executar a Aplicação

1.  Certifique-se de que o ambiente virtual está ativado e as variáveis de ambiente estão configuradas.
2.  Execute o arquivo principal da aplicação:
    ```bash
    python app.py
    ```
3.  Abra seu navegador e acesse: `http://127.0.0.1:5000/`

## Possíveis Melhorias Futuras

*   Implementar autenticação de usuários para gerenciar o dicionário.
*   Utilizar um banco de dados SQL (ex: SQLite, PostgreSQL) em vez de arquivo JSON para maior robustez.
*   Adicionar mais tópicos de Python.
*   Melhorar a interface do usuário com mais interatividade (ex: AJAX para o "Tira-Dúvidas").
*   Testes automatizados.

---

Hrasam Hussem G. Maneiro - 2025.1

