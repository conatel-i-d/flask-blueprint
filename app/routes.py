def register_routes(api, app, root="api"):
  # Importamos el metodo `register_routes` de cada `entity` y lo renombramos
  from app.entity import register_routes as attach_entity
  # Registramos las rutas
  attach_entity(api, app)