from flask import Flask, render_template, request, redirect, url_for, flash, session, Response, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message as MailMessage
from weasyprint import HTML, CSS
import os
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jahanbani.taha.923@gmail.com'
app.config['MAIL_PASSWORD'] = 'pqtp hohx yjwj smbr'
mail = Mail(app)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)
class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(120), nullable = False)
    content = db.Column(db.Text, nullable = False)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
def get_current_language():
    return request.args.get("lang", "EN")
def generate_bot_response(message, lang):
    message = message.lower()
    if "سلام، حالت چطوره؟" in message or "hi, how are you?" in message or "merhaba, nasılsın?" in message:
        return (
            "سلام! من خوبم، ممنون. چطور می‌تونم کمکت کنم؟" if lang == "FA" else
            "Hi! I'm doing well, thanks. How can I help you?" if lang == "EN" else
            "Merhaba! İyiyim, teşekkürler. Size nasıl yardımcı olabilirim?"
        )
    elif "سلام" in message or "hi" in message or "merhaba" in message:
        return (
            "سلام! چطور می‌تونم کمکت کنم؟" if lang == "FA" else
            "Hi there! How can I help you?" if lang == "EN" else
            "Merhaba! Size nasıl yardımcı olabilirim?"
        )
    elif "چطور با طاها تماس بگیریم؟" in message or "how to contact taha?" in message or "taha’ya nasıl ulaşabilirim?" in message:
        return (
            "برای تماس با من می‌تونی از فرم تماس استفاده کنی." if lang == "FA" else
            "You can use the contact form to reach me." if lang == "EN" else
            "Benimle iletişime geçmek için iletişim formunu kullanabilirsiniz."
        )

    elif "چطور رزومه طاها رو ببینم؟" in message or "how can i see taha’s resume?" in message or "taha’nın özgeçmişini nasıl görebilirim?" in message:
        return (
            "برای دیدن رزومه، به بخش رزومه در منوی بالا برو." if lang == "FA" else
            "To view the resume, go to the Resume section in the top menu." if lang == "EN" else
            "Özgeçmişi görmek için üst menüdeki Resume bölümüne gidebilirsiniz."
        )

    elif "نمونه‌کارهای طاها کجان؟" in message or "where are taha’s projects?" in message or "taha’nın projeleri nerede?" in message:
        return (
            "نمونه‌کارها در بخش پورتفولیو قابل مشاهده هستن." if lang == "FA" else
            "You can find the projects in the Portfolio section." if lang == "EN" else
            "Projeleri Portfolyo bölümünde bulabilirsiniz."
        )

    elif "چطور تم رو تغییر بدم؟" in message or "how to change the theme?" in message or "temayı nasıl değiştirebilirim?" in message:
        return (
            "برای تغییر تم، از دکمه‌ی بالا استفاده کن تا بین تاریک و روشن جابه‌جا بشی." if lang == "FA" else
            "To change the theme, use the button above to toggle between dark and light." if lang == "EN" else
            "Temayı değiştirmek için yukarıdaki düğmeyi kullanarak koyu ve açık arasında geçiş yapabilirsiniz."
        )

    elif "چت‌بات چه کاری انجام می‌ده؟" in message or "what does the chatbot do?" in message or "sohbet botu ne işe yarar?" in message:
        return (
            "چت‌بات برای راهنمایی بازدیدکننده‌ها در سایت طراحی شده." if lang == "FA" else
            "The chatbot is designed to guide visitors through the site." if lang == "EN" else
            "Sohbet botu, ziyaretçilere site içinde yardımcı olmak için tasarlanmıştır."
        )

    elif "آیا می‌تونم رزومه رو دانلود کنم؟" in message or "can i download the resume?" in message or "özgeçmişi indirebilir miyim?" in message:
        return (
            "بله! رزومه هم قابل مشاهده هست و هم قابل دانلود." if lang == "FA" else
            "Yes! The resume is available for both viewing and download." if lang == "EN" else
            "Evet! Özgeçmiş hem görüntülenebilir hem de indirilebilir."
        )

    elif "ممنون از راهنمایی‌ات" in message or "thanks for your help" in message or "yardımın için teşekkürler" in message:
        return (
            "خواهش می‌کنم! هر وقت خواستی سوال بپرس" if lang == "FA" else
            "You're welcome! Feel free to ask anything" if lang == "EN" else
            "Rica ederim! Her zaman soru sorabilirsiniz"
        )

    else:
        return (
            "متوجه نشدم، لطفاً واضح‌تر بپرس." if lang == "FA" else
            "I'm not sure I understood—could you rephrase?" if lang == "EN" else
            "Tam anlayamadım, lütfen tekrar eder misiniz?"
        )

@app.route("/")
def index():
    current_language = get_current_language()
    theme = request.args.get("theme", "light")
    return render_template("index.html", title="Home", current_language=current_language, theme=theme)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    current_language = get_current_language()
    theme = request.form.get("theme") or request.args.get("theme") or "light"

    messages = {
        "success": {
            "FA": "پیام شما با موفقیت ارسال شد!",
            "EN": "Your message has been sent successfully!",
            "TR": "Mesajınız başarıyla gönderildi!"
        },
        "error": {
            "FA": "لطفاً همه‌ی فیلدها را پر کنید.",
            "EN": "Please fill out all fields.",
            "TR": "Lütfen tüm alanları doldurun."
        }
    }

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            flash(messages["error"][current_language], "warning")
            return redirect(url_for("contact", lang=current_language, theme=theme))

        new_msg = Message(name=name, email=email, content=message)
        db.session.add(new_msg)
        db.session.commit()

        msg = MailMessage(
            subject="New Contact Message",
            sender=app.config['MAIL_USERNAME'],
            recipients=['jahanbani.taha.923@gmail.com'],
            body=f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
        )
        mail.send(msg)

        flash(messages["success"][current_language], "success")
        return redirect(url_for("contact", lang=current_language, theme=theme))

    return render_template("contact.html", title="Contact", current_language=current_language, theme=theme)

@app.route("/chat", methods=["GET", "POST"])
def chat():
    current_language = get_current_language()
    theme = request.args.get("theme", "light")
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        user_input = request.form.get("message")
        response = generate_bot_response(user_input, current_language)
        session["chat_history"].append({
            "user": user_input,
            "bot": response
        })
        session.modified = True

    return render_template("chat.html", title="Chatbot", current_language=current_language, chat_history=session["chat_history"], theme=theme)

@app.route("/clear_chat")
def clear_chat():
    current_language = request.args.get("lang", "EN")
    theme = request.args.get("theme", "light")
    session.pop("chat_history", None)
    return redirect(url_for("chat", lang=current_language, theme=theme))

@app.route("/portfolios")
def portfolios():
    current_language = get_current_language()
    theme = request.args.get("theme", "light")
    projects = [
    {
        "title": {
            "FA": "پروژه DNA با پایتون",
            "TR": "Python ile DNA Projesi",
            "EN": "CS50 DNA Project"
        },
        "description": {
            "FA": "ابزاری مبتنی بر پایتون برای تحلیل توالی‌های DNA و شناسایی افراد با الگوهای STR. تمرینی عالی در پردازش رشته‌ها، تجزیه داده‌ها و تفکر الگوریتمی.",
            "TR": "Python tabanlı bir araç; DNA dizilerini analiz eder ve STR desenleriyle kişileri tanımlar. Dize işleme, veri ayrıştırma ve algoritmik düşünme için harika bir alıştırma.",
            "EN": "It’s a Python-based tool that analyzes DNA sequences and identifies individuals using STR patterns. A great exercise in string manipulation, data parsing, and algorithmic thinking."
        },
        "link": "https://www.linkedin.com/posts/taha-cihan_python-bioinformatics-dna-activity-7378679633917001728-P0vB",
        "image": "/static/images/dna.png"
    },
    {
        "title": {
            "FA": "رندرهای صنعتی با SolidWorks",
            "TR": "SolidWorks ile Endüstriyel Tasarım",
            "EN": "SolidWorks Showcase"
        },
        "description": {
            "FA": "رندر قطعات صنعتی با استفاده از KeyShot و SolidWorks برای کاتالوگ‌ها و صفحات وب.",
            "TR": "KeyShot ve SolidWorks ile endüstriyel tasarım renderları.",
            "EN": "Industrial design renders with KeyShot and SolidWorks."
        },
        "link": "https://www.linkedin.com/posts/taha-cihan_aefaezaepaevahyabraedaeuaehaesahy-solidworks-activity-7377659651628351488-3UDA",
        "image": "/static/images/solid.jpg"
    },
    {
        "title": {
            "FA": "وب‌سایت رسمی شرکت تولیدی",
            "TR": "Üretim Şirketinin Resmi Web Sitesi",
            "EN": "Official Website of the Manufacturing Company"
        },
        "description": {
            "FA": "سایت معرفی محصولات صنعتی با تصاویر CAD و محتوای سفارشی—طراحی کامل توسط من.",
            "TR": "CAD görselleri ve özel içeriklerle endüstriyel ürün tanıtım sitesi—tamamı benim tasarımım.",
            "EN": "Industrial product showcase site with CAD visuals and custom content—fully designed by me."
        },
        "link": "https://condorimachinery.com/",
        "image": "/static/images/condori.jpg"
    }
]
    return render_template("portfolios.html", title="Portfolios", current_language=current_language, projects=projects, theme=theme)
@app.route("/resume")
def resume():
    current_language = get_current_language()
    theme = request.args.get("theme", "light")
    return render_template("resume.html", current_language=current_language, theme=theme)

@app.route("/resume_pdf/download")
def download_resume_pdf():
    current_language = request.args.get("lang", "EN")
    filename = f"Taha_Jahanbani_Resume_{current_language}.pdf"
    image_path = os.path.abspath("static/images/profile.jpeg")
    rendered = render_template("resume_pdf.html", current_language=current_language, image_path=image_path)
    pdf = HTML(string=rendered, base_url=os.path.abspath(".")).write_pdf()
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response

@app.route("/resume/printable")
def resume_printable():
    current_language = get_current_language()
    return render_template("resume_printable.html", current_language=current_language)
