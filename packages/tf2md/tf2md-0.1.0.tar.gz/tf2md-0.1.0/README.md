# TF2MD
A readme generator for terraform code.


# Usage

Run the command and point it to either a variable file or an output file

```
tf2md gen-docs --file-type output terraform/outputs.tf
```

Please note to include the `--file-type` as either `output` or `variable`

Right now it does not work if you have a mixture of variables and outputs in the same file.


# Dev Setup

- Setup dev env
```
poetry install
```

- Install pre-commit
```
poetry run pre-commit install
```