

import string

import constants

TEXT = constants.Text

# ---------------------------------------------------------------------------#

def is_entry_text_valid(text, text_type):
	if text_type == TEXT.INT_TYPE:
		if text:
			if is_any_char_not_valid(text = text, 
								     accepted_chars = TEXT.INT_CHARS):
				return False

		if len(text) > 1:
			if is_first_char_a_zero(text = text):
				return False

	elif text_type == TEXT.FLOAT_TYPE:
		if text:
			if is_any_char_not_valid(text = text, 
								     accepted_chars = TEXT.FLOAT_CHARS):
				return False

			if is_more_than_one_dot(text = text):
				return False

			if is_first_char_a_dot(text = text):
				return False

			if len(text) > 1:
				if is_first_char_a_zero(text = text) \
					and is_second_char_not_a_dot(text = text):
					return False

	else:
		if text_type == TEXT.STRING_TYPE:
			if text:
				if is_any_char_not_valid(text = text, 
									     accepted_chars = TEXT.STRING_CHARS):
					return False

	return True


# ---------------------------------------------------------------------------#

def are_bounds_valid(text, text_type, text_length_max, min_, max_):
	if text:
		if text_type == TEXT.INT_TYPE:
			return is_value_between_bounds(var = int(text),
										   text_type = text_type,
										   min_ = min_,
										   max_ = max_)

		elif text_type == TEXT.FLOAT_TYPE:
			if is_value_between_bounds(var = float(text),
									   text_type = text_type,
									   min_ = min_,
									   max_ = max_):

				integer_part_len = get_integer_part_len(float_string = text)
				decimal_part_len = get_decimal_part_len(
									  float_string = text)

				if integer_part_len <= TEXT.INTEGER_PART_LEN_MAX \
				and decimal_part_len <= TEXT.DECIMAL_PART_LEN_MAX:
					return True
				else:
					return False
			else:
				return False

		else:
			if text_type == TEXT.STRING_TYPE:
				textlen = len(text)

				if textlen <= int(text_length_max):
					return True
				else:
					return False

	return True


# ---------------------------------------------------------------------------#

def is_any_char_not_valid(text, accepted_chars):
	for char in text:
		if char not in accepted_chars:
			return True

	return False


# ---------------------------------------------------------------------------#

def get_integer_part_len(float_string):
	dot_pos = float_string.find(TEXT.CHAR_DOT)

	if dot_pos >= TEXT.DOT_POS_MIN:
		integer_part_len = dot_pos

		return integer_part_len
	else:
		integer_part_len = len(float_string)

		return integer_part_len


# ---------------------------------------------------------------------------#

def get_decimal_part_len(float_string):
	dot_pos = float_string.find(TEXT.CHAR_DOT)
	ending_part = dot_pos + 1

	if dot_pos >= TEXT.DOT_POS_MIN:
		decimal_part_len = len(float_string[:ending_part])

		return decimal_part_len
	else:
		return 0


# ---------------------------------------------------------------------------#

def is_value_between_bounds(var, text_type, min_, max_):
	if text_type == TEXT.INT_TYPE:
		min_ = int(min_)
		max_ = int(max_)
	else:
		min_ = float(min_)
		max_ = float(max_)
	if var >= min_ and var <= max_:
		return True
	else:
		return False


# ---------------------------------------------------------------------------#

def is_first_char_a_dot(text):
	if text[0] == TEXT.CHAR_DOT:
		return True
	return False


# ---------------------------------------------------------------------------#

def is_first_char_a_zero(text):
	if text[0] == TEXT.CHAR_ZERO:
		return True
	return False


# ---------------------------------------------------------------------------#

def is_second_char_not_a_dot(text):
	if text[1] == TEXT.CHAR_DOT:
		return False
	return True


# ---------------------------------------------------------------------------#

def is_more_than_one_dot(text):
	dot_count = 0

	for char in text:
		if char == TEXT.CHAR_DOT:
			dot_count += 1

	if dot_count > TEXT.DOT_COUNT_MAX:
		return True

	return False


# ---------------------------------------------------------------------------#

def is_text_length_valid(text, max_):
	if len(text) > max_:
		return False
	else:
		return True
