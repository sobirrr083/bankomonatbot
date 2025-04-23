import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# .env faylidan tokenni o'qish
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# /start buyrug'i uchun funksiya
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men bank omonatlari kalkulyator botiman.\n"
        "Omonat summasi, foiz stavkasi va muddatni kiritishingiz mumkin.\n"
        "Masalan: 1000000 5 12 (summa, yillik foiz, oy sifatida muddat)\n"
        "Hisoblashni boshlash uchun ma'lumotlarni yuboring!"
    )

# Foydalanuvchi xabarini qayta ishlash
async def calculate_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Foydalanuvchi xabarini olish va bo‘lish
        text = update.message.text
        data = text.split()
        
        if len(data) != 3:
            await update.message.reply_text(
                "Iltimos, ma'lumotlarni to‘g‘ri kiriting!\n"
                "Masalan: 1000000 5 12 (summa, yillik foiz, oy sifatida muddat)"
            )
            return
        
        # Ma'lumotlarni float/int ga aylantirish
        principal = float(data[0])  # Omonat summasi
        rate = float(data[1])       # Yillik foiz stavkasi
        time = int(data[2])         # Muddat (oylarda)

        # Oddiy foiz formulasi: A = P * (1 + r * t)
        # Murakkab foiz formulasi: A = P * (1 + r/n)^(n*t)
        # Bu yerda n = 12 (oylik hisoblash uchun)
        simple_interest = principal * (1 + (rate / 100) * (time / 12))
        compound_interest = principal * (1 + (rate / 100) / 12) ** (12 * (time / 12))

        # Natijalarni formatlash
        response = (
            f"Omonat summasi: {principal:,.2f} so‘m\n"
            f"Yillik foiz stavkasi: {rate}%\n"
            f"Muddat: {time} oy\n\n"
            f"Oddiy foiz bilan umumiy summa: {simple_interest:,.2f} so‘m\n"
            f"Murakkab foiz bilan umumiy summa: {compound_interest:,.2f} so‘m"
        )

        await update.message.reply_text(response)

    except ValueError:
        await update.message.reply_text(
            "Iltimos, raqamlarni to‘g‘ri kiriting!\n"
            "Masalan: 1000000 5 12"
        )
    except Exception as e:
        await update.message.reply_text(
            f"Xatolik yuz berdi: {str(e)}\n"
            "Iltimos, ma'lumotlarni qaytadan kiriting."
        )

# Asosiy funksiya
def main():
    # Botni ishga tushirish
    application = Application.builder().token(TOKEN).build()

    # Buyruqlar va xabarlar uchun handlerlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate_deposit))

    # Botni polling rejimida ishga tushirish
    print("Bot ishga tushdi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
