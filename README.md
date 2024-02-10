# banking transfer

## setup
```
pyenv local 3.11.4

poetry env use python
poetry config virtualenvs.in-project true
poetry install
poetry shell
```

## cli

```
# run 
make run

# migrate
make migrate

# test
make test

```