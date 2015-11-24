## Notes

One of the challenges with music XML is chords or places where an instrument is playing more than one note at one time. Music XML uses ```forward``` and ```backward``` to indicate it is changing places in the measure to signify multiple notes in one place. This is a bit trickier to parse. I have removed the chords in the rare cases where Bach has used them.

Also, for simplicity I've key signatures from all pieces meaning that notes with sharps or flats are always indicated as such via the ```alter``` tag.

### Musical Notes
* Pitch: Note name followed by its alteration. For example, "C0" is C, "C+1" is C sharp, C-1 is C flat.
* Octave
# Duration
* Position