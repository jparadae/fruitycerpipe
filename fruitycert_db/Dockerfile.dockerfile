# Se utiliza la imagen oficial de PostgreSQL
FROM postgres:latest

# Se definen las variables de entorno para la base de datos inicial
ENV POSTGRES_DB=fruitycert
ENV POSTGRES_USER=fruityadmin
ENV POSTGRES_PASSWORD=securepassword

# Se copia el script SQL de creación de tablas al contenedor
COPY create_tables.sql /docker-entrypoint-initdb.d/

# Expone el puerto predeterminado de PostgreSQL
EXPOSE 5432
