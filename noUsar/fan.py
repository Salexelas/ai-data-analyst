import ast
import csv
from pathlib import Path
from collections import defaultdict

root = Path(".")

modules = {}
imports = defaultdict(set)

# Discover all Python modules
for file in root.rglob("*.py"):
    if "venv" in file.parts or "__pycache__" in file.parts:
        continue

    module = file.relative_to(root).with_suffix("").as_posix().replace("/", ".")
    modules[module] = file

# Parse imports
for module, file in modules.items():
    try:
        tree = ast.parse(file.read_text(encoding="utf-8"))
    except Exception:
        continue

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            for alias in node.names:
                imported = alias.name.split(".")[0]

                for target in modules:
                    if target.split(".")[0] == imported:
                        imports[module].add(target)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported = node.module.split(".")[0]

                for target in modules:
                    if target.split(".")[0] == imported:
                        imports[module].add(target)

# Compute Fan-In
fan_in = defaultdict(int)

for source, targets in imports.items():
    for target in targets:
        fan_in[target] += 1

# Print report
print(f'{"Module":40} {"Fan In":>7} {"Fan Out":>8}')
print("-" * 58)

for module in sorted(modules):
    print(
        f"{module:40} "
        f"{fan_in[module]:>7} "
        f"{len(imports[module]):>8}"
    )

# Save CSV for Excel
with open("fan_metrics.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["Module", "Fan In", "Fan Out"])

    for module in sorted(modules):
        writer.writerow([
            module,
            fan_in[module],
            len(imports[module])
        ])

print("\nCSV report saved as fan_metrics.csv")