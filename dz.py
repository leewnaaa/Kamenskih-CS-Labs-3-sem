import sqlite3
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('study_bot.db')
    cursor = conn.cursor()

    # Таблица предметов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Таблица заданий
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            status INTEGER DEFAULT 0, -- 0 = не выполнено, 1 = выполнено
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (subject_id) REFERENCES subjects (id)
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# Функции для работы с БД
def add_subject(name):
    conn = sqlite3.connect('study_bot.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO subjects (name) VALUES (?)', (name,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_subjects():
    conn = sqlite3.connect('study_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM subjects ORDER BY name')
    subjects = cursor.fetchall()
    conn.close()
    return subjects

def delete_subject(name):
    conn = sqlite3.connect('study_bot.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM subjects WHERE name = ?', (name,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def add_task(subject_name, description):
    conn = sqlite3.connect('study_bot.db')
    cursor = conn.cursor()

    # Получаем ID предмета
    cursor.execute('SELECT id FROM subjects WHERE name = ?', (subject_name,))
    subject = cursor.fetchone()

    if subject:
        subject_id = subject[0]
        cursor.execute(
            'INSERT INTO tasks (subject_id, description) VALUES (?, ?)',
            (subject_id, description)
        )
        conn.commit()
        result = True
    else:
        result = False

    conn.close()
    return result

def get_tasks_by_subject(subject_name):
    conn = sqlite3.connect('study_bot.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT t.id, t.description, t.status
        FROM tasks t
        JOIN subjects s ON t.subject_id = s.id
        WHERE s.name = ?
        ORDER BY t.created_at
    ''', (subject_name,))

    tasks = cursor.fetchall()
    conn.close()
    return tasks

def mark_task_done(subject_name, task_number):
    conn = sqlite3.connect('study_bot.db')
    cursor = conn.cursor()

    # Получаем задание по номеру в списке
    cursor.execute('''
        SELECT t.id
        FROM tasks t
        JOIN subjects s ON t.subject_id = s.id
        WHERE s.name = ?
        ORDER BY t.created_at
        LIMIT 1 OFFSET ?
    ''', (subject_name, task_number - 1))

    task = cursor.fetchone()

    if task:
        task_id = task[0]
        cursor.execute('UPDATE tasks SET status = 1 WHERE id = ?', (task_id,))
        conn.commit()

        # Получаем описание задания для ответа
        cursor.execute('SELECT description FROM tasks WHERE id = ?', (task_id,))
        description = cursor.fetchone()[0]
        result = description
    else:
        result = None

    conn.close()
    return result

def delete_task(subject_name, task_number):
    conn = sqlite3.connect('study_bot.db')
    cursor = conn.cursor()

    # Получаем задание по номеру в списке
    cursor.execute('''
        SELECT t.id
        FROM tasks t
        JOIN subjects s ON t.subject_id = s.id
        WHERE s.name = ?
        ORDER BY t.created_at
        LIMIT 1 OFFSET ?
    ''', (subject_name, task_number - 1))

    task = cursor.fetchone()

    if task:
        task_id = task[0]
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        result = True
    else:
        result = False

    conn.close()
    return result

def get_overall_progress():
    conn = sqlite3.connect('study_bot.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM tasks')
    total = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = 1')
    completed = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        return 0, 0, 0
    return completed, total, int((completed / total) * 100)

def get_subject_progress(subject_name):
    conn = sqlite3.connect('study_bot.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT COUNT(*)
        FROM tasks t
        JOIN subjects s ON t.subject_id = s.id
        WHERE s.name = ?
    ''', (subject_name,))
    total = cursor.fetchone()[0]

    cursor.execute('''
        SELECT COUNT(*)
        FROM tasks t
        JOIN subjects s ON t.subject_id = s.id
        WHERE s.name = ? AND t.status = 1
    ''', (subject_name,))
    completed = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        return 0, 0, 0
    return completed, total, int((completed / total) * 100)

def get_pending_tasks():
    conn = sqlite3.connect('study_bot.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT s.name, t.description
        FROM tasks t
        JOIN subjects s ON t.subject_id = s.id
        WHERE t.status = 0
        ORDER BY s.name, t.created_at
    ''')

    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Обработчики команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Привет! Я бот для учета учебных заданий.\n\n"
        "Основные команды:\n"
        "1. Управление предметами:\n"
        "   /add_subject Название - добавить предмет\n"
        "   /subjects - список всех предметов\n"
        "   /delete_subject Название - удалить предмет\n\n"
        "2. Управление заданиями:\n"
        "   /add_task Физика \"Лабораторная №1\" - добавить задание\n"
        "   /tasks Физика - задания по предмету\n"
        "   /done Физика 1 - отметить задание выполненным\n"
        "   /delete_task Физика 1 - удалить задание\n\n"
        "3. Статистика:\n"
        "   /progress - общий прогресс\n"
        "   /progress Физика - прогресс по предмету\n"
        "   /deadlines - все несданные задания"
    )

async def add_subject_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Пожалуйста, укажите название предмета\nПример: /add_subject Физика")
        return

    subject_name = ' '.join(context.args)

    if add_subject(subject_name):
        await update.message.reply_text(f"✅ Предмет \"{subject_name}\" добавлен!")
    else:
        await update.message.reply_text(f"❌ Предмет \"{subject_name}\" уже существует!")

async def subjects_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subjects = get_all_subjects()

    if not subjects:
        await update.message.reply_text("📝 Список предметов пуст")
        return

    response = "📚 Список предметов:\n"
    for idx, subject in enumerate(subjects, 1):
        response += f"{idx}. {subject[1]}\n"

    await update.message.reply_text(response)

async def delete_subject_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Пожалуйста, укажите название предмета\nПример: /delete_subject Физика")
        return

    subject_name = ' '.join(context.args)

    if delete_subject(subject_name):
        await update.message.reply_text(f"✅ Предмет \"{subject_name}\" и все его задания удалены!")
    else:
        await update.message.reply_text(f"❌ Предмет \"{subject_name}\" не найден!")

async def add_task_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Пожалуйста, укажите предмет и описание задания\n"
            "Пример: /add_task Физика \"Лабораторная №1\""
        )
        return

    subject_name = context.args[0]
    description = ' '.join(context.args[1:])

    # Убираем кавычки если они есть
    if description.startswith('"') and description.endswith('"'):
        description = description[1:-1]

    if add_task(subject_name, description):
        await update.message.reply_text(f"✅ Задание по предмету \"{subject_name}\" добавлено!")
    else:
        await update.message.reply_text(f"❌ Предмет \"{subject_name}\" не найден!")

async def tasks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Пожалуйста, укажите предмет\nПример: /tasks Физика")
        return

    subject_name = ' '.join(context.args)
    tasks = get_tasks_by_subject(subject_name)

    if not tasks:
        await update.message.reply_text(f"📝 Нет заданий по предмету \"{subject_name}\"")
        return

    response = f"📚 {subject_name}:\n"
    for idx, task in enumerate(tasks, 1):
        status = "✅" if task[2] == 1 else "◻️"
        response += f"{idx}. {status} {task[1]}\n"

    await update.message.reply_text(response)

async def done_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Пожалуйста, укажите предмет и номер задания\n"
            "Пример: /done Физика 1"
        )
        return

    try:
        subject_name = context.args[0]
        task_number = int(context.args[1])

        if task_number < 1:
            raise ValueError

        result = mark_task_done(subject_name, task_number)

        if result:
            await update.message.reply_text(f"✅ Задание \"{result}\" отмечено как сданное!")
        else:
            await update.message.reply_text(f"❌ Задание №{task_number} по предмету \"{subject_name}\" не найдено!")

    except (ValueError, IndexError):
        await update.message.reply_text("❌ Неверный номер задания!")

async def delete_task_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Пожалуйста, укажите предмет и номер задания\n"
            "Пример: /delete_task Физика 1"
        )
        return

    try:
        subject_name = context.args[0]
        task_number = int(context.args[1])

        if task_number < 1:
            raise ValueError

        if delete_task(subject_name, task_number):
            await update.message.reply_text(f"✅ Задание №{task_number} по предмету \"{subject_name}\" удалено!")
        else:
            await update.message.reply_text(f"❌ Задание №{task_number} по предмету \"{subject_name}\" не найдено!")

    except (ValueError, IndexError):
        await update.message.reply_text("❌ Неверный номер задания!")

async def progress_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        # Общий прогресс
        completed, total, percentage = get_overall_progress()

        if total == 0:
            await update.message.reply_text("📊 Нет данных о заданиях")
        else:
            await update.message.reply_text(
                f"📊 Общий прогресс: {percentage}% ({completed} из {total} заданий выполнено)"
            )
    else:
        # Прогресс по предмету
        subject_name = ' '.join(context.args)
        completed, total, percentage = get_subject_progress(subject_name)

        if total == 0:
            await update.message.reply_text(f"📊 Нет заданий по предмету \"{subject_name}\"")
        else:
            await update.message.reply_text(
                f"📊 Прогресс по {subject_name}: {percentage}% ({completed} из {total} заданий)"
            )

async def deadlines_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = get_pending_tasks()

    if not tasks:
        await update.message.reply_text("🎉 Все задания выполнены!")
        return

    response = "📋 Несданные задания:\n\n"
    current_subject = None

    for subject, description in tasks:
        if subject != current_subject:
            current_subject = subject
            response += f"📚 {subject}:\n"
        response += f"  • {description}\n"

    await update.message.reply_text(response)

# Основная функция
def main():
    TOKEN = '8194444382:AAHVePH4rqAo6J4AWb71sl_h79izThFoUcY'

    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("add_subject", add_subject_command))
    application.add_handler(CommandHandler("subjects", subjects_command))
    application.add_handler(CommandHandler("delete_subject", delete_subject_command))
    application.add_handler(CommandHandler("add_task", add_task_command))
    application.add_handler(CommandHandler("tasks", tasks_command))
    application.add_handler(CommandHandler("done", done_command))
    application.add_handler(CommandHandler("delete_task", delete_task_command))
    application.add_handler(CommandHandler("progress", progress_command))
    application.add_handler(CommandHandler("deadlines", deadlines_command))

    # Запускаем бота
    print("🤖 Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
