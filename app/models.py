from app import db

class Ocorrencia(db.Model):
	codigo_ocorrencia = db.Column(db.Integer, primary_key=True)
	classificacao = db.Column(db.String(30))
	tipo = db.Column(db.String(80))
	localidade = db.Column(db.String(100))
	uf = db.Column(db.String(3))
	pais = db.Column(db.String(80))
	aerodromo = db.Column(db.String(4), nullable=True)
	dia_ocorrencia = db.Column(db.Date)
	horario_utc = db.Column(db.Time)
	sera_investigada = db.Column(db.String(5), nullable=True)
	comando_investigador = db.Column(db.String(15))
	status_investigacao = db.Column(db.String(10), nullable=True)
	numero_relatorio = db.Column(db.String(150), nullable=True)
	relatorio_publicado = db.Column(db.String(5), nullable=True)
	dia_publicacao = db.Column(db.Date, nullable=True, default=None)
	quantidade_recomendacoes = db.Column(db.Integer, default=0)
	aeronaves_envolvidas = db.Column(db.Integer)
	saida_pista = db.Column(db.Integer, nullable=True, default=None)
	dia_extracao = db.Column(db.Date)
	aeronaves = db.relationship('Aeronave', backref=db.backref('ocorrencia', lazy='joined'), lazy='dynamic')
	fatores = db.relationship('FatorContribuinte', backref=db.backref('ocorrencia', lazy='joined'), lazy='dynamic')

	@property
	def serialize(self):	
		return self.localidade

class Aeronave(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	codigo_aeronave = db.Column(db.Integer, primary_key=True)
	codigo_ocorrencia = db.Column(db.Integer, db.ForeignKey('ocorrencia.codigo_ocorrencia'))
	matricula = db.Column(db.String(10))
	codigo_operador = db.Column(db.Integer)
	equipamento = db.Column(db.String(45))
	fabricante = db.Column(db.String(45))
	modelo = db.Column(db.String(45))
	tipo_motor = db.Column(db.String(45))
	quantidade_motores = db.Column(db.Integer, default=0)
	peso_maximo_decolagem = db.Column(db.Float)
	quantidade_assentos = db.Column(db.Integer, default=0)
	ano_fabricacao = db.Column(db.Integer, default=0)
	pais_registro = db.Column(db.String(80))
	categoria_registro = db.Column(db.String(6))
	categoria_aviacao = db.Column(db.String(50))
	origem_voo = db.Column(db.String(5), nullable=True, default=None)
	destino_voo = db.Column(db.String(5), nullable=True, default=None)
	fase_operacao = db.Column(db.String(100))
	tipo_operacao = db.Column(db.String(30))
	nivel_dano = db.Column(db.String(30), nullable=True, default=None)
	quantidade_fatalidades = db.Column(db.Integer, default=0)
	dia_extracao = db.Column(db.Date)


class FatorContribuinte(db.Model):
	codigo_fator = db.Column(db.Integer, primary_key=True)
	codigo_ocorrencia = db.Column(db.Integer, db.ForeignKey('ocorrencia.codigo_ocorrencia'))
	fator = db.Column(db.String(80))
	aspecto = db.Column(db.String(40), nullable=True, default=None)
	condicionante = db.Column(db.String(40), nullable=True, default=None)
	area = db.Column(db.String(15), nullable=True, default=None)	
	detalhe_fator = db.Column(db.String(100), nullable=True, default=None)
	dia_extracao = db.Column(db.Date)
