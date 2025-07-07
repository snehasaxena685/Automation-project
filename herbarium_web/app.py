from flask import Flask, render_template, request, redirect
import pandas as pd
import os
from datetime import datetime
from openpyxl import load_workbook

app = Flask(__name__)
EXCEL_PATH = "Live_Herbarium_Log.xlsx"
IMAGE_DIR = "herb_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def get_next_specimen_id():
    try:
        df = pd.read_excel(EXCEL_PATH)
        if df.empty:
            return "HSPC001"
        last_id = df["Specimen ID"].dropna().iloc[-1]
        num = int(last_id[4:]) + 1
        return f"HSPC{num:03d}"
    except:
        return "HSPC001"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        sid = request.form["specimen_id"]
        herb = request.form["herb_name"]
        sci = request.form["scientific_name"]
        region = request.form["region"]
        weight = request.form["weight"]
        image = request.files.get("herb_image")

        filename = ""
        if image:
            ext = os.path.splitext(image.filename)[1]
            filename = f"{sid}_{herb.lower().replace(' ', '_')}{ext}"
            image.save(os.path.join(IMAGE_DIR, filename))

        row = [sid, herb, sci, datetime.now().strftime("%Y-%m-%d"), region, weight, "High" if region in ["Delhi", "Punjab"] else "Low", filename]
        
        try:
            wb = load_workbook(EXCEL_PATH)
            sheet = wb.active
            sheet.append(row)
            wb.save(EXCEL_PATH)
        except:
            pd.DataFrame([row], columns=["Specimen ID", "Herb Name", "Scientific Name", "Date", "Region", "Weight", "Priority", "Image"]).to_excel(EXCEL_PATH, index=False)

        return redirect("/")
    
    return render_template("index.html", sid=get_next_specimen_id())

if __name__ == "__main__":
    app.run(debug=True)
