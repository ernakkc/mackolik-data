import os 
import sys
import subprocess   
from time import sleep
from datetime import datetime, timedelta

def install_dependencies():
    try:
        import os
        from time import sleep
        import selenium
        import webdriver_manager
        import pandas as pd
        import openpyxl
        import requests
    except ImportError:
        print("Selenium ve bağımlılıkları yükleniyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver_manager"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        print("\n\n\n")
        print("Bağımlılıklar yüklendi. Program yeniden başlatılıyor...")
        sleep(4)
        os.execl(sys.executable, sys.executable, *sys.argv)
        
install_dependencies()
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoAlertPresentException, TimeoutException     

class Mackolik:
    def __init__(self):
        self.GITHUB_FILE_URL = "https://raw.githubusercontent.com/ernakkc/mackolik-data/refs/heads/main/flag.txt"
        self.check_permission()
        self.browser = None
        self.url = "https://arsiv.mackolik.com/Canli-Sonuclar"
        self.complatedDays = []
        self.basliklar = ["Tarih", "Maç", "Link", "Score", "Maç Sonucu", "Çifte Şans" , "1. Yarı Sonucu","İlk Yarı/Maç Sonucu", "1. Yarı 0,5 Alt/Üst", "1. Yarı 1,5 Alt/Üst", "1. Yarı 2,5 Alt/Üst", "1,5 Alt/Üst", "2,5 Alt/Üst", "3,5 Alt/Üst", "4,5 Alt/Üst", "5,5 Alt/Üst", "Karşılıklı Gol", "Toplam Gol Aralığı"]
        self.excelFile = "data.xlsx"
        self.data = self.get_data_from_excel()
        
        self.from_day = "2019-01-01" # YYYY-MM-DD
        
        self.run()
        
    def check_permission(self):
        permission = False
        try:
            response = requests.get(self.GITHUB_FILE_URL, timeout=5)
            if response.status_code == 200 and response.text.strip() == "1": permission = True
        except Exception as e: print(f"Bağlantı hatası: {e}")
        
        if not permission:
            print("[ERROR] Programı kullanabilmek için izniniz yok.")
            print("[INFO] İzin almak için: https://instagram.com/ern.akkc adresinden ulaşabilirsiniz.")
            exit()

        
    def start_browser(self):
        print("[INFO] Tarayıcı başlatılıyor...")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        self.browser.get(self.url)
        print("[SUCCESS] Tarayıcı başlatıldı.")
        
    def close_browser(self):
        self.browser.quit()
        print("[INFO] Tarayıcı kapatıldı.")
        self.browser = None
        
    def reopen_browser(self):
        self.close_browser()
        self.start_browser()
        print("[INFO] Tarayıcı yeniden başlatıldı.")
        
    def get_data_from_excel(self) -> pd.DataFrame:
        try:
            return pd.read_excel(self.excelFile)
        except FileNotFoundError:
            return pd.DataFrame(columns=self.basliklar)
        
    def append_new_row(self, tarih=None, mac=None, link=None, score=None, mac_sonucu=None, cift_sans=None, birinci_yari_sonucu=None, ilk_yari_mac_sonucu=None, birinci_yari_05=None, birinci_yari_15=None, birinci_yari_25=None, birbucluk_ust=None, iki_bucuk_ust=None, uc_bucuk_ust=None, dort_bucuk_ust=None, bes_bucuk_ust=None, karsilikli_gol=None, toplam_gol_araligi=None):
        new_row = pd.DataFrame([{ 
        "Tarih": tarih,
        "Maç": mac,
        "Link": link,
        "Score": score,
        "Maç Sonucu": mac_sonucu,
        "Çifte Şans": cift_sans,
        "1. Yarı Sonucu": birinci_yari_sonucu,
        "İlk Yarı/Maç Sonucu": ilk_yari_mac_sonucu,
        "1. Yarı 0,5 Alt/Üst": birinci_yari_05,
        "1. Yarı 1,5 Alt/Üst": birinci_yari_15,
        "1. Yarı 2,5 Alt/Üst": birinci_yari_25,
        "1,5 Alt/Üst": birbucluk_ust,
        "2,5 Alt/Üst": iki_bucuk_ust,
        "3,5 Alt/Üst": uc_bucuk_ust,
        "4,5 Alt/Üst": dort_bucuk_ust,
        "5,5 Alt/Üst": bes_bucuk_ust,
        "Karşılıklı Gol": karsilikli_gol,
        "Toplam Gol Aralığı": toplam_gol_araligi
        }])    
        self.data = pd.concat([self.data, new_row], ignore_index=True)
    
    def update_data(self, tarih, mac, **kwargs):
        columns = list(kwargs.keys())
        values = [str(v) for v in kwargs.values()]
        mask = (self.data["Tarih"] == tarih) & (self.data["Maç"] == mac)

        if self.data[mask].empty:
            new_row = {col: None for col in self.data.columns}  
            new_row["Tarih"] = tarih
            new_row["Maç"] = mac
            for col, val in zip(columns, values):
                new_row[col] = val
            self.data = pd.concat([self.data, pd.DataFrame([new_row])], ignore_index=True)
        else:
            self.data.loc[mask, columns] = values

    def write_to_excel(self, count=None, total=None):
        self.data.to_excel(self.excelFile, index=False)
        print(f"[INFO] {count}/{total} Excel dosyası güncelleniyor. Lütfen Bekleyiniz...")
        
    def open_webpage(self):
        # Accept cookies
        wait = WebDriverWait(self.browser, 50)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "accept-all-btn"))).click()
        
        # Remove thicks
        self.browser.execute_script("checkSport(2);")
        self.browser.execute_script("getSelectedMatch('chkIddaa')")
        
        WebDriverWait(self.browser, 10)
    
    def get_match_links(self):
        for day in self.data["Tarih"]:
            self.complatedDays.append(day)
        
        date_input = self.browser.find_element(By.ID, "txtCalendar")

        start_date = datetime(int(self.from_day.split("-")[0]), int(self.from_day.split("-")[1]), int(self.from_day.split("-")[2]))
        end_date = datetime.today()
        
        print(f"[INFO] {start_date} - {end_date}")
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%d/%m/%Y")
            if date_str in self.complatedDays:
                print(f"[INFO] {date_str} zaten tamamlandı.")
                current_date += timedelta(days=1)
                continue
            self.complatedDays.append(date_str)
            
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "dvScores")))
            date_input.clear()
            date_input.send_keys(date_str) 
            ActionChains(self.browser).send_keys(Keys.ENTER).perform()
            ActionChains(self.browser).send_keys(Keys.ENTER).perform()
            while self.browser.find_element(By.ID, "dvScores").text == "Yükleniyor":
                sleep(1)
            if self.browser.find_element(By.ID, "dvScores").text == "Maç bulunamadı.":
                print(f"[INFO] {date_str} tarihli maçlar bulunamadı.")
                current_date += timedelta(days=1)
                continue
            
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "resultsList")))
            resultList = self.browser.find_element(By.ID, "resultsList")
            elements = resultList.find_elements(By.TAG_NAME, "tr")
            for element in elements:
                if element.get_attribute("class") == "rows-bg": continue
                teams = element.find_elements(By.CLASS_NAME, "teamDiv")
                team_s = ""
                for team in teams:
                    name = ""
                    for a in team.text.split(" "):
                        if a == "": continue
                        name += a + " "
                    name = name[:-1]
                    team_s += name + " - "
                team_s = team_s[:-3]
                try:
                    link = element.find_element(By.CLASS_NAME, "td_score").get_attribute("href")
                    score = element.find_element(By.CLASS_NAME, "td_score").text
                except: continue
                self.append_new_row(tarih=date_str, mac=team_s, link=link, score=score)

            print(f"[INFO] {date_str} tarihli maçlar alındı.")
            current_date += timedelta(days=1)    
        print("[INFO] Tüm maçlar alındı.")
        self.write_to_excel()
        print("[INFO] Çekilen linkler üzerinden iddia oranları çekilecek.")
           
    def iddia_oranlari(self):
        print("[INFO] Iddia oranları çekiliyor...")
        for index, row in self.data.iterrows():
            link = row["Link"]
            self.browser.get(link)
            compare_left_coll = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "compare-left-coll")))
            mds = compare_left_coll.find_elements(By.CLASS_NAME, "md")
            for md in mds:  
                md_divs = md.find_elements(By.TAG_NAME, "div")          
                baslik = md_divs[0].text.replace(md_divs[0].find_element(By.TAG_NAME, "span").text, "").replace("\n", "")
                icerik_divs = md_divs[1].find_elements(By.TAG_NAME, "div")
                name_value = ""
                for div in icerik_divs:
                    divs = div.find_elements(By.TAG_NAME, "div")
                    if len(divs) == 0: continue
                    name = divs[0].text.replace("\n", "")
                    value = divs[1].text.replace("\n", "")
                    name_value += f"{name}: {value}\n"
                self.update_data(row["Tarih"], row["Maç"], **{baslik: name_value[:-1]})
            self.write_to_excel(index, len(self.data))
        print("[INFO] Iddia oranları çekildi.")
        self.write_to_excel()
        
    def edit_excel(self):
        print("[INFO] Excel dosyası düzenleniyor. Lütfen Bekleyiniz...")
        self.df = self.data.loc[:, ["Tarih", "Maç", "Link"]]
        self.df.drop_duplicates(inplace=True)
        print("[INFO] Yanlış veriler düzeltiliyor...")
        print("[INFO] Yeni başlıklar oluşuyor...")
        column_names = []
        for column in self.data.columns:
            if column == "Tarih" or column == "Maç" or column == "Link" or column == "Score": continue
            for index, row in self.data.iterrows():
                icerik = {}
                if row[column] is not None:
                    try: row[column].split("\n")
                    except: continue
                    for data in row[column].split("\n"):
                        icerik[f"{column}({data.split(': ')[0]})"] = data.split(': ')[1]
                    if column not in column_names:
                        column_names.append(column)
                        
                columns = list(icerik.keys())
                values = list(icerik.values())
                mask = (self.df["Tarih"] == row["Tarih"]) & (self.df["Maç"] == row["Maç"]) & (self.df["Link"] == row["Link"])
                if self.df[mask].empty:
                    new_row = {col: None for col in column_names}
                    new_row["Tarih"] = row["Tarih"]
                    new_row["Maç"] = row["Maç"]
                    new_row["Score"] = row["Score"]
                    for col, val in zip(columns, values):
                        new_row[col] = val
                    self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
                else:
                    self.df.loc[mask, columns] = values
        print("[INFO] Excel dosyası düzenlendi.")
        self.df.to_excel("edited_data.xlsx", index=False)
        print("[INFO] Excel dosyası kaydedildi. (edited_data.xlsx)")
    
    def run(self):
        self.start_browser()
        self.open_webpage()
        self.get_match_links()
        self.iddia_oranlari()
        self.edit_excel()
        self.close_browser()
        print("[INFO] Program sonlandırıldı.")
        
if __name__ == "__main__":
    Mackolik()