CREATE TABLE "login" (
	"id"	INTEGER NOT NULL UNIQUE,
	"login"	INTEGER NOT NULL UNIQUE,
	"password"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

INSERT INTO login (login, password) VALUES ("admin", "admin") ;
INSERT INTO login (login, password) VALUES ("user", "password") ;