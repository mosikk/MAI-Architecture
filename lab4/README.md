# Лабораторная работа 3
## Stateful сервис для NoSQL

**Вариант 4 - Сайт заказа услуг**

В рамках данной работы в будущем сервисе реализована модель для пользователя, БД Postrgres для хранения и обработки информации о пользователях и API для взаимодействия с базой.

Реализован следующий функционал:
* создание пользовалея
* поиск пользователей по логину
* поиск пользователей по маске имени и фамилии
* удаление пользователя из базы

Запуск:
1. `docker compose up`
2. <localhost:8080/docs> - потыкаться в API

Зайти в базу:
1. `docker exec -it postgres /bin/bash`
2. `psql -U stud -d postgres`
3. `\c users_db`