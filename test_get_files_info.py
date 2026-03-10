from functions.get_files_info import get_files_info

results = []


results.append((get_files_info("calculator", "."), "."))
results.append((get_files_info("calculator", "pkg"), "pkg"))
results.append((get_files_info("calculator", "/bin"), "/bin"))
results.append((get_files_info("calculator", "../"), "../"))

for result, d in results:
    if d == ".":
        d = "current"

    print(f"Result for {d} directory:")
    print(result)
    print("")
