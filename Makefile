.PHONY: init test
init:
	pipenv install --dev
test:
    pytest
publish:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg codechain.egg-info
