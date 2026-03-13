import os
import time
import requests
from bs4 import BeautifulSoup

# Настройки
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://www.avito.ru/voronezh/telefony/mobilnye_telefony/apple-ASgBAgICAkS0wa3OqzmmwQ2I_Dc"

seen_ads = set()
first_run = True  # Чтобы не спамить старыми объявлениями при запуске

def check_avito():
    global first_run
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    
    try:
        print(f"[{time.strftime('%H:%M:%S')}] Проверяю Авито...")
        response = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', {'data-marker': 'item'})
        
        if not items:
            print("Предупреждение: Не нашел объявлений на странице. Возможно, Авито просит капчу.")
            return

        new_found = 0
        for item in items:
            ad_id = item.get('data-item-id') or item.get('id')
            if ad_id and ad_id not in seen_ads:
                if not first_run:
                    title_elem = item.find('h3')
                    price_elem = item.find('meta', {'itemprop': 'price'})
                    link_elem = item.find('a', {'data-marker': 'item-title'})
                    
                    if title_elem and link_elem:
                        title = title_elem.text.strip()
                        price = price_elem['content'] if price_elem else "Цена не указана"
                        link = "https://www.avito.ru" + link_elem['href']
                        
                        message = f"📱 Нашел новый iPhone!\n\n📌 {title}\n💰 Цена: {price} руб.\n\n🔗 Ссылка: {link}"
                        
                        send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                        requests.post(send_url, json={"chat_id": CHAT_ID, "text": message})
                        new_found += 1
                
                seen_ads.add(ad_id)
        
        if first_run:
            print(f"Первый запуск: запомнил {len(seen_ads)} существующих объявлений.")
            first_run = False
        else:
            print(f"Проверка завершена. Найдено новых: {new_found}")

    except Exception as e:
        print(f"Ошибка при проверке: {e}")

if __name__ == "__main__":
            print("Бот запущен и мониторит Воронеж...")
    while True:
                check_avito()
                time.sleep(300) # Проверка каждые 5 минут
