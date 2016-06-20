import os
from flask import Flask
from flask.json import jsonify
from app.models import Ocorrencia, FatorContribuinte, Aeronave
from app.schemas import OcorrenciaSchema, AeronaveSchema, FatorContribuinteSchema
from sqlalchemy.orm import Load
from app import db

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
	return 'Sorry, page not exists!'

@app.route('/')
def index():
	return 'It Works!'

# Endpoints para ocorrencias

@app.route('/ocorrencias')
def ocorrencias():
	
	ocorrencias = Ocorrencia.query.limit(10).all()
	oc_schema = OcorrenciaSchema()
	result = oc_schema.dump(ocorrencias, many=True)
	
	return jsonify(result.data)

@app.route('/ocorrencias/<codigo_ocorrencia>')
def find_ocorrencia(codigo_ocorrencia):
	
	ocorrencia = Ocorrencia.query.filter_by(codigo_ocorrencia=codigo_ocorrencia).first_or_404()
	oc_schema = OcorrenciaSchema()
	result = oc_schema.dump(ocorrencia)
	
	return jsonify(result.data)

@app.route('/ocorrencias/<codigo_ocorrencia>/fatores')
def find_fatores_ocorrencia(codigo_ocorrencia):

	ocorrencia = db.session.query(Ocorrencia)\
	.options(Load(Ocorrencia).load_only("fatores"),)\
	.filter(Ocorrencia.codigo_ocorrencia==codigo_ocorrencia).first()

	print(ocorrencia)

	oc_schema = OcorrenciaSchema()
	result = oc_schema.dump(ocorrencia)
	
	return jsonify(result.data)

# Endpoints para aeronaves

@app.route('/aeronaves')
def aeronaves():
	
	aeronaves = Aeronave.query.limit(10).all()
	aero_schema = AeronaveSchema()
	result = aero_schema.dump(aeronaves, many=True)

	return jsonify(result.data)

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

