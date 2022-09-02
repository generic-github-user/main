## Commands

### extract
Returns `null`
Move a database path to a separate 'block' and store a reference in the original database

**Parameters**
- path: `string` -- The section of the database to transfer

### ffind
Returns `null`
Find a file in the database (based on its name)

**Parameters**
- name: `string` -- The file name

### imfind
Returns `null`
Find images containing the specified text

**Parameters**
- query: `string` -- The text you want to search for

### limit
Returns `null`
Limit the number of results an action returns

**Parameters**
- n: `int` -- null

### manifest
Returns `null`
Gather information about a directory and its contents

**Parameters**
- path: `string (filepath)` -- null

### process
Returns `null`
Extract data from files to build databases

**Parameters**
- target: `null` -- null

### rose
Returns `string`
Display a randomly generated mosaic, for fun

**Parameters**
- size: `int` -- The size of the output

### summarize
Returns `json`
Compute a summary of a specified property/path over the database

**Parameters**
- key: `string (JSON path)` -- The database path to aggregate

