# VK_project
Для запуска API Вам потребутеся:
0) Скачать docker desktop и запустить его
1) Скачать в виде зип-архива все файлы с данного репозитория
2) Распоковать архив
3) Перейти в папку, где хранятся скачанные файлы
4) Написать команду "docker-compose up --build"
5) Полождать, пока проект соберется и запустится
6) Как только проект запустится, вы увидите уведомление, а также 2 ссылки; приложение работает по ссылке http://127.0.0.1:8001.

Начало работы с api:
По умолчанию уже создан токен "dbb2b02087a67bfe920d84403165f15c86f3805a58aace7e93d971d072852155" для username="admin" и password="presale". Токен един и уникален для каждого пользователя, так что, если Вы забыли свой токен, то можете просто получить его заново. Для записи данных требуется Ваш токен. Для чтения данных также требуется Ваш токен. Каждый пользователь может читать только свои записи, т.е чтобы получить информацию из БД, Вы должны использовать тот же токен, что использовался для записи данных.
Возможные ошибки: Bad request 400 - вы передали неверную информацию, которая не соответсвует формату из примера задания.
При записи информации с одинаковыми ключами будет записана информация, соответсвующая последнему ключу из одинаковых. При попытке записать те же данные, будет получен ответ, что такие данные в БД уже имеются.

Примеры запросов и ответов: 
<img width="495" alt="image" src="https://github.com/user-attachments/assets/44ed2fb2-a24d-4f86-9b6a-d6f4b9ba9424">
