

import os
import dill
from tkinter import filedialog
from functools import partial

import constants
import models
from entry_validation import is_entry_text_valid, are_bounds_valid

# declaration des propriétés constantes
APPLICATION = constants.Application
CALLBACK = constants.Callback
MOUSE = constants.Mouse
KEYBOARD = constants.Keyboard
WIDGET = constants.Widget
CANVAS = constants.Canvas
NEURON = constants.Neuron
DIALOG = constants.Dialog
FILE = constants.File
TEXT = constants.Text
ERROR = constants.Error
Point = constants.Point

class PresenterShapeRecognition (object):

	def __init__ (self, model, view, interactor):

		self._model = models.ModelShapeRecognition ()

		# declaration des propriétés variables
		view = view (entry_command = self.on_entry_validate)
		self._view = view

		self._interactor = interactor ()
		self.interactor.bind_view_to_presenter (presenter = self, 
											   view = view)


	#------------------------------------------------------------------------#

		self._modified_dots = []

		self._mouse_last_clicked_button = None
		self._mouse_last_dot_position = None
		self._neuron_selected_to_correct = 0
		self._neuron_selected_to_show = 0
		self._neuron_last_selected_selected_to_show = 0
		self._neuron_variant_selected_to_show = 0
		self._neuron_variant_last_selected_to_show = 0
		self._mouse_wheel_counter_min = 0
		self._mouse_wheel_counter_max = 0
		self._keyboard_ctrl_state = KEYBOARD.CTRL_RELEASED
		self._keyboard_shiftl_state = KEYBOARD.SHIFTL_RELEASED

		self._file_name = FILE.NO_NAME_GIVEN

		self._file_modified = False
		self._compared_canvas_modified = False
		self._compared_canvas_mouse_button_released = True
		self._compared_canvas_neuron_current_selection_modified = False
		self._compared_canvas_neuron_variant_current_selection_modified = False
		self._entry_create_neuron_modified = False
		self._combo_box_add_shape_modified = False
		self._combo_box_add_shape_current_selection_modified = False
		self._combo_box_correct_neuron_modified = False
		self._combo_box_correct_neuron_current_selection_modified = False
		self._entry_iteration_max_modified = False
		self._entry_correction_modified = False
		self._treeview_learning_informations_modified = False


	#------------------------------------------------------------------------#

		# affiche la vue
		view.start ()


	#------------------------------------------------------------------------#
	#																		 #
	#				   classe presenter_shape_recognition: 					 #
	#						  liste des callbacks							 #
	#																		 #
	#------------------------------------------------------------------------#

	def on_compared_canvas_mouse_button_clicked (self, mouse, mouse_abs, mouse_button):
		if not self._is_mouse_in_compared_canvas (mouse_abs = mouse_abs):
			return CALLBACK.FAILED

		# verifie si le bouton de la souris cliqué à changé depuis le dernier appel de cet callback
		mouse_last_clicked_button_changed \
		= self._has_mouse_last_clicked_button_changed (
			mouse_button = mouse_button)

		if mouse_last_clicked_button_changed:
			self._set_mouse_last_clicked_button (
				mouse_button = mouse_button)

		dot = self._get_compared_canvas_dot_at_mouse_position (mouse = mouse)

		mouse_last_dot_position_changed \
		= self._has_mouse_last_dot_position_changed (dot = dot)

		if mouse_last_dot_position_changed:
			self._update_mouse_last_dot_position (new_position = dot)

		if mouse_last_dot_position_changed \
			or mouse_last_clicked_button_changed:
			self.compared_canvas_modified = True

			self._update_compared_input_state (dot = dot,
											   mouse_button = mouse_button)

			self._update_compared_canvas_dot_color (
				dot = dot,
				mouse_button = mouse_button)

			self._update_view ()

		return CALLBACK.SUCCEED


	#------------------------------------------------------------------------#

	def on_compared_canvas_mouse_button_released (self):
		self.compared_canvas_mouse_button_released = True

		(neuron, variant) = self.model.get_neuron_and_variant()

		if (neuron, variant) \
			!= (NEURON.INDEX_DONT_EXIST, NEURON.FIRST_INPUT_VARIANT):
			self.neuron_selected_to_show = neuron
			self.neuron_variant_selected_to_show = variant
		else:
			self.neuron_selected_to_show = NEURON.INDEX_DONT_EXIST

		# affiche le neurone reconnue dans la vue
		self._update_view ()

		return CALLBACK.SUCCEED


	#------------------------------------------------------------------------#

	def on_compared_canvas_mouse_wheel_clicked (self):
		if self.model.get_neuron_count ():
			if self.keyboard_ctrl_state == KEYBOARD.CTRL_RELEASED:
				self.on_correct_neuron_button ()

			elif self.keyboard_ctrl_state == KEYBOARD.CTRL_PRESSED:
				if self.keyboard_shiftl_state == KEYBOARD.SHIFTL_RELEASED:
					self.on_add_shape_button ()

		return CALLBACK.SUCCEED


	#------------------------------------------------------------------------#

	def on_compared_canvas_mouse_wheel_moved (self, mouse_button):
		if self.model.get_neuron_count ():
			if self.keyboard_ctrl_state == KEYBOARD.CTRL_RELEASED:
				self.neuron_selected_to_correct \
				= self._set_mouse_wheel_counter (
					mouse_button = mouse_button,
					counter = self.neuron_selected_to_correct)

				self.combo_box_correct_neuron_current_selection_modified \
				= True

			elif self.keyboard_ctrl_state == KEYBOARD.CTRL_PRESSED:
				if self.keyboard_shiftl_state == KEYBOARD.SHIFTL_RELEASED:
					self.neuron_selected_to_show \
					= self._set_mouse_wheel_counter (
						mouse_button = mouse_button,
						counter = self.neuron_selected_to_show)

					self.compared_canvas_neuron_current_selection_modified \
					= True
					self.compared_canvas_mouse_button_released = True
					self.combo_box_add_shape_current_selection_modified = True

				elif self.keyboard_shiftl_state == KEYBOARD.SHIFTL_PRESSED:
					self.neuron_variant_selected_to_show \
					= self._set_mouse_wheel_counter (
						mouse_button = mouse_button,
						counter = self.neuron_variant_selected_to_show)

					self.compared_canvas_neuron_variant_current_selection_modified \
					= True
					self.compared_canvas_mouse_button_released = True

			self._update_view ()

		return CALLBACK.SUCCEED


	#------------------------------------------------------------------------#

	def on_keyboard_ctrl_pressed (self):
		self.keyboard_ctrl_state = KEYBOARD.CTRL_PRESSED
		self.neuron_selected_to_show \
		= self.neuron_last_selected_selected_to_show

		return CALLBACK.SUCCEED


	#------------------------------------------------------------------------#

	def on_keyboard_ctrl_released (self):
		self.keyboard_ctrl_state = KEYBOARD.CTRL_RELEASED

		return CALLBACK.SUCCEED


	#------------------------------------------------------------------------#

	def on_keyboard_shiftl_pressed (self):
		self.keyboard_shiftl_state = KEYBOARD.SHIFTL_PRESSED
		self._set_mouse_wheel_counter_max_to_neuron_variant_count (
			neuron = self.neuron_selected_to_show)
		self.neuron_variant_selected_to_show = self.neuron_variant_last_selected_to_show

		return CALLBACK.SUCCEED


	#------------------------------------------------------------------------#

	def on_keyboard_shiftl_released (self):
		self.keyboard_shiftl_state = KEYBOARD.SHIFTL_RELEASED
		self._set_mouse_wheel_counter_max_to_neuron_count ()

		return CALLBACK.SUCCEED


	#------------------------------------------------------------------------#

	def on_create_neuron_button (self):
		name = self.view.get_entry_text (key = WIDGET.ENTRY_CREATE_NEURON)

		# appel de la callback de création de nouveau neurone dans le modèle
		result = self.model.on_create_neuron (name = name)

		# mise à jour des widgets concernés dans la vue
		if result == CALLBACK.SUCCEED:
			self._set_mouse_wheel_counter_max_to_neuron_count ()

			self.file_modified = True
			self.compared_canvas_mouse_button_released = True
			self.combo_box_add_shape_modified = True
			self.combo_box_correct_neuron_modified = True
			self.treeview_learning_informations_modified = True

			self._update_view ()

			callback_return = CALLBACK.SUCCEED
		else:
			# si erreur alors affichage d'une alerte avec les détails de l'erreur dans la vue
			warning_message = result[CALLBACK.RETURN_MESSAGE]

			self.view.show_warning (message = warning_message)

			callback_return = CALLBACK.FAILED

		return callback_return


	#------------------------------------------------------------------------#

	def on_add_shape_button (self, event = None):
		name = self.view.get_combo_box_text (
				   key = WIDGET.COMBO_BOX_ADD_SHAPE)

		# appel de la callback de correction du neurone dans le modèle
		result = self.model.on_add_shape (name = name)

		# mise à jour des widgets concernés dans la vue
		if result == CALLBACK.SUCCEED:
			self.file_modified = True
			self.compared_canvas_mouse_button_released = True
			self.treeview_learning_informations_modified = True

			self._update_view ()

			callback_return = CALLBACK.SUCCEED
		else:
			# si erreur alors affichage d'une alerte avec les détails de l'erreur dans la vue
			warning_message = result[CALLBACK.RETURN_MESSAGE]

			self.view.show_warning (message = warning_message)

			callback_return = CALLBACK.FAILED

		return callback_return

	#------------------------------------------------------------------------#

	def on_correct_neuron_button (self, event = None):
		name = self.view.get_combo_box_text (
				   key = WIDGET.COMBO_BOX_CORRECT_NEURON)

		# appel de la callback de correction du neurone dans le modèle
		result = self.model.on_correct_neuron (name = name)

		# mise à jour des widgets concernés dans la vue
		if result == CALLBACK.SUCCEED:
			self.file_modified = True
			self.compared_canvas_mouse_button_released = True
			self.treeview_learning_informations_modified = True

			self._update_view ()

			callback_return = CALLBACK.SUCCEED
		else:
			# si erreur alors affichage d'une alerte avec les détails de l'erreur dans la vue
			warning_message = result[CALLBACK.RETURN_MESSAGE]

			self.view.show_warning (message = warning_message)

			callback_return = CALLBACK.FAILED

		return callback_return


	#------------------------------------------------------------------------#

	def on_auto_correct_button (self):
		# appel de la callback d'apprentissage automatique du reseau de neurones dans le modèle
		result = self.model.on_auto_correct ()

		# mise à jour des widgets concernés dans la vue
		if result == CALLBACK.SUCCEED:
			self.file_modified = True
			self.compared_canvas_mouse_button_released = True
			self.treeview_learning_informations_modified = True
			
			self._update_view ()

			callback_return = CALLBACK.SUCCEED
		else:
			# si erreur alors affichage d'une alerte avec les détails de l'erreur dans la vue
			warning_message = result[CALLBACK.RETURN_MESSAGE]

			self.view.show_warning (message = warning_message)

			callback_return = CALLBACK.FAILED

		return callback_return


	#------------------------------------------------------------------------#

	def on_button_clean_shape (self):
		# appel de la callback pour effacer les pixels déssinés
		self.mouse_last_clicked_button = None
		self.mouse_last_dot_position = None

		for synapse in range (NEURON.SYNAPSE_COUNT):
			self.model.update_compared_input_state (
				index = synapse,
				new_state = NEURON.INPUT_INACTIVATED)

		(neuron, variant) = self.model.get_neuron_and_variant()

		if  (neuron, variant) != (NEURON.INDEX_DONT_EXIST, NEURON.FIRST_INPUT_VARIANT):
			self.neuron_selected_to_show = neuron
			self.neuron_variant_selected_to_show = variant
		else:
			self.neuron_selected_to_show = NEURON.INDEX_DONT_EXIST

		# mise à jour des widgets concernés dans la vue
		self.file_modified = True
		self.compared_canvas_mouse_button_released = True
		self.treeview_learning_informations_modified = True
		self._clean_canvas (canvas = WIDGET.COMPARED_CANVAS)
		self._update_view ()


		return CALLBACK.SUCCEED


	#------------------------------------------------------------------------#
	def on_file_menu_new (self):
		# appel de la callback d'apprentissage automatique du reseau de neurones dans le modèle
		if self.file_modified == True:
			self._ask_file_saving ()

		# si apres la demande de sauvegarde l'utilisateur a sauvegarder ou si
		# le reseau de neurone n'avait pas ete modifier
		if self.file_modified == False:
			self._new_file ()

			# mise à jour la vue
			self._update_view ()

		return CALLBACK.SUCCEED


	#------------------------------------------------------------------------#
	
	def on_file_menu_open (self):
		# appel de la callback d'apprentissage automatique du reseau de neurones dans le modèle
		if self.file_modified == True:
			self._ask_file_saving ()

		# si apres la demande de sauvegarde l'utilisateur a sauvegarder ou si
		# le reseau de neurone n'avait pas ete modifier
		if self.file_modified == False:
			self._open_file ()
				
			# mise à jour la vue
			self._update_view ()

		return CALLBACK.SUCCEED


	#------------------------------------------------------------------------#
	
	def on_file_menu_save (self):
		if self.file_name:
			self._save_file (file_name = self.file_name)

			self.file_modified = False
		else:
			file_name = self._save_as_file ()

			if file_name:
				self.file_modified = False

		return CALLBACK.SUCCEED


	#------------------------------------------------------------------------#
	
	def on_file_menu_save_as (self):
		file_name = self._save_as_file ()

		if file_name:
			self.file_modified = False

		return CALLBACK.SUCCEED


	#------------------------------------------------------------------------#
	
	def on_file_menu_quit (self):
		# appel de la callback d'apprentissage automatique du reseau de neurones dans le modèle
		if self.file_modified == True:
			self._ask_file_saving ()

		# si apres la demande de sauvegarde l'utilisateur a sauvegarder ou si
		# le reseau de neurone n'avait pas ete modifier
		if self.file_modified == False:
			application_window = self.view.get_application_window ()
			application_window.quit ()

		return CALLBACK.SUCCEED


	#------------------------------------------------------------------------#

	def on_entry_validate (self, action, index, value_if_allowed, prior_value,
						  text, validation_type, trigger_type, widget_name,
						  key, text_type, text_length_max,
						  text_variable_bound_min, text_variable_bound_max):

		return self._entry_validate (
				   key = key,
				   value_if_allowed = value_if_allowed,
				   text_type = text_type,
				   text_length_max = text_length_max,
				   text_variable_bound_min = text_variable_bound_min, 
				   text_variable_bound_max = text_variable_bound_max)


	#------------------------------------------------------------------------#
	#																		 #
	#				   classe presenter_shape_recognition: 					 #
	#				  méthodes utilisées par les callbacks					 #
	#																		 #
	#------------------------------------------------------------------------#

	def _update_compared_canvas_dot_color (self, dot, mouse_button):
		new_dot_color = self._get_dot_new_color (mouse_button = mouse_button)

		self.modified_dots[:] = []
		self.modified_dots = [{CANVAS.DOT : dot,
							   CANVAS.DOT_COLOR : new_dot_color}]


	#------------------------------------------------------------------------#

	def _update_compared_input_state (self, dot, mouse_button):
		compared_input_index = self._get_compared_input_index_by_dot_position (
								   dot = dot)

		new_compared_input_state = self.get_compared_input_new_state (
									   mouse_button = mouse_button)

		self.model.update_compared_input_state (
			index = compared_input_index,
			new_state = new_compared_input_state)


	#------------------------------------------------------------------------#

	def _set_mouse_wheel_counter (self, mouse_button, counter):
		if mouse_button == MOUSE.WHEEL_UP:
			if counter > self.mouse_wheel_counter_min:
				counter -= 1
			else:
				counter = self.mouse_wheel_counter_max
		else:
			if counter < self.mouse_wheel_counter_max:
				counter += 1
			else:
				counter = self.mouse_wheel_counter_min

		return counter

	#------------------------------------------------------------------------#

	def _set_mouse_wheel_counter_max_to_neuron_count (self):
		self.mouse_wheel_counter_max = self.model.get_neuron_count () - 1


	#------------------------------------------------------------------------#

	def _set_mouse_wheel_counter_max_to_neuron_variant_count (self, neuron):
		neuron_variant_count = self.model.get_neuron_variant_count (
								   neuron = neuron)

		self.mouse_wheel_counter_max = neuron_variant_count - 1


	#------------------------------------------------------------------------#

	def _create_treeview_new_items (self, olds, news):
		treeview_items = []

		for name, value in zip (olds, news):
			treeview_items.append ((name, value))

		return treeview_items


	#------------------------------------------------------------------------#

	def _set_all_widgets_to_refresh (self):
		self.modified_dots[:] = []
		self.mouse_last_clicked_button = None
		self.mouse_last_dot_position = None

		self.compared_canvas_modified = True
		self.compared_canvas_mouse_button_released = True
		self.entry_create_neuron_modified = True
		self.combo_box_add_shape_modified = True
		self.combo_box_correct_neuron_modified = True
		self.treeview_learning_informations_modified = True
		self.entry_iteration_max_modified = True
		self.entry_correction_modified = True


	#------------------------------------------------------------------------#

	def _has_mouse_last_clicked_button_changed (self, mouse_button):
		if self.mouse_last_clicked_button != mouse_button:
			return True
		else:
			return False


	#------------------------------------------------------------------------#

	def _set_mouse_last_clicked_button (self, mouse_button):
		self.mouse_last_clicked_button = mouse_button


	#------------------------------------------------------------------------#

	def _has_mouse_last_dot_position_changed (self, dot):
		if self.mouse_last_dot_position != dot:
			return True
		else:
			return False


	#------------------------------------------------------------------------#

	def _update_mouse_last_dot_position (self, new_position):
		self.mouse_last_dot_position = new_position


	#------------------------------------------------------------------------#

	def get_compared_input_new_state (self, mouse_button):
		if mouse_button == MOUSE.LEFT_CLICK \
		or mouse_button == MOUSE.LEFT_CLICK_MOVE:
			return NEURON.INPUT_ACTIVATED
		else:
			return NEURON.INPUT_INACTIVATED


	#------------------------------------------------------------------------#

	def _get_dot_new_color (self, mouse_button):
		if mouse_button == MOUSE.LEFT_CLICK \
		or mouse_button == MOUSE.LEFT_CLICK_MOVE:
			return CANVAS.DOT_ACTIVATED_COLOR
		else:
			return CANVAS.DOT_INACTIVATED_COLOR


	#------------------------------------------------------------------------#

	def _get_compared_input_index_by_dot_position (self, dot):
		return  (dot.y * NEURON.INPUT_X_COUNT) + dot.x


	#------------------------------------------------------------------------#

	def _is_mouse_in_compared_canvas (self, mouse_abs):
		compared_canvas = self.view.get_canvas (
					   key = WIDGET.COMPARED_CANVAS)

		(left, top, right, bottom) = self._get_canvas_edge_rect (
									 canvas = compared_canvas,
									 absolute = True)

		if mouse_abs.x > (left + CANVAS.BD) \
			and mouse_abs.y > (top + CANVAS.BD) \
			and mouse_abs.x <= (right - CANVAS.BD) \
			and mouse_abs.y <= (bottom - CANVAS.BD):
			return True
		else:
			return False


	#------------------------------------------------------------------------#

	def _get_compared_canvas_dot_at_mouse_position (self, mouse):
		mouse.x -= CANVAS.BD + 1
		mouse.y -= CANVAS.BD + 1
		dot = Point (int(mouse.x / CANVAS.DOT_PIXEL_SIZE),
					int (mouse.y / CANVAS.DOT_PIXEL_SIZE))

		return dot


	#------------------------------------------------------------------------#

	def _get_canvas_dot_rect (self, dot):
		left = (dot.x * CANVAS.DOT_PIXEL_SIZE) + CANVAS.BD
		top = (dot.y * CANVAS.DOT_PIXEL_SIZE) + CANVAS.BD

		right = ((dot.x + 1) * CANVAS.DOT_PIXEL_SIZE)
		bottom = ((dot.y + 1) * CANVAS.DOT_PIXEL_SIZE)

		return (left, top, right, bottom)


	#------------------------------------------------------------------------#

	def _get_canvas_edge_rect (self, canvas, absolute = False):
		if absolute == False:
			left = CANVAS.BD
			top = CANVAS.BD

			right = (CANVAS.DOT_X_COUNT * CANVAS.DOT_PIXEL_SIZE) + CANVAS.BD
			bottom = (CANVAS.DOT_Y_COUNT * CANVAS.DOT_PIXEL_SIZE) + CANVAS.BD
		else:
			left = canvas.winfo_rootx ()
			top = canvas.winfo_rooty ()

			right = canvas.winfo_rootx () + canvas.winfo_width()
			bottom = canvas.winfo_rooty () + canvas.winfo_height()

		return (left, top, right, bottom)


	#------------------------------------------------------------------------#

	def convert_activated_inputs_to_activated_dots (self, inputs):
		dots = []

		for input_ in inputs:
			dot = Point (input_ % CANVAS.DOT_X_COUNT,
						int (input_ / CANVAS.DOT_X_COUNT))

			dots.append ({CANVAS.DOT: dot,
						 CANVAS.DOT_COLOR: CANVAS.DOT_ACTIVATED_COLOR})

		return dots


	#------------------------------------------------------------------------#

	def _get_canvas_modified_dots_rect_to_draw (self,
												canvas, 
												modified_dots,
												color):
		canvas_modified_dots_rect = []

		for modified_dot in modified_dots:
			if color == modified_dot[CANVAS.DOT_COLOR]:
				canvas_modified_dots_rect.append ( \
					self._get_canvas_dot_rect ( \
						dot = modified_dot[CANVAS.DOT]))

		return canvas_modified_dots_rect


	# -----------------------------------------------------------------------#

	def _clean_canvas (self, canvas):
		canvas_edge_rect = self._get_canvas_edge_rect (canvas = canvas)

		self.view.draw_on_canvas (key = canvas,
								  dots_rect = [canvas_edge_rect],
								  color = CANVAS.DOT_INACTIVATED_COLOR)


	#------------------------------------------------------------------------#
	
	def _get_learning_informations (self):
		neuron_count = self.model.get_neuron_count ()
		neuron_valid_count = self.model.get_neuron_valid_count ()

		iteration = self.model.get_iteration ()
		iteration_total = self.model.get_iteration_total ()

		elapsed_time = self.model.get_elapsed_time ()
		elapsed_time_total = self.model.get_elapsed_time_total ()

		current_error = self.model.get_error ()

		learning_informations = [str (neuron_count), 
								 str (neuron_valid_count),
								 str (iteration),
								 str (iteration_total),
								 str (elapsed_time) \
								 + TEXT.MILLI_SECONDS,
								 str (elapsed_time_total) \
								 + TEXT.MILLI_SECONDS,
								 str (current_error) \
								 + TEXT.PERCENTAGE]

		return learning_informations

	def reset_counters (self):
		self.neuron_selected_to_correct = 0
		self.neuron_selected_to_show = 0
		self.neuron_last_selected_selected_to_show = 0
		self.neuron_variant_selected_to_show = 0
		self.neuron_variant_last_selected_to_show = 0
		self.mouse_wheel_counter_min = 0
		self.mouse_wheel_counter_max = 0
		self.keyboard_ctrl_state = KEYBOARD.CTRL_RELEASED
		self.keyboard_shiftl_state = KEYBOARD.SHIFTL_RELEASED

	#------------------------------------------------------------------------#
	#																		 #
	#				   classe presenter_shape_recognition: 					 #
	#			méthodes utilisées par les callbacks de file_menu			 #
	#																		 #
	#------------------------------------------------------------------------#

	def _get_file_name (self, command):
		current_dir = os.getcwd ()

		filetypes = (DIALOG.FILE_TYPES, DIALOG.ALL_FILE_TYPES)

		if command == DIALOG.OPEN:
			return filedialog.askopenfilename (initialdir = current_dir, 
											  title = DIALOG.TITLE,
											  filetypes = filetypes)
		elif command == DIALOG.SAVEAS:
			return filedialog.asksaveasfilename (initialdir = current_dir, 
												title = DIALOG.TITLE,
												filetypes = filetypes)
		else:
			return DIALOG.NO_NAME_GIVEN


	#------------------------------------------------------------------------#

	def _ask_file_saving (self):
		# appel de la callback d'apprentissage automatique du reseau de neurones dans le modèle
		answer = self.view.show_ask_saving_box (
					 title = DIALOG.ASK_SAVING_TITLE,
					 text = DIALOG.ASK_SAVING_MESSAGE)
		if answer == True:

			if self.file_name:
				self._save_file (file_name = self.file_name)

				self.file_modified = False
			else:
				file_name = self._save_as_file ()

				if file_name:
					self.file_modified = False
		else:
			if answer == False:
				self.file_modified = False


	#------------------------------------------------------------------------#

	def _new_file (self):
		# met à jour le nom du fichier courant
		self.file_name = FILE.NO_NAME_GIVEN

		self.reset_counters ()
		self._clean_canvas (canvas = WIDGET.COMPARED_CANVAS)
		self._set_all_widgets_to_refresh ()

		# mise à jour de la liste des noms de la combobox de correction des neurones et
		# les widgets concernés dans la vue
		self.model = models.ModelShapeRecognition ()


	#------------------------------------------------------------------------#

	def _open_file (self):

		file_name = self._get_file_name (command = DIALOG.OPEN)

		if file_name:
			# met à jour le nom du fichier courant
			self.file_name = file_name

			self.reset_counters ()
			self._set_all_widgets_to_refresh ()

			# charge la sauvegarde
			file = open (file_name, FILE.READING_MODE)
			self.model = dill.load (file)
			file.close ()

			# initialise les valeurs d'entrée du réseau de neurone
			activated_inputs = self.model.get_activated_inputs (
							   for_compared_input = False,
							   neuron = self.neuron_selected_to_show,
							   variant = self.neuron_variant_selected_to_show)

			self.modified_dots = self.convert_activated_inputs_to_activated_dots (inputs = activated_inputs)

			self._set_mouse_wheel_counter_max_to_neuron_count ()

			return file_name
		else :
			return DIALOG.NO_NAME_GIVEN


	#------------------------------------------------------------------------#

	def _save_file (self, file_name):
		self.file_name = file_name

		file = open (file_name, FILE.WRITING_MODE)
		dill.dump (self.model, file)
		file.close ()


	#------------------------------------------------------------------------#

	def _save_as_file (self):
		file_name = self._get_file_name (command = DIALOG.SAVEAS)

		if file_name:
			self._save_file (file_name = file_name)

			return file_name
		else :
			return DIALOG.NO_NAME_GIVEN


	#------------------------------------------------------------------------#

	def _entry_validate (self,
						 key,
						 value_if_allowed,
						 text_type,
						 text_length_max,
						 text_variable_bound_min,
						 text_variable_bound_max):

		if len (value_if_allowed):
			if is_entry_text_valid (text = value_if_allowed,
								    text_type = text_type):

				if are_bounds_valid (text = value_if_allowed,
									 text_type = text_type,
									 text_length_max = text_length_max,
									 min_ = text_variable_bound_min,
									 max_ = text_variable_bound_max):
					self.file_modified = True

					if key == WIDGET.ENTRY_ITERATION_MAX:
						self.model.set_iteration_max (iteration_max = int (value_if_allowed))
						self.entry_iteration_max_modified = True
					if key == WIDGET.ENTRY_CORRECTION:
						self.model.set_correction (correction = float (value_if_allowed))
						self.entry_correction_modified = True

					value_if_allowed

					return True
				else:
					message = { ERROR.TITLE_KEY: "attention", 
								ERROR.MESSAGE_KEY: "valeur incorrecte" }

					self.view.show_warning (message = message)
					return False
			else:
				return False
		else:
			value_if_allowed
			return True


	#------------------------------------------------------------------------#
	#																		 #
	#				   classe presenter_shape_recognition: 					 #
	#				   méthodes de mise à jour de la vue					 #
	#																		 #
	#------------------------------------------------------------------------#

	def _update_canvas (self, canvas, modified_dots):
		colors = [CANVAS.DOT_INACTIVATED_COLOR, CANVAS.DOT_ACTIVATED_COLOR]

		for color in colors:
			canvas_modified_dots_rect \
				= self._get_canvas_modified_dots_rect_to_draw (
				canvas = canvas,
				modified_dots = modified_dots,
				color = color)

			# dessine l'ensemble des points activés du canvas output dans la vue
			self.view.draw_on_canvas (key = canvas,
									  dots_rect = canvas_modified_dots_rect,
									  color = color)


	#------------------------------------------------------------------------#

	def _update_compared_canvas (self):
		self._update_canvas (canvas = WIDGET.COMPARED_CANVAS,
							 modified_dots = self.modified_dots)


	# -----------------------------------------------------------------------#

	def _update_output_canvas (self):
		# si au moins un neurone a été créé
		if self.model.get_neuron_count ():
			if self.neuron_selected_to_show == NEURON.INDEX_DONT_EXIST:
				self.view.set_label_text (
					key = WIDGET.LABEL_SHAPE_DRAWN_TWO,
					text = WIDGET.LABEL_SHAPE_DRAWN_TWO_INITIAL_TEXT)

				self.view.set_label_text (
					key = WIDGET.LABEL_SHAPE_DRAWN_THREE,
					text = WIDGET.LABEL_SHAPE_DRAWN_THREE_INITIAL_TEXT)
			else:
				neuron_name = self.model.get_neuron_name (
								  neuron = self.neuron_selected_to_show)

				self.view.set_label_text (
					key = WIDGET.LABEL_SHAPE_DRAWN_TWO,
					text = WIDGET.LABEL_SHAPE_DRAWN_TWO_INITIAL_TEXT 
						   + neuron_name)

				self.view.set_label_text (
					key = WIDGET.LABEL_SHAPE_DRAWN_THREE,
					text = WIDGET.LABEL_SHAPE_DRAWN_THREE_INITIAL_TEXT 
						   + str (self.neuron_variant_selected_to_show))
			
			# recupere la liste des entrés activés du neurone
			(activated_outputs, name) = self.model.get_activated_outputs()

			name = WIDGET.LABEL_SHAPE_RECOGNIZED_TWO_INITIAL_TEXT + name

			self.view.set_label_text (key = WIDGET.LABEL_SHAPE_RECOGNIZED_TWO, 
									  text = name)

			activated_output_dots = self.convert_activated_inputs_to_activated_dots (inputs \
														 = activated_outputs)

			if activated_output_dots:
				self._clean_canvas (canvas = WIDGET.OUTPUT_CANVAS)

				self._update_canvas (canvas = WIDGET.OUTPUT_CANVAS,
									 modified_dots = activated_output_dots)
			else:
				self._clean_canvas (canvas = WIDGET.OUTPUT_CANVAS)

				self.view.set_label_text (
					key = WIDGET.LABEL_SHAPE_RECOGNIZED_TWO,
					text = WIDGET.LABEL_SHAPE_RECOGNIZED_TWO_INITIAL_TEXT)
		else:
			self._clean_canvas (canvas = WIDGET.OUTPUT_CANVAS)

			self.view.set_label_text (
				key = WIDGET.LABEL_SHAPE_DRAWN_TWO,
				text = WIDGET.LABEL_SHAPE_DRAWN_TWO_INITIAL_TEXT)

			self.view.set_label_text (
				key = WIDGET.LABEL_SHAPE_DRAWN_THREE,
				text = WIDGET.LABEL_SHAPE_DRAWN_THREE_INITIAL_TEXT)		
						
			self.view.set_label_text (
				key = WIDGET.LABEL_SHAPE_RECOGNIZED_TWO,
				text = WIDGET.LABEL_SHAPE_RECOGNIZED_TWO_INITIAL_TEXT)


	# -----------------------------------------------------------------------#

	def _update_compared_canvas_neuron_current_selection (self):
		self.modified_dots[:] = []
		self.neuron_last_selected_selected_to_show \
		= self.neuron_selected_to_show

		self.neuron_variant_selected_to_show = NEURON.FIRST_INPUT_VARIANT
		self.neuron_variant_last_selected_to_show = 0

		neuron_name = self.model.get_neuron_name (
						  neuron = self.neuron_selected_to_show)

		neuron_inputs = self.model.get_neuron_inputs (
							neuron = self.neuron_selected_to_show,
							variant = self.neuron_variant_selected_to_show)

		for synapse in range (NEURON.SYNAPSE_COUNT):
			self.model.update_compared_input_state (
				index = synapse,
				new_state = neuron_inputs[synapse])

		activated_inputs = self.model.get_activated_inputs (
							   for_compared_input = False,
							   neuron = self.neuron_selected_to_show,
							   variant = self.neuron_variant_selected_to_show)

		self.modified_dots = self.convert_activated_inputs_to_activated_dots (inputs = activated_inputs)

		self.view.set_label_text (
			key = WIDGET.LABEL_SHAPE_DRAWN_TWO,
			text = WIDGET.LABEL_SHAPE_DRAWN_TWO_INITIAL_TEXT + neuron_name)

		self.view.set_label_text (
			key = WIDGET.LABEL_SHAPE_DRAWN_THREE,
			text = WIDGET.LABEL_SHAPE_DRAWN_THREE_INITIAL_TEXT
				   + str (self.neuron_variant_selected_to_show))

		self._clean_canvas (canvas = WIDGET.COMPARED_CANVAS)
		self._update_compared_canvas ()


	# -----------------------------------------------------------------------#

	def _update_compared_canvas_neuron_variant_current_selection (self):
		self.modified_dots[:] = []
		self.neuron_variant_last_selected_to_show \
		= self.neuron_variant_selected_to_show
		
		neuron_name = self.model.get_neuron_name (
						  neuron = self.neuron_selected_to_show)

		neuron_inputs = self.model.get_neuron_inputs (
							neuron = self.neuron_selected_to_show,
							variant = self.neuron_variant_selected_to_show)

		for synapse in range (NEURON.SYNAPSE_COUNT):
			self.model.update_compared_input_state (
				index = synapse,
				new_state = neuron_inputs[synapse])

		activated_inputs = self.model.get_activated_inputs (
							   for_compared_input = False,
							   neuron = self.neuron_selected_to_show,
							   variant = self.neuron_variant_selected_to_show)

		self.modified_dots = self.convert_activated_inputs_to_activated_dots (inputs = activated_inputs)

		self.view.set_label_text (
			key = WIDGET.LABEL_SHAPE_DRAWN_TWO,
			text = WIDGET.LABEL_SHAPE_DRAWN_TWO_INITIAL_TEXT + neuron_name)
		
		self.view.set_label_text (
			key = WIDGET.LABEL_SHAPE_DRAWN_THREE,
			text = WIDGET.LABEL_SHAPE_DRAWN_THREE_INITIAL_TEXT
				   + str (self.neuron_variant_selected_to_show))

		self._clean_canvas (canvas = WIDGET.COMPARED_CANVAS)
		self._update_compared_canvas ()


	#------------------------------------------------------------------------#

	def _update_entry_create_neuron (self):
		self.view.set_entry_text (
			key = WIDGET.ENTRY_CREATE_NEURON,
			text = WIDGET.ENTRY_CREATE_NEURON_INITIAL_TEXT)


	#------------------------------------------------------------------------#

	def _update_combo_box_add_shape (self):
		# recuperation de la liste de noms des neurones créés
		neuron_names = self.model.get_neuron_names ()

		# mise à jour de la liste des noms des neurones de la combobox de correction
		self.view.set_combo_box_values (key = WIDGET.COMBO_BOX_ADD_SHAPE,
									    values = neuron_names)

		if self.model.get_neuron_count ():
			if self.neuron_selected_to_show >= 0:
				self.view.set_combo_box_index (
					key = WIDGET.COMBO_BOX_ADD_SHAPE,
					index = self.neuron_selected_to_show)
			else:
				self.view.set_combo_box_text (
					key = WIDGET.COMBO_BOX_ADD_SHAPE,
					text = WIDGET.COMBO_BOX_ADD_SHAPE_INITIAL_TEXT)
		else:
			self.view.set_combo_box_text (
				key = WIDGET.COMBO_BOX_ADD_SHAPE,
				text = WIDGET.COMBO_BOX_ADD_SHAPE_INITIAL_TEXT)


	#------------------------------------------------------------------------#

	def _update_combo_box_add_shape_current_selection (self):
		self.view.set_combo_box_index (key = WIDGET.COMBO_BOX_ADD_SHAPE,
									   index = self.neuron_selected_to_show)


	#------------------------------------------------------------------------#

	def _update_combo_box_correct_neuron (self):
		# recuperation de la liste de noms des neurones créés
		neuron_names = self.model.get_neuron_names ()

		# mise à jour de la liste des noms des neurones de la combobox de correction
		self.view.set_combo_box_values (key = WIDGET.COMBO_BOX_CORRECT_NEURON,
									   values = neuron_names)

		if self.neuron_selected_to_correct:
			self.view.set_combo_box_index (
				key = WIDGET.COMBO_BOX_CORRECT_NEURON,
				index = self.neuron_selected_to_correct)
		else:
			self.view.set_combo_box_text (
						key = WIDGET.COMBO_BOX_CORRECT_NEURON,
						text = WIDGET.COMBO_BOX_CORRECT_NEURON_INITIAL_TEXT)


	# -----------------------------------------------------------------------#

	def _update_combo_box_correct_neuron_current_selection (self):
		self.view.set_combo_box_index (key = WIDGET.COMBO_BOX_CORRECT_NEURON,
									   index = self.neuron_selected_to_correct)


	#------------------------------------------------------------------------#

	def _update_entry_iteration_max (self):
		iteration_max = self.model.get_iteration_max ()

		self.view.set_entry_text (key = WIDGET.ENTRY_ITERATION_MAX,
								  text = iteration_max)


	#------------------------------------------------------------------------#

	def _update_entry_correction (self):
		correction = self.model.get_correction ()
		
		self.view.set_entry_text (key = WIDGET.ENTRY_CORRECTION,
								  text = correction)


	#------------------------------------------------------------------------#

	def _update_treeview_learning_informations (self):
		# recupère la liste des caractéristiques du réseau de neurones
		new_learning_informations = self._get_learning_informations ()

		old_treeview_items = self.view.get_treeview_items (
							 key = WIDGET.TREEVIEW_LEARNING_INFORMATIONS)

		# met à jour la liste des caractéristiques du réseau de neurones du treeview
		treeview_items = self._create_treeview_new_items (
							 olds = old_treeview_items,
							 news = new_learning_informations)

		# met à jour le treeview des caractéristiques du réseau de neurones dans la vue
		self.view.update_treeview_items (
			key = WIDGET.TREEVIEW_LEARNING_INFORMATIONS,
			items = treeview_items)


	#------------------------------------------------------------------------#

	def _update_view (self):
		if self.compared_canvas_modified:
			self.compared_canvas_modified = False
			self._update_compared_canvas ()

		if self.compared_canvas_neuron_current_selection_modified:
			self.compared_canvas_neuron_current_selection_modified = False
			self._update_compared_canvas_neuron_current_selection ()

		if self.compared_canvas_neuron_variant_current_selection_modified:
			self.compared_canvas_neuron_variant_current_selection_modified = False
			self._update_compared_canvas_neuron_variant_current_selection ()

		if self.compared_canvas_mouse_button_released:
			self.compared_canvas_mouse_button_released = False
			self._update_output_canvas ()

		# la condition suivante est seulement utilisé lors de la creation d'un
		# nouveau reseau de neurones

		if self.entry_create_neuron_modified:
			self.entry_create_neuron_modified = False
			self._update_entry_create_neuron ()

		if self.combo_box_add_shape_modified:
			self.combo_box_add_shape_modified = False
			self._update_combo_box_add_shape ()

		if self.combo_box_add_shape_current_selection_modified:
			self.combo_box_add_shape_current_selection_modified = False
			self._update_combo_box_add_shape_current_selection ()

		if self.combo_box_correct_neuron_modified:
			self.combo_box_correct_neuron_modified = False
			self._update_combo_box_correct_neuron ()

		if self.combo_box_correct_neuron_current_selection_modified:
			self.combo_box_correct_neuron_current_selection_modified = False
			self._update_combo_box_correct_neuron_current_selection ()

		if self.entry_iteration_max_modified:
			self.entry_iteration_max_modified = False
			self._update_entry_iteration_max ()

		if self.entry_correction_modified:
			self.entry_correction_modified = False
			self._update_entry_correction ()

		if self.treeview_learning_informations_modified:
			self.treeview_learning_informations_modified = False
			self._update_treeview_learning_informations ()


	#------------------------------------------------------------------------#
	#																		 #
	#				   classe presenter_shape_recognition: 					 #
	#				     listes des propriétés variables					 #
	#																		 #
	#------------------------------------------------------------------------#

	@property
	def model (self):
		return self._model

	@model.setter
	def model (self, model):
		self._model = model


	#------------------------------------------------------------------------#

	@property
	def view (self):
		return self._view

	@view.setter
	def view (self, view):
		self._view = view


	#------------------------------------------------------------------------#

	@property
	def interactor (self):
		return self._interactor

	@interactor.setter
	def interactor (self, interactor):
		self._interactor = interactor


	#------------------------------------------------------------------------#

	@property
	def compared_canvas_mouse_button_released (self):
		return self._compared_canvas_mouse_button_released

	@compared_canvas_mouse_button_released.setter
	def compared_canvas_mouse_button_released (self, compared_canvas_mouse_button_released):
		self._compared_canvas_mouse_button_released = compared_canvas_mouse_button_released


	#------------------------------------------------------------------------#

	@property
	def compared_canvas_neuron_current_selection_modified (self):
		return self._compared_canvas_neuron_current_selection_modified

	@compared_canvas_neuron_current_selection_modified.setter
	def compared_canvas_neuron_current_selection_modified (
		self, compared_canvas_neuron_current_selection_modified):
		self._compared_canvas_neuron_current_selection_modified \
			= compared_canvas_neuron_current_selection_modified


	#------------------------------------------------------------------------#

	@property
	def compared_canvas_neuron_variant_current_selection_modified (self):
		return self._compared_canvas_neuron_variant_current_selection_modified

	@compared_canvas_neuron_variant_current_selection_modified.setter
	def compared_canvas_neuron_variant_current_selection_modified (
		self, compared_canvas_neuron_variant_current_selection_modified):
		self._compared_canvas_neuron_variant_current_selection_modified \
			= compared_canvas_neuron_variant_current_selection_modified



	#------------------------------------------------------------------------#

	@property
	def mouse_last_clicked_button (self):
		return self._mouse_last_clicked_button

	@mouse_last_clicked_button.setter
	def mouse_last_clicked_button (self, mouse_last_clicked_button):
		self._mouse_last_clicked_button = mouse_last_clicked_button


	#------------------------------------------------------------------------#

	@property
	def mouse_last_dot_position (self):
		return self._mouse_last_dot_position

	@mouse_last_dot_position.setter
	def mouse_last_dot_position (self, mouse_last_dot_position):
		self._mouse_last_dot_position = mouse_last_dot_position


	#------------------------------------------------------------------------#

	@property
	def modified_dots (self):
		return self._modified_dots

	@modified_dots.setter
	def modified_dots (self, modified_dots):
		self._modified_dots = modified_dots


	#------------------------------------------------------------------------#

	@property
	def neuron_selected_to_correct (self):
		return self._neuron_selected_to_correct

	@neuron_selected_to_correct.setter
	def neuron_selected_to_correct (self, neuron_selected_to_correct):
		self._neuron_selected_to_correct = neuron_selected_to_correct


	#------------------------------------------------------------------------#

	@property
	def neuron_selected_to_show (self):
		return self._neuron_selected_to_show

	@neuron_selected_to_show.setter
	def neuron_selected_to_show (self, neuron_selected_to_show):
		self._neuron_selected_to_show = neuron_selected_to_show


	#------------------------------------------------------------------------#

	@property
	def neuron_last_selected_selected_to_show (self):
		return self._neuron_last_selected_selected_to_show

	@neuron_last_selected_selected_to_show.setter
	def neuron_last_selected_selected_to_show (self, neuron_last_selected_selected_to_show):
		self._neuron_last_selected_selected_to_show = neuron_last_selected_selected_to_show


	#------------------------------------------------------------------------#

	@property
	def neuron_variant_selected_to_show (self):
		return self._neuron_variant_selected_to_show

	@neuron_variant_selected_to_show.setter
	def neuron_variant_selected_to_show (self, neuron_variant_selected_to_show):
		self._neuron_variant_selected_to_show = neuron_variant_selected_to_show


	#------------------------------------------------------------------------#

	@property
	def neuron_variant_last_selected_to_show (self):
		return self._neuron_variant_last_selected_to_show

	@neuron_variant_last_selected_to_show.setter
	def neuron_variant_last_selected_to_show (self, neuron_variant_last_selected_to_show):
		self._neuron_variant_last_selected_to_show = neuron_variant_last_selected_to_show


	#------------------------------------------------------------------------#

	@property
	def mouse_wheel_counter_min (self):
		return self._mouse_wheel_counter_min

	@mouse_wheel_counter_min.setter
	def mouse_wheel_counter_min (self, mouse_wheel_counter_min):
		self._mouse_wheel_counter_min = mouse_wheel_counter_min


	#------------------------------------------------------------------------#

	@property
	def mouse_wheel_counter_max (self):
		return self._mouse_wheel_counter_max

	@mouse_wheel_counter_max.setter
	def mouse_wheel_counter_max (self, mouse_wheel_counter_max):
		self._mouse_wheel_counter_max = mouse_wheel_counter_max


	#------------------------------------------------------------------------#

	@property
	def keyboard_ctrl_state (self):
		return self._keyboard_ctrl_state

	@keyboard_ctrl_state.setter
	def keyboard_ctrl_state (self, keyboard_ctrl_state):
		self._keyboard_ctrl_state = keyboard_ctrl_state


	#------------------------------------------------------------------------#

	@property
	def keyboard_shiftl_state (self):
		return self._keyboard_shiftl_state

	@keyboard_shiftl_state.setter
	def keyboard_shiftl_state (self, keyboard_shiftl_state):
		self._keyboard_shiftl_state = keyboard_shiftl_state


	#------------------------------------------------------------------------#

	@property
	def file_name (self):
		return self._file_name

	@file_name.setter
	def file_name (self, file_name):
		self._file_name = file_name

	#------------------------------------------------------------------------#

	@property
	def file_modified (self):
		return self._file_modified

	@file_modified.setter
	def file_modified (self, file_modified):
		self._file_modified = file_modified


	#------------------------------------------------------------------------#

	@property
	def compared_canvas_modified (self):
		return self._compared_canvas_modified

	@compared_canvas_modified.setter
	def compared_canvas_modified (self, compared_canvas_modified):
		self._compared_canvas_modified = compared_canvas_modified


	#------------------------------------------------------------------------#

	@property
	def entry_create_neuron_modified (self):
		return self._entry_create_neuron_modified

	@entry_create_neuron_modified.setter
	def entry_create_neuron_modified (self, entry_create_neuron_modified):
		self._entry_create_neuron_modified = entry_create_neuron_modified


	#------------------------------------------------------------------------#

	@property
	def combo_box_add_shape_modified (self):
		return self._combo_box_add_shape_modified

	@combo_box_add_shape_modified.setter
	def combo_box_add_shape_modified (self, combo_box_add_shape_modified):
		self._combo_box_add_shape_modified = combo_box_add_shape_modified


	#------------------------------------------------------------------------#

	@property
	def combo_box_add_shape_current_selection_modified (self):
		return self._combo_box_add_shape_current_selection_modified

	@combo_box_add_shape_current_selection_modified.setter
	def combo_box_add_shape_current_selection_modified (self, combo_box_add_shape_current_selection_modified):
		self._combo_box_add_shape_current_selection_modified = combo_box_add_shape_current_selection_modified


	#------------------------------------------------------------------------#

	@property
	def combo_box_correct_neuron_modified (self):
		return self._combo_box_correct_neuron_modified

	@combo_box_correct_neuron_modified.setter
	def combo_box_correct_neuron_modified (self, combo_box_correct_neuron_modified):
		self._combo_box_correct_neuron_modified = combo_box_correct_neuron_modified


	#------------------------------------------------------------------------#

	@property
	def combo_box_correct_neuron_current_selection_modified (self):
		return self._combo_box_correct_neuron_current_selection_modified

	@combo_box_correct_neuron_current_selection_modified.setter
	def combo_box_correct_neuron_current_selection_modified (self, combo_box_correct_neuron_current_selection_modified):
		self._combo_box_correct_neuron_current_selection_modified = combo_box_correct_neuron_current_selection_modified


	#------------------------------------------------------------------------#

	@property
	def entry_iteration_max_modified (self):
		return self._entry_iteration_max_modified

	@entry_iteration_max_modified.setter
	def entry_iteration_max_modified (self, entry_iteration_max_modified):
		self._entry_iteration_max_modified = entry_iteration_max_modified


	#------------------------------------------------------------------------#

	@property
	def entry_correction_modified (self):
		return self._entry_correction_modified

	@entry_correction_modified.setter
	def entry_correction_modified (self, entry_correction_modified):
		self._entry_correction_modified = entry_correction_modified


	#------------------------------------------------------------------------#

	@property
	def treeview_learning_informations_modified (self):
		return self._treeview_learning_informations_modified

	@treeview_learning_informations_modified.setter
	def treeview_learning_informations_modified (self, treeview_learning_informations_modified):
		self._treeview_learning_informations_modified = treeview_learning_informations_modified
