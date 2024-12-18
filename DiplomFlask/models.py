# Импортируем класс SQLAlchemy из библиотеки flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# Создаем экземпляр SQLAlchemy, который будет использоваться для работы с базой данных
db = SQLAlchemy()


# Определяем модель Book, которая будет представлять таблицу книг в базе данных
class Book(db.Model):
    # Указываем, что 'id' является первичным ключом и будет автоматически увеличиваться
    id = db.Column(db.Integer, primary_key=True)

    # Поле для хранения имени автора книги
    author = db.Column(db.String)

    # Поле для хранения названия книги, добавляем индекс для ускорения поиска
    title = db.Column(db.String, index=True)

    # Поле для хранения жанра книги
    genre = db.Column(db.String)

    # Поле для хранения описания книги
    description = db.Column(db.String)

    # Поле для хранения информации о публикации (например, издательство)
    publish = db.Column(db.String)

    # Поле для хранения года публикации книги
    year = db.Column(db.Integer)

    # Поле для хранения количества страниц в книге
    pages = db.Column(db.Integer)


'''
Модель Book представляет собой структуру данных для хранения информации о книгах.
Каждая книга имеет уникальный идентификатор (id), автора, название, жанр, описание,
информацию о публикации, год издания и количество страниц.
'''