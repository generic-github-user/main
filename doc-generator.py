import importlib, inspect
import datetime

module_name = 'main'
docs_directory = './docs'
d_ = docs_directory
template = d_+'/class_template.md'
output = d_+'/main.md'
result = ''
method_template = d_+'/method_template.md'

with open(template, 'r') as file:
    template_content = file.read()
    # print(template_content)
with open(method_template, 'r') as file:
    method_template = file.read()

for name, cls in inspect.getmembers(importlib.import_module(module_name), inspect.isclass):
    if cls.__module__ == module_name:
        section_content = template_content
        # print(name, cls)
        # print(docstring)
        try:
            print(cls.__annotations__)
        except:
            pass
        docstring = cls.__doc__
        if docstring is None:
            docstring = 'Not yet documented'
        section_content = section_content.replace('{class}', name)
        section_content = section_content.replace('{docstring}', docstring)
