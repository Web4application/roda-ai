from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import sqlite3

app = FastAPI()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LeadRequest(BaseModel):
    name: str
    email: str
    message: str

def save_to_db(name, email, message, reply):
    conn = sqlite3.connect("leads.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leads
                 (name TEXT, email TEXT, message TEXT, reply TEXT)''')
    c.execute("INSERT INTO leads VALUES (?, ?, ?, ?)", (name, email, message, reply))
    conn.commit()
    conn.close()

def classify_message(message):
    classification_prompt = f"Classify this message: '{message}' into categories like 'Support', 'Sales', 'Demo Request', or 'Other'."
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": classification_prompt}],
        max_tokens=50
    )
    return response.choices[0].message.content.strip()

def send_email(to_email, subject, body, from_email="noreply@roda.ai", from_name="RODA AI"):
    msg = MIMEMultipart()
    msg['From'] = formataddr((from_name, from_email))
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        server.sendmail(from_email, to_email, msg.as_string())

@app.post("/auto_reply")
async def auto_reply(lead: LeadRequest):
    prompt = f'''
You're RODA AI, a smart, friendly Web4 assistant.
A user just submitted a message:

📩 Name: {lead.name}
📧 Email: {lead.email}
📝 Message: {lead.message}

Write a warm, professional auto-reply.
'''

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    reply = response.choices[0].message.content
    save_to_db(lead.name, lead.email, lead.message, reply)

    category = classify_message(lead.message)

    full_reply = f"{reply}\n\n🗂 Category: {category}"
    send_email(lead.email, "Thanks for contacting RODA AI", full_reply)

    return {
        "reply": reply,
        "category": category,
        "status": "Email sent and saved"
    }
