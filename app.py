import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import pyfiglet

banner = pyfiglet.figlet_format("Attendance Tracker")
print(banner)

load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

if not EMAIL_USER or not EMAIL_PASS:
    raise Exception("EMAIL_USER or EMAIL_PASS not set in .env")

today_attendance = pd.read_csv("input.csv")
today_attendance.columns = today_attendance.columns.str.strip()
today_attendance['Date'] = today_attendance['Date'].astype(str).str.strip()
today_attendance['Date'] = pd.to_datetime(today_attendance['Date'], errors='coerce')
today_attendance.dropna(subset=['Date'], inplace=True)

log_file = "attendance_log.csv"

if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
    log_df = pd.read_csv(log_file)
    log_df.columns = log_df.columns.str.strip()
    log_df['Date'] = pd.to_datetime(log_df['Date'], errors='coerce')
    log_df.dropna(subset=['Date'], inplace=True)
    combined = pd.concat([log_df, today_attendance], ignore_index=True)
else:
    combined = today_attendance

combined.drop_duplicates(subset=["Name", "Date"], keep="last", inplace=True)
combined.sort_values(by=['Name', 'Date'], inplace=True)
combined.to_csv(log_file, index=False)

def detect_consecutive_absences(df, min_days=3):
    alerts = []
    for name, group in df.groupby('Name'):
        group = group.sort_values('Date').reset_index(drop=True)
        if "Email" not in group.columns:
            continue
        absent_dates = group[group["Status"].astype(str).str.lower() == "absent"]["Date"].reset_index(drop=True)
        count = 1
        for i in range(1, len(absent_dates)):
            if (absent_dates[i] - absent_dates[i - 1]).days == 1:
                count += 1
                if count >= min_days:
                    alerts.append((name, group.iloc[0]["Email"], absent_dates[i]))
                    break
            else:
                count = 1
    return alerts

def send_warning_email(to, name, last_date):
    msg = EmailMessage()
    msg['Subject'] = "Attendance Alert: 3+ Days Absent"
    msg['From'] = EMAIL_USER
    msg['To'] = to
    msg.set_content(f"Hi {name}, you've been absent for 3+ consecutive days as of {last_date.date()}.")

    msg.add_alternative(f"""
    <html>
      <body>
        <p>Hi <strong>{name}</strong>,</p>
        <p>We noticed that you've been <span style="color:red;"><strong>absent for 3 or more consecutive days</strong></span>, with your last absence recorded on <strong>{last_date.date()}</strong>.</p>
        <p>If you're facing any issues or need support, feel free to reach out.<br><br>
        <em>We're here to help!</em></p>
        <p>Best regards,<br>
        <strong>Your Class Representative</strong></p>
      </body>
    </html>
    """, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

    log_email(name, to, last_date)

def log_email(name, email, date):
    with open("email_log.csv", "a") as f:
        f.write(f"{name},{email},{date},{datetime.now()}\n")

def export_absentees_to_pdf(absentees):
    c = canvas.Canvas("absentee_report.pdf", pagesize=A4)
    c.setFont("Helvetica", 14)
    c.drawString(100, 800, "🚨 Students Absent 3+ Days in a Row:")
    y = 780
    for name, email, date in absentees:
        c.drawString(100, y, f"{name} ({email}) - Last Absence: {date.date()}")
        y -= 20
    c.save()

combined['Date'] = pd.to_datetime(combined['Date'], errors='coerce')
combined.dropna(subset=['Date'], inplace=True)

absentees = detect_consecutive_absences(combined)

for name, email, last_date in absentees:
    send_warning_email(email, name, last_date)

export_absentees_to_pdf(absentees)

print(f"\n📅 Date Processed: {today_attendance['Date'].iloc[0].date()}")
print(f"🧑‍🎓 Students Marked Today: {today_attendance['Name'].nunique()}")
print(f"❌ Absentees Today: {today_attendance[today_attendance['Status'].astype(str).str.lower() == 'absent']['Name'].nunique()}")
print(f"📨 Emails Sent : {len(absentees)}")
