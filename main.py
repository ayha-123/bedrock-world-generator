import sys
import subprocess
import tempfile
import tarfile
import os
import glob


def main():
    print("Minecraft Bedrock World Generator")
    print("Reading writeNBT implementation...")
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
        print("Download failed:")
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

    # البحث عن ملف C/C++ الذي يحتوي writeNBT
    matches = []

    for root, dirs, files in os.walk(extract_dir):
        for filename in files:
            if filename.endswith((".cpp", ".c", ".h")):
                path = os.path.join(root, filename)

                try:
                    with open(
                        path,
                        "r",
                        encoding="utf-8",
                        errors="ignore"
                    ) as f:
                        content = f.read()

                    if "writeNBT" in content:
                        matches.append(path)

                except Exception:
                    pass

    if not matches:
        print("writeNBT source not found.")
        return

    print("Files containing writeNBT:")
    for path in matches:
        print(path)

    print()
    print("=" * 80)

    # طباعة الجزء الذي يحتوي على writeNBT
    for path in matches:
        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if "writeNBT" not in line:
                continue

            print()
            print("=" * 80)
            print("FILE:", path)
            print("STARTING AROUND LINE:", i + 1)
            print("=" * 80)

            start = max(0, i - 20)
            end = min(len(lines), i + 180)

            for j in range(start, end):
                print(f"{j + 1}: {lines[j].rstrip()}")

            print()
            print("=" * 80)

    print("Finished.")
    print("No world files were modified.")


if __name__ == "__main__":
    main()
