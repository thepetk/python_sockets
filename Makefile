PYCODE = import flask.ext.statics as a; print a.__path__[0]

default:
	@echo "\nPython sockets make commands\n"
	@echo "Commands available:\n"
	@echo "    make run		# Starts a Flask development server with local variables."
	
run:
	flask run