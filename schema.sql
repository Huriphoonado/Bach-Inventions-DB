drop table if existst note;
drop table if exists measure;
drop table if exists part;
drop table if exists invention;

CREATE TABLE invention (
	inumber integer PRIMARY KEY NOT NULL,
	book integer PRIMARY KEY NOT NULL,
	key text NOT NULL
);

CREATE TABLE part (
	inumber integer PRIMARY KEY NOT NULL,
	book integer PRIMARY KEY NOT NULL,
	pnumber integer PRIMARY KEY NOT NULL,
	FOREIGN KEY(inumber, book) REFERENCES invention(inumber, book)
);

CREATE TABLE measure (
	inumber integer PRIMARY KEY NOT NULL,
	book integer PRIMARY KEY NOT NULL,
	pnumber integer PRIMARY KEY NOT NULL,
	mnumber integer PRIMARY KEY NOT NULL,
	timesig text NOT NULL,
	FOREIGN KEY(inumber, book, pnumber) REFERENCES part(inumber, book, pnumber)
);

CREATE TABLE note (
	inumber integer PRIMARY KEY NOT NULL,
	book integer PRIMARY KEY NOT NULL,
	pnumber integer PRIMARY KEY NOT NULL,
	mnumber integer PRIMARY KEY NOT NULL,
	position integer PRIMARY KEY NOT NULL,
	duration text NOT NULL,
	pitch text NOT NULL,
	octave integer,
	FOREIGN KEY(inumber, book, pnumber, mnumber) REFERENCES measure(inumber, book, pnumber, mnumber)
);