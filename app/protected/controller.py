from flask import request
from flask_restplus import Namespace, Resource, fields
from flask.wrappers import Response

from app.api_response import ApiResponse
from app.utils.authorize import authorize
from app.utils.decorators import parse_query_parameters
from app.utils.query import Query
from .service import ProtectedEntityService
from .model import ProtectedEntity
from .interfaces import ProtectedEntityInterfaces

api_description = """
Este recurso es equivalente al anterios, con la excepción
de que estos recursos están protegidos. Para poder acceder
a los mismos, es necesario contar con un token JWT valido.

El proceso para crear un JWT valido es externo a este servicio.

Para su correcto funcionamiento, es necesario compartir la
llave privada utilizada para encriptar el token, y la audiencia
del mismo. Estos valores se configurán a través de las
siguientes variables de entorno:

- `PRIVATE_KEY`
- `AUDIENCE`

Ambos valores se cargarán en la configuración de la aplicación.
"""

api = Namespace('ProtectedEntity', description=api_description)
interfaces = ProtectedEntityInterfaces(api)

@api.route("/")
@api.response(400, 'Bad Request', interfaces.error_response_model)
@api.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal server error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
})
class ProtectedEntityResource(Resource):
    """
    ProtectedEntity Resource
    """
    
    @api.doc(security='apiKey')
    @api.doc(params=Query.index_query_params)
    @api.response(200, 'ProtectedEntity List', interfaces.many_response_model)
    @parse_query_parameters
    @authorize
    def get(self) -> ApiResponse:
        """
        Returns the list of entities
        """
        entities = ProtectedEntityService.get_all()
        return ApiResponse(interfaces.many_schema.dump(entities).data)

    @api.doc(security='apiKey')
    @api.response(200, 'New ProtectedEntity', interfaces.single_response_model)
    @api.expect(interfaces.create_model)
    @authorize
    def post(self) -> ProtectedEntity:
        """
        Creates a single ProtectedEntity

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
        entity = ProtectedEntityService.create(body)
        return ApiResponse(interfaces.single_schema.dump(entity).data)


@api.route("/<int:id>")
@api.param("id", "ProtectedEntity unique identifier")
@api.response(400, 'Bad Request', interfaces.error_response_model)
@api.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal server error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
})
class ProtectedEntityIdResource(Resource):
    @api.response(200, 'Wanted entity', interfaces.single_response_model)
    @api.doc(security='apiKey')
    @authorize
    def get(self, id: int) -> ProtectedEntity:
        """
        Get a single ProtectedEntity
        """
        entity = ProtectedEntityService.get_by_id(id)
        return ApiResponse(interfaces.single_schema.dump(entity).data)

    @api.response(204, 'No Content')
    @api.doc(security='apiKey')
    @authorize
    def delete(self, id: int) -> Response:
        """
        Delete a single ProtectedEntity
        """
        from flask import jsonify

        id = ProtectedEntityService.delete_by_id(id)
        return ApiResponse(None, 204)

    @api.expect(interfaces.update_model)
    @api.response(200, 'Updated ProtectedEntity', interfaces.single_response_model)
    @api.doc(security='apiKey')
    @authorize
    def put(self, id: int):
        """Update a single ProtectedEntity"""
        body = interfaces.single_schema.load(request.json).data
        entity = ProtectedEntityService.update(id, body)
        return ApiResponse(interfaces.single_schema.dump(entity).data)
