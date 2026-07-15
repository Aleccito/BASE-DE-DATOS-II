Esta carpeta se completa automáticamente al ejecutar:

    flask db init

Luego usa:

    flask db migrate -m "mensaje"
    flask db upgrade

para generar y aplicar migraciones basadas en los modelos de `models/`.
Si prefieres no usar migraciones, puedes crear el esquema directamente
con `database/schema.sql`.
