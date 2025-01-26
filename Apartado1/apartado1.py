import os, sys
import subprocess

# Clone the repository
subprocess.run(['git', 'clone', 'https://github.com/CDPS-ETSIT/practica_creativa2.git'], check=True)

# Replace "Simple Bookstore App" with "GRUPO15" in all files
subprocess.run(
    ['find', './practica_creativa2', '-type', 'f', '-exec', 'sed', '-i',
     's/Simple Bookstore App/GRUPO15/g', '{}', '+'],
    check=True
)

# Navigate to the product page directory
os.chdir('practica_creativa2/bookinfo/src/productpage')

# Modify the requirements.txt file to remove pinned version of `requests`
subprocess.run(["sed", "-i", "s/^requests==.*/requests/", "requirements.txt"], check=True)

# Install the required Python packages
subprocess.run(['pip3', 'install', '-r', 'requirements.txt'], check=True)

orden = sys.argv[1]

if orden == "9080":
    subprocess.run(['python3', 'productpage_monolith.py', str(orden)], check=True)
else:
    subprocess.run(['python3', 'productpage_monolith.py', str(orden)], check=True)