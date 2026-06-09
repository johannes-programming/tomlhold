.ONESHELL:
.PHONY: all beautiful black build clean commit echo isort jacobus pypi rebase test toml_sorted_pyproject upload version works
SHELL := /bin/zsh

all: beautiful commit

beautiful: isort black jacobus toml_sorted_pyproject

black: works
	conda run -n works pip install 'black>=24.5,<26';
	conda run -n works black --line-length=79 . ;

build: works
	conda run -n works pip install 'build>=1.3,<2';
	conda run -n works python -m build;

commit: works
	git add -A;
	conda run -n works pip install 'toml_get>=1.0,<2';
	git commit --allow-empty "$$(conda run -n works python -m toml_get @make/toml_get.txt)";

clean:
	rm -fr 'dist/';

echo:
	echo $(PARAMS);

isort: works
	conda run -n works pip install 'isort>=6.0,<7';
	conda run -n works isort . ;

jacobus: works
	conda run -n works pip install 'jacobus>=2.0,<3';
	conda run -n works python -m jacobus @make/jacobus.txt;

pypi: clean build upload

rebase:
	git rebase --empty=drop --interactive $(PARAMS);

test:
	@conda env remove -y -n test311 2>/dev/null || true;
	conda create -y -n test311 python=3.11;
	conda run -n test311 pip install -e .;
	conda run -n test311 python -c 'import tomlhold.tests; tomlhold.tests.test()';
	conda run -n test311 pip install mypy;
	conda run -n test311 python -m mypy -p tomlhold;

toml_sorted_pyproject: works
	conda run -n works pip install 'toml_sorted>=2.0,<3';
	conda run -n works python -m toml_sorted @make/toml_sorted_pyproject.txt;

upload: works
	conda run -n works pip install 'twine>=5.2,<7';
	conda run -n works twine upload 'dist/*';

version: all pypi

works:
	@conda env list | awk '{print $$1}' | grep -qx 'works' \
	|| conda create --name works --yes --channel conda-forge --override-channels python=3.11;
