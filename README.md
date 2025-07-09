# papers-fetcher

Fetch PubMed papers with at least one author affiliated with a pharmaceutical or biotech company, using a simple command-line tool.

---

## 🚀 Overview
This project provides a Python CLI tool to search PubMed for research papers matching a user query, and filter for papers with at least one author from a non-academic (pharma/biotech) company. Results can be saved as a CSV or printed to the console.

---

## ✨ Features
- **Flexible PubMed search**: Supports full PubMed query syntax.
- **Company author detection**: Uses heuristics to identify non-academic authors and company affiliations.
- **CSV output**: Save results to a file or print to the console.
- **Typed Python**: All code is type-annotated for clarity and safety.
- **Robust CLI**: Helpful options for debugging and output control.

---

## 🛠️ Setup & Installation

### 1. Prerequisites
- Python 3.9+
- [Poetry](https://python-poetry.org/docs/#installation) (for dependency management)
- [Git](https://git-scm.com/download/win) (for version control)

### 2. Clone the Repository
```sh
git clone https://github.com/yourusername/papers-fetcher.git
cd papers-fetcher
```

### 3. Install Dependencies
```sh
poetry install
```

### 4. Activate the Environment (Windows)
Find your Poetry environment path:
```sh
poetry env info --path
```
Then activate it:
```sh
& "<paste-the-path-here>\Scripts\Activate"
```

---

## 🏃 Usage

### Run as a CLI tool
```sh
poetry run get-papers-list "your pubmed query" -f results.csv
```

#### Options
- `-d`, `--debug` : Enable debug output
- `-f`, `--file`  : Output CSV file name (prints to console if omitted)
- `-h`, `--help`  : Show usage instructions

#### Example
```sh
poetry run get-papers-list "cancer immunotherapy" -f results.csv
```

---

## 🗂️ Code Organization
- `get_papers_list.py` : CLI entry point
- `papers_fetcher/`    : Core logic module
  - `fetch.py`         : Fetching, parsing, and filtering logic
  - `utils.py`         : Heuristics for affiliation detection
- `README.md`          : This file
- `.gitignore`         : Standard Python ignores
- `pyproject.toml`     : Poetry configuration

---

## 🧠 Heuristics for Non-Academic/Company Detection
- **Academic keywords**: Affiliations containing words like `university`, `institute`, `college`, `hospital`, etc. are considered academic.
- **Company keywords**: Affiliations with `pharma`, `biotech`, `inc`, `ltd`, `llc`, etc. are flagged as company.
- **Email domains**: Non-academic emails (not `.edu`, `.ac`, etc.) are considered company if found in the affiliation.
- **You can expand the keyword lists in `papers_fetcher/utils.py` for better accuracy.**

---

## 📦 Dependencies
- [requests](https://pypi.org/project/requests/)
- [click](https://pypi.org/project/click/)
- [pandas](https://pypi.org/project/pandas/)
- [lxml](https://pypi.org/project/lxml/)
- [typing-extensions](https://pypi.org/project/typing-extensions/)

---

## 📝 Publishing to Test PyPI (Bonus)
1. Register at [Test PyPI](https://test.pypi.org/account/register/)
2. Build your package:
   ```sh
   poetry build
   ```
3. Publish to Test PyPI:
   ```sh
   poetry publish -r testpypi
   ```
   (You may need to add the repository URL: `poetry config repositories.testpypi https://test.pypi.org/legacy/`)

---

## 🤖 Tools Used
- Developed with the help of LLMs and open-source libraries.
- All dependencies and tools are documented above.

---

## 🙋‍♂️ Need Help?
- If you have issues with Poetry or Windows PATH, see the [Poetry docs](https://python-poetry.org/docs/#installation) or ask for help!
- For improvements or bug reports, open an issue or pull request on GitHub.

---

Happy researching! 🎉
