from bancodado import BancoDado
import crypto

class Categoria:
    def __init__(self,id,nome):
        self.id = id
        self.nome_categoria = nome
        
    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome_categoria

    def insert_categoria(self):
        banco = BancoDado()
        conexao = banco.get_conexao()

        COMANDO_INSERT = 'INSERT INTO categoria (nome) values (%s)'
        valor = (self.nome_categoria,)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_INSERT,valor)
        conexao.commit()

    def select_todas_categorias(self):
        banco = BancoDado()
        conexao = banco.get_conexao()

        COMANDO_SELECT = 'SELECT id, nome FROM categoria ORDER BY nome'
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT)
        
        lista_categoria = []
        for x in manipulador_sql.fetchall():
            categoria = Categoria(id = x[0],nome = x[1])
            lista_categoria.append(categoria)

        return lista_categoria

class Produto:
    def __init__(self,id=None, nome=None, quantidade=None,  valor=None, chegada=None, validade=None,
    descricao=None, categoria=None):
        self.id_produto = id
        self.nome_produto = nome
        self.quantidade_produto = quantidade
        self.valor_produto = valor
        self.descricao_produto = descricao
        self.chegada_produto = chegada
        self.validade_produto = validade 
        self.categoria_produto = categoria

    def insere_produto(self):
        banco = BancoDado()
        conexao = banco.get_conexao()

        if self.validade_produto != '':
            COMANDO_INSERT = 'INSERT INTO produto (nome_produto, quantidade, valor, chegada, validade, descricao, id_categoria) VALUES (%s, %s, %s, %s, %s, %s,%s)'
            valores = (self.nome_produto, self.quantidade_produto, self.valor_produto, self.chegada_produto, self.validade_produto, self.descricao_produto, self.categoria_produto)

        else:
            COMANDO_INSERT = 'INSERT INTO produto (nome_produto, quantidade, valor, chegada, descricao, id_categoria) VALUES (%s,%s,%s,%s,%s,%s)'
            valores = (self.nome_produto, self.quantidade_produto, self.valor_produto, self.chegada_produto, self.descricao_produto, self.categoria_produto)

        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_INSERT, valores)
        conexao.commit()

    def select_todos_produtos(self):
        banco = BancoDado()
        conexao = banco.get_conexao()

        COMANDO_SELECT = 'SELECT p.id, nome_produto, quantidade, valor, chegada, validade, descricao, id_categoria, nome FROM produto p, categoria c WHERE p.id_categoria = c.id;'
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT)
        
        lista_produto = []

        for produto in manipulador_sql.fetchall():
            categoria_objeto = Categoria(produto[7],produto[8])
            objeto = Produto(id=produto[0], nome=produto[1],quantidade=produto[2], valor=produto[3], chegada=produto[4],
                    validade=produto[5], descricao=produto[6], categoria=categoria_objeto)
            lista_produto.append(objeto)
        return lista_produto

    def busca_produto(self, nome_p):
        banco = BancoDado()
        conexao = banco.get_conexao()

        COMANDO_SELECT = 'SELECT p.id, nome_produto, quantidade, valor, chegada, validade, descricao, id_categoria, nome FROM produto p, categoria c  WHERE  p.id_categoria = c.id AND nome_produto = %s'
        manipulador_sql = conexao.cursor()
        nome_buscado = (nome_p,)
        manipulador_sql.execute(COMANDO_SELECT, nome_buscado)
        
        lista_produto = []

        for produto in manipulador_sql.fetchall():
            categoria_objeto = Categoria(produto[7],produto[8])
            objeto = Produto(id=produto[0], nome=produto[1],quantidade=produto[2], valor=produto[3], chegada=produto[4],
                    validade=produto[5], descricao=produto[6], categoria=categoria_objeto)
            lista_produto.append(objeto)
            
        return lista_produto

    def excluir_produto(self, id_produto):
        banco = BancoDado()
        conexao = banco.get_conexao()

        COMANDO_DELETE = 'DELETE FROM produto where id = %s'
        valor = (id_produto,)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_DELETE, valor)
        conexao.commit()

    def  busca_produto_id(self, id):
        banco = BancoDado()
        conexao = banco.get_conexao()

        COMANDO_SELECT = 'SELECT p.id, nome_produto, quantidade, valor, chegada, validade, descricao, id_categoria, nome FROM produto p, categoria c WHERE id_categoria = c.id AND p.id = %s'
        valor =  (id,)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT, valor)

        lista_produto = []

        for produto in manipulador_sql.fetchall():
            categoria_objeto = Categoria(produto[7],produto[8])
            objeto = Produto(id=produto[0], nome=produto[1],quantidade=produto[2], valor=produto[3], chegada=produto[4],
                    validade=produto[5], descricao=produto[6], categoria=categoria_objeto)
            lista_produto.append(objeto)
            
        return lista_produto

    def atualiza_quantidade(self, id, quantidade_vendida):
        banco = BancoDado()
        conexao = banco.get_conexao()

        COMANDO_UPDATE = 'UPDATE produto SET quantidade = %s WHERE id = %s'
        value = (quantidade_vendida, id)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_UPDATE,value)
        conexao.commit()

class Vendas:
    def __init__(self, id = None, usuario = None, produto_id = None, quantidade = None, valor = None, data = None, horario = None):
        self.id_venda = id
        self.vendedor = usuario
        self.produto_venda = produto_id
        self.quantidade_venda = quantidade
        self.valor_venda = valor
        self.data_venda = data
        self.horario_venda = horario

    def registra_vendas(self):
        banco = BancoDado()
        conexao = banco.get_conexao()

        COMANDO_INSERT = 'INSERT INTO vendas (produto_vendido, vendedor, data_venda, horario_venda, quantidade_venda, valor_venda) VALUES (%s, %s, %s, %s, %s, %s)'
        values = (self.produto_venda, self.vendedor, self.data_venda, self.horario_venda, self.quantidade_venda, self.valor_venda)

        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_INSERT,values)
        conexao.commit()

    def select_registros(self):
        banco = BancoDado()
        conexao = banco.get_conexao()

        COMANDO_SELECT = 'SELECT nome_produto, nome, vendedor, data_venda, horario_venda, quantidade_venda, valor_venda, v.id FROM vendas v, produto p, categoria c WHERE p.id = v.produto_vendido AND c.id = id_categoria'

        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT)
        lista_venda = []

        for venda in manipulador_sql.fetchall():
            categoria = Categoria(None, venda[1])
            produto = Produto(None, venda[0], None, venda[6], None, None, None, categoria = categoria)
            objeto = Vendas(id = venda[7], usuario = venda[2], produto_id = produto, quantidade = venda[5], valor = venda[6], data = venda[3], horario = venda[4])
            lista_venda.append(objeto)

        return lista_venda

    def pesquisar_periodo(self, data_inicial, data_final):
        banco = BancoDado()
        conexao = banco.get_conexao()

        COMANDO_SELECT = 'SELECT nome_produto, nome, vendedor, data_venda, horario_venda, quantidade_venda, valor_venda, v.id FROM vendas v, produto p, categoria c WHERE p.id = v.produto_vendido AND c.id = id_categoria and data_venda between %s and %s'
        values = (data_inicial, data_final)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT,values)
        lista_venda = []
        
        for venda in manipulador_sql.fetchall():
            categoria = Categoria(None, venda[1])
            produto = Produto(None, venda[0], None, venda[6], None, None, None, categoria = categoria)
            objeto = Vendas(id = venda[7], usuario = venda[2], produto_id = produto, quantidade = venda[5], valor = venda[6], data = venda[3], horario = venda[4])
            lista_venda.append(objeto)

        return lista_venda

    def valor_por_periodo(self, data_inicial, data_final):
        banco = BancoDado()
        conexao = banco.get_conexao()

        COMANDO_SELECT = 'SELECT sum(valor_venda) FROM vendas WHERE data_venda BETWEEN %s AND %s'
        values = (data_inicial, data_final)

        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT, values)
        
        valor_final = []
        for valor in manipulador_sql.fetchall():
            valor_final.append(valor)
        return valor_final


class Usuario:
    def __init__(self, user = None, senha = None, grupo = None):
        self.usuario = user
        self.senha = senha
        self.grupo = grupo

    def cadastrar_usuario(self):
        banco = BancoDado()
        conexao = banco.get_conexao()

        try:
            COMANDO_INSERT = 'INSERT INTO usuarios (usuario, senha, grupo) values (%s,%s, %s)'
            senha_cryptada = crypto.cryptar(self.senha)
            values = (self.usuario, senha_cryptada, self.grupo)

            manipulador_sql = conexao.cursor()
            manipulador_sql.execute(COMANDO_INSERT,values)
            conexao.commit()
            return 'cadastrado com sucesso'
        except:
            return 'usuário já existe'

    def verifica_login(self):
        banco = BancoDado()
        conexao = banco.get_conexao()

        COMANDO_SELECT = 'SELECT * FROM usuarios WHERE usuario LIKE BINARY %s'
        values = (self.usuario,)
        manipulador_SQL = conexao.cursor()
        manipulador_SQL.execute(COMANDO_SELECT, values)

        obj_banco = manipulador_SQL.fetchone()

        if obj_banco != None:
            resultado = crypto.valida_senha(self.senha, obj_banco[2])
            self.grupo = obj_banco[3]
            return resultado
        else:
            return False

    def select_usuarios(self):
        banco = BancoDado()
        conexao = banco.get_conexao()

        COMANDO_SELECT = 'SELECT usuario, grupo FROM usuarios ORDER BY usuario'
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT)
        
        lista_usuario = []

        for x in manipulador_sql.fetchall():
            usuario = Usuario(user = x[0] , grupo = x[1])
            lista_usuario.append(usuario)

        return lista_usuario

    def excluir_usuario(self, nome_usuario):
        banco = BancoDado()
        conexao = banco.get_conexao()

        COMANDO_DELETE = 'DELETE FROM usuarios WHERE usuario LIKE BINARY %s'
        value = (nome_usuario,)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_DELETE,value)
        conexao.commit()

