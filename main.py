import sys
import subprocess
import tempfile
import tarfile
import os
import glob


def main():
    print("Searching pybedrock source files...")
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

    print("Files containing NBT or JSON:")
    print()

    found = 0

    for root, dirs, files in os.walk(extract_dir):
        for filename in files:
            lower = filename.lower()

            if (
                "nbt" in lower
                or lower.endswith(".json")
                or "subchunk" in lower
            ):
                path = os.path.join(root, filename)
                print(path)
                found += 1

    print()
    print("=" * 80)
    print("Found:", found)
    print("Finished.")


if __name__ == "__main__":
    main()
