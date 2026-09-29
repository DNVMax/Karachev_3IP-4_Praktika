Met1:
|POST https://jsonplaceholder.typicode.com/posts \{"title": "Мой пост", "body": "Текст", "userId": 1}/ (\/ - указывал в Body raw со значением JSON)|
|Статус = 201 Created|
|Полученный ID = 101|
|Статус от GET = 404 not found|
|Вывод - API лишь имитирует создание поста через запроос но не содаёт его (Делал через PostMan)|

