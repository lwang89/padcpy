#!/usr/bin/env python3
# Main program, including UI and callbacks

import time, datetime, sys
import random
import threading
import tkinter as tk
import tkinter.ttk as ttk

import pad
import brainclient

############################################################
# SEMANTIC CALLBACKS
############################################################

#
# Save button callback: Save current page in appropriate pad
#
def saveCB ():
	if overrideVar.get() == -1 or continuousSaveVar.get()==1:
		pad.allPads[pad.currentState].add (pad.getBookmark())
	else:
		pad.allPads[overrideVar.get()].add (pad.getBookmark())
		overrideVar.set(-1)

	# Update bookmarks display (optional)
	viewCB()

#
# View button callback: displays bookmarks for current Pad,
# is also called from some other places
# 
def viewCB ():
	if overrideVar.get() == -1 or continuousViewVar.get()==1:
		want = pad.currentState
	else:
		want = overrideVar.get()
		overrideVar.set(-1)

	bookmarks = pad.allPads[want].bookmarks
	tellLabel["text"] = "Viewing: " + pad.brainCategories[want]

	# Plug the bookmarks into the bookmark widgets
	ndraw = min (len(bookmarks), len(bookmarkWidgets))

	for i in range (ndraw):
		bookmarkWidgets[i].showBookmark (bookmarks[i])

	# Make the rest of them, if any, invisible
	for i in range (ndraw, len(bookmarkWidgets)):
		bookmarkWidgets[i].hideBookmark()

#
# Observer callback, ie when value changes: Toggle continuous view refresh.
# Actually simply setting continousViewVar itself is what does the job,
# we just disable/enable the view button here
#
def continuousViewVarCB (*ignoreargs):
	if continuousViewVar.get()==1:
		# Optional if brain data is streaming anyway, just to start us off
		viewCB()

	viewButton["state"] = tk.DISABLED if continuousViewVar.get()==1 else tk.NORMAL

#
# Similar, for save
#
def continuousSaveVarCB (*ignoreargs):
	if continuousSaveVar.get()==1:
		continuousSaveTick ()

	saveButton["state"] = tk.DISABLED if continuousSaveVar.get()==1 else tk.NORMAL

#
# Timer callback for continousSave
# Receive tick, do the job, then set up the next callback
# Unlike regular saveCB, we do not do a viewCB(), to prevent jumpiness/biofeedback
#
def continuousSaveTick ():
	if continuousSaveVar.get()==1:
		bookmark = pad.getBookmark()
		
		if bookmark.url not in map (lambda b: b.url, pad.allPads[pad.currentState].bookmarks):
			pad.allPads[pad.currentState].add (bookmark)

		top.after (1000, continuousSaveTick)

############################################################
# OTHER UI-RELATED FUNCTIONS
############################################################

# Layout parameters
# NB See pad.thumbSize for pixel size of our [square] thumbnails
buttonPadding=[30, 20, 30, 20]
padding = 3
allPadding = [padding, padding, padding, padding]
xPadding = [padding, 0, padding, 0]
titleWidth = 30
urlWidth = 40
selectionWidth = 40

# An initially-blank widget that can show data for a bookmark,
# can be changed subsequently to show a different bookmark.
# Doing it this way, rather than deleting the widgets and making new ones,
# seems to avoid flashing in the UI
class BookmarkW:
	# Make the blank widget
	def __init__ (self, bookmarksPanel):
		self.bookmark = None
		
		style = ttk.Style()

		self.main = ttk.Frame (bookmarksPanel)
		# We will set our grid() parameters below not here
		self.main.grid (row=0, column=0)

		self.main.grid_rowconfigure(0, weight=1)
		sep = ttk.Separator (self.main, orient="horizontal")
		sep.grid (row=0, column=0, sticky="ew", columnspan=2)

		style.configure ("bm.TFrame", padding=allPadding)
		leftGrid = ttk.Frame (self.main, style="bm.TFrame")
		leftGrid.grid (row=1, column=0)

		rightGrid = ttk.Frame (self.main, style="bm.TFrame")
		rightGrid.grid (row=1, column=1)

		self.thumbw = tk.Canvas (leftGrid, width=pad.thumbSize, height=pad.thumbSize)
		self.thumbw.grid (row=0, column=0, padx=padding, pady=padding)

		style.configure ("title.TLabel", padding=xPadding, font=('', '16', 'bold'))
		self.titlew = ttk.Label (rightGrid, style="title.TLabel")
		self.titlew.grid (sticky=tk.W+tk.N)

		style.configure ("time.TLabel", padding=xPadding, foreground="grey50")
		self.timew = ttk.Label (rightGrid, style="time.TLabel")
		self.timew.grid (sticky=tk.W+tk.N)

		style.configure ("url.TLabel", padding=xPadding, font=('', '10', ''))
		self.urlw = ttk.Label (rightGrid, style="url.TLabel")
		self.urlw.grid (sticky=tk.W+tk.N)

		style.configure ("selection.TLabel", font=('', '10', 'italic'), fg="grey40", padding=allPadding)
		self.selectionw = ttk.Label (rightGrid, style="selection.TLabel")
		self.selectionw.grid (sticky=tk.W+tk.N)

		# Attach our callback to our widget and everything inside
		self._bindAll (self.main, "<Button-1>")

		# Hide ourself until someone uses us
		self.main.grid_forget()

	# Private helper function, for recursive binding
	def _bindAll (self, root, event):
		root.bind (event, self.callback)
		if len(root.children.values())>0:
			for child in root.children.values():
				self._bindAll (child, event)

	# Populate this widget with data from the given bookmark
	def showBookmark (self, bookmark):
		self.bookmark = bookmark

		# Thumbnail
		# Preserve image as ivar, cause canvas only keeps pointer to it
		self.thumbImage = tk.PhotoImage (file=bookmark.thumb)
		self.thumbw.delete(tk.ALL)
		self.thumbw.create_image (0, 0, image=self.thumbImage, anchor=tk.NW)

		# Text fields
		self.titlew["text"] = self._shorten (self.bookmark.title, titleWidth)
		self.urlw["text"] = self._shorten (self.bookmark.url, urlWidth)
		self.selectionw["text"] = self._shorten (self.bookmark.selection, selectionWidth)
		self.timew["text"] = "%.0f sec. ago" % (datetime.datetime.today() - self.bookmark.time).total_seconds()

		# Set our parameters here not above
		self.main.grid (sticky=tk.E + tk.W)

	# Hide the widget, for those we currently don't need
	def hideBookmark (self):
		self.main.grid_forget()

	# Tell browser to go to our bookmarked page
	def callback (self, ignoreevent):
		pad.sendBookmark (self.bookmark.url)

	# Private helper function, truncates string to width,
	# adding "..." if appropriate
	# also turns None into ""
	# Similar to textwrap.shorten()
	def _shorten (self, string, width):
		if string==None:
			return ""
		elif len(string)<width:
			return string
		else:
			return string[:width] + "..."

############################################################
# COMMUNICATE WITH BRAIN DEVICE
############################################################

# Call from brainclient, arg = line of text from matlab
# First item (before ";") = ML classifier output A/B/C/etc.
# This is coming from a separate thread,
# both threads access currentBrainState
# we set it, others just read it (except the GUI slider)
# and it's a single atomic setting of a variable,
# so synchronization issues should be ok
def brainCB (line):
	tokens = line.strip().split (";")
	if len(tokens) < 1:
		print ("brainCB: can't parse input line: " + line, file=sys.stderr)

	elif tokens[0][0] not in pad.brainCategories:
		print ("brainCB: can't parse input line: " + line, file=sys.stderr)

	else:
		pad.currentState = pad.brainCategories.index (tokens[0][0])

		# Display it back to user via the radio
		brainVar.set (pad.currentState)

		# ...which will also trigger a viewCB() so no need for us to call it

# Our callback, ie when value of radio buttons change
# manually or because brainCB() above changes them
def brainVarCB (*ignoreargs):
	pad.currentState = brainVar.get()

	if continuousViewVar.get()==1: viewCB()

############################################################
# WINDOW AND WIDGET SETUP
############################################################

# Main window
top = tk.Tk()
top.title ("Brain Scratchpad Prototype with Classifier")

# Control panel area
controlPanel = ttk.Frame (top)
controlPanel.grid (row=0, column=0, columnspan=2)

# Our button style
style = ttk.Style()
style.configure ("cp.TButton",
	 font=('', 24, 'bold'), foreground="saddlebrown", padding=buttonPadding)

# View button, only applies if not in continuous view update mode
viewButton = ttk.Button (controlPanel, text = "View", style="cp.TButton")
viewButton["command"] = viewCB
viewButton.grid (row=0, column=0)

# Save button
saveButton = ttk.Button (controlPanel, text="Save", style="cp.TButton")
saveButton["command"] = saveCB
saveButton.grid (row=0, column=1)

# Toggle continuous update mode
continuousViewVar = tk.IntVar()
style.configure ("cp.TCheckbutton", foreground="saddlebrown")
continuousViewBox = ttk.Checkbutton (controlPanel, text="Update continuously", variable=continuousViewVar, style="cp.TCheckbutton")
continuousViewVar.trace ("w", continuousViewVarCB)
continuousViewBox.grid (row=1, column=0)

# Toggle continuous save mode
continuousSaveVar = tk.IntVar()
style.configure ("cp.TCheckbutton", foreground="saddlebrown")
continuousSaveBox = ttk.Checkbutton (controlPanel, text="Save continuously", variable=continuousSaveVar, style="cp.TCheckbutton")
continuousSaveVar.trace ("w", continuousSaveVarCB)
continuousSaveBox.grid (row=1, column=1)

# Bookmarks panel area
bookmarksPanel = ttk.Frame (top)
bookmarksPanel.grid (row=2, column=0, columnspan=2, pady=20)

# Empty widgets, each can show a bookmark, arbitrarily 5
bookmarkWidgets = []
for i in range (5):
	bookmarkWidgets.append (BookmarkW (bookmarksPanel))

# Tell user what they're seeing (if not in continuous view mode)
tellLabel = ttk.Label (top, style="tellLabel.TLabel")
tellLabel["text"] = "Viewing: " + pad.brainCategories[pad.currentState]
style.configure ("tellLabel.TLabel", font=('', 20, ''), foreground="saddlebrown")
tellLabel.grid (row=3, column=0, sticky="ns")

# Override brain state (does not apply to view or save if each is in continuous mode)
overrideLabel = ttk.Label (text="Override for next command only", style="override.TLabel")
style.configure ("override.TLabel", foreground="saddlebrown")
overrideFrame = ttk.Labelframe (top, labelwidget=overrideLabel, style="override.TLabelframe")
style.configure ("override.TLabelframe", foreground="saddlebrown")
overrideFrame.grid (row=3, column=1)
overrideVar = tk.IntVar()
b = ttk.Radiobutton (overrideFrame, text="(None)", variable=overrideVar, value=-1, style="override.TRadiobutton")
style.configure ("override.TRadiobutton", foreground="saddlebrown")
b.grid (row=0, column=0)
for i in range (len (pad.brainCategories)):
	b = ttk.Radiobutton (overrideFrame, text=pad.brainCategories[i], variable=overrideVar, value=i, style="override.TRadiobutton")
	b.grid (row=0, column=i+1)

# Simulated brain input radio button panel
brainFrame = tk.LabelFrame (top, text="Brain input")
brainFrame.grid (row=4, column=0, columnspan=2, pady=20, sticky="we")

brainVar = tk.IntVar()
brainVar.trace ("w", brainVarCB)
for i in range (len (pad.brainCategories)):
	b = tk.Radiobutton (brainFrame, text=pad.brainCategories[i], variable=brainVar, value=i)
	b.grid (row=0, column=i)

############################################################
# MAIN LOOP
############################################################

# Start up brainclient
bclientThread = threading.Thread (target=brainclient.mainloop, args=[brainCB])
bclientThread.start()

# Start things off
viewCB()

# Run our GUI loop
top.mainloop()

# To quit brainclient cleanly, after our main window closes
brainclient.quit = True
