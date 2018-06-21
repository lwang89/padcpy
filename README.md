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

You have several scratch pads (lists of web browser bookmarks)

* Each is associated with one of the brain
states that the classifier can distinguish

* Each contains web bookmarks thank you created while in the corresponding brain state.

* The benefit of the system is that it chooses the appropriate scratchpad for you at all times, without your effort or attention.
And you can override its choice if it guesses wrong.


### Brain:

The selection by brain state applies to both input and output:

* Save: when you bookmark something, brain determines
which pad it goes to.

* View: When you request information, brain determines
which pad you get. (Or maybe just
which one is displayed more prominently.)

### View:

Press View button = displays the pad that corresponds
to current brain state.

Optional command lets you
manually override the choice of pad.

TO DO MAYBE:

	Avoid biofeedback effect, where the 2 peripheral windows
	keep swapping as my brain state changes. Maybe it's very subtle.
	*Or it only shows up when you try to bookmark something.

	Otherwise, could I blend smoothly between the two scratch
	pads, so that if we guess wrong it's not terrible. So the
	system just makes one or the other scratchpad more prominent
	but the other one is still tucked away but available. And
	maybe new input goes to the more prominent one. Kind of like
	the currently selected window in a GUI. Input goes to the
	currently selected window, we switch to make different windows
	currently selected based on your brain state. Remember here
	that currently selected just means it's the featured
	peripheral window, we're not messing with the main window.

### Save:

Press Save button = saves to the pad that corresponds
to current brain state.

Optional manual override as above.

TO DO
	And the auxiliary display changes to the scratchpad you just
	saved into? (which is usually the one that corresponds to your
	current brain state, unless you used the pulldown override)

	And we should provide some manual control for choosing
	the currently selected [peripheral] window, so you can
	override the guess that our brain state makes

	You press a button to bookmark something, but we also record
	the amount of interest you had in it.

### Other plans:

Maybe the choice of pads is based on spatial
vs. verbal or some other category like that.

The bookmarks could also be marked with a separate orthogonal
dimension giving interest or arousal (placeholder is implemented,
could use the bar graph that padpy uses for distance to display interest).

Maybe we use context and other information as well as
brain state to choose among several bookmarks or group or
configurations, thinking again back to
activity-based window managers as an analogy

Could associate some explicit index terms with the lists, like maybe 5:

* Select content, Hit Save.

* Then think of one of 5 predefined distinctive thoughts
(like Donchin wheelchair commands) to pick which list to display
or display first.

* May be more useful with Glass, where input is more limited.


## UI Implementation

Main window = vanilla Safari, running independently

Bookmark window =

* "Save" button and manual override

* "View" button and manual override

* Bookmarks display

* Sliders window = like other prototypes, not intended to be in final system

    * Also shows brain state back to the user

Bookmarks display

* Shows pad corresponding to brain state

* If you click a bookmark it sends main browser there.

* If you had copied a text region to the system clipboard, we save that (along
with URL of the page it was on) when you Save, otherwise we just save the
URL.

TO DO:
	Shows last scratchpad that I saved into,
	i.e., don't respond visually to changing brain state
	(unless/until user pushes Save button)

	Sort by time
	Sort by interest level
	Visualize

TO DO

Save button = You press a button to bookmark something, but we also record
the amount of interest you had in it.

	Make it a button with a pulldown below it

	if you just click it, it picks which scratchpad to use by your brain,
	but pulldown lets you override

	Save: if you select a region, we copy that (along
	with URL of the page it was on), otherwise we just save the
	URL.

View scratchpad(s)
	Continuously displays last saved-in or else last one
	specifically viewed.
	When Save, it displays that one.
	When hit View, it switches to the one for the current brain state

	Maybe another pull down button for viewing the scratchpad,
	which shows me the scratchpad corresponding to my current
	brain state, and the pulldown lets me override/choose
	explicitly

	Not clear if the scratchpad(s) is always visible, just the
	appropriate one, just the one that was last used, all of them?

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
