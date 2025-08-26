# cache

### __init__(self, project_root)

"Initializes a new instance of 'Project' with specified project root directory."\nArgs:\
- self (required): The Project object itself.\
- projec_root :The base path to start searching from. This can be either an absolute or relative file system path. 
(end)

### _load_cache(self)

Function to load a cache from disk into memory.

Description about parameters and returns in separate lines with explanations for each one on their own line within brackets []. For instance - Parameter 'self' is not included because it does nothing differently than the function name suggests. In this case, self refers to an object of class that implements a method load_cache(). Returns value description follows immediately after parameter names in square brakets [] and then brief details about what each part returns (if any).

### get_file_hash(self, file_path)

"Computes file hash using SHA256 algorithm from 'hashlib' library."

### needs_update(self, file_path)

Function `needs_update` checks if a file needs to be updated or not based on its last modification time.

### update(self, file_path)

Updates a file with details provided by another dictionary.

Args:
- self (required) : An instance of this class or an object that will use `update` method to update. This is mandatory because the first argument in any Python method must be always passed, usually 'self'.

