import importlib, inspect
import datetime

module_name = 'main'
docs_directory = './docs'
d_ = docs_directory
output = d_+'/main.md'
result = ''

templates = {
    'class': 'class_template.md',
    'method': 'method_template.md',
    'parameter': 'parameter_template.md'
}
template_content = {}
for k, v in templates.items():
    path = d_+'/'+v
    with open(path, 'r') as file:
        template_content[k] = file.read()

def indent_width(s):
    indent = len(s) - len(s.lstrip())
    # print(indent)
    return indent

def clean_tabs(text):
    lines = text.split('\n')
    if not lines[0]:
        lines = lines[1:]
    tabs = indent_width(lines[0])
    # print(lines[0])
    # for l in lines:
    #     l = l[tabs:]
    return '\n'.join([l[tabs:] for l in lines])

def extract_info(s):
    info = {}
    s = clean_tabs(s)
    lines = s.split('\n')
    section = 'text'
    subsection = ''
    # print(lines)
    for l in lines:

        t = indent_width(l)
        if t == 0:
            if l and l[0] == '@':
                section = l[1:]

            if section not in info:
                info[section] = {}
            if section == 'text':
                if 'val' not in info['text']:
                    info['text']['val'] = []
                info[section]['val'].append(l)
        elif t in [1, 4]:
            subsection = clean_tabs(l)
            if subsection not in info[section]:
                info[section][subsection] = []
        elif t in [2, 8]:
            parts = clean_tabs(l).split(': ')
            label = parts[1]
            type_info = parts[0][1:-1].replace(' ','').split(',')
            arg_info = {
                'type': type_info,
                'label': label
            }
            info[section][subsection].append(arg_info)


    return info

def generate_section(stype, object, replacements):
    docstring = object.__doc__
    if docstring is None:
        docstring = 'Not yet documented'
    replacements.append(('{docstring}', docstring))
    content = template_content[stype]
    for r in replacements:
        content = content.replace(*r)
    return content

doc_module = importlib.import_module(module_name)
doc_classes = inspect.getmembers(doc_module, inspect.isclass)
for name, cls in doc_classes:
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

        methods = inspect.getmembers(cls, predicate=inspect.isfunction)
        # print(methods)
        method_info = ''
        for m in methods:
            subsection_content = method_template
            subsection_content = subsection_content.replace('{method}', m[0])
            mstring = m[1].__doc__
            if mstring is None:
                mstring = 'Not yet documented'
            subsection_content = subsection_content.replace('{docstring}', mstring)
            method_info += subsection_content + '\n'
            print(extract_info(mstring))
        section_content = section_content.replace('[methods]', method_info)
        section_content = section_content.replace('{timestamp}', str(datetime.datetime.now()))


        result += section_content + '\n'

with open(output, 'w') as file:
    file.write(result)

# print(result)
# print('{}% of classes and {}% of methods documented')
