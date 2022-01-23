

import random
import numpy as np

import constants

# declaration des propriétés constantes
NEURON = constants.Neuron

class Neuron(object):

	def __init__(self):
		# declaration des propriétés variables
		self._count = 0
		self._variant_count = 0
		self._activating_threshold = 0

		self._names = list()
		self._inputs = list()
		self._outputs = list()
		self._weights = list()


	#------------------------------------------------------------------------#
	#																		 #
	#							  classe Neuron: 							 #
	#						   liste des méthodes							 #
	#																		 #
	#------------------------------------------------------------------------#

	def get_neuron_and_variant(self, input_matrice):
		for neuron in range(self.count):
			neuron_variant_count = len(self.inputs[neuron])

			for variant in range(neuron_variant_count):
				identical_synapse = 0

				for synapse in range(NEURON.SYNAPSE_COUNT):
					if self.inputs[neuron][variant][synapse] == input_matrice[synapse]:
						identical_synapse += 1

				if identical_synapse == NEURON.SYNAPSE_COUNT:
					return (neuron, variant)

		return (NEURON.INDEX_DONT_EXIST, NEURON.FIRST_INPUT_VARIANT)


	# -----------------------------------------------------------------------#

	def create(self, new_name, new_inputs):
		self.names.append(new_name)

		# initialise les tableaux
		self.outputs.append(NEURON.INACTIVE)

		self.inputs.append([new_inputs.copy()])

		self.init_weights()

		self.count += 1
		self.variant_count += 1
		self.activating_threshold = self.get_new_activating_threshold()


	# -----------------------------------------------------------------------#

	def create_input_matrice_variant(self, neuron, new_inputs):
		# initialise les tableaux
		self.inputs[neuron].append(new_inputs.copy())
		self.variant_count += 1
		self.activating_threshold = self.get_new_activating_threshold()


	# -----------------------------------------------------------------------#

	def get_index(self, name):
		for neuron in range(self.count):
			if self.names[neuron] == name:
				return neuron

		return NEURON.INDEX_DONT_EXIST


	# -----------------------------------------------------------------------#
		
	def does_name_exist(self, name):
		for neuron in range(self.count):
			if self.names[neuron] == name:
				return not NEURON.NAME_DONT_EXIST

		return NEURON.NAME_DONT_EXIST


	# -----------------------------------------------------------------------#

	def does_input_matrice_exist(self, input_matrice):
		if self.get_neuron_and_variant(input_matrice = input_matrice) \
			!= (NEURON.INDEX_DONT_EXIST, NEURON.FIRST_INPUT_VARIANT):
				return not NEURON.INPUT_MATRICE_DONT_EXIST

		return NEURON.INPUT_MATRICE_DONT_EXIST


	# -----------------------------------------------------------------------#

	def init_weights(self):
		new_weight = []

		for synapse in range(NEURON.SYNAPSE_COUNT):
			new_weight.append(round(
							  random.uniform(
							  NEURON.SYNAPSE_BLOCKING,
							  NEURON.SYNAPSE_PASSING),
							  2))

		self.weights.append(new_weight.copy())


	# -----------------------------------------------------------------------#

	def _calculate_output(self, neuron, activated_inputs):
		output = 0.0

		for synapse in range(NEURON.SYNAPSE_COUNT):
			output += activated_inputs[synapse] * self.weights[neuron][synapse]

		return output


	# -----------------------------------------------------------------------#

	def get_output_state(self, neuron, activated_inputs):
		output = self._calculate_output(neuron = neuron, 
										activated_inputs = activated_inputs)

		if output >= self.activating_threshold:
			output = NEURON.ACTIVE
		else:
			output = NEURON.INACTIVE

		return output


	# -----------------------------------------------------------------------#

	def tend_toward_new_output_state(
			self, new_output_state, correction, neuron, activated_inputs):
		output = 0.0

		correction_factor = correction * (new_output_state - self.outputs[neuron])

		for synapse in range(NEURON.SYNAPSE_COUNT):
			self.weights[neuron][synapse] += activated_inputs[synapse] * correction_factor
			output += activated_inputs[synapse] * self.weights[neuron][synapse]

		if output >= self.activating_threshold:
			output = NEURON.ACTIVE
		else:
			output = NEURON.INACTIVE

		return output


	# -----------------------------------------------------------------------#

	def is_active(self, checked_active, activated_inputs):
		valid = 0

		for neuron in range(self.count):
			self.outputs[neuron] = self.get_output_state(
								   neuron = neuron, 
						   		   activated_inputs = activated_inputs)

		for neuron in range(self.count):
			if neuron == checked_active:
				if self.outputs[neuron] == NEURON.ACTIVE:
					valid += 1

			else: 
				if self.outputs[neuron] == NEURON.INACTIVE:
					valid += 1

		if valid == self.count:
			return True
		else:
			return False


	# -----------------------------------------------------------------------#

	def is_not_active(self, checked_active, activated_inputs):
		return not self.is_active(checked_active = checked_active,
								  activated_inputs = activated_inputs)


	# -----------------------------------------------------------------------#

	def get_error(self):
		valid = 0

		for neuron in range(self.count):
			variant_valid = 0
			neuron_variant_count = len(self.inputs[neuron])

			for variant in range(neuron_variant_count):
				if self.is_active(checked_active = neuron,
								  activated_inputs = self.inputs[neuron][variant]):
					variant_valid += 1

			if variant_valid == neuron_variant_count:
				valid += 1

		error = int((1.0 - (valid / self.count)) * 100)

		return error


	# -----------------------------------------------------------------------#

	def get_valid_count(self, current_error):
		valid_count = round((1.0 - (current_error / 100.0)) * self.count)

		return valid_count


	# -----------------------------------------------------------------------#

	def get_active(self, activated_inputs):
		for neuron in range(self.count):
			if self.is_active(checked_active = neuron,
							  activated_inputs = activated_inputs):
				return neuron

		return NEURON.NONE_ACTIVE


	# -----------------------------------------------------------------------#

	def get_new_activating_threshold(self):
		return (self.variant_count / 2.0)


	#------------------------------------------------------------------------#
	#																		 #
	#					class model_shape_recognition: 						 #
	#	liste des "getters" utilisées par la class "ModelShapeRecognition"	 #
	#																		 #
	#------------------------------------------------------------------------#

	def get_count(self):
		return self.count


	#------------------------------------------------------------------------#

	def get_name(self, neuron):
		return self.names[neuron]


	#------------------------------------------------------------------------#

	def get_names(self):
		return self.names


	#------------------------------------------------------------------------#

	def get_inputs(self, neuron, variant):
		return self.inputs[neuron][variant]


	#------------------------------------------------------------------------#

	def get_variant_count(self, neuron):
		return len(self.inputs[neuron])


	#------------------------------------------------------------------------#
	#																		 #
	#							  classe Neuron: 							 #
	#						   liste des propriétés							 #
	#																		 #
	#------------------------------------------------------------------------#

	@property
	def count(self):
		return self._count

	@count.setter
	def count(self, count):
		self._count = count


	# -----------------------------------------------------------------------#

	@property
	def variant_count(self):
		return self._variant_count

	@variant_count.setter
	def variant_count(self, variant_count):
		self._variant_count = variant_count


	# -----------------------------------------------------------------------#

	@property
	def activating_threshold(self):
		return self._activating_threshold

	@activating_threshold.setter
	def activating_threshold(self, activating_threshold):
		self._activating_threshold = activating_threshold


	# -----------------------------------------------------------------------#

	@property
	def names(self):
		return self._names

	@names.setter
	def names(self, names):
		self._names = names


	# -----------------------------------------------------------------------#

	@property
	def inputs(self):
		return self._inputs

	@inputs.setter
	def inputs(self, inputs):
		self._inputs = inputs


	# -----------------------------------------------------------------------#

	@property
	def outputs(self):
		return self._outputs

	@outputs.setter
	def outputs(self, outputs):
		self._outputs = outputs


	# -----------------------------------------------------------------------#

	@property
	def weights(self):
		return self._weights

	@weights.setter
	def weights(self, weights):
		self._weights = weights
