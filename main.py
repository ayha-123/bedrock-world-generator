import sys
import subprocess
import tempfile
import tarfile
import os
import glob
import json


def main():
    print("Minecraft Bedrock World Generator")
    print("Reading blockentity_demo NBT examples...")
    print("=" * 80)

    temp_dir = tempfile.mkdtemp()

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "download",
            "pybedrock==0.0.7",
            "--no-binary",
            ":all:",
            "--no-deps",
            "--no-build-isolation",
            "-d",
            temp_dir,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(result.stderr)
        return

    archives = glob.glob(os.path.join(temp_dir, "*.tar.gz"))

    if not archives:
        print("Source archive not found.")
        return

    extract_dir = os.path.join(temp_dir, "source")
    os.makedirs(extract_dir, exist_ok=True)

    with tarfile.open(archives[0], "r:gz") as tar:
        tar.extractall(extract_dir)

    notebook = None

    for root, dirs, files in os.walk(extract_dir):
        if "blockentity_demo.ipynb" in files:
            notebook = os.path.join(root, "blockentity_demo.ipynb")
            break

    if notebook is None:
        print("Notebook not found.")
        return

    with open(notebook, "r", encoding="utf-8") as f:
        data = json.load(f)

    found = 0

    for cell_number, cell in enumerate(data.get("cells", []), 1):
        source = "".join(cell.get("source", []))

        if any(x in source for x in [
            "writeNBT",
            "readNBT",
            "cspawner",
            "schunk",
            "palette"
        ]):
            found += 1

            print()
            print("=" * 80)
            print("CELL:", cell_number)
            print("=" * 80)
            print(source)

    print()
    print("=" * 80)
    print("Found relevant cells:", found)
    print("Finished.")
    print("No world files were modified.")


if __name__ == "__main__":
    main()
