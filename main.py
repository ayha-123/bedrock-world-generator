import sys
import subprocess
import tempfile
import tarfile
import os
import glob


def main():
    print("Reading pybedrock readSubchunk source...")
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
        if "subchunk.cpp" in files:
            target = os.path.join(root, "subchunk.cpp")
            break

    if target is None:
        print("subchunk.cpp not found.")
        return

    with open(target, "r", encoding="utf-8", errors="replace") as f:
        source = f.read()

    start = source.find("py_readSubchunk")

    if start == -1:
        print("py_readSubchunk not found.")
        print()
        print("Functions found:")
        for line in source.splitlines():
            if "readSubchunk" in line:
                print(line)
        return

    # اطبع جزءًا كبيرًا حول الدالة
    print(source[start:start + 12000])

    print()
    print("=" * 80)
    print("Finished.")


if __name__ == "__main__":
    main()
