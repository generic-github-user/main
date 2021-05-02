import importlib, inspect
import datetime

module_name = 'main'
docs_directory = './docs'
d_ = docs_directory
template = d_+'/class_template.md'
output = d_+'/main.md'
result = ''
method_template = d_+'/method_template.md'
