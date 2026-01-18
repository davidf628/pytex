import os

dir_path = '/Users/flennerdr/Library/CloudStorage/OneDrive-CollegeofCharleston/Courses/MATH 120/question-bank'

def build_enumerated_tex(dir_path=".", output_file="combined.tex"):
    # Collect .tex files
    tex_files = [f for f in os.listdir(dir_path) if f.endswith(".tex")]

    # Sort them alphabetically (optional)
    tex_files.sort()

    # Build LaTeX content
    lines = []
    lines.append(r"\documentclass{article}")
    lines.append('')
    lines.append(r'\usepackage[margin=0.75in,left=0.5in,right=0.5in]{geometry}')
    lines.append(r'\usepackage{mymath}')
    lines.append(r'\usepackage{pytex}')
    lines.append('')
    lines.append(r"\begin{document}")
    lines.append("")
    lines.append(r"\begin{enumerate}")
    lines.append('')
    lines.append(f"    @setlibraryfolder('{dir_path}')@")
    lines.append('')

    for filename in tex_files:
        lines.append(r"  \item")
        safe_filename = filename.replace('_', '\\_')
        lines.append(f"    File: {safe_filename}\\\\")
        lines.append(f"    @importpytex('{filename}')@")
        lines.append("")

    lines.append(r"\end{enumerate}")
    lines.append(r"\end{document}")

    # Write output
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Created {output_file} with {len(tex_files)} items.")


if __name__ == "__main__":
    build_enumerated_tex(dir_path=dir_path)