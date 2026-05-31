# Moviluno

API Flask con blueprints, JWT y migraciones.

## Migraciones

```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

## Ejecutar

```bash
flask run
```

## Autenticación / Postman

1. Llama a `/api/auth/login` con `email` y `password` para obtener el token.
2. En Postman coloca en Headers: `Authorization: Bearer <ACCESS_TOKEN>` (campo `KEY` = `Authorization`).
3. Las rutas de usuarios requieren rol `admin`. Las de productos aceptan roles `admin` o `user`.

## Seeder

Para poblar datos iniciales (admin, usuario de ejemplo y productos):

```bash
# Ejecutar desde el directorio del proyecto con FLASK_APP apuntando a `app.py`
flask seed run
```

Las credenciales por defecto para el admin son `ADMIN_EMAIL=admin@example.com` y `ADMIN_PASSWORD=adminpass` (puedes sobreescribir con variables de entorno antes de ejecutar).