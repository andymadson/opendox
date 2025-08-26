# mkdocs_formatter

### __init__(self, output_dir)

Initializes an instance of OutputDir object with 'self' as reference and output directory path.

### create_config(self, project_name)

**create_config() -> dict : Creates a configuration file for project in json format with default values (if not already defined). Returns dictionary containing all details about your new config object.

### create_index(self, project_name, description)

**Function to create an index for a project in Python using paramiko library and S3 bucket storage API from AWS SDK (Boto). One-line functionality is provided by creating SSH connection on local machine with target server. Args include 'self', the name of your Project, which also acts as description when necessary**

### format_function(self, func_data, docstring)

Function to format a given data according to provided parameters.

Args:
   func_data (required for this method) : Data structure containing necessary information about functionality/operation that needs be performed. This could include inputs or other details like type of operation(addition, multiplication etc.), the values and order in which they should appear inside 'func' list data to perform operations on them as per requirement by user .
   
Returns: 
   Formatted version (or result) according to requirements specified within docstring. It could be a value or an output from function that is dependent upon input information passed through func_data parameter, such things happen in this scenario when 'add' and multiplication operations are performed on the list of numbers provided by user as inputs with given order mentioned inside it (e.g., addition before Multiplication).
      This docstring explains what exactly function does while also specifying its parameters and return type so that others who have looked

### create_module_page(self, module_name, functions, docs)

# Function to create a module page on Github Pagination (Issues). This method creates documentation for each issue by using GitHub API and writes into markdown file with front matter. Returns None if failed or returns the created filename else return error message in case of failure. Parameters are ['self', 'module_name' - Name, ‘functions’- list['create'],
# docs'] where self is reference to current instance object module name as string and functions a dictionary contains method calls for Github API with type check on None otherwise returns error message else return filename in case of success. Docs parameter should contain markdown formatted documentation strings corresponding the methods' inputs/outputs which are used by 'create_module'.

