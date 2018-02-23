start:
	/mnt/c/Program\ Files\ \(x86\)/Google/Chrome/Application/chrome.exe http://localhost:8010; \
	export FLASK_DEBUG=1; \
	export FLASK_APP=app.py; \
	flask run --port=8010; \

setup:
	ansible-playbook -i ansible/hosts ansible/tasks/setup.yml
