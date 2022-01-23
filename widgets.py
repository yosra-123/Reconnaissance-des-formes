
import tkinter
import tkinter.ttk as ttk

import constants

APPLICATION = constants.Application
CANVAS = constants.Canvas
WIDGET = constants.Widget

class Widgets(object):

	def __init__(self, entry_command):
		# declaration des propriétés variables
		self._application_window = tkinter.Tk()
		self._canvas = {}
		self._label = {}
		self._button = {}
		self._check_box = {}
		self._entry = {}
		self._treeview = {}
		self._combo_box = {}
		self._main_frame = None

		self._entry_width = 24

		self._padding_x = 0
		self._padding_y = 0
		self._i_padding_x = 0
		self._i_padding_y = 0

		self._entry_command = entry_command

	#------------------------------------------------------------------------#
	#																		 #
	#					 		 classe widgets: 							 #
	#				listes des méthodes utilisées par la vue				 #
	#																		 #
	#------------------------------------------------------------------------#

	def start_view(self):
		self.application_window.mainloop()


	# -----------------------------------------------------------------------#

	def set_application(self, title, theme, font, widgets_font_to_be_changed):
		self.application_window.title(title)

		if APPLICATION.OS == APPLICATION.LINUX_OS:
			# Selection du thème de la fenêtre
			application_Style = ttk.Style()
			application_Style.theme_use(theme)

			# Changement du Font utilisé par les widgets et la fenêtre
			for widget in widgets_font_to_be_changed:
				application_Style.configure(widget, 
											font = font)

			self.application_window.option_add("*Font", 
											   font)

		self.application_window.pack_propagate(True)


	# -----------------------------------------------------------------------#

	def create_main_frame(self):
		self.main_frame = ttk.Frame(master = self.application_window,
									borderwidth = 1)

		self.main_frame.pack(fill = tkinter.BOTH,
							 expand = True)


	# -----------------------------------------------------------------------#

	def create_label(self, key, text, anchor = tkinter.W, **kwargs):
		if APPLICATION.OS == APPLICATION.LINUX_OS:
			self.label[key] = ttk.Label(master = self.main_frame, 
										text = text,
										anchor = anchor)
		else:
			self.label[key] = ttk.Label(master = self.main_frame, 
										text = text,
										width = 20,
										anchor = anchor)

		self._grid_with_kwargs(self.label[key], kwargs)


	# -----------------------------------------------------------------------#

	def create_button(self, key, text, **kwargs):
		self.button[key] = ttk.Button(master = self.main_frame, 
									  text = text)

		self._grid_with_kwargs(self.button[key], kwargs)


	# -----------------------------------------------------------------------#

	def create_entry(self, key, text, text_type,
					 text_length_max = None, text_variable_bound_min = None, 
					 text_variable_bound_max = None, **kwargs):
		vcmd = (self.main_frame.register(self.entry_command),
			   '%d', '%i', '%P', '%s', '%S', '%v', 
			   '%V', '%W', key, text_type, text_length_max,
			   text_variable_bound_min, text_variable_bound_max)

		self.entry[key] = ttk.Entry(master = self.main_frame,
						  width	= self.entry_width,
						  validate = 'key', 
						  validatecommand = vcmd)
		
		self.entry[key].insert(tkinter.END, text)

		self._grid_with_kwargs(self.entry[key], kwargs)


	# -----------------------------------------------------------------------#

	def create_combo_box(self, key, state = None, **kwargs):
		self.combo_box[key] = ttk.Combobox(master = self.main_frame)

		if state != None:
			self.combo_box[key]['state'] = state

		self._grid_with_kwargs(self.combo_box[key], kwargs)


	# -----------------------------------------------------------------------#

	def create_treeview(self, key, headers, column_width, items, **kwargs):
		length = len(items)

		self.treeview[key] = ttk.Treeview(master = self.main_frame, 
										  columns = headers, 
										  height = length, 
										  show = 'headings')

		for i in range(len(headers)):
			self.treeview[key].heading(column = headers[i],
									   text = headers[i])

		for i in range(len(headers)):
			self.treeview[key].column(column = headers[i],
									  width = column_width)

		self.set_treeview_column_anchor(self.treeview[key],
										column = headers[1], 
										anchor = tkinter.E)

		for name, value in items:
			self.treeview[key].insert(parent = "", 
									  index = "end", 
									  iid	= name, 
									  values = (name, value))

		self._grid_with_kwargs(self.treeview[key], kwargs)


	# -----------------------------------------------------------------------#

	def create_canvas(self, key, **kwargs):
		width = CANVAS.DOT_X_COUNT * CANVAS.DOT_PIXEL_SIZE
		height = CANVAS.DOT_Y_COUNT * CANVAS.DOT_PIXEL_SIZE

		self.canvas[key] = tkinter.Canvas(master = self.main_frame, 
										  bd = CANVAS.BD,
										  width = width,
										  height = height,
										  relief = tkinter.SUNKEN,
										  background = 'white',
										  highlightthickness = 0)

		self._grid_with_kwargs(self.canvas[key], kwargs)


	# -----------------------------------------------------------------------#

	def set_treeview_item(self, key, name, value):
		self.treeview[key].item(item = name, 
					  values = (name, value))


	# -----------------------------------------------------------------------#

	def set_treeview_column_anchor(self, treeview, column, anchor):
		treeview.column(column = column, 
						anchor = anchor)


	# -----------------------------------------------------------------------#

	def update_treeview_items(self, key, items):
		for name, value in items:
			self.set_treeview_item(key = key,
								   name = name, 
								   value = value)


	# -----------------------------------------------------------------------#

	def draw_on_canvas(self, key, dots_rect, color):
		for dot_rect in dots_rect:
			self.canvas[key].create_rectangle(dot_rect,
											  fill = color,
											  outline = color)


	# -----------------------------------------------------------------------#

	def _grid_with_kwargs(self, widget, kwargs):
		row = column = rowspan = columnspan = sticky = None

		for key, value in kwargs.items(): 
			if key == "row":
				row = value
			if key == "column":
				column = value
			if key == "rowspan":
				rowspan = value
			if key == "columnspan":
				columnspan = value
			if key == "sticky":
				sticky = value

		if rowspan == None:
			rowspan = 1
		if columnspan == None:
			columnspan = 1
		if sticky == None:
			sticky = tkinter.W + tkinter.N + tkinter.E + tkinter.S

		widget.grid(padx = self.padding_x, 
					pady = self.padding_y,
					ipadx = self.i_padding_x,
					ipady = self.i_padding_y,
					row = row,
					column = column,
					rowspan = rowspan,
					columnspan = columnspan,
					sticky = sticky)


	# -----------------------------------------------------------------------#

	def get_application_window(self):
		return self.application_window


	# -----------------------------------------------------------------------#

	def set_padding_x(self, padding_x):
		self.padding_x = padding_x


	# -----------------------------------------------------------------------#

	def set_padding_y(self, padding_y):
		self.padding_y = padding_y


	# -----------------------------------------------------------------------#

	def set_entry_width(self, entry_width):
		self.entry_width = entry_width


	# -----------------------------------------------------------------------#

	def get_label(self, key):
		return self.label[key]


	# -----------------------------------------------------------------------#

	def set_label_text(self, key, text):
		self.label[key]['text'] = text


	# -----------------------------------------------------------------------#

	def get_label_text(self, key):
		return self.label[key].get()


	# -----------------------------------------------------------------------#

	def get_button(self, key):
		return self.button[key]


	# -----------------------------------------------------------------------#

	def get_check_box(self, key):
		return self.check_box[key]


	# -----------------------------------------------------------------------#

	def set_check_box_state(self, key, state):
		if state:
			self.check_box[key].state(['selected'])
		else:
			self.check_box[key].state(['!selected'])


	# -----------------------------------------------------------------------#

	def get_entry(self, key):
		return self.entry[key]


	# -----------------------------------------------------------------------#

	def set_entry_text(self, key, text):
		self.entry[key].delete(0, tkinter.END)
		self.entry[key].insert(0, str(text))


	# -----------------------------------------------------------------------#

	def get_entry_text(self, key):
		return self.entry[key].get()


	# -----------------------------------------------------------------------#

	def get_combo_box(self, key):
		return self.combo_box[key]


	# -----------------------------------------------------------------------#

	def set_combo_box_index(self, key, index):
		self.combo_box[key].current(index)


	# -----------------------------------------------------------------------#

	def set_combo_box_text(self, key, text):
		self.combo_box[key].set(text)


	# -----------------------------------------------------------------------#

	def set_combo_box_values(self, key, values):
		self.combo_box[key]['values'] = values


	# -----------------------------------------------------------------------#

	def get_combo_box_text(self, key):
		return self.combo_box[key].get()


	# -----------------------------------------------------------------------#

	def get_canvas(self, key):
		return self.canvas[key]


	# -----------------------------------------------------------------------#

	def get_treeview(self, key):
		return self.treeview[key]


	# -----------------------------------------------------------------------#

	def get_treeview_items(self, key):
		return self.treeview[key].get_children()


	#------------------------------------------------------------------------#
	#																		 #
	#					 		 classe widgets: 							 #
	#						  listes des propriétés							 #
	#																		 #
	#------------------------------------------------------------------------#

	@property
	def application_window(self):
		return self._application_window

	@application_window.setter
	def application_window(self, application_window):
		self._application_window = application_window

		
	# -----------------------------------------------------------------------#

	@property
	def main_frame(self):
		return self._main_frame

	@main_frame.setter
	def main_frame(self, main_frame):
		self._main_frame = main_frame


	# -----------------------------------------------------------------------#

	@property
	def label(self):
		return self._label

	@label.setter
	def label(self, label):
		self._label = label

		
	# -----------------------------------------------------------------------#

	@property
	def button(self):
		return self._button

	@button.setter
	def button(self, button):
		self._button = button

		
	# -----------------------------------------------------------------------#

	@property
	def check_box(self):
		return self._check_box

	@check_box.setter
	def check_box(self, check_box):
		self._check_box = check_box


	# -----------------------------------------------------------------------#

	@property
	def entry(self):
		return self._entry

	@entry.setter
	def entry(self, entry):
		self._entry = entry


	# -----------------------------------------------------------------------#

	@property
	def combo_box(self):
		return self._combo_box

	@combo_box.setter
	def combo_box(self, combo_box):
		self._combo_box = combo_box


	# -----------------------------------------------------------------------#

	@property
	def treeview(self):
		return self._treeview

	@treeview.setter
	def treeview(self, treeview):
		self._treeview = treeview


	# -----------------------------------------------------------------------#

	@property
	def canvas(self):
		return self._canvas

	@canvas.setter
	def canvas(self, canvas):
		self._canvas = canvas


	# -----------------------------------------------------------------------#

	@property
	def entry_width(self):
		return self._entry_width

	@entry_width.setter
	def entry_width(self, entry_width):
		self._entry_width = entry_width


	# -----------------------------------------------------------------------#

	@property
	def treeview_column_width(self):
		return self._treeview_column_width

	@treeview_column_width.setter
	def treeview_column_width(self, treeview_column_width):
		self._treeview_column_width = treeview_column_width


	# -----------------------------------------------------------------------#

	@property
	def padding_x(self):
		return self._padding_x

	@padding_x.setter
	def padding_x(self, padding_x):
		self._padding_x = padding_x


	# -----------------------------------------------------------------------#

	@property
	def padding_y(self):
		return self._padding_y

	@padding_y.setter
	def padding_y(self, padding_y):
		self._padding_y = padding_y


	# -----------------------------------------------------------------------#

	@property
	def i_padding_x(self):
		return self._i_padding_x

	@i_padding_x.setter
	def i_padding_x(self, i_padding_x):
		self._i_padding_x = i_padding_x


	# -----------------------------------------------------------------------#

	@property
	def i_padding_y(self):
		return self._i_padding_y

	@i_padding_y.setter
	def i_padding_y(self, i_padding_y):
		self._i_padding_y = i_padding_y


	# -----------------------------------------------------------------------#

	@property
	def entry_command(self):
		return self._entry_command

	@entry_command.setter
	def entry_command(self, entry_command):
		self._entry_command = entry_command
