# PCD_PY

This is a PCD_PY package. You can use
[GitHub-AkshuDev](https://github.com/AkshuDev)

## Overview:

PCD stands for Python Clipped Dictionaries, a versatile package that empowers you to seamlessly work with numerous files using minimal code. It extends its capabilities beyond file manipulation, enabling the creation of simple folders with secure functionality. Additionally, it facilitates tracking changes in directories, designed with the primary goal of accelerating your coding speed. PCD_PY is not just limited to file operations; it introduces an embedded programming language known as AOL (Assembly Oriented Language). This language allows users to craft intricate assembly code effortlessly, and even build operating systems with just a few lines.

## Key Features:

- **Effortless File Operations:** PCD_PY simplifies file handling, providing functions that read, write, append, and delete files effortlessly.

- **Secure Functionality:** Create folders with secure and MySQL capabilities, adding an organized layer to your file management.

- **Directory Change Tracking:** Keep track on changes within directories, ensuring your code adapts to evolving file structures.

- **AOS Command Prompt:** PCD_PY comes with an AOS (Assembly Oriented Language) command prompt, allowing users to interactively work with assembly-oriented code.

- **Embedded Programming Language (AOL):** Unleash the power of AOL, an embedded language that empowers users to write complex assembly code with ease. It opens the door to crafting entire operating systems using concise commands.

## Usage

To use this module, simply import it and call the desired function:

```python
import pcd_py

pcd_py.run_cmdline({command you want to run})

Or

import pcd_py

pcd_py.EXTRA_cmds.{the name of command you want to run}({Parameters})

## Some Functions

### `run_cmdline("read file {Parameters}") -> str`

This function reads the contents of a file and returns them as a string.

**Parameters:**
- `filepath`: A string representing the path of the file to be read.

**Returns:**
- A string containing the contents of the file.

**Raises:**
- `FileNotFoundError`: If the file does not exist.

### `run_cmdline("write file {Parameters}") -> None`

This function writes a string to a file.

**Parameters:**
- `filepath`: A string representing the path of the file to be written.
- `content`: A string containing the contents to be written to the file.

**Returns:**
- None

**Raises:**
- `FileNotFoundError`: If the file does not exist.
- `PermissionError`: If the user does not have permission to write to the file.

### `run_cmdline("append file {Parameters}") -> None`

This function appends a string to the end of a file.

**Parameters:**
- `filepath`: A string representing the path of the file to be appended.
- `content`: A string containing the contents to be appended to the file.

**Returns:**
- None

**Raises:**
- `FileNotFoundError`: If the file does not exist.
- `PermissionError`: If the user does not have permission to append to the file.

### `run_cmdline("delete file {Parameters}") -> None`

This function deletes a file.

**Parameters:**
- `filepath`: A string representing the path of the file to be deleted.

**Returns:**
- None

**Raises:**
- `FileNotFoundError`: If the file does not exist.
- `PermissionError`: If the user does not have permission to delete the file.

### `run_cmdline("create os bootloader {Parameters}") -> None`

This function creates a bootloader for loading an operating system. The code will be written in AMS format.

**Parameters:**
- `filepath`: A string representing the path of the file to be created.

**Returns:**
- None

**Raises:**
- `FileNotFoundError`: If the file does not exist.
- `PermissionError`: If the user does not have permission to create the file.

### `run_cmdline("aos cmdline") -> None`

This function launches an interactive AOS (Assembly Oriented Language) command prompt, providing users with a powerful environment to work with assembly-oriented code.

**Parameters:**
- None

**Returns:**
- None

## All Functions

### File Operations

#### `run_cmdline("read file {Parameters}") -> str`

Reads the contents of a file and returns them as a string.

**Parameters:**
- `filepath`: A string representing the path of the file to be read.

**Returns:**
- A string containing the contents of the file.

**Raises:**
- `FileNotFoundError`: If the file does not exist.

#### `run_cmdline("write file {Parameters}") -> None`

Writes a string to a file.

**Parameters:**
- `filepath`: A string representing the path of the file to be written.
- `content`: A string containing the contents to be written to the file.

**Raises:**
- `FileNotFoundError`: If the file does not exist.
- `PermissionError`: If the user does not have permission to write to the file.

#### `run_cmdline("append file {Parameters}") -> None`

Appends a string to the end of a file.

**Parameters:**
- `filepath`: A string representing the path of the file to be appended.
- `content`: A string containing the contents to be appended to the file.

**Raises:**
- `FileNotFoundError`: If the file does not exist.
- `PermissionError`: If the user does not have permission to append to the file.

#### `run_cmdline("delete file {Parameters}") -> None`

Deletes a file.

**Parameters:**
- `filepath`: A string representing the path of the file to be deleted.

**Raises:**
- `FileNotFoundError`: If the file does not exist.
- `PermissionError`: If the user does not have permission to delete the file.

### Operating System Tools

#### `run_cmdline("create os bootloader {Parameters}") -> None`

Creates a bootloader for loading an operating system. The code will be written in AMS format.

**Parameters:**
- `filepath`: A string representing the path of the file to be created.

**Raises:**
- `FileNotFoundError`: If the file does not exist.
- `PermissionError`: If the user does not have permission to create the file.

#### `run_cmdline("aos cmdline") -> None`

Launches an interactive AOS (Assembly Oriented Language) command prompt, providing users with a powerful environment to work with assembly-oriented code.

**Parameters:**
- None

**Returns:**
- None

### Directory and File Management

#### `run_cmdline("make dir {Parameters}") -> None`

Creates a new directory.

**Parameters:**
- `path`: A string representing the path of the directory to be created.

#### `run_cmdline("make dirs {Parameters}") -> None`

Creates multiple directories.

**Parameters:**
- `path`: A string representing the path of the directories to be created.

#### `run_cmdline("dir file check {Parameters}") -> None`

Checks if files within a directory are valid.

**Parameters:**
- `path`: A string representing the path of the directory to be checked.

### PCD Operations

#### `run_cmdline("pcd {Query}") -> None`

Executes a PCD query, allowing for interactions with Python Clipped Dictionaries (PCD) functionality.

**Parameters:**
- `Query`: A string representing the PCD query to be executed.

## Additional Convenience with EXTRA_cmds

The `EXTRA_cmds` class provides a convenient way to streamline your interactions with the PCD_PY module. This class encapsulates various commands, making it easier to perform common operations with just a few lines of code.

### Usage Example:

```python
import pcd_py

# Example: Creating a Database with EXTRA_cmds
EXTRA_cmds.make_db("path/to/directory", "database_name", "your_password")

# Example: Adding Files to a Database with EXTRA_cmds
EXTRA_cmds.add_files_in_db("path/to/database", type="str", content="your_content", name="file_name")

# Example: Launching the AOS Command Prompt with EXTRA_cmds
EXTRA_cmds.aos_cmdline()

# ... and more!

## Assembly Oriented Language (AOL) Integration

PCD_PY comes with an integrated programming language called AOL (Assembly Oriented Language). This language provides users with the capability to write complex assembly code or even create an entire operating system with just a few lines.

### Example Usage:

```python
import pcd_py

# Example: Writing AOL code using AOS Command Line
pcd_py.EXTRA_cmds.aol("your_aol_code_here")

# Example: Launching the AOS Command Line with AOL
pcd_py.EXTRA_cmds.aos_cmdline()

To use AOL in AOS Command Line, Type -
$aos -> aol

Make sure to note that '$aos -> ' is the AOS Command Line Interpreter

### Using AOL from a File

To execute AOL code stored in a file, follow these steps:

1. Create a file with the extension `.aol` containing your AOL code.
2. Use the `AOS Command Line` to run the AOL code from the file.

### Example Usage:

Assuming you have a file named `example.aol` with AOL code:

```aol
; example.aol
#include <PACI.aol.stdlib>
section .var
    var msg = "Hello World! \n";

stdlib.global((section .var));

int main(){
    var not_a_global_msg = "Hello World! \n";
    print(msg);
    print(not_a_global_msg);
}
; Your AOL code here

Make sure to replace `"example.aol"` with the actual path or name of your AOL file.

Now, start your AOS Command Line using -

import pcd
pcd.EXTRA_cmds.aos_cmdline()

Assuming you have started AOS Command Line, you can use the following command to execute your aol file -

$aos -> aol --convert:asm example.aol

Make sure to note that '$aos -> ' is the AOS Command Line Interpreter

### AOL Compilations

1. **Convert AOL Code:**
   - Command: `aol --convert: (asm, bin) (file path)`
   - Description: Converts AOL code into the specified language. Supported languages are assembly (asm) or binary (bin).

   Example:
   ```AOS Command Line
   $aos -> aol --convert:asm path/to/your/aol/code.aol

2. Compile AOL Code:

    Command: 'aol --compile (file path)'
    Description: Compiles AOL code using the AOS cmdline.
    Example:
    ```AOS Command Line
    $aos -> aol --compile path/to/your/aol/code.aol

Important Notice -

1. The --convert option supports two output formats: assembly (asm) and binary (bin). Ensure that you specify the desired output language.

2. The --compile option compiles the AOL code using AOS cmdline.

3. Make sure that you leave no space between --convert: and your output format.