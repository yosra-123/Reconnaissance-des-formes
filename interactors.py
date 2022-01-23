

import tkinter
from functools import partial

import constants

# declaration des propriétés constantes
APPLICATION = constants.Application
MENU = constants.Menu
CALLBACK = constants.Callback
MOUSE = constants.Mouse
WIDGET = constants.Widget
CANVAS = constants.Canvas
Point = constants.Point

class InteractorShapeRecognition(object):

	def bind_view_to_presenter(self, presenter, view):
		# declaration des propriétés variables
		
		self._view = view
		self._presenter = presenter


		# -------------------------------------------------------------------#

		# assignation des callbacks
		compared_canvas = view.get_canvas(key = WIDGET.COMPARED_CANVAS)
		button_create_neuron = view.get_button(key = WIDGET.BUTTON_CREATE_NEURON)
		button_add_shape = view.get_button(key = WIDGET.BUTTON_ADD_SHAPE)
		button_correct_neuron = view.get_button(key = WIDGET.BUTTON_CORRECT_NEURON)
		button_auto_correct = view.get_button(key = WIDGET.BUTTON_AUTO_CORRECT)
		button_clean_shape = view.get_button(key = WIDGET.BUTTON_CLEAN_SHAPE)
		treeview_infos = view.get_treeview(key = WIDGET.TREEVIEW_LEARNING_INFORMATIONS)

		self.application_window = view.get_application_window()

		self._multiple_bind_with_mouse_button(
			compared_canvas,
			self._on_compared_canvas_mouse_button_clicked,
			MOUSE.LEFT_CLICK,
			MOUSE.LEFT_CLICK_MOVE,
			MOUSE.RIGHT_CLICK,
			MOUSE.RIGHT_CLICK_MOVE)

		self._multiple_bind_with_mouse_button(
			compared_canvas,
			self._on_compared_canvas_mouse_button_released,
			MOUSE.LEFT_RELEASED,
			MOUSE.RIGHT_RELEASED)

		self._multiple_bind_with_mouse_button(
			compared_canvas,
			self._on_compared_canvas_mouse_wheel_moved,
			MOUSE.WHEEL_UP,
			MOUSE.WHEEL_DOWN,
			MOUSE.WHEEL_WINDOWS_MOVED)

		compared_canvas.bind(MOUSE.WHEEL_CLICK,
						  partial(self._on_compared_canvas_mouse_wheel_clicked,
								  mouse_button = MOUSE.WHEEL_CLICK))

		self.application_window.bind_all("<Control_L>", 
										 self._on_keyboard_ctrl_pressed)
		self.application_window.bind_all("<KeyRelease-Control_L>",
										 self._on_keyboard_ctrl_released)
		self.application_window.bind_all("<Shift_L>", 
										 self._on_keyboard_shiftl_pressed)
		self.application_window.bind_all("<KeyRelease-Shift_L>",
										 self._on_keyboard_shiftl_released)
		
		button_create_neuron.bind(MOUSE.LEFT_CLICK,
								  self._on_create_neuron_button)

		button_add_shape.bind(MOUSE.LEFT_CLICK,
							  self._on_add_shape_button)

		button_correct_neuron.bind(MOUSE.LEFT_CLICK,
								   self._on_correct_neuron_button)

		button_auto_correct.bind(MOUSE.LEFT_CLICK,
								 self._on_auto_correct_button)

		button_clean_shape.bind(MOUSE.LEFT_CLICK,
								self._on_button_clean_shape)

		self._on_file_menu()

		self.application_window.protocol(APPLICATION.DELETE_WINDOW,
										 presenter.on_file_menu_quit)


	#------------------------------------------------------------------------#
	#																		 #
	#					classe interactor_shape_recognition: 				 #
	#							liste des callbacks							 #
	#																		 #
	#------------------------------------------------------------------------#

	def _on_compared_canvas_mouse_button_clicked(self, event, mouse_button):
		mouse = self._get_mouse_position(event = event)

		mouse_abs = self._get_mouse_position(event = event,
		 									 absolute = True)

		result = self.presenter.on_compared_canvas_mouse_button_clicked(
			   mouse = mouse,
			   mouse_abs = mouse_abs,
			   mouse_button = mouse_button)

		return result[CALLBACK.RETURN_VALUE]


	#------------------------------------------------------------------------#

	def _on_compared_canvas_mouse_button_released(self, event, mouse_button):
		result = self.presenter.on_compared_canvas_mouse_button_released()

		return result[CALLBACK.RETURN_VALUE]


	#------------------------------------------------------------------------#

	def _on_compared_canvas_mouse_wheel_clicked(self, event, mouse_button):
		result = self.presenter.on_compared_canvas_mouse_wheel_clicked()

		return result[CALLBACK.RETURN_VALUE]


	#------------------------------------------------------------------------#

	def _on_compared_canvas_mouse_wheel_moved(self, event, mouse_button):
		if APPLICATION.OS == APPLICATION.WINDOWS_OS:
			if event.delta == 120:
				mouse_button = MOUSE.WHEEL_UP
			else:
				mouse_button = MOUSE.WHEEL_DOWN

		result = self.presenter.on_compared_canvas_mouse_wheel_moved(
			   mouse_button = mouse_button)

		return result[CALLBACK.RETURN_VALUE]


	#------------------------------------------------------------------------#

	def _on_keyboard_ctrl_pressed(self, event):
		result = self.presenter.on_keyboard_ctrl_pressed()

		return result[CALLBACK.RETURN_VALUE]


	#------------------------------------------------------------------------#
	
	def _on_keyboard_ctrl_released(self, event):
		result = self.presenter.on_keyboard_ctrl_released()

		return result[CALLBACK.RETURN_VALUE]


	#------------------------------------------------------------------------#

	def _on_keyboard_shiftl_pressed(self, event):
		result = self.presenter.on_keyboard_shiftl_pressed()

		return result[CALLBACK.RETURN_VALUE]


	#------------------------------------------------------------------------#
	
	def _on_keyboard_shiftl_released(self, event):
		result = self.presenter.on_keyboard_shiftl_released()

		return result[CALLBACK.RETURN_VALUE]


	#------------------------------------------------------------------------#

	def _on_create_neuron_button(self, event):
		result = self.presenter.on_create_neuron_button()

		return result[CALLBACK.RETURN_VALUE]


	#------------------------------------------------------------------------#

	def _on_add_shape_button(self, event):
		result = self.presenter.on_add_shape_button()

		return result[CALLBACK.RETURN_VALUE]


	#------------------------------------------------------------------------#

	def _on_correct_neuron_button(self, event):
		result = self.presenter.on_correct_neuron_button()

		return result[CALLBACK.RETURN_VALUE]


	#------------------------------------------------------------------------#

	def _on_auto_correct_button(self, event):
		result = self.presenter.on_auto_correct_button()

		return result[CALLBACK.RETURN_VALUE]


	#------------------------------------------------------------------------#

	def _on_button_clean_shape(self, event):
		result = self.presenter.on_button_clean_shape()

		return result[CALLBACK.RETURN_VALUE]


	#------------------------------------------------------------------------#
	def _on_file_menu(self):
		# création du menu et des diverses commandes associées
		menubar = tkinter.Menu(self.application_window)

		file_menu = tkinter.Menu(menubar, 
								 tearoff = 0)

		file_menu.add_command(label = MENU.FILE_LABEL_NEW, 
							  command = self.presenter.on_file_menu_new)

		file_menu.add_command(label = MENU.FILE_LABEL_OPEN, 
							  command = self.presenter.on_file_menu_open)

		file_menu.add_separator()

		file_menu.add_command(label = MENU.FILE_LABEL_SAVE, 
							  command = self.presenter.on_file_menu_save)

		file_menu.add_command(label = MENU.FILE_LABEL_SAVE_AS, 
							  command = self.presenter.on_file_menu_save_as)

		file_menu.add_separator()

		file_menu.add_command(label = MENU.FILE_LABEL_QUIT, 
							  command = self.presenter.on_file_menu_quit)

		menubar.add_cascade(label = MENU.FILE_LABEL, 
							menu = file_menu)

		self.application_window.config(menu = menubar)


	#------------------------------------------------------------------------#

	def _get_mouse_position(self, event, absolute = False):
		if absolute == False:
			position = Point(event.x,
							 event.y)
		else:
			position = Point(event.x_root,
							 event.y_root)

		return position


	#------------------------------------------------------------------------#

	def _multiple_bind_with_mouse_button(self, widget, callback, *mouse_buttons):
		for mouse_button in mouse_buttons: 
			widget.bind(mouse_button,
						partial(callback,
							  	mouse_button = mouse_button))


	#------------------------------------------------------------------------#
	#																		 #
	#					classe interactor_shape_recognition: 				 #
	#							liste des propriétés						 #
	#																		 #
	#------------------------------------------------------------------------#

	@property
	def view(self):
		return self._view
	
	@view.setter
	def view(self, view):
		self._view = view	


	#------------------------------------------------------------------------#

	@property
	def presenter(self):
		return self._presenter

	@presenter.setter
	def presenter(self, presenter):
		self._presenter = presenter
