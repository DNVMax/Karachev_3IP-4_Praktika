Met1:\
|POST https://jsonplaceholder.typicode.com/posts \{"title": "Мой пост", "body": "Текст", "userId": 1}/ (\/ - указывал в Body raw со значением JSON)                                                                                                                     |\
|Статус = 201 Created                                                                                                               |\
|Полученный ID = 101                                                                                                                |\
|Статус от GET = 404 not found                                                                                                      |\
|Вывод - API лишь имитирует создание поста через запроос но не создаёт его (Делал через PostMan)                                    |\
_____________________________________________________________________________________________________________________________________

Met3:\
|Поля которые посылал = "name"| \
|Поля в ответе на PUT = "name", "id"| \
|Поля в ответе на PATCH = "id", "name", "username", "email", "address" ("street","suite","city","zipcode","geo"("lat","ing")),"phone","website","company"("name","catchPhrase","bs")| \
|Поля которые не посылал но они пришли = "id","username","email","address"("street","suite","city","zipcode","geo"("lat","ing")),"phone","website","company"("name","catchPhrase","bs")| \
|Вывод = это слияние (т.к. он выводит не только запрошенную информацию а информацию всего объекта, а не его параметра)|

