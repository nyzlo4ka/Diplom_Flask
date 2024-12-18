# Импорт необходимых библиотек для работы с Flask и SQLAlchemy
from flask import Flask, jsonify, request, render_template
from sqlalchemy import or_
from load_books import load_books  # Импорт функции для загрузки книг
from models import db, Book  # Импорт модели базы данных и таблицы книг
import logging  # Импорт библиотеки для логирования

# Создаем экземпляр приложения Flask
app = Flask(__name__)

# Настройка URI базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///list_books1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных с приложением
db.init_app(app)

# В контексте приложения создаем все таблицы и загружаем книги
with app.app_context():
    db.create_all()  # Создание всех таблиц в базе данных
    load_books()  # Загрузка книг в базу данных из файла или другого источника


# Обработка маршрута для главной страницы
@app.route('/')
def home_page():
    return render_template('home.html')  # Возвращаем шаблон главной страницы


# Обработка маршрута для чтения всех книг
@app.route('/books', methods=['GET'])
def read_books():
    books = Book.query.all()  # Получение всех книг из базы данных
    return render_template('books.html', books=books)  # Возвращаем шаблон со списком книг


# Обработка маршрута для получения книги по ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    book = Book.query.get(book_id)  # Попытка получить книгу по ID
    if book:
        return render_template('book_detail.html', book=book)  # Возвращаем шаблон с деталями книги
    else:
        return jsonify({'error': 'Книга не найдена'}), 404  # Ошибка, если книга не найдена


# Обработка маршрута для поиска книг
@app.route('/books/search', methods=['GET'])
def get_searched_book():
    query = request.args.get('query')  # Получение параметра запроса на поиск
    logging.info(f"Полученный запрос: {query}")  # Логирование полученного запроса
    if query:
        # Фильтрация книг по автору, заголовку, жанру или ID, используя нечувствительный к регистру поиск
        books = Book.query.filter(
            or_(
                Book.author.ilike(f'%{query}%'),
                Book.title.ilike(f'%{query}%'),
                Book.genre.ilike(f'%{query}%'),
                Book.id.ilike(f'%{query}%'),
            )
        ).all()
        return render_template('book_search.html', books=books)  # Возвращаем результаты поиска
    else:
        logging.error("Нет запроса для поиска")  # Логирование ошибки в случае отсутствия запроса
        return jsonify({'error': 'Нет запроса для поиска'}), 400  # Ошибка 400 для отсутствия запроса


# Обработка маршрута для добавления новой книги
@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':  # Если метод POST (форма отправлена)
        # Создание нового объекта книги на основе данных из формы
        new_book = Book(
            author=request.form['author'],
            title=request.form['title'],
            genre=request.form['genre'],
            description=request.form['description'],
            publish=request.form['publish'],
            year=int(request.form['year']),
            pages=int(request.form['pages'])
        )
        db.session.add(new_book)  # Добавляем новую книгу в сессию
        db.session.commit()  # Фиксируем изменения в базе данных
        success_message = "Книга добавлена!"  # Сообщение об успешном добавлении
        return render_template('add_book.html', success_message=success_message)  # Возвращаем шаблон с сообщением
    return render_template('add_book.html')  # Если GET, возвращаем шаблон для добавления книги


# Запускаем приложение
if __name__ == '__main__':
    app.run(debug=True)  # Запускаем сервер в режиме отладки
