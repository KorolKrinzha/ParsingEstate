# Парсинг сайтов с недвижимостью

## Описание

Скрипты были написаны по заказу для российского студенческого стартапа

Из десяти запрошенных для парсинга сайтов у меня успешно и эффективно получилось написать скрипты для восьми сайтов за несколько дней

Скрипт может парсить следующие сайты:

- https://kf.expert
- https://www.rentavik.ru
- https://reka.fm
- https://ires-group.ru
- https://osobnyaki.com
- https://дом.рф
- https://www.trust.ru
- https://www.auction-house.ru

Для объекта с каждого сайта доступна следующая информация:

- адрес объекта
- цена
- ссылки на картинки
- ссылка на оригинальную страницу

Также в пяти из восьми случаев был найден способ нахождения точной геолокации объекта без применения сторонних API

## Использование

### Использование парсинга через bash-скрипт

```console
user@server:~$ git clone https://github.com/KorolKrinzha/ParsingEstate
user@server:~$ cd ParsingEstate
user@server:~$ ./startParsing.sh
```

### Использование парсинга вручную

На примере сайта [Особняки](https://osobnyaki.com)

```console
user@server:~$ git clone https://github.com/KorolKrinzha/ParsingEstate
user@server:~$ cd ParsingEstate
user@server:~$ pip3 install -r requirements.txt
user@server:~$ cd osobnyaki
user@server:~$ python3 main.py
```

### Дополнительные ссылки

[Таблица с прогрессом выполнения задач](https://docs.google.com/spreadsheets/d/1I0OCBfHPGB_wAFBxVLcaSrqDxfv6iFBW6UZlcDLsmRA/edit?usp=sharing)