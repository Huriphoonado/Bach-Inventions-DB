# all the imports
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# configuration
DATABASE = '/tmp/invention.db'
DEBUG = True

# create our application
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_db_info():
	basic_info = query_db('SELECT inumber, key from invention order by inumber asc')
	more_info = []
	for i in basic_info:
		inum = str(i[0])
		i = list(i)

		measureCount = query_db('SELECT MAX(mnumber) FROM measure where inumber=?', [inum])
		i.append(measureCount[0][0])
		
		mostCommonTimeSig = query_db('SELECT timesig FROM measure WHERE inumber=? GROUP BY timesig ORDER BY COUNT(timesig) DESC LIMIT 1', [inum])
		i.append(str(mostCommonTimeSig[0][0]))

		mostUsedPitch = query_db('SELECT pitch, COUNT(pitch) AS pitch_occ FROM note WHERE inumber=? GROUP BY pitch ORDER BY pitch_occ DESC LIMIT 3', [inum])
		ps = ''
		for p in mostUsedPitch:
			if ps != '':
				ps = ps + ", "
			ps = ps + str(p[0]) + ", " + str(p[1])
		i.append(ps)

		mostUsedRhythm = query_db('SELECT duration, COUNT(duration) AS duration_occ FROM note WHERE inumber=? GROUP BY duration ORDER BY duration_occ DESC LIMIT 2', [inum])
		rs = ''
		for r in mostUsedRhythm:
			if rs != '':
				rs = rs + ", "
			rs = rs + str(r[0]) + ", " + str(r[1])
		i.append(rs)

		more_info.append(i)

	return more_info

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

@app.route('/')
def show_entries():
	cur = get_db_info()
	entries = [dict(title=str(row[0]), key=row[1], measures=row[2], timeSig=row[3], pitch=row[4], rhythm=row[5]) for row in cur]
	return render_template('show_entries.html', entries=entries)

if __name__ == '__main__':
	app.debug = DEBUG
	app.run()