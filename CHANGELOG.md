# Changelog - MyFinance

All notable changes to this project will be documented in this file.
This project uses semantic versioning.

## [3.0.0] - 06/06/2026
### Added
- Tkinter GUI workflow with buttons for incomes, expenses, transaction history, graphs, credits, and currency changes.
- Local website assets in `Website/` with screenshots and project download information.
- Root-level packaging metadata in `pyproject.toml` and `requirements.txt`.

### Changed
- Renamed the entry script to `Src/main.py` so the repository now has a standard launch point.
- Application files now resolve `DATA.json`, `LICENSE.txt`, and icon assets from the application directory for packaged runs.
- Repository documentation was refreshed to match the local GUI version of MyFinance.

### Fixed
- Transaction migration and date normalization continue to support older `enter`/`exit` records and legacy date formats.

## [2.0.0] - 15/03/2026
### Added
- Command-line interface for adding income and expense transactions.
- Transaction tables, balance summaries, and balance graph output.
- Currency switching and automatic JSON data migration.

## [1.0.0] - 02/02/2026
### Added
- Initial CLI release with transaction tracking, balance viewing, and saved data in `DATA.json`.
