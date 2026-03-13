import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_directory)

        target_path = os.path.normpath(os.path.join(abs_path, file_path))

        valid_target_dir = os.path.commonpath([abs_path, target_path]) == abs_path

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        file_type = target_path.split(".", 1) 
        if len(file_type) == 2:
            if file_type[1] != "py":
                return f'Error: "{file_path}" is not a Python file'
        else:
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]
        if args != None:
            for arg in args:
                command.extend(arg)
        output = ""

        ProcessObject = subprocess.run(command, capture_output=True, timeout=30, text=True)
        
        if ProcessObject.returncode != 0:
            output += f"\nProcess exited with code {ProcessObject.returncode}"

        if ProcessObject.stdout == None and ProcessObject.stderr == None:
            output += "\nNo output produced"
        else:
            output += f"\nSTDOUT:\n{ProcessObject.stdout}" 
            output += f"\nSTDERR:\n{ProcessObject.stderr}"

        return output

    except Exception as err:
        return f"Error: executing Python file: {err}"
