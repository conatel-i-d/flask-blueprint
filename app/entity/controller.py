from flask import request
from flask_restplus import Namespace, Resource, fields
from flask.wrappers import Response

from app.api_response import ApiResponse
from app.utils.decorators import parse_query_parameters
from app.utils.helpers import index_query_params
from .service import EntityService
from .model import Entity
from .interfaces import EntityInterfaces

api_description = """
Recursos para la entidad de ejemplo `Entity`.

La idea de esta entidad es mostrar como se pueden componer los recursos. 
Por ahora solo cuenta con metodos `CRUD` pero la idea es mostrar como extender
este comportamiento.

El ejemplo también esta pensado para mostrar como se puede construir la documentación
de forma automatica usando los decoradores correspondientes.

Para obtener una guía de como construir la documentación utilizando `flask_restplus`
mirar el siguiente link:

[`flask_restplus` - Swagger Documentation](https://flask-restplus.readthedocs.io/en/stable/swagger.html)

Se incluyeron múltiples tipos de respuesta para mostrar como los decoradores pueden aplicarse tanto
a nivel de la clase `Resource` como a nivel de método. 
"""

api = Namespace('Entity', description=api_description)
interfaces = EntityInterfaces(api)

@api.route("/")
@api.response(400, 'Bad Request', interfaces.error_response_model)
@api.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal server error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
})
class EntityResource(Resource):
    """
    Entity Resource
    """
    
    @api.response(200, 'Entity List', interfaces.many_response_model)
    @api.doc(params=index_query_params)
    @parse_query_parameters
    def get(self) -> ApiResponse:
        """
        Returns the list of entities
        """
        entities = EntityService.get_all()
        return ApiResponse(interfaces.many_schema.dump(entities).data)

    @api.expect(interfaces.create_model)
    @api.response(200, 'New Entity', interfaces.single_response_model)
    def post(self) -> Entity:
        """
        Creates a single Entity

        La primera oración de este `docstring` se coloca como título del `endpoint`.
        Despues se puede incluir todo el detalle a continuación.

        Por defecto, se acepta Markdown para construir estos menajes. Hasta se pueden
        incluir tablas:

        | Columna 1 | Columna 2  | Columna 3|
        |---|---|---|
        | Valor 1 | Valor 2 | Valor 3|
        """
        json_data = request.get_json()
        if json_data is None:
            raise Exception('JSON body is undefined')
        body = interfaces.single_schema.load(json_data).data
        print(json_data)
        entity = EntityService.create(body)
        return ApiResponse(interfaces.single_schema.dump(entity).data)


@api.route("/<int:id>")
@api.param("id", "Entity unique identifier")
@api.response(400, 'Bad Request', interfaces.error_response_model)
@api.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal server error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
})
class EntityIdResource(Resource):
    @api.response(200, 'Wanted entity', interfaces.single_response_model)
    def get(self, id: int) -> Entity:
        """
        Get a single Entity
        """
        entity = EntityService.get_by_id(id)
        return ApiResponse(interfaces.single_schema.dump(entity).data)

    @api.response(204, 'No Content')
    def delete(self, id: int) -> Response:
        """
        Delete a single Entity
        """
        from flask import jsonify

        id = EntityService.delete_by_id(id)
        return ApiResponse(None, 204)

    @api.expect(interfaces.update_model)
    @api.response(200, 'Updated Entity', interfaces.single_response_model)
    def put(self, id: int):
        """Update a single Entity"""
        body = interfaces.single_schema.load(request.json).data
        entity = EntityService.update(id, body)
        return ApiResponse(interfaces.single_schema.dump(entity).data)
