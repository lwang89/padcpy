# Classifier-Based Scratchpad Prototype

## Usage (on Mac)

Run Safari with one window

python3 main.py


### Compatibility and porting:

* This system is currently implemented for Mac, using Safari.

    * You may need to set 'Allow JavaScript from Apple Events' option in
Safari's Develop menu

* Should work with different browsers on Mac: 

    * Change the Applescript commands as noted

* Should work on windows:

    * Replace the Applescript commands
with powerscript or any other code that will
perform the same tasks

## Conceptual Design

You have several "scratch pads" (lists of web browser bookmarks)

* Each is associated with one of the brain
states that the classifier can distinguish

* Each contains web bookmarks thank you created while you were in the corresponding brain state.

* The benefit of the system is that it chooses the appropriate scratchpad for you at all times, without your effort or attention.
You can override its choice if it guesses wrong.


### Brain:

The selection by brain state applies to both input and output:

* Save: when you bookmark something, brain state determines
which pad it goes to.

* View: When you request information, brain state determines
which pad you get.

### View:

Press View button = displays the pad that corresponds
to current brain state.

Optional radio buttons at bottom let you
manually override the choice of pad.

### Save:

Press Save button = saves to the pad that corresponds
to current brain state.

Optional manual override as above.

If same URL was previously saved in the current pad, we do nothing.

### "Viewing" widget:

Indicates which pad is currently being viewed and will currently be used for saving,
in case the user's brain state has changed but the user hasn't pressed the
"View" button lately.

This is irrelevant in Continuous View mode.

### Override radio buttons:

Allows user to choose a different pad for the next View or Save command.

Once chosen, it remains until the next command, then it is canceled.
(Or choose "None" to cancel it)

Does not apply to a View or Save command if in View continously or Save
continuously mode respectively.


### Other plans:

The bookmarks could also be marked with a separate orthogonal
dimension giving interest or arousal at the time you bookmarked it
(placeholder is implemented,
could use bar graph display, like what padpy uses for distance,
to display interest).

Show all the pads, but prioritize based on brain state,
so that if we guess wrong it's not terrible.
That is, the system just makes one or another scratchpad more prominent
but the others are still tucked away but available. And
new inputs go to the more prominent one,
rather like the currently selected window in a GUI. Input goes to the
currently selected window, the system switches to make different "windows"
become currently selected, based on brain state.
Note that "currently selected" just means it's the featured
side window, we're not messing with the main browser window.

Maybe the choice of pads is based on spatial
vs. verbal or some other category like that.

Maybe we use context and other information as well as
brain state to choose among several bookmarks or groups or
configurations, analogous to activity-based window managers.

Could associate some explicit index terms with the lists, like maybe 5:

* Select content, Hit Save.

* Then think of one of 5 predefined distinctive thoughts
(like Donchin wheelchair commands) to pick which list to display
or display first.

* May be more useful with Glass, where input is more limited.


## UI Implementation

Main window = vanilla Safari, running independently

Bookmark window =

* "Save" button

* "View" button

* Bookmarks display

* "Viewing" widget

* Override radio buttons

* Radio buttons for brain state = like other prototypes, not intended to be in final system

    * Also shows brain state back to the user

Bookmarks display

* Shows pad corresponding to brain state as of last View or Save command,
or continuously.

* If you click a bookmark it sends main browser there.

* If you had copied a text region to the system clipboard, we save that (along
with URL of the page it was on) when you Save, otherwise we just save the
URL.


## Code Files

### main.py

Main program, including:

* UI and its commands and supporting code

* Communicate with brain device

* Main loop, including starting brainclient thread

### pad.py

Back end data structures and support functions, including:

* Pad (list of bookmarks), Bookmark, and related classes

* Communicate with browser

### brainclient.py

Runs in separate thread, calls back to pad.py when it gets data

## Miscellaneous

Thumbnail stuff leaves junk files in $TMPDIR
