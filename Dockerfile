# Python 3.9 slim image asosida
FROM python:3.9-slim

# Ishchi direktoriyani yaratish
WORKDIR /app

# requirements.txt faylini konteynerga nusxalash
COPY requirements.txt .

# Kutubxonalarni o'rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini konteynerga nusxalash
COPY . .

# Konteyner ishga tushganda botni start qilish
CMD ["python", "bot.py"]
