# TF2MD
A readme generator for terraform code.

## About

Have you ever wanted to generate markdown documentation based on `variables.tf` or `outputs.tf` files?
This tool aims to solve that.

# Usage

Install the program
```
pip install tf2md
```

Run the program <Where `terraform/outputs.tf` is the path to my file>:
```
tf2md gen-docs terraform/outputs.tf
```

Note: This does not work on `tf` files that have a mix of `outputs` and `variables`.

See the `./examples` dir for examples of generated code.



## Dev Notes

Here are things I want to do:

- Tests
- I am not happy with the `create_variables_file` function, I want to clean it up,
but right now I just want to use the tool.

- I want to be able to add an output arg to the cli so the created files do not
just get dummped in the `./`

- Verbose logging and options are required
