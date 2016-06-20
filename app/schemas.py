from app import ma, db
from app.models import Ocorrencia, Aeronave, FatorContribuinte
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

class BaseSchema(ma.ModelSchema):    
    class Meta:
        sqla_session = db.session  

class OcorrenciaSchema(BaseSchema):
	class Meta(BaseSchema.Meta):
		model = Ocorrencia
	aeronaves = fields.Nested('AeronaveSchema', many=True)
	fatores = fields.Nested('FatorContribuinteSchema', many=True)

class AeronaveSchema(BaseSchema):
	class Meta:
		model = Aeronave

class FatorContribuinteSchema(ModelSchema):
	class Meta:
		model = FatorContribuinte
