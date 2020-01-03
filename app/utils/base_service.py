from app import db
from app.utils.query import Query

class BaseService:
    # The model must be configured for each service
    model = None
    # The interface must be configured for each service
    interfaces = None

    @classmethod
    def get_all(cls):
        """
        Returns all the items paginated. The `page`, `per_page`, and `max_per_page`
        are gotten from Flask scope.
        """
        query = cls.model.query
        order_by = Query.get_param('order_by')
        order_dir = Query.get_param('order_dir')
        table_name = cls.model.__tablename__
        columns = [column.name for column in cls.model.metadata.tables[table_name].columns]
        if order_by is not None and order_by in columns:
            if order_dir == 'desc':
                query = query.order_by(getattr(cls.model, order_by).desc())
            else:
                query = query.order_by(getattr(cls.model, order_by).asc())
        return query.paginate(
            page=Query.get_param('page'),
            per_page=Query.get_param('per_page'),
            error_out=False,
            max_per_page=Query.get_param('max_per_page')
        ).items

    @classmethod
    def get_by_id(cls, id: int):
        return cls.model.query.get(id)

    @classmethod
    def update(cls, id: int, body):
        model = cls.get_by_id(id)
        update_keys = cls.interfaces.update_model_keys
        if model is None:
            return None
        model.update({ key: body[key] for key in update_keys if key in body})
        #model.update({ key: value for key, value in body.items() if key in update_keys })
        # pylint: disable=no-member
        db.session.commit()
        return model

    @classmethod
    def delete_by_id(cls, id: int):
        model = cls.model.query.filter(cls.model.id == id).first()
        if not model:
            return []
        # pylint: disable=no-member
        db.session.delete(model)
        # pylint: disable=no-member
        db.session.commit()
        return [id]

    @classmethod
    def create(cls, body):
        create_keys = cls.interfaces.create_model_keys
        # pylint: disable=not-callable
        model = cls.model(**{ key: body[key] for key in create_keys if key in body})
        # pylint: disable=no-member
        db.session.add(model)
        # pylint: disable=no-member
        db.session.commit()
        return model
