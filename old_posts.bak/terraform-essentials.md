---
title: "Terraform"
subtitle: "Cheatsheet"
tags: [tools]

date: 2022-02-28
featured: false
draft: true

reading_time: false
profile: false
commentable: true
summary: " "

---

## Notes 

- I have aliased `terraform` to `tf` in my .bashrc, and I'm referring to
  Terraform as TF.

- Create a directory to store TF settings.

- Running `tf init` in the TF directory initialises the backend.

- Write configuration (e.g. in `main.tf`).

- `tf apply` creates an execution plan and asks for confirmation to build
  resources. Can also use the command to ensure that infrastructure matches
  current specifications in `main.tf`.

- `tf show` lists values associated with resource.

- `tf destroy` is the reverse of `tf apply` in that it terminates and destroys
  all resources specified in configuration file (e.g. `main.tf`). Upon running,
  TF creates an execution plan and asks for confirmation to destroy
  resources.

- TF olas all .tf files in the current directory, so I can store variable names
  in a separate file (e.g. `variables.tf`) and refer to them in `main.tf` using
  `var.varname`.

- `tf output` prints all outputs from specification, `tf output outputname` the
  value of `outputname` (e.g. `instance_id`).


## Resources

- [Terraform AWS
  tutorial](https://learn.hashicorp.com/collections/terraform/aws-get-started)

- [Basic explanation](https://blog.gruntwork.io/an-introduction-to-terraform-f17df9c6d180)
- [Insanely useful setup guide](https://blog.gruntwork.io/an-introduction-to-terraform-f17df9c6d180)
- [AWS in plain English](https://expeditedsecurity.com/aws-in-plain-english/)



