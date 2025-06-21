# lovekesh-attendance-agent
 An AI-powered autonomous agent that reads attendance, marks status, and generates GPT summaries.

This is a simple Python-based AI tool I built during a Mini-hackathon organised by K.A.M.A.L.A , KAPIDHWAJ INNOVATIONS . It takes a CSV file of daily check-in times and automatically marks students as Present, Late, or Absent based on rules. Then it uses GPT (through Azure OpenAI) to generate a short, clean summary of the day.

The idea was to make something that just works — something a teacher or class rep can use daily without needing to do anything manually.

---

## 🔧 How it works

1. I load an `input.csv` file (Name + Check-In Time)
2. The code checks:
   - Present: On or before 9:00 AM
   - Late: Between 9:01 and 9:15 AM
   - Absent: After 9:15 AM or if time is blank
3. It writes the output into `Output.csv` with a status and today’s date
4. Finally, it asks GPT to generate a 2-line summary of the day, saved in `summary.txt`

---

## 📂 Files included

- `app.py` → The main script
- `input.csv` → Sample test data
- `Output.csv` → Final structured output
- `summary.txt` → AI-generated summary
- `.env` → Not included (for security, contains API key)

---

## 🤖 Technologies used

- Python 3
- Pandas (for handling the data)
- Datetime (for checking times)
- Azure OpenAI GPT-4 (for the summary)

---

## 📌 Why I built this

Most attendance systems are still manual. I’ve seen teachers copy things from WhatsApp, students forget to mark, and people get marked absent by mistake.

I just wanted to make something quick and clean that could remove the boring part of it. And the GPT summary was a fun way to end it — something you could even post in a group chat.

---

## 🚀 Future ideas

- Email/SMS alerts to absent students
- A streak tracker (for consistent attendance)
- Sync with Google Sheets or school systems

---

## 🙋‍♂️ About Me

Hi, I’m Lovekesh. I enjoy building real things with code — not just for marks, but for fun and impact.

If you have ideas, feedback, or just want to say hi:
- [LinkedIn](https://www.linkedin.com/in/lovekesh-524660370)

---

