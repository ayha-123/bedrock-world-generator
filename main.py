import sys
import subprocess
import tempfile
import tarfile
import os
import glob


def main():
    print("Minecraft Bedrock World Generator")
    print("Reading complete writeSubchunk implementation...")

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

    archive = archives[0]

    extract_dir = os.path.join(temp_dir, "source")
    os.makedirs(extract_dir, exist_ok=True)

    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(extract_dir)

    source_file = None

    for root, dirs, files in os.walk(extract_dir):
        for filename in files:
            if filename == "subchunk.cpp":
                source_file = os.path.join(root, filename)
                break

        if source_file:
            break

    if not source_file:
        print("subchunk.cpp not found.")
        return

    print()
    print("Source:", source_file)
    print()
    print("=" * 80)
    print("COMPLETE py_writeSubchunk")
    print("=" * 80)

    with open(
        source_file,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:
        lines = f.readlines()

    start = None
    end = None

    for i, line in enumerate(lines):
        if "PyObject* py_writeSubchunk" in line:
            start = i

            # ابحث عن نهاية الدالة
            brace_count = 0
            started = False

            for j in range(i, len(lines)):
                brace_count += lines[j].count("{")
                brace_count -= lines[j].count("}")

                if "{" in lines[j]:
                    started = True

                if started and brace_count == 0:
                    end = j + 1
                    break

            break

    if start is None:
        print("py_writeSubchunk not found.")
        return

    if end is None:
        end = min(len(lines), start + 250)

    for i in range(start, end):
        print(f"{i + 1}: {lines[i].rstrip()}")

    print()
    print("=" * 80)
    print("END")
    print("=" * 80)


if __name__ == "__main__":
    main()
