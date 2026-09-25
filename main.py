import sys
import subprocess
import tempfile
import tarfile
import os
import glob


def main():
    print("Minecraft Bedrock World Generator")
    print("Searching pybedrock examples for block palette...")
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

    found = 0

    for root, dirs, files in os.walk(extract_dir):
        for filename in files:
            if not filename.endswith((".py", ".ipynb", ".txt")):
                continue

            path = os.path.join(root, filename)

            try:
                with open(
                    path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:
                    content = f.read()
            except Exception:
                continue

            # نبحث عن أمثلة مرتبطة بالبلوكات والـpalette
            keywords = [
                "minecraft:stone",
                "minecraft:grass",
                "minecraft:dirt",
                "minecraft:water",
                "palette",
                "writeNBT",
            ]

            if any(keyword in content for keyword in keywords):
                print()
                print("=" * 80)
                print("FILE:", path)
                print("=" * 80)

                lines = content.splitlines()

                for i, line in enumerate(lines):
                    if any(keyword in line for keyword in keywords):
                        start = max(0, i - 8)
                        end = min(len(lines), i + 15)

                        print()
                        print(f"--- around line {i + 1} ---")

                        for j in range(start, end):
                            print(f"{j + 1}: {lines[j]}")

                        found += 1

                        if found >= 20:
                            break

            if found >= 20:
                break

        if found >= 20:
            break

    print()
    print("=" * 80)
    print("Finished.")
    print("No world files were modified.")


if __name__ == "__main__":
    main()
