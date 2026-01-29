# 📊 Mackolik Data Scraper

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

*Automated football match data scraper from Mackolik archives with comprehensive statistics*

</div>

---

## 📖 Overview

Mackolik Data Scraper is a Python-based automation tool that extracts detailed football match data from Mackolik's archives. It collects comprehensive statistics including scores, betting odds, half-time results, goals, and more, exporting everything to Excel format for analysis.

## ✨ Features

- 🏆 **Comprehensive Data Collection**: 18+ different match metrics
- 📅 **Historical Data**: Scrape matches from any date range
- 📊 **Excel Export**: Clean, organized data in `.xlsx` format
- 🔄 **Automated Pagination**: Handles multiple pages automatically
- 🌐 **Chrome WebDriver**: Automated browser interactions
- 🛡️ **Permission System**: GitHub-based access control
- 📝 **Detailed Logging**: Track scraping progress and errors
- ⏸️ **Resume Capability**: Continue from last completed day

## 📊 Collected Data Fields

The scraper collects the following match statistics:

| Field | Description |
|-------|-------------|
| **Tarih** | Match date |
| **Maç** | Team names (Home vs Away) |
| **Link** | Match details URL |
| **Score** | Final score |
| **Maç Sonucu** | Match result (1/X/2) |
| **Çifte Şans** | Double chance odds |
| **1. Yarı Sonucu** | First half result |
| **İlk Yarı/Maç Sonucu** | Half-time/Full-time result |
| **1. Yarı 0,5/1,5/2,5 Alt/Üst** | First half goal markets |
| **1,5/2,5/3,5/4,5/5,5 Alt/Üst** | Full match goal markets |
| **Karşılıklı Gol** | Both teams to score |
| **Toplam Gol Aralığı** | Total goals range |

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Google Chrome browser
- Internet connection

### Quick Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ernakkc/mackolik-data.git
   cd mackolik-data
   ```

2. **Run the script** (auto-installs dependencies):
   ```bash
   python main.py
   ```

   The script automatically installs required packages:
   - selenium
   - webdriver-manager
   - pandas
   - openpyxl
   - requests

## 🚀 Usage

### Basic Usage

```bash
python main.py
```

The script will:
1. Check permission from GitHub
2. Initialize Chrome WebDriver
3. Navigate to Mackolik archives
4. Prompt for date range
5. Scrape all matches
6. Export to Excel

### Interactive Prompts

```
Hangi tarihe kadar geri gitmek istersiniz?
Format: GG.AA.YYYY (Örnek: 01.01.2023)
> 01.01.2024

Başlangıç tarihi: 29.01.2026
Bitiş tarihi: 01.01.2024
Toplam gün sayısı: 393

Devam etmek istiyor musunuz? (E/H):
> E
```

### Output

Data is saved to `mackolik_data_YYYYMMDD_HHMMSS.xlsx` with columns for all collected metrics.

## 📁 Project Structure

```
mackolik-data/
├── main.py              # Main scraper script
├── bugun.py            # Today's matches scraper
├── flag.txt            # Permission flag (GitHub)
├── requirements.txt    # Python dependencies (optional)
└── README.md           # This file
```

## 🔧 Configuration

### Permission System

The script checks `flag.txt` from GitHub:

```python
GITHUB_FILE_URL = "https://raw.githubusercontent.com/ernakkc/mackolik-data/main/flag.txt"
```

- `flag.txt` content: `1` = Access granted, `0` = Access denied

### Browser Options

Customize Chrome settings in `main.py`:

```python
chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--start-maximized')
# chrome_options.add_argument('--headless')  # Uncomment for headless mode
```

### Date Range

Modify date format and range logic:

```python
# Custom start date
start_date = datetime(2024, 1, 1)

# Custom end date
end_date = datetime.now()
```

## 🎯 Features Explained

### Automated WebDriver Management

```python
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
```

No manual ChromeDriver download needed!

### Data Extraction Pipeline

1. **Navigate to Archives**: Opens Mackolik historical data page
2. **Date Selection**: Clicks calendar and selects dates
3. **Match Extraction**: Loops through all match rows
4. **Details Scraping**: Clicks each match for statistics
5. **Data Storage**: Appends to pandas DataFrame
6. **Export**: Saves to Excel with formatting

### Error Handling

```python
try:
    # Scraping logic
except TimeoutException:
    print("Element bulunamadı, devam ediliyor...")
except NoAlertPresentException:
    pass
```

## 📊 Data Analysis Examples

### Using Pandas

```python
import pandas as pd

# Load scraped data
df = pd.read_excel('mackolik_data_20240129_143022.xlsx')

# High scoring matches
high_scores = df[df['Toplam Gol Aralığı'].str.contains('6+')]

# Home wins
home_wins = df[df['Maç Sonucu'] == '1']

# Average goals per match
df['Goals'] = df['Score'].str.extract('(\d+)-(\d+)').astype(int).sum(axis=1)
avg_goals = df['Goals'].mean()
```

## ⚠️ Legal & Ethical Considerations

- 🤖 Web scraping may violate website Terms of Service
- 📜 Respect robots.txt and rate limiting
- 🔒 This tool is for educational and research purposes
- ⚖️ Users are responsible for compliance with applicable laws
- 🚫 Do not use for commercial purposes without permission

## 🐛 Troubleshooting

### Permission Denied
```
GitHub dosyası okunamıyor
```
- Check internet connection
- Verify flag.txt exists in GitHub repo
- Ensure flag.txt contains "1"

### ChromeDriver Issues
```bash
# Update ChromeDriver automatically
pip install --upgrade webdriver-manager
```

### Element Not Found
- Website structure may have changed
- Update CSS selectors in code
- Increase wait times:
  ```python
  WebDriverWait(driver, 20)  # Increase timeout
  ```

### Excel Export Errors
```bash
pip install openpyxl --upgrade
```

## 🚀 Advanced Usage

### Scrape Specific League

```python
# Add league filter
league_name = "Süper Lig"
matches = [m for m in matches if league_name in m['League']]
```

### Custom Output Format

```python
# Save as CSV instead
df.to_csv('mackolik_data.csv', index=False, encoding='utf-8-sig')

# Save as JSON
df.to_json('mackolik_data.json', orient='records', force_ascii=False)
```

### Parallel Scraping

```python
from concurrent.futures import ThreadPoolExecutor

def scrape_day(date):
    # Scraping logic
    pass

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(scrape_day, date_range)
```

## 🤝 Contributing

Contributions are welcome! Ideas:
- Add more statistics (corners, cards, shots)
- Support for other sports
- Database storage instead of Excel
- Live match tracking
- Data visualization dashboard

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Eren Akkoç**
- GitHub: [@ernakkc](https://github.com/ernakkc)
- Email: ern.akkc@gmail.com

## 🌟 Acknowledgments

- Data source: [Mackolik](https://www.mackolik.com/)
- Selenium WebDriver for automation
- Pandas for data processing

---

<div align="center">

**Use Responsibly! ⚽📊**

*For educational and research purposes only*

</div>
