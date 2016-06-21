import os
from flask import Flask, render_template
from flask.json import jsonify
from app.models import Ocorrencia, FatorContribuinte, Aeronave
from app.schemas import OcorrenciaSchema, AeronaveSchema, FatorContribuinteSchema
from sqlalchemy import func, desc
from app import db

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
	return render_template('not_found.html')

@app.route('/')
def index():
	return render_template('index.html')

##
# Endpoints para ocorrencias
##

# Todas as ocorrencias

@app.route('/api/ocorrencias/')
def ocorrencias():
	
	ocorrencias = Ocorrencia.query.limit(10).all()
	oc_schema = OcorrenciaSchema()
	result = oc_schema.dump(ocorrencias, many=True)
	
	return jsonify(result.data)

# Ocorrencia detalhada: busca por codigo

@app.route('/api/ocorrencias/<codigo_ocorrencia>/')
def find_ocorrencia(codigo_ocorrencia):
	
	ocorrencia = Ocorrencia.query.filter_by(codigo_ocorrencia=codigo_ocorrencia).first_or_404()
	oc_schema = OcorrenciaSchema()
	result = oc_schema.dump(ocorrencia)
	
	return jsonify(result.data)

# Fatores contribuintes de uma ocorrencia selecionada atraves do codigo

@app.route('/api/ocorrencias/<codigo_ocorrencia>/fatores/')
def find_fatores_ocorrencia(codigo_ocorrencia):

	fatores = db.session.query(FatorContribuinte).join(Ocorrencia)\
	.filter(Ocorrencia.codigo_ocorrencia==codigo_ocorrencia).all()

	fator_schema = FatorContribuinteSchema()
	result = fator_schema.dump(fatores, many=True)
	
	return jsonify(result.data)

# Aeronaves envolvidas em uma ocorrencia selecionada atraves do codigo

@app.route('/api/ocorrencias/<codigo_ocorrencia>/aeronaves/')
def find_aeronaves_ocorrencia(codigo_ocorrencia):

	aeronaves = db.session.query(Aeronave).join(Ocorrencia)\
	.filter(Ocorrencia.codigo_ocorrencia==codigo_ocorrencia).all()

	aeronave_schema = AeronaveSchema()
	result = aeronave_schema.dump(aeronaves, many=True)
	
	return jsonify(result.data)

# Todas as classificacoes de ocorrencia

@app.route('/api/tipos_classificacao/')
def classificacao_ocorrencias():
	
	classificacoes = []

	for ocorrencia in Ocorrencia.query.distinct(Ocorrencia.classificacao).group_by(Ocorrencia.classificacao).all():
		classificacoes.append({'classificacao': ocorrencia.classificacao})
	
	return jsonify(classificacoes)

# Todos os tipos de ocorrencia

@app.route('/api/tipos_ocorrencia/')
def tipo_ocorrencias():
	
	tipos = []

	for ocorrencia in Ocorrencia.query.distinct(Ocorrencia.tipo).group_by(Ocorrencia.tipo).all():
		tipos.append({'tipo': ocorrencia.tipo})
	
	return jsonify(tipos)

# Ocorrencias selecionadas em um intervalo de tempo

@app.route('/api/ocorrencias/entre/<data_inicio>/<data_fim>/')
def find_ocorrencias_entre(data_inicio, data_fim):
	
	ocorrencias = Ocorrencia.query.filter(Ocorrencia.dia_ocorrencia.between(data_inicio, data_fim)).all()
	oc_schema = OcorrenciaSchema()
	result = oc_schema.dump(ocorrencias, many=True)
	
	return jsonify(result.data)

# Todas as ocorrencias por UF

@app.route('/api/ocorrencias/uf/<uf>/')
def find_ocorrencias_estado(uf):

	ocorrencias = Ocorrencia.query.filter(Ocorrencia.uf==uf).all()
	oc_schema = OcorrenciaSchema()
	result = oc_schema.dump(ocorrencias, many=True)	

	return jsonify(result.data)

##
# Endpoints para aeronaves
##

# Todas as aeronaves

@app.route('/api/aeronaves/')
def aeronaves():
	
	aeronaves = Aeronave.query.limit(10).all()
	aero_schema = AeronaveSchema()
	result = aero_schema.dump(aeronaves, many=True)

	return jsonify(result.data)

# Modelos de aeronave que mais estiveram em ocorrencias

@app.route('/api/aeronaves/modelos_mais_ocorrencias/')
def find_modelos_com_mais_acidentes():

	modelos = db.session.query(Aeronave.modelo, func.count(Aeronave.modelo).label('cont'))\
	.group_by(Aeronave.modelo).order_by(desc(func.count(Aeronave.modelo))).all()

	result = []

	for modelo in modelos:
		result.append({'modelo': modelo.modelo, 'quantidade': modelo.cont})

	return jsonify(result)

##
# Main
##

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port, debug=True)

