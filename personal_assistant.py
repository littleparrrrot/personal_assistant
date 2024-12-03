import json
import csv
from datetime import datetime


class Note:
    def __init__(self, note_id, title, content, timestamp=None):
        self.id = note_id
        self.title = title
        self.content = content
        self.timestamp = timestamp or datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp
        }

    @staticmethod
    def from_dict(data):
        return Note(
            note_id=data["id"],
            title=data["title"],
            content=data["content"],
            timestamp=data["timestamp"]
        )


class NotesManager:
    def __init__(self, filename="notes.json"):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                return [Note.from_dict(note) for note in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_notes(self):
        with open(self.filename, "w") as file:
            json.dump([note.to_dict() for note in self.notes], file, indent=4)

    def create_note(self, title, content):
        note_id = max([note.id for note in self.notes], default=0) + 1
        note = Note(note_id, title, content)
        self.notes.append(note)
        self.save_notes()
        print(f"Заметка с ID {note_id} создана.")

    def list_notes(self):
        if not self.notes:
            print("Список заметок пуст.")
            return
        print("\nСписок заметок:")
        for note in self.notes:
            print(f"ID: {note.id}, Title: {note.title}, Timestamp: {note.timestamp}")

    def view_note_details(self, note_id):
        note = self.find_note_by_id(note_id)
        if note:
            print(f"\nID: {note.id}\nTitle: {note.title}\nContent: {note.content}\nTimestamp: {note.timestamp}")
        else:
            print(f"Заметка с ID {note_id} не найдена.")

    def edit_note(self, note_id, title=None, content=None):
        note = self.find_note_by_id(note_id)
        if note:
            if title:
                note.title = title
            if content:
                note.content = content
            note.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.save_notes()
            print(f"Заметка с ID {note_id} обновлена.")
        else:
            print(f"Заметка с ID {note_id} не найдена.")

    def delete_note(self, note_id):
        note = self.find_note_by_id(note_id)
        if note:
            self.notes.remove(note)
            self.save_notes()
            print(f"Заметка с ID {note_id} удалена.")
        else:
            print(f"Заметка с ID {note_id} не найдена.")

    def import_from_csv(self, csv_file):
        try:
            with open(csv_file, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.create_note(
                        title=row["title"],
                        content=row["content"]
                    )
            print(f"Заметки импортированы из файла {csv_file}.")
        except FileNotFoundError:
            print(f"Файл {csv_file} не найден.")

    def export_to_csv(self, csv_file):
        with open(csv_file, "w", newline="") as file:
            fieldnames = ["id", "title", "content", "timestamp"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for note in self.notes:
                writer.writerow(note.to_dict())
            print(f"Заметки экспортированы в файл {csv_file}.")

    def find_note_by_id(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return note
        return None



class Task:
    def __init__(self, task_id, title, description, done=False, priority="Средний", due_date=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date or datetime.now().strftime("%d-%m-%Y")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "priority": self.priority,
            "due_date": self.due_date
        }

    @staticmethod
    def from_dict(data):
        return Task(
            task_id=data["id"],
            title=data["title"],
            description=data["description"],
            done=data["done"],
            priority=data["priority"],
            due_date=data["due_date"]
        )


class TasksManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                return [Task.from_dict(task) for task in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def create_task(self, title, description, priority, due_date):
        task_id = max([task.id for task in self.tasks], default=0) + 1
        task = Task(task_id, title, description, priority=priority, due_date=due_date)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Задача с ID {task_id} создана.")

    def list_tasks(self):
        if not self.tasks:
            print("Список задач пуст.")
            return
        print("\nСписок задач:")
        for task in self.tasks:
            status = "Выполнена" if task.done else "Не выполнена"
            print(f"ID: {task.id}, Title: {task.title}, Status: {status}, Priority: {task.priority}, Due Date: {task.due_date}")

    def mark_task_done(self, task_id):
        task = self.find_task_by_id(task_id)
        if task:
            task.done = True
            self.save_tasks()
            print(f"Задача с ID {task_id} отмечена как выполненная.")
        else:
            print(f"Задача с ID {task_id} не найдена.")

    def edit_task(self, task_id, title=None, description=None, priority=None, due_date=None):
        task = self.find_task_by_id(task_id)
        if task:
            if title:
                task.title = title
            if description:
                task.description = description
            if priority:
                task.priority = priority
            if due_date:
                task.due_date = due_date
            self.save_tasks()
            print(f"Задача с ID {task_id} обновлена.")
        else:
            print(f"Задача с ID {task_id} не найдена.")

    def delete_task(self, task_id):
        task = self.find_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print(f"Задача с ID {task_id} удалена.")
        else:
            print(f"Задача с ID {task_id} не найдена.")

    def import_from_csv(self, csv_file):
        try:
            with open(csv_file, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.create_task(
                        title=row["title"],
                        description=row["description"],
                        priority=row["priority"],
                        due_date=row["due_date"]
                    )
            print(f"Задачи импортированы из файла {csv_file}.")
        except FileNotFoundError:
            print(f"Файл {csv_file} не найден.")

    def export_to_csv(self, csv_file):
        with open(csv_file, "w", newline="") as file:
            fieldnames = ["id", "title", "description", "done", "priority", "due_date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                writer.writerow(task.to_dict())
        print(f"Задачи экспортированы в файл {csv_file}.")

    def filter_tasks(self, status=None, priority=None, due_date=None):
        """Фильтрация задач."""
        filtered_tasks = self.tasks
        if status is not None:
            filtered_tasks = [task for task in filtered_tasks if task.done == status]
        if priority:
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority]
        if due_date:
            filtered_tasks = [task for task in filtered_tasks if task.due_date == due_date]

        if not filtered_tasks:
            print("Нет задач, соответствующих критериям фильтрации.")
        else:
            for task in filtered_tasks:
                status_str = "Выполнена" if task.done else "Не выполнена"
                print(f"ID: {task.id}, Title: {task.title}, Status: {status_str}, Priority: {task.priority}, Due Date: {task.due_date}")

    def find_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None


class Contact:
    def __init__(self, contact_id, name, phone, email):
        self.id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }

    @staticmethod
    def from_dict(data):
        return Contact(
            contact_id=data["id"],
            name=data["name"],
            phone=data["phone"],
            email=data["email"]
        )


class ContactsManager:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                return [Contact.from_dict(contact) for contact in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_contacts(self):
        with open(self.filename, "w") as file:
            json.dump([contact.to_dict() for contact in self.contacts], file, indent=4)

    def add_contact(self, name, phone, email):
        contact_id = max([contact.id for contact in self.contacts], default=0) + 1
        contact = Contact(contact_id, name, phone, email)
        self.contacts.append(contact)
        self.save_contacts()
        print(f"Контакт с ID {contact_id} добавлен.")

    def find_contacts(self, query):
        results = [
            contact for contact in self.contacts
            if query.lower() in contact.name.lower() or query in contact.phone
        ]
        if results:
            print("\nНайденные контакты:")
            for contact in results:
                print(f"ID: {contact.id}, Name: {contact.name}, Phone: {contact.phone}, Email: {contact.email}")
        else:
            print("Контакты не найдены.")

    def edit_contact(self, contact_id, name=None, phone=None, email=None):
        contact = self.find_contact_by_id(contact_id)
        if contact:
            if name:
                contact.name = name
            if phone:
                contact.phone = phone
            if email:
                contact.email = email
            self.save_contacts()
            print(f"Контакт с ID {contact_id} обновлён.")
        else:
            print(f"Контакт с ID {contact_id} не найден.")

    def delete_contact(self, contact_id):
        contact = self.find_contact_by_id(contact_id)
        if contact:
            self.contacts.remove(contact)
            self.save_contacts()
            print(f"Контакт с ID {contact_id} удалён.")
        else:
            print(f"Контакт с ID {contact_id} не найден.")

    def import_from_csv(self, csv_file):
        try:
            with open(csv_file, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.add_contact(
                        name=row["name"],
                        phone=row["phone"],
                        email=row["email"]
                    )
            print(f"Контакты импортированы из файла {csv_file}.")
        except FileNotFoundError:
            print(f"Файл {csv_file} не найден.")

    def export_to_csv(self, csv_file):
        with open(csv_file, "w", newline="") as file:
            fieldnames = ["id", "name", "phone", "email"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for contact in self.contacts:
                writer.writerow(contact.to_dict())
        print(f"Контакты экспортированы в файл {csv_file}.")

    def find_contact_by_id(self, contact_id):
        for contact in self.contacts:
            if contact.id == contact_id:
                return contact
        return None



class FinanceRecord:
    def __init__(self, record_id, amount, category, date, description):
        self.id = record_id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description
        }

    @staticmethod
    def from_dict(data):
        return FinanceRecord(
            record_id=data["id"],
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
            description=data["description"]
        )


class FinanceManager:
    def __init__(self, filename="finance.json"):
        self.filename = filename
        self.records = self.load_records()

    def load_records(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                return [FinanceRecord.from_dict(record) for record in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_records(self):
        with open(self.filename, "w") as file:
            json.dump([record.to_dict() for record in self.records], file, indent=4)

    def add_record(self, amount, category, date, description):
        record_id = max([record.id for record in self.records], default=0) + 1
        record = FinanceRecord(record_id, amount, category, date, description)
        self.records.append(record)
        self.save_records()
        print(f"Финансовая запись с ID {record_id} добавлена.")

    def list_records(self, category=None, date=None):
        filtered_records = self.records
        if category:
            filtered_records = [record for record in filtered_records if record.category == category]
        if date:
            filtered_records = [record for record in filtered_records if record.date == date]

        if not filtered_records:
            print("Записей не найдено.")
        else:
            print("\nСписок финансовых записей:")
            for record in filtered_records:
                print(f"ID: {record.id}, Amount: {record.amount}, Category: {record.category}, Date: {record.date}, Description: {record.description}")

    def calculate_balance(self):
        balance = sum(record.amount for record in self.records)
        print(f"\nОбщий баланс: {balance:.2f}")

    def group_by_category(self):
        categories = {}
        for record in self.records:
            if record.category not in categories:
                categories[record.category] = 0
            categories[record.category] += record.amount

        print("\nГруппировка по категориям:")
        for category, total in categories.items():
            print(f"Категория: {category}, Сумма: {total:.2f}")

    def generate_report(self, start_date, end_date):
        records_in_period = [
            record for record in self.records
            if start_date <= record.date <= end_date
        ]
        if not records_in_period:
            print("Нет записей за указанный период.")
        else:
            print(f"\nФинансовый отчёт с {start_date} по {end_date}:")
            for record in records_in_period:
                print(f"ID: {record.id}, Amount: {record.amount}, Category: {record.category}, Date: {record.date}, Description: {record.description}")
            total_amount = sum(record.amount for record in records_in_period)
            print(f"\nОбщий итог за период: {total_amount:.2f}")

    def import_from_csv(self, csv_file):
        try:
            with open(csv_file, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.add_record(
                        amount=float(row["amount"]),
                        category=row["category"],
                        date=row["date"],
                        description=row["description"]
                    )
            print(f"Финансовые записи импортированы из файла {csv_file}.")
        except FileNotFoundError:
            print(f"Файл {csv_file} не найден.")

    def export_to_csv(self, csv_file):
        with open(csv_file, "w", newline="") as file:
            fieldnames = ["id", "amount", "category", "date", "description"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for record in self.records:
                writer.writerow(record.to_dict())
        print(f"Финансовые записи экспортированы в файл {csv_file}.")




class Calculator:
    def __init__(self):
        pass

    def calculate(self, expression):
        try:
            allowed_chars = "0123456789+-*/.() "
            if not all(char in allowed_chars for char in expression):
                raise ValueError("Выражение содержит недопустимые символы.")

            result = eval(expression)
            return result
        except ZeroDivisionError:
            return "Ошибка: Деление на ноль невозможно."
        except ValueError as ve:
            return f"Ошибка: {ve}"
        except Exception as e:
            return f"Ошибка: Некорректное выражение ({e})."


class PersonalAssistant:
    def __init__(self):
        self.running = True
        self.notes_manager = NotesManager()
        self.tasks_manager = TasksManager()
        self.contacts_manager = ContactsManager()
        self.finance_manager = FinanceManager()
        self.calculator = Calculator()

    def display_menu(self):
        print("\nДобро пожаловать в Персональный помощник!")
        print("Выберите действие:")
        print("1. Управление заметками")
        print("2. Управление задачами")
        print("3. Управление контактами")
        print("4. Управление финансовыми записями")
        print("5. Калькулятор")
        print("6. Выход")

    def handle_input(self):
        try:
            choice = int(input("Введите номер действия: "))
            if choice == 1:
                self.manage_notes()
            elif choice == 2:
                self.manage_tasks()
            elif choice == 3:
                self.manage_contacts()
            elif choice == 4:
                self.manage_finances()
            elif choice == 5:
                self.run_calculator()
            elif choice == 6:
                self.exit_app()
            else:
                print("Функционал ещё не реализован.")
        except ValueError:
            print("Пожалуйста, введите число от 1 до 6.")

        def manage_finances(self):
            while True:
                print("\nУправление финансовыми записями:")
                print("1. Добавить запись")
                print("2. Просмотреть записи")
                print("3. Посчитать общий баланс")
                print("4. Группировать по категориям")
                print("5. Сгенерировать отчёт")
                print("6. Импорт из CSV")
                print("7. Экспорт в CSV")
                print("8. Вернуться в главное меню")
                try:
                    choice = int(input("Выберите действие: "))
                    if choice == 1:
                        amount = float(
                            input("Введите сумму операции (положительная для дохода, отрицательная для расхода): "))
                        category = input("Введите категорию: ")
                        date = input("Введите дату операции (ДД-ММ-ГГГГ): ")
                        description = input("Введите описание: ")
                        self.finance_manager.add_record(amount, category, date, description)
                    elif choice == 2:
                        category = input("Введите категорию для фильтрации (или оставьте пустым): ")
                        date = input("Введите дату для фильтрации (ДД-ММ-ГГГГ или оставьте пустым): ")
                        self.finance_manager.list_records(category or None, date or None)
                    elif choice == 3:
                        self.finance_manager.calculate_balance()
                    elif choice == 4:
                        self.finance_manager.group_by_category()
                    elif choice == 5:
                        start_date = input("Введите начальную дату (ДД-ММ-ГГГГ): ")
                        end_date = input("Введите конечную дату (ДД-ММ-ГГГГ): ")
                        self.finance_manager.generate_report(start_date, end_date)
                    elif choice == 6:
                        csv_file = input("Введите имя CSV-файла для импорта: ")
                        self.finance_manager.import_from_csv(csv_file)
                    elif choice == 7:
                        csv_file = input("Введите имя CSV-файла для экспорта: ")
                        self.finance_manager.export_to_csv(csv_file)
                    elif choice == 8:
                        break
                    else:
                        print("Неверный выбор. Попробуйте снова.")
                except ValueError:
                    print("Пожалуйста, введите корректное число.")

    def run_calculator(self):
        print("\nКалькулятор:")
        print("Введите математическое выражение.")
        print("Введите 'exit', чтобы вернуться в главное меню.")
        while True:
            expression = input("Введите выражение: ").strip()
            if expression.lower() == "exit":
                break
            result = self.calculator.calculate(expression)
            print(f"Результат: {result}")



    def manage_contacts(self):
        while True:
            print("\nУправление контактами:")
            print("1. Добавить контакт")
            print("2. Найти контакт")
            print("3. Редактировать контакт")
            print("4. Удалить контакт")
            print("5. Импорт контактов из CSV")
            print("6. Экспорт контактов в CSV")
            print("7. Вернуться в главное меню")
            try:
                choice = int(input("Выберите действие: "))
                if choice == 1:
                    name = input("Введите имя контакта: ")
                    phone = input("Введите номер телефона: ")
                    email = input("Введите адрес электронной почты: ")
                    self.contacts_manager.add_contact(name, phone, email)
                elif choice == 2:
                    query = input("Введите имя или номер телефона для поиска: ")
                    self.contacts_manager.find_contacts(query)
                elif choice == 3:
                    contact_id = int(input("Введите ID контакта: "))
                    name = input("Введите новое имя (оставьте пустым для сохранения текущего): ")
                    phone = input("Введите новый номер телефона (оставьте пустым для сохранения текущего): ")
                    email = input("Введите новый адрес электронной почты (оставьте пустым для сохранения текущего): ")
                    self.contacts_manager.edit_contact(contact_id, name or None, phone or None, email or None)
                elif choice == 4:
                    contact_id = int(input("Введите ID контакта: "))
                    self.contacts_manager.delete_contact(contact_id)
                elif choice == 5:
                    csv_file = input("Введите имя CSV-файла для импорта: ")
                    self.contacts_manager.import_from_csv(csv_file)
                elif choice == 6:
                    csv_file = input("Введите имя CSV-файла для экспорта: ")
                    self.contacts_manager.export_to_csv(csv_file)
                elif choice == 7:
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите корректное число.")


    def manage_tasks(self):
        while True:
            print("\nУправление задачами:")
            print("1. Добавить задачу")
            print("2. Просмотреть список задач")
            print("3. Отметить задачу как выполненную")
            print("4. Редактировать задачу")
            print("5. Удалить задачу")
            print("6. Импорт задач из CSV")
            print("7. Экспорт задач в CSV")
            print("8. Фильтровать задачи")
            print("9. Вернуться в главное меню")
            try:
                choice = int(input("Выберите действие: "))
                if choice == 1:
                    title = input("Введите название задачи: ")
                    description = input("Введите описание задачи: ")
                    priority = input("Введите приоритет (Высокий, Средний, Низкий): ")
                    due_date = input("Введите срок выполнения (ДД-ММ-ГГГГ): ")
                    self.tasks_manager.create_task(title, description, priority, due_date)
                elif choice == 2:
                    self.tasks_manager.list_tasks()
                elif choice == 3:
                    task_id = int(input("Введите ID задачи: "))
                    self.tasks_manager.mark_task_done(task_id)
                elif choice == 4:
                    task_id = int(input("Введите ID задачи: "))
                    title = input("Введите новый заголовок (оставьте пустым для сохранения текущего): ")
                    description = input("Введите новое описание (оставьте пустым для сохранения текущего): ")
                    priority = input("Введите новый приоритет (оставьте пустым для сохранения текущего): ")
                    due_date = input("Введите новый срок выполнения (оставьте пустым для сохранения текущего): ")
                    self.tasks_manager.edit_task(task_id, title or None, description or None, priority or None, due_date or None)
                elif choice == 5:
                    task_id = int(input("Введите ID задачи: "))
                    self.tasks_manager.delete_task(task_id)
                elif choice == 6:
                    csv_file = input("Введите имя CSV-файла для импорта: ")
                    self.tasks_manager.import_from_csv(csv_file)
                elif choice == 7:
                    csv_file = input("Введите имя CSV-файла для экспорта: ")
                    self.tasks_manager.export_to_csv(csv_file)
                elif choice == 8:
                    status = input("Фильтр по статусу (Выполнена/Не выполнена или оставьте пустым): ").strip()
                    priority = input("Фильтр по приоритету (Высокий, Средний, Низкий или оставьте пустым): ").strip()
                    due_date = input("Фильтр по сроку (ДД-ММ-ГГГГ или оставьте пустым): ").strip()
                    self.tasks_manager.filter_tasks(
                        status=(status == "Выполнена") if status else None,
                        priority=priority or None,
                        due_date=due_date or None
                    )
                elif choice == 9:
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите корректное число.")

    def manage_notes(self):
        while True:
            print("\nУправление заметками:")
            print("1. Создать заметку")
            print("2. Просмотреть список заметок")
            print("3. Просмотреть подробности заметки")
            print("4. Редактировать заметку")
            print("5. Удалить заметку")
            print("6. Импорт заметок из CSV")
            print("7. Экспорт заметок в CSV")
            print("8. Вернуться в главное меню")
            try:
                choice = int(input("Выберите действие: "))
                if choice == 1:
                    title = input("Введите заголовок заметки: ")
                    content = input("Введите содержимое заметки: ")
                    self.notes_manager.create_note(title, content)
                elif choice == 2:
                    self.notes_manager.list_notes()
                elif choice == 3:
                    note_id = int(input("Введите ID заметки: "))
                    self.notes_manager.view_note_details(note_id)
                elif choice == 4:
                    note_id = int(input("Введите ID заметки: "))
                    title = input("Введите новый заголовок (оставьте пустым для сохранения текущего): ")
                    content = input("Введите новое содержимое (оставьте пустым для сохранения текущего): ")
                    self.notes_manager.edit_note(note_id, title or None, content or None)
                elif choice == 5:
                    note_id = int(input("Введите ID заметки: "))
                    self.notes_manager.delete_note(note_id)
                elif choice == 6:
                    csv_file = input("Введите имя CSV-файла для импорта: ")
                    self.notes_manager.import_from_csv(csv_file)
                elif choice == 7:
                    csv_file = input("Введите имя CSV-файла для экспорта: ")
                    self.notes_manager.export_to_csv(csv_file)
                elif choice == 8:
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите корректное число.")

    def exit_app(self):
        print("Выход из приложения. До свидания!")
        self.running = False

    def run(self):
        while self.running:
            self.display_menu()
            self.handle_input()


if __name__ == "__main__":
    app = PersonalAssistant()
    app.run()