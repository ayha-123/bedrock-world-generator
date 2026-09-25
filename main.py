import sys
import subprocess
import tempfile
import tarfile
import os
import glob


def main():
    print("Searching for getuInt...")
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

    for root, dirs, files in os.walk(extract_dir):
        for filename in files:
            if filename.endswith((".cpp", ".h", ".hpp")):
                path = os.path.join(root, filename)

                with open(
                    path,
                    "r",
                    encoding="utf-8",
                    errors="replace"
                ) as f:
                    source = f.read()

                if "getuInt" in source:
                    print("FILE:", path)
                    print("=" * 80)

                    pos = 0

                    while True:
                        pos = source.find("getuInt", pos)

                        if pos == -1:
                            break

                        print(
                            source[
                                max(0, pos - 500):
                                pos + 1500
                            ]
                        )

                        print("=" * 80)

                        pos += len("getuInt")

    print("Finished.")


if __name__ == "__main__":
    main()
