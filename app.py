from flask import Flask, render_template, request, redirect, url_for
import os
import json
import google.generativeai as genai


app = Flask(__name__)

try:
    API_KEY_GEMINI = os.getenv("GEMINI_API_KEY")
    if not API_KEY_GEMINI:
        print("ERRO: Variável de ambiente GEMINI_API_KEY não definida. A API do Gemini não será configurada.")
        model = None # Garante que o modelo é None se a chave não for encontrada
    else:
        # Apenas configure se a chave existir
        print("INFO: Variável de ambiente GEMINI_API_KEY encontrada. Configurando a API do Gemini...")
        genai.configure(api_key=API_KEY_GEMINI)
        model = genai.GenerativeModel('gemini-pro')
        print("INFO: API do Gemini configurada com sucesso.")
except Exception as e:
    print(f"ERRO CRÍTICO ao configurar a API do Gemini: {e}")
    model = None # Define model como None se a configuração falhar


DICIONARIO_ARQUIVO = 'dicionario.json'

#funções abaixo
def carregar_termos():
    if not os.path.exists(DICIONARIO_ARQUIVO):
        return [] # Retorna lista vazia se o arquivo não existir
    try:
        with open(DICIONARIO_ARQUIVO, 'r', encoding='utf-8') as f:
            termos = json.load(f)
            # Garantir que seja sempre uma lista (caso o arquivo esteja vazio ou com JSON inválido que não seja uma lista)
            if not isinstance(termos, list):
                return []
            return termos
    except json.JSONDecodeError: # Trata o caso de JSON malformado ou arquivo vazio
        return []
    except FileNotFoundError: # Segurança extra, embora o os.path.exists já cubra
        return []

def salvar_termos(termos):
    with open(DICIONARIO_ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(termos, f, ensure_ascii=False, indent=2) # indent=2 para formatação legível


#rotas abaixo
@app.route('/')
def index():
    return render_template('index.html', page_title='pagina inicial')

@app.route('/equipe')
def equipe():
    membros_equipe = [
        {'nome': 'Hrasam Hussem', 'github': 'https://github.com/hrasam01', 'foto': 'img/bomb.jpg'},
    ]
    return render_template('equipe.html', page_title='Nossa Equipe', equipe=membros_equipe)

@app.route('/dicionario')
def dicionario():
    termos = carregar_termos()
    return render_template('dicionario.html', page_title='Dicionário de Termos', termos=termos)

@app.route('/dicionario/adicionar', methods=['GET', 'POST'])
def adicionar_termo():
    if request.method == 'POST':
        termo_novo = request.form['termo'].strip()
        definicao_nova = request.form['definicao'].strip()

        if termo_novo and definicao_nova:
            termos = carregar_termos()
            # Verifica se o termo já existe (ignorando maiúsculas/minúsculas)
            if not any(t['termo'].lower() == termo_novo.lower() for t in termos):
                termos.append({'termo': termo_novo, 'definicao': definicao_nova})
                # Ordenar alfabeticamente antes de salvar (opcional, mas bom para consistência)
                termos.sort(key=lambda x: x['termo'].lower())
                salvar_termos(termos)
                # flash('Termo adicionado com sucesso!', 'success') # Exemplo de flash message
            else:
                # flash(f"O termo '{termo_novo}' já existe.", 'warning') # Exemplo
                # Para passar a mensagem de erro para o template sem flash:
                return render_template('adicionar_termo.html',
                                       page_title='Adicionar Novo Termo',
                                       erro=f"O termo '{termo_novo}' já existe.",
                                       termo_preenchido=termo_novo, # Para repopular o formulário
                                       definicao_preenchida=definicao_nova)
            return redirect(url_for('dicionario'))
    return render_template('adicionar_termo.html', page_title='Adicionar Novo Termo')

@app.route('/dicionario/alterar/<path:termo_original>', methods=['GET', 'POST'])
def alterar_termo(termo_original):
    termos = carregar_termos()
    termo_encontrado = None
    index_termo = -1

    for i, t in enumerate(termos):
        if t['termo'] == termo_original: # Busca pelo termo original
            termo_encontrado = t
            index_termo = i
            break

    if not termo_encontrado:
        # flash('Termo não encontrado para alteração.', 'danger')
        return redirect(url_for('dicionario'))

    if request.method == 'POST':
        novo_termo_str = request.form['termo'].strip()
        nova_definicao_str = request.form['definicao'].strip()

        if novo_termo_str and nova_definicao_str:
            # Verifica se o novo nome do termo já existe EM OUTRO REGISTRO
            # (ou seja, não é o próprio termo que estamos editando, caso o nome não mude)
            if novo_termo_str.lower() != termo_original.lower() and \
               any(t['termo'].lower() == novo_termo_str.lower() for i, t in enumerate(termos) if i != index_termo):
                # flash(f"O nome de termo '{novo_termo_str}' já está em uso por outro item.", 'danger')
                return render_template('alterar_termo.html',
                                       page_title='Alterar Termo',
                                       termo_item=termo_encontrado, # Mantém os dados originais no form
                                       erro=f"O nome de termo '{novo_termo_str}' já está em uso por outro item.")

            # Atualiza o termo na lista
            termos[index_termo]['termo'] = novo_termo_str
            termos[index_termo]['definicao'] = nova_definicao_str
            termos.sort(key=lambda x: x['termo'].lower()) # Reordenar se o nome mudou
            salvar_termos(termos)
            # flash('Termo alterado com sucesso!', 'success')
            return redirect(url_for('dicionario'))
        else:
            # flash('Termo e definição não podem ser vazios.', 'warning')
            return render_template('alterar_termo.html',
                                   page_title='Alterar Termo',
                                   termo_item=termo_encontrado,
                                   erro="Termo e definição não podem ser vazios.")


    return render_template('alterar_termo.html', page_title='Alterar Termo', termo_item=termo_encontrado)

@app.route('/dicionario/deletar/<path:termo_original>', methods=['POST']) # Usar POST para deleção
def deletar_termo(termo_original):
    termos = carregar_termos()
    # Cria uma nova lista sem o termo a ser deletado
    # É importante comparar de forma case-sensitive aqui para garantir que o termo correto seja deletado
    # ou normalizar se a intenção for case-insensitive (mas a URL já é case-sensitive)
    termos_atualizados = [t for t in termos if t['termo'] != termo_original]

    if len(termos_atualizados) < len(termos): # Se algum termo foi removido
        salvar_termos(termos_atualizados)
        # flash('Termo deletado com sucesso!', 'success')
    else:
        # flash('Termo não encontrado para deleção.', 'warning')
        pass
    return redirect(url_for('dicionario'))

@app.route('/tira-duvidas', methods=['GET', 'POST'])
def tira_duvidas():
    resposta_gemini = None
    pergunta_usuario = ""
    erro_api = None

    if not model: # Verifica se o modelo foi inicializado corretamente
        erro_api = "A API do Gemini não pôde ser inicializada. Verifique a configuração da chave API."
        return render_template('tira_duvidas.html', page_title='Tirar Dúvidas', erro_api=erro_api)

    if request.method == 'POST':
        pergunta_usuario = request.form['pergunta']
        if pergunta_usuario:
            try:
                # Adicionando um contexto simples para o Gemini focar em Python, se desejado
                # prompt_completo = f"Contexto: Fundamentos de programação em Python.\n\nPergunta: {pergunta_usuario}\n\nResposta:"
                # response = model.generate_content(prompt_completo)
                # Ou simplesmente a pergunta direta:
                response = model.generate_content(pergunta_usuario)
                resposta_gemini = response.text
            except Exception as e:
                print(f"Erro ao chamar a API do Gemini: {e}")
                erro_api = f"Ocorreu um erro ao tentar obter a resposta: {e}"
                # Você pode querer inspecionar response.prompt_feedback se houver bloqueios
                try:
                    if response and response.prompt_feedback:
                        erro_api += f" (Feedback do Prompt: {response.prompt_feedback})"
                except: # pode dar erro se response nao existir
                    pass


    return render_template('tira_duvidas.html',
                           page_title='Tirar Dúvidas',
                           pergunta=pergunta_usuario,
                           resposta=resposta_gemini,
                           erro_api=erro_api)

if __name__ == '__main__':
    app.run(debug=True)
