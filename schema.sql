drop table if exists note;
drop table if exists measure;
drop table if exists part;
drop table if exists invention;

CREATE TABLE invention (
	inumber integer NOT NULL,
	book integer NOT NULL,
	key text NOT NULL,
	PRIMARY KEY (inumber, book)
);

CREATE TABLE part (
	inumber integer NOT NULL,
	book integer NOT NULL,
	pnumber integer NOT NULL,
	PRIMARY KEY (inumber, book, pnumber),
	FOREIGN KEY(inumber, book) REFERENCES invention(inumber, book)
);

CREATE TABLE measure (
	inumber integer NOT NULL,
	book integer NOT NULL,
	pnumber integer NOT NULL,
	mnumber integer NOT NULL,
	timesig text NOT NULL,
	PRIMARY KEY (inumber, book, pnumber, mnumber),
	FOREIGN KEY(inumber, book, pnumber) REFERENCES part(inumber, book, pnumber)
);

CREATE TABLE note (
	inumber integer NOT NULL,
	book integer NOT NULL,
	pnumber integer NOT NULL,
	mnumber integer NOT NULL,
	position integer NOT NULL,
	duration text NOT NULL,
	pitch text NOT NULL,
	octave integer,
	PRIMARY KEY (inumber, book, pnumber, mnumber, position),
	FOREIGN KEY(inumber, book, pnumber, mnumber) REFERENCES measure(inumber, book, pnumber, mnumber)
);