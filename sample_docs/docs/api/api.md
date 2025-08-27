# api

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)

## Module Overview

This module contains 3 functions:

| Function | Description | Line |
|----------|-------------|------|
| `constructor` | **Function : constructor() -> object { }  # Brief ... | 6 |
| `getUsers` | Function: `getUsers` ... | 14 |
| `createUser` | # Function: createUser(userId, userName) ... | 24 |

## Functions

### `constructor()`

*Defined at line 6*

```python
constructor()
```

**Function : constructor() -> object { }  # Brief Function's description   **\n\n", Args:\nparam1: param_name (Description for parameter)\nReturns::Return Value Description)

**Example Usage:**

```python
# Example usage of constructor
result = constructor()
```

---

### `getUsers()`

*Defined at line 14*

```python
getUsers()
```

Function: `getUsers` 
Parameters: []  
Include: Brief description, Args section with Parameter descriptions and Returns sections for both parameters as well returns part; Example if helpful (if any) can be included here.   
Format exactly like this using markdown formatting rules - you should include a brief summary of what the function does in one line followed by an args: parameter description, then return value/s along with their descriptions after that are separated for better readability and maintainablity (if any).   Examples can be included if there're specific ways to use this functions.

**Example Usage:**

```python
# Example usage of getUsers
result = getUsers()
```

---

### `createUser()`

*Defined at line 24*

```python
createUser()
```

# Function: createUser(userId, userName) 

Create a new User in our database with provided ID and name (username). If such an existing account already exists or if other parameters are not valid then it will return False. Otherwise True is returned indicating successful creation of the user. This function can be invoked from users module to create, manage & update Users information within system like adding new User into DB etc..
Args: 
    -userId (int): Unique id for this account in our database . Must not exist beforehand and will generate randomly if it is unique or random. It should start with a positive integer value indicating the ID of user, which can be used to identify users globally within system e.g., UserID 10 would always represent active/logged-in status for account_id = 10 .
    -userName (str): The name that uniquely identifies this particular person in our database and should not exist if a user with the same username already exists, as it will be used to identify users globally. It can contain alphanumeric characters only allowing uppercase letters or lower case Letters followed by numbers from 0-

**Example Usage:**

```python
# Example usage of createUser
result = createUser()
```

---

