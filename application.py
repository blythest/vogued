from flask import Flask, render_template, redirect, request, g, session, url_for, flash
import tasks
import random
import config
import uuid
from forms import TextInputForm
application = Flask(__name__)
application.config.from_object(config)

@application.route('/', methods=['GET', 'POST'])
def index():
	form = TextInputForm()
	tmp_file_name = str(uuid.uuid4()).encode('utf-8').split('-')[0]

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('index.html', form=form)
		else:
			# Get the text from the request dictionary and strip of whitespace
			text_input_str = " ".join(request.form.to_dict()['textInput'].split())
			source_input_str = request.form.to_dict()['source']
			if (len(source_input_str) == 0):
				source_input_str = "Source Unknown"
			text_unicodestring = text_input_str.encode('utf-8')
			source_unicodestring = source_input_str.encode('utf-8')
			all_output = source_unicodestring + '\n' + text_unicodestring
    		with open(tmp_file_name,"w") as text_output:
   				text_output.write(all_output)
   		tasks.main(tmp_file_name)
		return redirect(url_for('vogued'))
	
	elif request.method == 'GET':
  		return render_template('index.html', form=form)

@application.route('/vogued')
def vogued():
	results = open("converted_output.txt").read()
	lines = results.split('\n')
	source = lines[0]
	line = random.choice(lines[1:-1]).strip()
	if not line.endswith('.'):
		line = line + '.'
	return render_template('vogued.html', source=source, line=line)

if __name__ == "__main__":
    application.run(debug=True)
