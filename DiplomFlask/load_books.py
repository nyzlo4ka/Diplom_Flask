import json  # Импортируем библиотеку для работы с JSON
from models import db, Book  # Импортируем объекты базы данных и модель книги


def load_books():
    """
    Функция для загрузки книг из файла books.json в базу данных.
    Если книга с таким ID уже существует, она не будет добавлена.
    """
    try:
        # Открываем файл books.json с кодировкой UTF-8
        with open('books.json', encoding='utf-8') as f:
            # Загружаем данные из файла в формате JSON
            books_data = json.load(f)
            # Проходим по каждому элементу в загруженных данных
            for book_data in books_data:
                book_id = book_data['id']  # Получаем ID книги
                existing_book = Book.query.get(book_id)  # Проверяем, существует ли книга с таким ID
                if not existing_book:  # Если книга не найдена
                    # Создаем новый объект книги с данными из файла
                    book = Book(
                        id=book_id,
                        author=book_data['автор'],
                        title=book_data['название'],
                        genre=book_data['жанр'],
                        description=book_data['описание'],
                        publish=book_data['издательство'],
                        year=book_data['год публикации'],
                        pages=book_data['Количество страниц'],
                    )
                    db.session.add(book)  # Добавляем книгу в сессию базы данных
            db.session.commit()  # Сохраняем изменения в базе данных
    except Exception as e:
        # Обрабатываем исключения и выводим сообщение об ошибке
        print(f"Ошибка при загрузке книг: {e}")


'''
Этот код эффективно загружает книги, избегая дублирования записей.
'''