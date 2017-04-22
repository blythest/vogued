from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError

class TextInputForm(FlaskForm):
	def str_length_check(FlaskForm, textInput):
		print len(textInput.data.split())
		if len(textInput.data.split()) > 250:
			raise ValidationError('Field must be less than 250 characters')

	source = TextField("Source (e.g. The New York Times, Dr. Seuss, etc.)")
	textInput = TextAreaField("Your text here. Please limit to 200 words.", [validators.Required("Please enter some text."), str_length_check])
	submit = SubmitField("Submit")