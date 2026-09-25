import sys
import subprocess
import tempfile
import tarfile
import os
import glob


def main():
    print("Minecraft Bedrock World Generator")
    print("Searching blockentity_demo JSON files...")
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

    demo_dir = None

    for root, dirs, files in os.walk(extract_dir):
        if os.path.basename(root) == "blockentity_demo":
            demo_dir = root
            break

    if demo_dir is None:
        # بعض النسخ يكون المثال ملف ipynb فقط
        for root, dirs, files in os.walk(extract_dir):
            if "blockentity_demo.ipynb" in files:
                demo_dir = root
                break

    if demo_dir is None:
        print("blockentity_demo directory not found.")
        return

    print("Demo directory:")
    print(demo_dir)
    print()

    found = False

    for root, dirs, files in os.walk(demo_dir):
        for filename in files:
            path = os.path.join(root, filename)

            print("FILE:", path)

            try:
                size = os.path.getsize(path)
                print("SIZE:", size, "bytes")
            except Exception:
                pass

            if filename.endswith(".json"):
                found = True

                print()
                print("JSON CONTENT:")
                print("-" * 80)

                try:
                    with open(
                        path,
                        "r",
                        encoding="utf-8",
                        errors="ignore"
                    ) as f:
                        content = f.read()

                    print(content[:12000])

                except Exception as e:
                    print("Could not read:", e)

                print("-" * 80)

            print()

    if not found:
        print("No JSON files found in blockentity_demo.")

    print("=" * 80)
    print("Finished.")
    print("No world files were modified.")


if __name__ == "__main__":
    main()
