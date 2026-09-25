import sys
import subprocess
import tempfile
import tarfile
import os
import glob
import json


def main():
    print("Reading subchunk.nbt.json")
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

    target = None

    for root, dirs, files in os.walk(extract_dir):
        if "subchunk.nbt.json" in files:
            target = os.path.join(root, "subchunk.nbt.json")
            break

    if target is None:
        print("subchunk.nbt.json not found.")
        return

    print("FILE:", target)
    print("=" * 80)

    with open(target, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(json.dumps(data, ensure_ascii=False, indent=2))

    print()
    print("=" * 80)
    print("Finished.")


if __name__ == "__main__":
    main()
