

import platform
import string

class Application(object):
	"""docstring for Application"""
	OS = platform.system()
	LINUX_OS = "Linux"
	WINDOWS_OS = "Windows"

	DELETE_WINDOW = "WM_DELETE_WINDOW"

	TITLE = "Reconnaissance de formes"
	THEME = "clam"
	FONT = ('courrier', '8')
	WIDGETS_FONT_TO_BE_CHANGED = ["TLabel",
								  "TCheckbutton",
								  "TButton",
								  "Treeview",
								  "Treeview.Heading"]


	#------------------------------------------------------------------------#

class Callback(object):
	RETURN_VALUE = "VALUE"
	RETURN_MESSAGE = "MESSAGE"
	BREAK = "break"
	SUCCEED = {RETURN_VALUE: True}
	FAILED = {RETURN_VALUE: BREAK}


	#------------------------------------------------------------------------#

class Menu(object):
	FILE_LABEL = "Fichier"
	FILE_LABEL_NEW = "Nouveau"
	FILE_LABEL_OPEN = "Ouvrir..."
	FILE_LABEL_SAVE = "Enregistrer"
	FILE_LABEL_SAVE_AS = "Enregistrer sous..."
	FILE_LABEL_QUIT = "Quitter"


	#------------------------------------------------------------------------#

class Widget(object):
	"""docstring for Widgets"""
	COMPARED_CANVAS = "COMPARED_CANVAS"
	OUTPUT_CANVAS = "OUTPUT_CANVAS"

	LABEL_SHAPE_DRAWN_ONE = "LABEL_SHAPE_DRAWN_ONE"
	LABEL_SHAPE_DRAWN_TWO = "LABEL_SHAPE_DRAWN_TWO"
	LABEL_SHAPE_DRAWN_TWO_INITIAL_TEXT = "nom : "
	LABEL_SHAPE_DRAWN_THREE = "LABEL_SHAPE_DRAWN_THREE"
	LABEL_SHAPE_DRAWN_THREE_INITIAL_TEXT = "n° de variante : "

	LABEL_SHAPE_RECOGNIZED_ONE = "LABEL_SHAPE_RECOGNIZED_ONE"
	LABEL_SHAPE_RECOGNIZED_TWO = "LABEL_SHAPE_RECOGNIZED_TWO"
	LABEL_SHAPE_RECOGNIZED_TWO_INITIAL_TEXT = "nom : "

	LABEL_CREATE_NEURON = "LABEL_CREATE_NEURON"
	ENTRY_CREATE_NEURON = "ENTRY_CREATE_NEURON"
	ENTRY_CREATE_NEURON_INITIAL_TEXT = ""
	BUTTON_CREATE_NEURON = "BUTTON_CREATE_NEURON"

	LABEL_ADD_SHAPE = "LABEL_ADD_SHAPE"
	COMBO_BOX_ADD_SHAPE = "COMBO_BOX_ADD_SHAPE"
	COMBO_BOX_ADD_SHAPE_INITIAL_TEXT = ""
	BUTTON_ADD_SHAPE = "BUTTON_ADD_SHAPE"

	LABEL_CORRECT_NEURON = "LABEL_CORRECT_NEURON"
	COMBO_BOX_CORRECT_NEURON = "COMBO_BOX_CORRECT_NEURON"
	COMBO_BOX_CORRECT_NEURON_INITIAL_TEXT = ""
	BUTTON_CORRECT_NEURON = "BUTTON_CORRECT_NEURON"

	LABEL_ITERATION_MAX = "LABEL_ITERATION_MAX"
	ENTRY_ITERATION_MAX = "ENTRY_ITERATION_MAX"
	ENTRY_ITERATION_MAX_INITIAL_TEXT = "1000"

	LABEL_CORRECTION = "LABEL_CORRECTION"
	ENTRY_CORRECTION = "ENTRY_CORRECTION"
	ENTRY_CORRECTION_INITIAL_TEXT = "0.1"

	BUTTON_AUTO_CORRECT = "BUTTON_AUTO_CORRECT"

	BUTTON_CLEAN_SHAPE = "BUTTON_CLEAN_SHAPE"

	TREEVIEW_LEARNING_INFORMATIONS = "TREEVIEW_LEARNING_INFORMATIONS"
	TREEVIEW_LEARNING_INFORMATIONS_HEADERS = ("caractéristique", "valeur")
	TREEVIEW_LEARNING_INFORMATIONS_ITEMS \
		= [("formes créées" , "0"), 
		("formes reconnues" , "0"),
		("itérations" , "0"), 
		("itérations totales" , "0"), 
		("temps d'apprentissage" , "0 ms"), 
		("temps d'apprentissage total" , "0 ms"),
		("taux d'erreur", "0 %")]


	#------------------------------------------------------------------------#

class Mouse(object):
	"""docstring for Mouse"""
	LEFT_CLICK = "<Button-1>"
	LEFT_CLICK_MOVE = "<B1-Motion>"
	LEFT_RELEASED = "<ButtonRelease-1>"

	WHEEL_CLICK = "<Button-2>"
	WHEEL_UP = "<Button-4>"
	WHEEL_DOWN = "<Button-5>"
	WHEEL_WINDOWS_MOVED = "<MouseWheel>"

	RIGHT_CLICK = "<Button-3>"
	RIGHT_CLICK_MOVE = "<B3-Motion>"
	RIGHT_RELEASED = "<ButtonRelease-3>"

	RELEASED = ""


	#------------------------------------------------------------------------#

class Keyboard(object):
	CTRL_PRESSED = "CTRL_PRESSED"
	CTRL_RELEASED = "CTRL_RELEASED"
	SHIFTL_PRESSED = "SHIFTL_PRESSED"
	SHIFTL_RELEASED = "SHIFTL_RELEASED"

	#------------------------------------------------------------------------#

class Canvas(object):
	"""docstring for Canvas"""
	BD = 1
	DOT_PIXEL_SIZE = 19
	DOT_X_COUNT = 12
	DOT_Y_COUNT = 16

	DOT = "DOT"
	DOT_COLOR = "DOT_COLOR"

	DOT_ACTIVATED = 1
	DOT_INACTIVATED = -1

	DOT_ACTIVATED_COLOR = "RED"
	DOT_INACTIVATED_COLOR = "WHITE"


	#------------------------------------------------------------------------#

class Neuron(object):
	"""docstring for Neuron"""
	INPUT_X_COUNT = Canvas.DOT_X_COUNT
	SYNAPSE_COUNT = Canvas.DOT_X_COUNT * Canvas.DOT_Y_COUNT

	ACTIVE = 1
	INACTIVE = -1
	NONE_ACTIVE = -2

	INPUT_ACTIVATED = ACTIVE
	INPUT_INACTIVATED = INACTIVE

	SYNAPSE_PASSING = float(ACTIVE)
	SYNAPSE_BLOCKING = float(INACTIVE)

	NAME_DONT_EXIST = True
	INDEX_DONT_EXIST = -1
	INPUT_MATRICE_DONT_EXIST = True

	FIRST_INPUT_VARIANT = 0


	#------------------------------------------------------------------------#

class Dialog(object):
	TITLE = "Selectionner fichier"
	OPEN = "OPEN"
	SAVEAS = "SAVEAS"
	NO_NAME_GIVEN = ()
	FILE_TYPES = ("fichiers Reconnaissance de Formes","*.srarn")
	ALL_FILE_TYPES = ("Tout types de fichiers","*.*")
	ASK_SAVING_TITLE = "attention"
	ASK_SAVING_MESSAGE = "Le fichier a été modifié, voulez vous enregistrer" \
						 + " les modifications apportées ?"


	#------------------------------------------------------------------------#

class File(object):
	NO_NAME_GIVEN = ""
	READING_MODE = "rb"
	WRITING_MODE = "wb"


	#------------------------------------------------------------------------#

class Text(object):
	INT_TYPE = "INT_TYPE"
	FLOAT_TYPE = "FLOAT_TYPE"
	STRING_TYPE = "STRING_TYPE"
	CHAR_DOT = '.'
	CHAR_ZERO = '0'
	INT_CHARS = string.digits
	FLOAT_CHARS = string.digits + CHAR_DOT
	STRING_CHARS = string.ascii_letters + string.digits
	DOT_POS_MIN = 0
	DOT_COUNT_MAX = 1
	INTEGER_PART_LEN_MAX = 1
	DECIMAL_PART_LEN_MAX = 2
	MILLI_SECONDS = " ms"
	PERCENTAGE = " %"


	#------------------------------------------------------------------------#

class Error(object):
	TITLE_KEY = "title"
	MESSAGE_KEY ="error"
	TITLE = "attention"
	NAME_EXIST = "le nom de la forme a créer est déjà utilisé."
	INPUT_MATRICE_EXIST = "la forme a déjà été créée."
	NO_NAME_GIVEN \
	= "le nom de la forme a créer doit comporter au minimum 1 caractère."
	INDEX_DONT_EXIST = "Le neurone n'a pas été trouvé."
	NO_NEURON_CREATED \
	= "il faut au moins 1 forme créée au réseau pour corriger."


	#------------------------------------------------------------------------#

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
