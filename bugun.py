from datetime import datetime
import pandas as pd
import os
import subprocess
import sys

print("[INFO] Bugünün maçları güncelleniyor...")
# data.xlsx dosya üzerinden bugünün maçları silinecek.
if not os.path.exists("data.xlsx"):
    print("[ERROR] data.xlsx dosyası bulunamadı. Lütfen veri çekme işlemi yaparak data.xlsx dosyasını oluşturun.")
    exit()
data = pd.read_excel("data.xlsx")
data = data[data["Tarih"] != datetime.today().strftime("%d/%m/%Y")]
data.to_excel("data.xlsx", index=False)
print("[INFO] Bugünün maçları güncellendi.")
print("[INFO] Bugünün maçları çekiliyor...")
subprocess.run([sys.executable, "main.py"])
print("[INFO] Bugünün maçları çekildi.")
print("[INFO] Program sonlandırıldı.")