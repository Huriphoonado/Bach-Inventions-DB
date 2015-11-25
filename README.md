## Installation

## Notes

One of the challenges with music XML is chords or places where an instrument is playing more than one note at one time. Music XML uses ```forward``` and ```backward``` to indicate it is changing places in the measure to signify multiple notes in one place. This is a bit trickier to parse. I have removed the chords in the rare cases where Bach has used them.

Also, for simplicity I've key signatures from all pieces meaning that notes with sharps or flats are always indicated as such via the ```alter``` tag.

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