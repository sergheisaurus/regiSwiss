import subprocess

# List of scripts to execute in order
scripts = ["get_xml.py", "xml_parser.py", "ne_admin.py", "vat_check.py", "final.py"]

for script in scripts:
    print(f"Executing {script}...")
    result = subprocess.run(["python", script], text=True)

    if result.returncode == 0:
        print(f"{script} executed successfully!\n")
    else:
        print(f"Error executing {script}. Exiting.\n")
        break

print("All scripts executed.")
