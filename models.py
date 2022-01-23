

import numpy as np
from time import perf_counter, sleep
from math import exp

import constants
import neuron

APPLICATION = constants.Application
CALLBACK = constants.Callback
WIDGET = constants.Widget
NEURON = constants.Neuron
ERROR = constants.Error


error_message = lambda error: {CALLBACK.RETURN_VALUE: False,
							   CALLBACK.RETURN_MESSAGE: {
							   ERROR.TITLE_KEY: ERROR.TITLE, 
							   ERROR.MESSAGE_KEY: error}}

class ModelShapeRecognition(object):

	# declaration des propriétés constantes

	def __init__(self):

		# declaration du sous modèle
		self._neuron = neuron.Neuron()

		
		# -------------------------------------------------------------------#

		# declaration des propriétés variables
		self._compared_input_matrice = list()

		self._correction = float(WIDGET.ENTRY_CORRECTION_INITIAL_TEXT)
		self._current_error = 0
		self._valid_count = 0

		self._iteration = 0
		self._iteration_total = 0
		self._iteration_max = int(WIDGET.ENTRY_ITERATION_MAX_INITIAL_TEXT)
		
		self._elapsed_time = 0
		self._elapsed_time_total = 0

		self.init_compared_inputs()


	#------------------------------------------------------------------------#
	#																		 #
	#				   	classe model_shape_recognition: 					 #
	#						 liste des callbacks							 #
	#																		 #
	#------------------------------------------------------------------------#

	def on_create_neuron(self, name):
		if name:
			name_dont_exist = self.neuron.does_name_exist(name = name)
			input_matrice_dont_exist \
			= self.neuron.does_input_matrice_exist(
				  input_matrice = self.compared_input_matrice)

			if name_dont_exist and input_matrice_dont_exist:
				self.neuron.create(new_name = name, 
								   new_inputs = self.compared_input_matrice)

				self.current_error = self.neuron.get_error()
				self.valid_count = self.neuron.get_valid_count(
									   current_error = self.current_error)

				callback_return = CALLBACK.SUCCEED

			elif not name_dont_exist:
				callback_return =  error_message(ERROR.NAME_EXIST)
			else:
				callback_return =  error_message(ERROR.INPUT_MATRICE_EXIST)
		else:
			callback_return =  error_message(ERROR.NO_NAME_GIVEN)

		return callback_return


	#------------------------------------------------------------------------#

	def on_add_shape(self, name):
		# si au moins un neurone a été créé
		if self.neuron.get_count():
			index = self.neuron.get_index(name = name)

			if index != NEURON.INDEX_DONT_EXIST:
				input_matrice_dont_exist = \
					self.neuron.does_input_matrice_exist(
						input_matrice = self.compared_input_matrice)

				if input_matrice_dont_exist:
					self.neuron.create_input_matrice_variant(
						neuron = index,
						new_inputs = self.compared_input_matrice)

					self.current_error = self.neuron.get_error()
					self.valid_count = self.neuron.get_valid_count(
										   current_error = self.current_error)

					callback_return = CALLBACK.SUCCEED

				else:
					callback_return =  error_message(ERROR.INPUT_MATRICE_EXIST)

			else:	
				callback_return = error_message(ERROR.INDEX_DONT_EXIST)
		else:
			callback_return = error_message(ERROR.NO_NEURON_CREATED)

		return callback_return


	#------------------------------------------------------------------------#

	def on_correct_neuron(self, name):
		# si au moins un neurone a été créé
		if self.neuron.get_count():
			index = self.neuron.get_index(name = name)

			if index != NEURON.INDEX_DONT_EXIST:
				self._correct(neuron = index)

				callback_return = CALLBACK.SUCCEED
			else:	
				callback_return = error_message(ERROR.INDEX_DONT_EXIST)
		else:
			callback_return = error_message(ERROR.NO_NEURON_CREATED)

		return callback_return


	#------------------------------------------------------------------------#
	
	def on_auto_correct(self):
		# si au moins un neurone a été créé
		if self.neuron.get_count():
			self._auto_correct()

			callback_return = CALLBACK.SUCCEED
		else:
			callback_return = error_message(ERROR.NO_NEURON_CREATED)

		return callback_return


	#------------------------------------------------------------------------#
	#																		 #
	#					  class model_shape_recognition: 					 #
	#				  méthodes utilisées par les callbacks					 #
	#																		 #
	#------------------------------------------------------------------------#

	def _correct(self, neuron):
		self.iteration = 0

		neuron_is_not_active = self.neuron.is_not_active(
							   checked_active = neuron,
							   activated_inputs = self.compared_input_matrice)
		if neuron_is_not_active:
			self._start_timer()

			while neuron_is_not_active \
			and self.iteration < self.iteration_max:
				self._learning_loop(wished_active = neuron,
									activated_inputs = self.compared_input_matrice)

				neuron_is_not_active \
					= self.neuron.is_not_active(
						  checked_active = neuron,
						  activated_inputs = self.compared_input_matrice)

			self._stop_timer()

			self._get_learning_results()


	#------------------------------------------------------------------------#

	def _auto_correct(self):
		self.iteration = 0
		neuron_count = self.neuron.get_count()

		self._start_timer()

		self.valid_count = 0

		while self.valid_count != neuron_count:
			for neuron in range(neuron_count):
				neuron_variant_count = self.get_neuron_variant_count(neuron = neuron)

				for variant in range(neuron_variant_count):
					inputs = self.get_neuron_inputs(neuron = neuron,
													variant = variant)
					
					neuron_is_not_active = self.neuron.is_not_active(
										   checked_active = neuron,
										   activated_inputs = inputs)

					if neuron_is_not_active:
						while neuron_is_not_active \
						and self.iteration < self.iteration_max:
							self._learning_loop(wished_active = neuron,
												activated_inputs = inputs)

							neuron_is_not_active \
								= self.neuron.is_not_active(
									  checked_active = neuron,
									  activated_inputs = inputs)

					if self.iteration >= self.iteration_max:
						break

				if self.iteration >= self.iteration_max:
					break
		
			if self.iteration >= self.iteration_max:
				break

			self.current_error = self.neuron.get_error()
			self.valid_count = self.neuron.get_valid_count(current_error \
														   = self.current_error)

		self._stop_timer()

		if self.iteration:
			self._get_learning_results()


	#------------------------------------------------------------------------#

	def _learning_loop(self, wished_active, activated_inputs):
		neuron_count = self.neuron.get_count()

		for neuron in range(neuron_count):
			if neuron == wished_active:
				new_output_state = NEURON.ACTIVE
			else:
				new_output_state = NEURON.INACTIVE

			while self.neuron.outputs[neuron] != new_output_state \
			and self.iteration < self.iteration_max:

				self.neuron.outputs[neuron] \
				= self.neuron.tend_toward_new_output_state(
					new_output_state = new_output_state, 
					correction = self.correction, 
					neuron = neuron,
					activated_inputs = activated_inputs)

				self.iteration += 1

			if self.iteration >= self.iteration_max:
				break


	#------------------------------------------------------------------------#

	def _get_learning_results(self):
		self.current_error = self.neuron.get_error()
		self.valid_count = self.neuron.get_valid_count(current_error \
													   = self.current_error)

		self.elapsed_time = self._get_timer_elapsed_time()
		self.elapsed_time_total += self.elapsed_time

		self.iteration_total += self.iteration


	#------------------------------------------------------------------------#

	def _start_timer(self):
		self.starting_time = perf_counter()


	#------------------------------------------------------------------------#

	def _stop_timer(self):
		self.ending_time = perf_counter()


	#------------------------------------------------------------------------#

	def _get_timer_elapsed_time(self):
		return int((self.ending_time - self.starting_time) * 1000)


	#------------------------------------------------------------------------#
	#																		 #
	#					class model_shape_recognition: 						 #
	#		méthodes utilisées par la class "PresenterShapeRecognition"		 #
	#																		 #
	#------------------------------------------------------------------------#

	def get_neuron_name(self, neuron):
		return self.neuron.get_name(neuron = neuron)


	#------------------------------------------------------------------------#

	def get_neuron_names(self):
		return self.neuron.get_names()


	#------------------------------------------------------------------------#

	def get_neuron_inputs(self, neuron, variant):
		return self.neuron.get_inputs(neuron = neuron,
									  variant = variant)


	#------------------------------------------------------------------------#

	def get_neuron_variant_count(self, neuron):
		return self.neuron.get_variant_count(neuron = neuron)


	#------------------------------------------------------------------------#

	def get_neuron_and_variant(self):
		return self.neuron.get_neuron_and_variant(input_matrice = \
												  self.compared_input_matrice)


	#------------------------------------------------------------------------#

	def get_neuron_count(self):
		return self.neuron.get_count()


	#------------------------------------------------------------------------#

	def get_neuron_valid_count(self):
		return self.valid_count


	#------------------------------------------------------------------------#

	def set_correction(self, correction):
		self.correction = correction


	#------------------------------------------------------------------------#

	def get_correction(self):
		return self.correction


	#------------------------------------------------------------------------#

	def set_iteration_max(self, iteration_max):
		self.iteration_max = iteration_max


	#------------------------------------------------------------------------#

	def get_iteration_max(self):
		return self.iteration_max


	#------------------------------------------------------------------------#

	def get_iteration(self):
		return self.iteration


	#------------------------------------------------------------------------#

	def get_iteration_total(self):
		return self.iteration_total


	#------------------------------------------------------------------------#

	def get_elapsed_time(self):
		return self.elapsed_time


	#------------------------------------------------------------------------#

	def get_elapsed_time_total(self):
		return self.elapsed_time_total


	#------------------------------------------------------------------------#

	def get_error(self):
		return self.current_error


	#------------------------------------------------------------------------#

	def init_compared_inputs(self):
		for synapse in range(NEURON.SYNAPSE_COUNT):
			self.compared_input_matrice.append(NEURON.INPUT_INACTIVATED)


	#------------------------------------------------------------------------#

	def update_compared_input_state(self, index, new_state):
		self.compared_input_matrice[index] = new_state


	#------------------------------------------------------------------------#

	def get_activated_inputs(self, for_compared_input, neuron = None, variant = None):
		activated_inputs = []

		if for_compared_input:
			for synapse in range(NEURON.SYNAPSE_COUNT):
				if self.compared_input_matrice[synapse] == NEURON.INPUT_ACTIVATED:
					activated_inputs.append(synapse)
		else:
			for synapse in range(NEURON.SYNAPSE_COUNT):
				if self.neuron.inputs[neuron][variant][synapse] == NEURON.INPUT_ACTIVATED:
					activated_inputs.append(synapse)

		return activated_inputs


	#------------------------------------------------------------------------#

	def get_activated_outputs(self):
		activated_outputs = []

		neuron = self.neuron.get_active(
					 activated_inputs = self.compared_input_matrice)

		if neuron == NEURON.NONE_ACTIVE:
			return ([], "")

		for synapse in range(NEURON.SYNAPSE_COUNT):
			if self.neuron.inputs[neuron][NEURON.FIRST_INPUT_VARIANT][synapse] == NEURON.INPUT_ACTIVATED:
				activated_outputs.append(synapse)

		return (activated_outputs, self.neuron.get_name(neuron = neuron))


	#------------------------------------------------------------------------#
	#																		 #
	#				   	classe model_shape_recognition: 					 #
	#						 liste des propriétés							 #
	#																		 #
	#------------------------------------------------------------------------#

	@property
	def neuron(self):
		return self._neuron

	@neuron.setter
	def neuron(self, neuron):
		self._neuron = neuron


	#------------------------------------------------------------------------#

	@property
	def compared_input_matrice(self):
		return self._compared_input_matrice

	@compared_input_matrice.setter
	def compared_input_matrice(self, compared_input_matrice):
		self._compared_input_matrice = compared_input_matrice


	#------------------------------------------------------------------------#

	@property
	def correction(self):
		return self._correction

	@correction.setter
	def correction(self, correction):
		self._correction = correction


	#------------------------------------------------------------------------#

	@property
	def current_error(self):
		return self._current_error

	@current_error.setter
	def current_error(self, current_error):
		self._current_error = current_error


	#------------------------------------------------------------------------#

	@property
	def valid_count(self):
		return self._valid_count

	@valid_count.setter
	def valid_count(self, valid_count):
		self._valid_count = valid_count


	#------------------------------------------------------------------------#

	@property
	def iteration(self):
		return self._iteration

	@iteration.setter
	def iteration(self, iteration):
		self._iteration = iteration


	#------------------------------------------------------------------------#

	@property
	def iteration_total(self):
		return self._iteration_total

	@iteration_total.setter
	def iteration_total(self, iteration_total):
		self._iteration_total = iteration_total


	#------------------------------------------------------------------------#

	@property
	def iteration_max(self):
		return self._iteration_max

	@iteration_max.setter
	def iteration_max(self, iteration_max):
		self._iteration_max = iteration_max


	#------------------------------------------------------------------------#

	@property
	def elapsed_time(self):
		return self._elapsed_time

	@elapsed_time.setter
	def elapsed_time(self, elapsed_time):
		self._elapsed_time = elapsed_time


	#------------------------------------------------------------------------#

	@property
	def elapsed_time_total(self):
		return self._elapsed_time_total

	@elapsed_time_total.setter
	def elapsed_time_total(self, elapsed_time_total):
		self._elapsed_time_total = elapsed_time_total


	#------------------------------------------------------------------------#
