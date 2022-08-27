File = Class(
    "File", """\
        A class for representing an entry in a filesystem; includes some basic
        metadata.""",

    ('name', "The file's name, including its extension(s)", String != ''),
    ('base', "A file name, excluding any file extensions", String != ''),
    ('path', "A relative or absolute path to a file", String != ''),
    (('extension', 'ext'), "The file extension, not including the leading period", String),
    ('size', "The size of the file in bytes", Int >= 0),
    ('time', "Time metadata, normalized to a Python datetime object", Tuple(
            ('created', datetime),
            ('modified', datetime),
            ('accessed', datetime)
        )),

    #(File.name in File.path)
)
#f = File()

def demo():
    print(File.doc('markdown'))
    print(File.doc('text'))

demo()
