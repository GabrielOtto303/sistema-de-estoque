create database db_estoque;
use db_estoque;
create table categoria(
			id integer primary key auto_increment,
            nome varchar(225));
            
select * from categoria;


#1 - N > Um para muitos
#1 - 1 > Um para um
#N - N > Muito para muitos

# primary key - PK - Chave Primaria
# Chave Estrangeira - FK - foreign key

create table if not exists produto(id integer primary key auto_increment,
							nome_produto varchar(255),
                            quantidade integer ,
                            valor double,
                            chegada date,
                            validade date,
                            descricao varchar(255),
                            id_categoria integer,
                            foreign key (id_categoria) references categoria(id)
                            );
						
                        
select nome_produto, quantidade, valor, validade, descricao, id_categoria, nome from 
produto p, categoria c where  p.id_categoria = c.id;

#JOIN - conceito de juntar informações de duas ou mais tabelas

# not null = nao pode ficar em branco
create table usuarios(id int primary key auto_increment,
					usuario varchar(255) not null,
                    senha varchar (255) not null);
select*from usuarios;

alter table usuarios add unique (nome);

create table vendas(id integer primary key auto_increment,
					produto_vendido integer not null,
                    vendedor varchar(255),
                    data_venda date not null,
                    horario_venda time not null,
                    quantidade_venda integer not null,
					valor_venda double not null,
                    foreign key (produto_vendido) references produto (id));