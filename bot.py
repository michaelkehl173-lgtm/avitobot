import os
import time
import requests
from bs4 import BeautifulSoup

# Берем данные из настроек Railway
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Ссылка на поиск айфонов (сортировка по дате, чтобы видеть новые)
URL = "https://www.avito.ru/voronezh/telefony/mobilnye_telefony/apple-ASgBAgICAkS0wA3OqzmwwQ2I_Dc"

seen_ads = set()

def check_avito():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем блоки с объявлениями
        items = soup.find_all('div', {'data-marker': 'item'})
        
        for item in items:
            ad_id = item.get('data-item-id') or item.get('id')
            if ad_id and ad_id not in seen_ads:
                title_elem = item.find('h3')
                price_elem = item.find('meta', {'itemprop': 'price'})
                link_elem = item.find('a', {'data-marker': 'item-title'})
                
                if title_elem and link_elem:
                    title = title_elem.text.strip()
                    price = price_elem['content'] if price_elem else "Цена не указана"
                    link = "https://www.avito.ru" + link_elem['href']
                    
                    message = f"📱 Нашел новый iPhone!\n\n📌 {title}\n💰 Цена: {price} руб.\n\n🔗 Ссылка: {link}"
                    
                    # Отправка в телеграм
                    send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                    requests.post(send_url, json={"chat_id": CHAT_ID, "text": message})
                    
                    seen_ads.add(ad_id)
    except Exception as e:
        print(f"Ошибка при проверке: {e}")

# Запуск цикла
if __name__ == "__main__":
    print("Бот запущен и ищет айфоны...")
    while True:
        check_avito()
        time.sleep(300)  # Ждать 5 минут перед следующей проверкой
