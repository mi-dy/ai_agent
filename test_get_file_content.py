from functions.get_file_content import get_file_content

content = get_file_content("calculator", "lorem.txt")
print(len(content))
if '[...File "lorem.txt" truncated at 10000 characters]' in content:
    print("Truncated")

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))
