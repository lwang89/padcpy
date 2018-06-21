# Back end data structures and functions,
# separated out to here just for modularity

import time, datetime, sys
import subprocess
import tempfile

# Parameter
thumbSize =  70

############################################################
# BOOKMARK AND RELATED CLASSES
############################################################

class Bookmark:
	def __init__ (self, url, title, thumb=None, selection=None):
		self.url = url
		self.title = title

		# Specific selection if applicable (vice just save URL)
		# text or None
		self.selection = selection

		# Filename (temporary file) of thumbnail
		# or placeholder dummy file
		if thumb: self.thumb = thumb
		else: self.thumb = "dummy.gif"

		# An optional feature, you can ignore it.
		# Could hold 1 scalar of other brain or body state info,
		# for gradient bookmark retrieval
		self.interest = 0

		# We set this one ourselves upon creation
		self.time = datetime.datetime.today()

# A list of Bookmarks
class Pad:
	def __init__ (self, state):
		self.state = state
		self.bookmarks = []

	# Just an abbreviation for prepend to list
	def add (self, bookmark):
		self.bookmarks.insert (0, bookmark)

############################################################
# COMMUNICATE WITH BROWSER
############################################################

# Collects data for making a bookmark
# This is Mac OS-specific, if using another OS, write an equivalent function.
def getBookmark ():
	# Fetch URL from applescript
	# these assume there's only one Safari window
	url = callApplescript ('tell application "Safari" to do JavaScript "window.document.URL" in item 1 of (get every document)')

	# Fetch page "name" from applescript
	title = callApplescript ('tell application "Safari" to do JavaScript "window.document.title" in item 1 of (get every document)')

	# Fetch clipboard selection if any
	selection = callShell ("pbpaste -Prefer txt ; pbcopy </dev/null")
	if selection == "": selection = None

	# Fetch thumbnail (screendump the window, save to file, scale image, save file name to pass to front end)
	windowid = callApplescript ('tell application "Safari" to get id of item 1 of (get every window)')
	temppngfilename = tempfile.mkstemp(prefix="proj.brain.proto.pad", suffix=".png")[1]
	tempgiffilename = tempfile.mkstemp(prefix="proj.brain.proto.pad", suffix=".gif")[1]
	err = callShell ("screencapture -l" + windowid + " " + temppngfilename)
	if err!="": print ("Error from screencapture: " + err, file=sys.stderr)
	callShell ("sips " + temppngfilename + " -Z " + str(thumbSize) + " -s format gif --out " + tempgiffilename)

	# Create a new Bookmark and return it
	return Bookmark (url, title, tempgiffilename, selection)

# Send a URL (given as arg) to our main browser window
# This is Mac OS-specific, if using another OS, write an equivalent function.
def sendBookmark (url):
	callApplescript ('tell application "Safari" to do JavaScript "window.location.href = ' + "'" + url + "'" + '"in item 1 of (get every document)')

# Utility function, arg = the script as text
# Should be no need to escape double quotes or other shell metacharacters
# We return stdout, converted to a python3 text string if nec.
def callApplescript (script):
	ans = subprocess.check_output (["osascript", "-e", script])
	ans = ans.strip()
	if type(ans)!=type(""): return ans.decode("utf-8", "ignore")
	else: return ans

# Ditto, for shell script
def callShell (script):
	ans = subprocess.check_output (script, shell=True)
	ans = ans.strip()
	if type(ans)!=type(""): return ans.decode("utf-8", "ignore")
	else: return ans

############################################################
# OUR GLOBALS AND INITIALIZATIONS
############################################################

# Names of our possible classifier outputs
# internally, we'll use subscript of this list
brainCategories = ["A", "B", "C"]

# NB Index in allPads = brain state of this pad
allPads = list (map (lambda i: Pad(i), range(len (brainCategories))))

# Latest category
currentState = 0

# Some miscellaneous initialization to start us up
allPads[0].bookmarks.append (Bookmark ("http://www.tufts.edu/", "Tufts University", None, None))
allPads[0].bookmarks.append (Bookmark ("http://www.cs.tufts.edu/~jacob/", "Rob Jacob Home Page", None, None))
allPads[0].bookmarks.append (Bookmark ("http://www.tufts.edu/home/visiting_directions/", "Visiting, Maps & Directions - Tufts University", None, None))
allPads[1].bookmarks.append (Bookmark ("http://www.tufts.edu/", "Tufts University", None, None))
