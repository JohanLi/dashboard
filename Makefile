port = 8010

start:
	if [ $$(uname) = "Darwin" ]; \
	then \
		open -a Google\ Chrome http://localhost:$(port); \
	else \
		/mnt/c/Program\ Files\ \(x86\)/Google/Chrome/Application/chrome.exe http://localhost:$(port); \
	fi; \
	export FLASK_DEBUG=1; \
	export FLASK_APP=app.py; \
	flask run --port=$(port); \

setup:
	ansible-playbook -i ansible/hosts ansible/tasks/setup.yml

deploy:
	ansible-playbook -i ansible/hosts ansible/tasks/deploy.yml

.PHONY: test
test:
	python3 -m unittest -v
