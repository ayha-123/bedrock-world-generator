import sys
import subprocess
import tempfile
import tarfile
import os
import glob


def main():
    print("Minecraft Bedrock World Generator")
    print("Inspecting pybedrock source...")

    temp_dir = tempfile.mkdtemp()

    print()
    print("Downloading pybedrock 0.0.7 source...")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "download",
            "pybedrock==0.0.7",
            "--no-binary",
            ":all:",
            "-d",
            temp_dir,
        ],
        capture_output=True,
        text=True,
    )

    print(result.stdout)

    if result.returncode != 0:
        print("Download failed:")
        print(result.stderr)
        return

    files = glob.glob(os.path.join(temp_dir, "*.tar.gz"))

    if not files:
        print("Source archive not found.")
        return

    archive = files[0]

    print("Source archive:", archive)

    extract_dir = os.path.join(temp_dir, "source")

    os.makedirs(extract_dir, exist_ok=True)

    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(extract_dir)

    print()
    print("Searching source files for writeSubchunk...")

    found = False

    for root, dirs, filenames in os.walk(extract_dir):
        for filename in filenames:

            path = os.path.join(root, filename)

            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                continue

            if "writeSubchunk" in content:
                found = True

                print()
                print("=" * 70)
                print("FOUND:", path)
                print("=" * 70)

                lines = content.splitlines()

                for i, line in enumerate(lines):
                    if "writeSubchunk" in line:
                        start = max(0, i - 8)
                        end = min(len(lines), i + 15)

                        for n in range(start, end):
                            print(f"{n + 1}: {lines[n]}")

    if not found:
        print()
        print("writeSubchunk was not found in the source files.")

    print()
    print("Source inspection completed.")


if __name__ == "__main__":
    main()
