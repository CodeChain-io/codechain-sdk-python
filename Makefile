.PHONY: init test
init:
	pipenv install --dev
test:
	tox
test-e2e:
	tox -e e2e
publish:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg codechain.egg-info
