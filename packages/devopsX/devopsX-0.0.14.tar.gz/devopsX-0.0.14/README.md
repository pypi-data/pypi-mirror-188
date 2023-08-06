# DevopsX

## General Information
* **Software**:DevopsX
* **Author**:Paulo Sérgio dos Santos Júnior
* **Author's e-mail**:paulossjunior@gmail.com
* **Source Repository**: [https://gitlab.com/immigrant-data-driven-development/libs/application/azuredevops](https://gitlab.com/immigrant-data-driven-development/libs/application/azuredevops)  

## Goal
DevOps é um produto da Microsoft que fornece controle de versão, relatórios, gerenciamento de requisitos, gerenciamento de projetos, compilações automatizadas, gerenciamento de laboratório, recursos de gerenciamento de testes e versões.

## Documentation

The Documentation can be found in this [link](./docs/documentation.md)

## Generate documentation

To create the code documentation:
```bash
pdoc --html --force devopsX/ --output docs

```
### Acess code documentation	

To accesss the documenation, go to folder docs/devopsX and open index.html 
	
## Instalation

To install devopsX, run this command in your terminal:
```bash
pip install devopsX
```

## Usage

```python

from devopsX import factories
from pprint import pprint 
organization_url = "<DEVOPS URL>"
personal_access_token =  "<personal code access>"

project_service = factories.ProjectFactory(personal_access_token=personal_access_token,
                                            organization_url=organization_url)
projects = project_service.get_projects()

for project in projects:
    pprint(project.__dict__)

```
