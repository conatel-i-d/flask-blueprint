from marshmallow import fields as marshmallow_fields, Schema
from flask_restplus import fields as restplus_fields

class BaseInterfaces(object):
    """
    This class simplifies the creation of `marshmallo` schemas, and 
    `flask_restplus` models to document the API.

    Args:
        api (flask_restplus.Namespace): `flask_restplus` Namespace instance.
        name (str, optional): Name of the entity.

    Attributes:
        _api (flask_restplus.Namespace): `flask_restplus` Namespace instance.
        __name__ (string): Name of the entity. Used as prefix for the model names.
        _shcema (marshmallow.Schema): Dynamically generated `marshmallow` :class:`Schema`.
        single_schema (marshmallow.Schema): `marshmallow` instance for a single entity.
        many_shcema (marshmallow.Schema): `marshmallow` instance for a list of entities.
        create_model_keys (:list:str): List of field names that creates the entity's create model.
        update_model_keys (:list:str): List of field names that creates the entity's update model.
        create_model (flask_restplus.Namespace.model): Entity's create model.
        update_model (flask_restplus.Namespace.model): Entity's update model.
        model (flask_resplus.Namespace.model): Entity's model.
        single_response_model (flask_restplus.Namespace.model): Single entity's response model.
        many_response_model (flask_restplus.Namespace.model): Multiple entity's response model.
    """

    def __init__(self, api, name=''):
        self._api = api
        self.__name__ = getattr(self, '__name__', None) or name
        self._schema = self.create_marshmallow_schema()
        self.single_schema = self._schema()
        self.many_schema = self._schema(many=True)
        self.create_model_keys = getattr(self, 'create_model_keys', None) or self.get_restplus_fields_keys()
        self.create_model = self._api.model(self.__name__ + 'Create', self.get_restplus_fields(self.create_model_keys))
        self.update_model_keys = getattr(self, 'update_model_keys', None) or self.create_model_keys
        self.update_model = self._api.model(self.__name__ + 'Update', self.get_restplus_fields(self.update_model_keys))
        self.model = self._api.model(self.__name__, self.get_restplus_fields(self.get_restplus_fields_keys()))
        self.single_response_model = self.create_single_response_model()
        self.many_response_model = self.create_many_response_model()

    def get_restplus_fields(self, keys):
        """Returns a dictionary of `flask_restplus fields.

        Args:
            keys (:obj:`list` of :obj:`str`): List of fields to include

        Returns:
            A dictionary with its keys as the names of the wanted `flask_restplus``
            fields, and its values with their configuration.
        """
        return {key: getattr(self, key).get('r') for key in self.get_restplus_fields_keys() if key in keys}

    def get_restplus_fields_keys(self):
        """Gets the list of the `flask_restplus` configured fields.

        Returns:
            The list of `flask_restplus` fields.
        """
        return [field for field in self.attributes() if
            type(getattr(self, field)) is dict
            and getattr(self, field).get('r') is not None
        ]

    def get_marshmallow_fields_keys(self):
        """Gets the list of the `marshmallow` configured fields.

        Returns:
            The list of `marshmallow` fields.
        """
        return [field for field in self.attributes() if
            type(getattr(self, field)) is dict
            and getattr(self, field).get('m') is not None
        ]

    def attributes(self):
        """
        Returns a list with all the object attributes that are not
        callable or doesn't start with '__'.

        Returns:
            The list of attribute names.
        """
        return [key for key in dir(self) if 
            not key.startswith('__')
            and not key in ['schema']
            and not callable(getattr(self, key))
        ]

    def pick(self, keys):
        """Returns a list of current attributes included in the `keys` list.

        Args:
            keys (:obj:`list` of :obj:`str`): List of attribute names.

        Returns:
            The list of attributes that match the ones on the `keys` list.
        """
        values = [getattr(self, key) for key in self.attributes() if key in keys]
        return values
    
    def create_marshmallow_schema(self):
        """
        Dynamically creates a `marshmallow.Schema` class given the object
        configured `marshmallow.fields`.

        Returns:
            A `marshmallow.Schema` class.
        """
        fields_keys = self.get_marshmallow_fields_keys()
        return type(self.__name__ + 'MarshmallowSchema', (Schema,), {field_key: getattr(self, field_key).get('m') for field_key in fields_keys})

    def create_single_response_model(self):
        """Creates the single response model.

        Returns:
            A `flask_resplus.Namespace.model` for a single entity's response body.
        """
        return self._api.model(self.__name__ + 'SingleResponse', dict(
            item=restplus_fields.Nested(self.model),
        ))

    def create_many_response_model(self):
        """Creates the single response model.

        Returns:
            A `flask_resplus.Namespace.model` for a multuple entity's response body.
        """
        return self._api.model(self.__name__ + 'ManyResponse', dict(
            items=restplus_fields.List(restplus_fields.Nested(self.model)),
            count=restplus_fields.Integer
        ))