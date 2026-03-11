import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):

    try:
        abs_path = os.path.abspath(working_directory)

        target_path = os.path.normpath(os.path.join(abs_path, file_path))

        valid_target_dir = os.path.commonpath([abs_path, target_path]) == abs_path

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_path, "r") as file:
            f_content = file.read(MAX_CHARS)

            if file.read(1):
                f_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]' 
            
            return f_content

    except Exception as err:
        return f"Error: {err}"
