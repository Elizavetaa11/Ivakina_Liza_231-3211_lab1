import random  # Импортируем модуль random для генерации случайных чисел.
from flask import Flask, render_template  # Импортируем класс Flask и функцию render_template из модуля flask.
from faker import Faker  # Импортируем класс Faker из модуля faker для генерации фейковых данных.

fake = Faker()  # Создаем экземпляр класса Faker для генерации фейковых данных.

app = Flask(__name__)  # Создаем экземпляр класса Flask, который будет представлять наше веб-приложение.
application = app  # Присваиваем переменной application наше приложение для совместимости с некоторыми веб-серверами.

# Список идентификаторов изображений для использования в постах.
images_ids = [
    '7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
    '2d2ab7df-cdbc-48a8-a936-35bba702def5',
    '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
    'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
    'cab5b7f2-774e-4884-a200-0c0180fa777f'
]

def generate_comments(replies=True):
    # Функция для генерации списка комментариев с возможными ответами.
    comments = []
    for i in range(random.randint(1, 3)):  # Генерируем от 1 до 3 комментариев.
        comment = {'author': fake.name(), 'text': fake.text()}  # Создаем комментарий с фейковыми данными.
        if replies:
            comment['replies'] = generate_comments(replies=False)  # Добавляем ответы к комментарию.
        comments.append(comment)
    return comments

def generate_post(i):
    # Функция для генерации поста с использованием фейковых данных.
    return {
        'title': fake.sentence(),  # Генерируем заголовок поста.
        'text': fake.paragraph(nb_sentences=100),  # Генерируем текст поста.
        'author': fake.name(),  # Генерируем имя автора.
        'date': fake.date_time_between(start_date='-2y', end_date='now'),  # Генерируем дату публикации.
        'image_id': f'{images_ids[i]}.jpg',  # Выбираем идентификатор изображения.
        'comments': generate_comments()  # Генерируем комментарии к посту.
    }

# Генерируем список из 5 постов и сортируем их по дате в обратном порядке.
posts_list = sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)

@app.route('/')  # Определяем маршрут для главной страницы.
def index():
    return render_template('index.html')  # Возвращаем шаблон index.html.

@app.route('/posts')  # Определяем маршрут для страницы с постами.
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list)  # Возвращаем шаблон posts.html с данными постов.

@app.route('/posts/<int:index>')  # Определяем маршрут для страницы одного поста.
def post(index):
    p = posts_list[index]  # Получаем пост по индексу.
    return render_template('post.html', title=p['title'], post=p)  # Возвращаем шаблон post.html с данными поста.

@app.route('/about')  # Определяем маршрут для страницы "Об авторе".
def about():
    return render_template('about.html', title='Об авторе')  # Возвращаем шаблон about.html.

if __name__ == '__main__':
    app.run(debug=True)  # Запускаем приложение в режиме отладки.
