# pipeline

### __init__(self, model)

The `__init__` method is a special Python method that automatically executes when you create an instance (an object) from your class. It's used to set initial attributes for our objects in this case 'self', and also passing the model attribute which we are expected as input parameter of init function itself ie, `model = ...`

### generate(self, source_path, output_path, max_files)

"Function for generating multiple files from source to output path with a maximum number specified."\n\nArgs:\n   * `source_path` (str) : Path where sources are located.\n* `output_path` (str) : Destination folder's location, the generated file will be placed there. \n*  `max_files`  (int): Maximum number of files to generate from source."\n
Returns: Nothing unless an error occurs during execution which is then logged in console with exception handling mechanism provided by Python itself for debugging purpose.\ncalled as `generate(source, outputpath)".'

### _process_file(self, file_path, formatter)

"Processes a specific file located at given `file_path` with provided formatter." - One-line descrption using this exact format is included in below line by 'self', parameter and return values are described accordingly. However please note the implementation details of '_process_data' function, its parameters as well an output depends on how your specific requirement will work for processing data from a file ie., whether it needs to be transformed or manipulated before feeding into other functions/methods in this context not included within docstring because that would make the code too complex.

