import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai

# Gemini Kurulumu
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def etkinlikleri_getir():
    model = genai.GenerativeModel('gemini-3.8-flash')
    
    prompt = """
    Sen profesyonel bir kültür-sanat asistanısın. Bu hafta gerçekleşecek olan 
    etkinlikler arasından SADECE ÜCRETSİZ olanları belirle.
    Bunlar arasından en nitelikli, popüler ve çeşitlilik arz eden 20 tanesini seç.
    
    Çıktıyı şu şık formatta hazırla:
    - **Etkinlik Adı ve Türü** (Konser, Sergi, Tiyatro vb.)
    - **Tarih ve Saat:** ...
    - **Mekan:** ...
    - **Açıklama:** 1-2 cümlelik kısa özet.
    
    E-posta formatına uygun, okunabilir ve düzenli bir Türkçe metin oluştur.
    """
    
    response = model.generate_content(prompt)
    return response.text

def eposta_gonder(icerik):
    gonderen = os.environ.get("GMAIL_USER")
    sifre = os.environ.get("GMAIL_APP_PASSWORD")
    alici = os.environ.get("RECEIVER_EMAIL")
    
    msg = MIMEMultipart()
    msg['From'] = gonderen
    msg['To'] = alici
    msg['Subject'] = "Haftalık Ücretsiz Kültür-Sanat Etkinlikleri (Top 20)"
    
    msg.attach(MIMEText(icerik, 'plain', 'utf-8'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gonderen, sifre)
        server.sendmail(gonderen, alici, msg.as_string())
        server.quit()
        print("E-posta başarıyla gönderildi!")
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    ozet = etkinlikleri_getir()
    eposta_gonder(ozet)
