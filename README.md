<div align="center">
  <h1>MyFinance </h1>
  <img src="docs/MyFinance_Logo.png" alt="PyCalc Pro Logo" width="200">
  <br>
  <img src="https://img.shields.io/github/stars/Lorydima/MyFinance?color=gold" alt="GitHub stars">
  <img src="https://img.shields.io/badge/platforms-Windows%20%7C%20Linux%20via%20Wine or main.py%20%7C%20macOS%20via%20main.py-red" alt="Platforms">
  <img src="https://img.shields.io/badge/contributions-welcome-green" alt="Contributions welcome">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="License: MIT">
  <br>

</div>

<div align="center">
  <a href="https://lorydima.github.io/MyFinance/" target="_blank" style="font-size: 30px; font-weight: bold;">Website</a>
</div>

<br>
<p align="center"><strong>GUI App for finance managment</strong></p>

https://github.com/user-attachments/assets/609b535c-5e7d-4336-8034-67c8e6f1dfa4

# 🎲 Features

| Img | Feature Description |
|:---:|-------------------|
| <img src="https://lorydima.github.io/MyFinance/MyFInance_README02.png" width="600"> | **Graph functions:** This function allows you to generate visual charts of your balance over time, helping you analyze your financial growth and spending patterns. |
| <img src="https://lorydima.github.io/MyFinance/MyFinance_README03.png" width="600"> | **Transaction table:** This function displays a full historical record of your incomes and expenses in an organized table, allowing for easy data management and review. |

# 📁 Project Structure

```text
MyFinance/
├── Src/                             # Desktop app source code
│   ├── Assets/                      # Application data and icon files
│   │   ├── DATA.json                # Saved transactions and currency
│   │   └── MyFinance_Logo.ico       # App icon used by the GUI
│   ├── app.py                       # GUI windows, dialogs, and charts
│   ├── config.py                    # Shared paths, colors, fonts, and version values
│   ├── main.py                      # Application entry point
│   └── storage.py                   # JSON loading, saving, and data migration
├── Website/
│   ├── index.html                   # Website home page
│   └── style.css                    # Website styling
├── CHANGELOG.md                     # Version history
├── CONTRIBUTING.md                  # Contribution guide
├── LICENSE.txt                      # MIT license text
├── README.md                        # Project overview
├── SECURITY.md                      # Security policy
├── pyproject.toml                   # Packaging metadata
└── requirements.txt                 # Python dependencies
```

**About assets:**
Assets (icons and data files) are stored inside so the application can find them when run from source or packaged.

**About the docs/ folder:**
The docs/ folder contains files used for the source code of website. It is not required to run the application locally.

# 💾Downolad MyFinance

To donwload MyFinance V3.0 follow this link, the software is for **Windows OS, for linux use Wine:**
<a href="https://github.com/Lorydima/MyFinance/releases/download/MyFinanceV3.0/MyFinance_V3.0.zip" download>Download MyFinance V3.0</a>

**For macOS**  
The `.app` file is not available.

However, the application can be run from source by executing the `main.py` file,
provided that Python and the required dependencies are installed.

# 🔗Clone Repository

```bash
git clone https://github.com/Lorydima/MyFinance.git
```

```bash
pip install -r requirements.txt
```

```bash
run main.py
```

# 🛠️Bug reports and issue

I do my best to keep this project stable and reliable, but bugs can still happen.
If you spot any issues or errors, feel free to open a GitHub issue.
Your feedback really helps me improve the project.

Thanks for contributing and helping make this project better from *LDM Dev*❤️

# 📄License

Before you use the software please read the **MIT License** license at this link: <a href="https://github.com/Lorydima/MyFinance?tab=License-1-ov-file#">License</a>
