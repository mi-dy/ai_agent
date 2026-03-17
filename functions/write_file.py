import os

from google.genai import types

def write_file(working_directory, file_path, content):
    try:

        abs_path = os.path.abspath(working_directory)

        target_path = os.path.normpath(os.path.join(abs_path, file_path))

        valid_target_dir = os.path.commonpath([abs_path, target_path]) == abs_path

        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_path), exist_ok=True)


        with open(target_path, "w") as file:
            file.write(content)
            
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as err:
        return f"Error: {err}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the string of content to the specified file in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to to the desired file to be written to",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string to be written in the desired file",
            ),
        },
    ),
)
