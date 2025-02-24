#!/usr/bin/env python

import os
import shutil
import re

# Define the main LaTeX file that should stay in the root directory
MAIN_TEX_FILE = "ww_semiempirical_TRfmt.tex"
KEEP_IN_ROOT = ["ww_semiempirical_TRfmt.tex", "abstract.tex"]

# Ensure `packages.tex` is moved to `macros/`
SPECIAL_LOCATIONS = {
    "packages.tex": "macros"
}

# List of files that are \input{} in other LaTeX files
INPUT_FILES = {
    "sections": [
        "100_introduction.tex", "110_intro_slt_vs_statmech.tex", "120_intro_htsr.tex", 
        "130_intro_semiempirical.tex", "140_intro_setol.tex", "150_intro_outline.tex",
        "200_htsr.tex", "210_htsr_setup.tex", "220_htsr_gaussian.tex", "230_htsr_data_free.tex",
        "300_setol.tex", "310_setol_overview.tex", "320_setol_comparisons.tex", "330_setol_detecting.tex",
        "331_correlation_traps.tex", "332_over_regularization.tex", "400_smog.tex",
        "410_smog_traditional.tex", "420_smog_mathP.tex", "430_smog_st_model.tex",
        "440_smog_gen_gap.tex", "450_new.tex", "460_smog_theory_st_avg.tex",
        "500_matgen.tex", "510_new.tex", "520_matgen_multilayer_setup.tex",
        "530_matgen_quality_metrics.tex", "540_matgen_hciz.tex", "550_matgen_r_transforms.tex",
        "600_empirical.tex", "610_empirical_htsr.tex", "620_empirical_testing_ecs.tex",
        "630_empirical_eval_trace_log.tex", "650_empirical_corr_trap.tex",
        "660_empirical_overloading.tex", "data_mapping.tex", "precision_fig.tex",
        "overlap_figure.tex", "mapping_table.tex"
    ],
    "appendix": [
        "A1_tables.tex", "A2_sst_summary.tex", "A6_tanaka.tex",
        "A61_tanaka.tex", "A62_tanaka.tex", "A63_tanaka.tex", "A64_tanaka.tex", "A65_tanaka.tex",
        "pnas-supplementary.tex", "supplementary.tex"
    ]
}

# Define folder structure with regex patterns
FOLDERS = {
    "sections": re.compile(r"^\d{3}_.*\.tex$"),  # Numbered section files (e.g., 100_intro.tex)
    "appendix": re.compile(r"^A\d+_.*\.tex$"),  # Appendix files (e.g., A1_tables.tex)
    "figures": [".png", ".jpg", ".jpeg", ".eps", ".pdf"],
    "bibliography": [".bib"],
    "macros": ["macros.tex", "phrase_macros.tex"],  # Now includes `packages.tex`
    "scripts": [".py", ".sh"],
    "notebooks": [".ipynb"],
    "data": [".feather", ".h5"],
    "results": ["results", "evaluation", "summary"],
    "templates": ["PNAS-template.tex", "pnas-sample.bib", "prx_main.tex"],
    "notes": ["notes", "prompts", ".txt"],
    "misc": []  # Will be used for files that don't fit into other categories
}

# Define file extensions to delete (junk files) – will ask before deleting
DELETE_EXTENSIONS = [".bak", ".aux", ".log", ".out", ".bbl", ".blg", ".synctex.gz", ".toc", "~", ".orig"]

# Create folders if they don’t exist
for folder in FOLDERS:
    os.makedirs(folder, exist_ok=True)

# Move files to appropriate folders
for filename in os.listdir():
    if os.path.isdir(filename) or filename in KEEP_IN_ROOT:
        continue  # Skip directories and main files that should stay in root

    moved = False

    # Special case: Move specific files (like packages.tex) to predefined locations
    if filename in SPECIAL_LOCATIONS:
        shutil.move(filename, os.path.join(SPECIAL_LOCATIONS[filename], filename))
        moved = True

    # First, check if it's a required \input{} file and move accordingly
    if not moved:
        for folder, files in INPUT_FILES.items():
            if filename in files:
                shutil.move(filename, os.path.join(folder, filename))
                moved = True
                break

    # If not already moved, use regex-based or extension-based classification
    if not moved:
        for folder, pattern in FOLDERS.items():
            if isinstance(pattern, re.Pattern):  # Regex patterns for sections/appendix
                if pattern.match(filename):
                    shutil.move(filename, os.path.join(folder, filename))
                    moved = True
                    break
            else:
                if any(filename.endswith(ext) or filename.startswith(ext) for ext in pattern):
                    shutil.move(filename, os.path.join(folder, filename))
                    moved = True
                    break

    # If a file is still in the root and not part of KEEP_IN_ROOT, move it to misc/
    if not moved:
        shutil.move(filename, os.path.join("misc", filename))

# Ask before deleting unnecessary files
for filename in os.listdir():
    if any(filename.endswith(ext) for ext in DELETE_EXTENSIONS):
        response = input(f"❗ Do you want to delete {filename}? (y/n): ").strip().lower()
        if response == "y":
            os.remove(filename)
            print(f"🗑️ Deleted: {filename}")
        else:
            print(f"❌ Kept: {filename}")

# Create .gitignore file
GITIGNORE_CONTENT = """
# LaTeX auxiliary files
*.aux
*.log
*.bbl
*.blg
*.synctex.gz
*.out
*.toc
*.fdb_latexmk
*.fls
*.lof
*.lot
*.gz
*.glg
*.glo
*.gls
*.glsdefs

# Temporary files
*.bak
*~
.DS_Store
__pycache__/
"""

with open(".gitignore", "w") as f:
    f.write(GITIGNORE_CONTENT)

print(f"✅ Cleanup complete! '{MAIN_TEX_FILE}' remains in the root folder, 'packages.tex' moved to 'macros/', and sections & appendix files are in place.")
