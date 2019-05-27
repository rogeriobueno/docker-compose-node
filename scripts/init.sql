CREATE DATABASE "email_sender";

\c "email_sender"

CREATE TABLE emails(
    id serial NOT NULL,
    DATA TIMESTAMP NOT NULL DEFAULT current_timestamp,
    assunto VARCHAR(100) not null,
    mensagems VARCHAR(250) not null
);