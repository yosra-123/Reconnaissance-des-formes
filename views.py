

import tkinter
import tkinter.messagebox as messagebox

import constants
import widgets

# declaration des propriétés constantes
APPLICATION = constants.Application
WIDGET = constants.Widget
TEXT = constants.Text
ERROR = constants.Error

class ViewShapeRecognition(object):

	def __init__(self, entry_command):
		# création de l'objet contenant tous nos widgets
		self._widget = widgets.Widgets(entry_command = entry_command)

		self.widget.set_application(title = APPLICATION.TITLE,
									theme = APPLICATION.THEME, 
									font = APPLICATION.FONT, 
									widgets_font_to_be_changed \
									= APPLICATION.WIDGETS_FONT_TO_BE_CHANGED)

		# création d'une frame contenant tous les éléments
		self.widget.create_main_frame()


	#------------------------------------------------------------------------#
	#																		 #
	#					  classe view_shape_recognition: 					 #
	#					   partie supérieure de la vue						 #
	#																		 #
	#------------------------------------------------------------------------#

		self.set_widget_padding_x(padding_x = 3)
		self.set_widget_padding_y(padding_y = 1)

		self.widget.create_label(key = WIDGET.LABEL_SHAPE_DRAWN_ONE,
								 text = "Forme déssinée :",
								 row = 0,
								 column = 0,
								 columnspan = 2)

		self.widget.create_label(key = WIDGET.LABEL_SHAPE_DRAWN_TWO,
								 text = WIDGET.LABEL_SHAPE_DRAWN_TWO_INITIAL_TEXT,
								 row = 1,
								 column = 0)

		self.widget.create_label(key = WIDGET.LABEL_SHAPE_DRAWN_THREE,
								 text = WIDGET.LABEL_SHAPE_DRAWN_THREE_INITIAL_TEXT,
								 row = 2,
								 column = 0)

		self.widget.create_label(key = WIDGET.LABEL_SHAPE_RECOGNIZED_ONE,
								 text = "Forme reconnue :",
								 row = 1,
								 column = 3,
								 columnspan = 2,
								 sticky = tkinter.W,
								 anchor = tkinter.W)

		self.widget.create_label(
			key = WIDGET.LABEL_SHAPE_RECOGNIZED_TWO,
			text = WIDGET.LABEL_SHAPE_RECOGNIZED_TWO_INITIAL_TEXT,
			row = 2,
			column = 3,
			sticky = tkinter.W,
			anchor = tkinter.W)

		# création du canvas d'entrée

		self.widget.create_canvas(key = WIDGET.COMPARED_CANVAS,
								  row = 3,
								  column = 0,
								  rowspan = 9,
								  columnspan = 2,
								  sticky = tkinter.W)

		# création du canvas de sortie

		self.widget.create_canvas(key = WIDGET.OUTPUT_CANVAS,
								  row = 3,
								  column = 3,
								  rowspan = 9,
								  columnspan = 2,
								  sticky = tkinter.E)

		# change la taille des boutons poyur cette partie
		self.set_widget_padding_y(padding_y = 3)

		self.widget.create_label(key = WIDGET.LABEL_CREATE_NEURON,
								 text = "Nom de la forme a créer:",
								 row = 2,
								 column = 2)
		
		self.widget.create_entry(
			key = WIDGET.ENTRY_CREATE_NEURON,
			text = WIDGET.ENTRY_CREATE_NEURON_INITIAL_TEXT,
			text_type = TEXT.STRING_TYPE,
			text_length_max = 15,
			row = 3,
			column = 2)

		self.widget.create_button(key = WIDGET.BUTTON_CREATE_NEURON,
								  text = "Creer",
								  row = 4,
								  column = 2)

		self.widget.create_label(key = WIDGET.LABEL_ADD_SHAPE,
								 text = "Ajouter la variante à la forme :",
								 row = 5,
								 column = 2)

		self.widget.create_combo_box(key = WIDGET.COMBO_BOX_ADD_SHAPE,
									 state = "readonly",
									 row = 6,
									 column = 2)

		self.widget.create_button(key = WIDGET.BUTTON_ADD_SHAPE,
								  text = "Ajouter",
								  row = 7,
								  column = 2)

		self.widget.create_label(key = WIDGET.LABEL_CORRECT_NEURON,
								 text = "Nom de la forme a corriger:",
								 row = 8,
								 column = 2)

		self.widget.create_combo_box(key = WIDGET.COMBO_BOX_CORRECT_NEURON,
									 state = "readonly",
									 row = 9,
									 column = 2)

		self.widget.create_button(key = WIDGET.BUTTON_CORRECT_NEURON,
								  text = "Corriger",
								  row = 10,
								  column = 2)

		self.widget.create_button(key = WIDGET.BUTTON_AUTO_CORRECT,
								  text = "Apprentissage automatique",
								  row = 11,
								  column = 2)


	#------------------------------------------------------------------------#
	#																		 #
	#					  classe view_shape_recognition: 					 #
	#						partie centrale de la vue						 #
	#																		 #
	#------------------------------------------------------------------------#

		self.set_entry_widget_width(entry_width = 8)

		self.widget.create_button(key = WIDGET.BUTTON_CLEAN_SHAPE,
								  text = "Effacer la forme",
								  row = 12,
								  column = 0,
								  columnspan = 2)

		self.widget.create_label(key = WIDGET.LABEL_ITERATION_MAX,
								 text = "Nombre max d'iterations",
								 row = 12,
								 column = 2,
								 sticky = tkinter.W)

		self.widget.create_entry(
			key = WIDGET.ENTRY_ITERATION_MAX,
			text = WIDGET.ENTRY_ITERATION_MAX_INITIAL_TEXT,
			text_type = TEXT.INT_TYPE,
			text_variable_bound_min = 0,
			text_variable_bound_max = 1000000,
			row = 13,
			column = 2,
			sticky = tkinter.E)

		self.widget.create_label(key = WIDGET.LABEL_CORRECTION,
								 text = "Valeur de correction",
								 row = 12,
								 column = 3,
								 sticky = tkinter.W)

		self.widget.create_entry(key = WIDGET.ENTRY_CORRECTION,
								 text = WIDGET.ENTRY_CORRECTION_INITIAL_TEXT,
								 text_type = TEXT.FLOAT_TYPE,
								 text_variable_bound_min = 0.0,
								 text_variable_bound_max = 1.0,
								 row = 13,
								 column = 3,
								 sticky = tkinter.E)


	#------------------------------------------------------------------------#
	#																		 #
	#					  classe view_shape_recognition: 					 #
	#					   partie inférieure de la vue						 #
	#																		 #
	#------------------------------------------------------------------------#

		self.widget.create_treeview(
			key = WIDGET.TREEVIEW_LEARNING_INFORMATIONS,
			headers = WIDGET.TREEVIEW_LEARNING_INFORMATIONS_HEADERS,
			column_width = 180,
			items = WIDGET.TREEVIEW_LEARNING_INFORMATIONS_ITEMS,
			row = 14,
			column = 0,
			columnspan = 5)


	#------------------------------------------------------------------------#
	#																		 #
	#					  classe view_shape_recognition: 					 #
	#					  liste des méthodes utilisées						 #
	#																		 #
	#------------------------------------------------------------------------#

	def start(self):
		self.widget.start_view()


	# -----------------------------------------------------------------------#

	def show_warning(self, message):
		messagebox.showwarning(message[ERROR.TITLE_KEY],
							   message[ERROR.MESSAGE_KEY])


	# -----------------------------------------------------------------------#

	def show_ask_saving_box(self, title, text):
		return messagebox.askyesnocancel(title, text, icon='warning')


	#------------------------------------------------------------------------#
	#																		 #
	#					  classe view_shape_recognition: 					 #
	#					   liste des getters et setters						 #
	#																		 #
	#------------------------------------------------------------------------#

	def get_application_window(self):
		return self.widget.get_application_window()


	# -----------------------------------------------------------------------#

	def set_widget_padding_x(self, padding_x):
		self.widget.set_padding_x(padding_x = padding_x)


	# -----------------------------------------------------------------------#

	def set_widget_padding_y(self, padding_y):
		self.widget.set_padding_y(padding_y = padding_y)


	# -----------------------------------------------------------------------#

	def set_entry_widget_width(self, entry_width):
		self.widget.set_entry_width(entry_width = entry_width)


	# -----------------------------------------------------------------------#

	def get_label(self, key):
		return self.widget.get_label(key = key)


	# -----------------------------------------------------------------------#

	def set_label_text(self, key, text):
		self.widget.set_label_text(key = key,
								   text = text)


	# -----------------------------------------------------------------------#

	def get_label_text(self, key):
		self.widget.get_label_text(key = key)


	# -----------------------------------------------------------------------#

	def get_button(self, key):
		return self.widget.get_button(key = key)


	# -----------------------------------------------------------------------#

	def get_check_box(self, key):
		return self.widget.get_check_box(key = key)


	# -----------------------------------------------------------------------#

	def set_check_box_state(self, key, state):
		self.widget.set_check_box_state(key = key,
										state = state)


	# -----------------------------------------------------------------------#

	def get_entry(self, key):
		return self.widget.get_entry(key = key)


	# -----------------------------------------------------------------------#

	def set_entry_text(self, key, text):
		self.widget.set_entry_text(key = key,
								   text = text)


	# -----------------------------------------------------------------------#

	def get_entry_text(self, key):
		return self.widget.get_entry_text(key = key)


	# -----------------------------------------------------------------------#

	def get_combo_box(self, key):
		return self.widget.get_combo_box(key = key)


	# -----------------------------------------------------------------------#

	def set_combo_box_index(self, key, index):
		self.widget.set_combo_box_index(key = key,
										index = index)


	# -----------------------------------------------------------------------#

	def set_combo_box_text(self, key, text):
		self.widget.set_combo_box_text(key = key,
									   text = text)


	# -----------------------------------------------------------------------#

	def set_combo_box_values(self, key, values):
		self.widget.set_combo_box_values(key = key,
										 values = values)


	# -----------------------------------------------------------------------#

	def get_combo_box_text(self, key):
		return self.widget.get_combo_box_text(key = key)


	# -----------------------------------------------------------------------#

	def get_canvas(self, key):
		return self.widget.get_canvas(key = key)


	# -----------------------------------------------------------------------#

	def draw_on_canvas(self, key, dots_rect, color):
		self.widget.draw_on_canvas(key = key,
								   dots_rect = dots_rect,
								   color = color)


	# -----------------------------------------------------------------------#

	def get_treeview(self, key):
		return self.widget.get_treeview(key = key)


	# -----------------------------------------------------------------------#

	def get_treeview_items(self, key):
		return self.widget.get_treeview_items(key = key)


	# -----------------------------------------------------------------------#

	def update_treeview_items(self, key, items):
		self.widget.update_treeview_items(key = key,
										  items = items)


	#------------------------------------------------------------------------#
	#																		 #
	#					  classe view_shape_recognition: 					 #
	#						   liste des propriétés							 #
	#																		 #
	#------------------------------------------------------------------------#

	@property
	def widget(self):
		return self._widget

	@widget.setter
	def widget(self, widget):
		self._widget = widget
