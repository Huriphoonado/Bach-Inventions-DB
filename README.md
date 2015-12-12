## Bach Inventions



## Installation

First, make sure you have the required dependencies, namely [Flask, the Python Web framework used.](http://flask.pocoo.org)

```
$ pip install Flask
```

Then, create the Bach Inventions database by opening up a Python shell and calling the ```init_db()``` function from bachApp.py

```
$ python
...
>>> from bachApp import init_db
>>> init_db()
```

Then, run parser.py to parse the music XML files and store the Inventions in the database. It will begin printing feedack as it inserts into and queries the database. The output should look something like this:

```
$ python parser.py 
Database Connection Succesful: There are 482 notes in 1 Bach Invention(s).
Database Connection Succesful: There are 1158 notes in 2 Bach Invention(s).
Database Connection Succesful: There are 1683 notes in 3 Bach Invention(s).
Database Connection Succesful: There are 2148 notes in 4 Bach Invention(s).
Database Connection Succesful: There are 2898 notes in 5 Bach Invention(s).
Database Connection Succesful: There are 3488 notes in 6 Bach Invention(s).
Database Connection Succesful: There are 3988 notes in 7 Bach Invention(s).
Database Connection Succesful: There are 4596 notes in 8 Bach Invention(s).
Database Connection Succesful: There are 5198 notes in 9 Bach Invention(s).
Database Connection Succesful: There are 5666 notes in 10 Bach Invention(s).
Database Connection Succesful: There are 6251 notes in 11 Bach Invention(s).
Database Connection Succesful: There are 6983 notes in 12 Bach Invention(s).
Database Connection Succesful: There are 7576 notes in 13 Bach Invention(s).
Database Connection Succesful: There are 8200 notes in 14 Bach Invention(s).
Database Connection Succesful: There are 8691 notes in 15 Bach Invention(s).
```

## Notes

One of the challenges with music XML is chords or places where an instrument is playing more than one note at one time. Music XML uses ```forward``` and ```backward``` to indicate it is changing places in the measure to signify multiple notes in one place. This is a bit trickier to parse. I have removed the chords in the rare cases where Bach has used them.

Also, for simplicity I've key signatures from all pieces meaning that notes with sharps or flats are always indicated as such via the ```alter``` tag.

I may have discovered a bug or at least a confusion point in musicXML. The Finale Music Notation Software automatically fills empty measures with rests, but by appearence alone. If the user does actually fill anything into a measure then nothing actually exists. This caused my parser to break when it discovered measures without any content. The solution is to go into the Finale score and replace the empty measure with whole rests.

In Invention 6, I ignored the repeat signs.

I avoided multi-part music intentionally to make parsing the music XML files much easier. [A description of how music XML handles multi-part music may be found here.](http://www.musicxml.com/tutorial/the-midi-compatible-part/multi-part-music/)

### Schema

For this project, I have designed the schema specifically for Bach Inventions. The schema could be expanded in the future to include a composer table and compositions that functionally depend on the composer. The primary key is in bold.

* Invention (*inumber: int, book: int*, key: varchar)
* Part (*inumber: int, book: int, pnumber: int*)
* Measure (*inumber: int, book: int, pnumber: int, mnumber: int*, timeSig: varchar)
* Note (*inumber: int, book: int, pnumber: int, mnumber: int, position: int*, duration: varchar, pitch: varchar, octave: int)

### Musical Notes
* Pitch: Note name followed by its alteration. For example, "C0" is C, "C+1" is C sharp, C-1 is C flat.
* Octave
# Duration
* Position