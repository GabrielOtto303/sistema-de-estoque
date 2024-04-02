from flask import Flask, render_template, request, url_for,redirect, session
from dao import Produto, Categoria, Usuario, Vendas
import os
import datetime as dt


app = Flask(__name__)
app.secret_key = os.urandom(16)
#variável global
grupo_logado = None

def teste():
    for user in session:
        return print(user[0])

############################################LOGIN################################################################

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login_usuario():
    usuario = request.form['usuario']
    senha = request.form['senha']
    usuario_logado = Usuario(usuario,senha)

    if usuario_logado.verifica_login() == True:
        session['username'] = usuario_logado.usuario
        global grupo_logado 
        grupo_logado = usuario_logado.grupo
        return redirect(url_for('index'))
    else:
        return render_template('login.html', msg = 'login/senha inválidos')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))

###############################################INDEX#############################################################

@app.route('/')
def index():
        if 'username' in session:
            return render_template('index.html', grupo_user = grupo_logado, user = session['username'])
        return redirect(url_for('login'))

##############################################ADMNISTRATIVO######################################################

@app.route('/administrativo')
def administrativo():
    if 'username' in session and grupo_logado == 1:
        usuarios = Usuario()
        return render_template('adm.html', grupo_user = grupo_logado, lista_usuarios = usuarios.select_usuarios())
    else:
        return render_template('index.html', msg = 'somente administradores')  
 
@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    user = request.form['user']
    senha = request.form['senha']
    grupo = request.form['grupo']
    obj_usuario = Usuario(user, senha, grupo)
    msg = obj_usuario.cadastrar_usuario()
    return render_template('adm.html', msg = msg, lista_usuarios = Usuario().select_usuarios())

@app.route('/excluir_usuario', methods = ['POST'])
def excluir_usuario():
    nome_usuario = request.form['nome_usuario']
    usuario = Usuario()
    usuario.excluir_usuario(nome_usuario)
    usuario.select_usuarios()
    return render_template('adm.html',lista_usuarios = usuario.select_usuarios() ,msg = 'excluido')

###########################################PRODUTO###############################################################

@app.route('/produtos')
def produtos():
    if 'username' in session:
        produto_objeto = Produto()
        return render_template('produtos.html', grupo_user = grupo_logado, lista_produto = produto_objeto.select_todos_produtos())
    return redirect(url_for('login'))

@app.route('/produtos', methods = ['POST'])
def excluir_produto():
    id_excluido = request.form['id_produto']
    msg = 'produto excluido'
    produto_objeto = Produto()
    produto_objeto.excluir_produto(id_excluido)

    return render_template('produtos.html', msg = msg, grupo_user = grupo_logado, lista_produto = produto_objeto.select_todos_produtos())

@app.route('/cadastro')
def cadastro_produtos():
    if 'username' in session:
        categoria = Categoria(None,None)
        return render_template('cadastrar_produto.html', grupo_user = grupo_logado, lista_categoria = categoria.select_todas_categorias())
    return redirect(url_for('login'))

@app.route('/cadastro_produto', methods=['POST'])
def cadastrar_produtos():
    categoria = Categoria(None,None)

    try:
        msg = "salvo"
        nome = request.form['nome_produto']
        categoria_produto = request.form['categoria_produto']
        quantidade = request.form['quantidade_produto']
        valor = request.form['valor_produto']
        chegada = request.form['chegada_produto']
        validade = request.form['validade_produto']
        descricao = request.form['descricao_produto']

        produto_objeto = Produto(None,nome, quantidade, valor, chegada, validade, descricao, categoria_produto)
        produto_objeto.insere_produto()

        return render_template('produtos.html', msg = msg, grupo_user = grupo_logado, lista_produto = Produto().select_todos_produtos(), lista_categoria = categoria.select_todas_categorias())
    
    except:
        msg = 'categoria inválida'
        return render_template('cadastrar_produto.html', msg = msg, lista_produto = Produto().select_todos_produtos(), lista_categoria = categoria.select_todas_categorias())

@app.route('/pesquisa_produtos', methods = ['POST'])
def buscar_produto():
    produto_objeto = Produto()
    nome_buscado = request.form['nome_pesquisado']
    return render_template('produtos.html', lista_produto = produto_objeto.busca_produto(nome_buscado))

#########################################CATEGORIA###############################################################

@app.route('/categoria')
def categoria():
    if 'username' in session:
        categoria_objeto = Categoria(None,None)
        return render_template('categoria.html', grupo_user = grupo_logado, lista = categoria_objeto.select_todas_categorias())
    return redirect(url_for('login'))

@app.route('/cadastro_categoria')
def abre_cadastro_categoria():
    if 'username' in session:
        return render_template('categoria.html')
    return redirect(url_for('login'))

@app.route('/cadasto', methods=['POST'])
def cadastrar_categoria():
    msg = 'salvo'
    categoria = request.form['categoria']
    categoria_objeto = Categoria(None,categoria)
    categoria_objeto.insert_categoria()     
    return render_template('categoria.html', msg = msg, lista = Categoria(None,None).select_todas_categorias())

##########################################VENDAS#################################################################

@app.route('/registro')
def registro_vendas():
    if 'username' in session:
        return render_template('registro_vendas.html', grupo_user = grupo_logado, vendas_periodo = Vendas().select_registros())
    return redirect(url_for('login'))

@app.route('/vendas')
def vendas():
    if 'username' in session:
        obj_produto = Produto()
        return render_template('vendas.html', grupo_user = grupo_logado, produto = obj_produto)
    return redirect(url_for('login'))

@app.route('/pesquisa_produtos_vandas', methods = ['POST'])
def pesquisa_venda():
    codigo = request.form['codigo_pesquisado']
    obj_produto = Produto().busca_produto_id(codigo)
    return render_template('vendas.html', produtos = obj_produto, grupo_user = grupo_logado)

@app.route('/atualizar', methods=['POST'])
def realiza_venda():
    id = request.form['id']
    quantidade_estoque = int(request.form['quantidade_em_estoque'])
    quantidade_vendida = int(request.form['quantidade_vendidos'])
    user = session['username']
    tempo = dt.datetime.now()
    horario = tempo.time()
    data = tempo.date()
    valor = float(request.form['valor'])
    if quantidade_estoque >= quantidade_vendida and quantidade_vendida > 0:
        quantidade = quantidade_estoque - quantidade_vendida
        valor_venda = valor * quantidade_vendida
        obj_produto = Produto()
        objt_venda = Vendas(None, user, id, quantidade_vendida, valor_venda, data, horario)
        obj_produto.atualiza_quantidade(id, quantidade)
        objt_venda.registra_vendas()
        if grupo_logado == 1:
            return redirect(url_for('registro_vendas'))
        return render_template('vendas.html', msg = 'realizada com sucesso', grupo_user = grupo_logado)
    return render_template('vendas.html', msg = 'produtos insuficientes ou igual a zero', grupo_user = grupo_logado)

@app.route('/pesquisa_periodo', methods=['POST'])
def pesquisa_periodo():
    vendas = Vendas()
    data_inicial = request.form['data_inicial']
    data_final = request.form['data_final']
    vendas_periodo = vendas.pesquisar_periodo(data_inicial,data_final)
    valor_periodo = vendas.valor_por_periodo(data_inicial, data_final)
    for valor_tratado in valor_periodo:
        pass
    return render_template('registro_vendas.html', grupo_user = grupo_logado, vendas_periodo = vendas_periodo, valor_final = valor_tratado) 

#################################################################################################################

@app.template_filter()
def formata_valor(valor_html):
    try:
        valor = float(valor_html)
        return f'{valor:,.2f}'
    except:
        return ''

@app.template_filter()
def formata_data(data_html):
    return data_html.strftime('%d/%m/%Y')

app.run(debug=True)