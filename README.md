# Voice Assistant

* [English Version](#english-version)
* [Українська версія](#українська-версія)

---

# English Version

## Description

Voice Assistant is a desktop voice-controlled assistant developed with Python and Django. The application allows users to interact with their computer using voice commands, launch programs, open websites, and execute predefined actions.

The project demonstrates the integration of speech recognition technologies, automation tools, and Python application architecture.

---

## Project Purpose

This project was created to help beginner developers learn:

* Python application development;
* Django project architecture;
* Voice command processing;
* Automation of operating system tasks;
* Working with databases using Django ORM;
* Creating custom management commands;
* Organizing utility modules and reusable code.

The project demonstrates how a voice assistant can be built using modern Python technologies.

---

## Team Members

* Your Name — GitHub Profile

---

## Table of Contents

* Project Purpose
* Team Members
* Technologies and Modules
* Installation Guide
* Project Structure
* Application Description
* Main Files Description
* Features
* Conclusion

---

## Technologies and Modules

### Backend

* Python
* Django
* Django ORM
* SQLite
* python-dotenv

### Voice Processing

* Speech Recognition
* Text-to-Speech technologies
* Custom voice response system

### Utilities

* Program launching
* Website opening
* Command management
* System automation

---

## Installation Guide

### Clone Repository

```bash
git clone <repository_url>
cd Voice_Assistant
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file and specify required settings.

### Run Database Migrations

```bash
python manage.py migrate
```

### Start the Assistant

```bash
python manage.py run_assistant
```

or

```bash
python start_project.py
```

---

## Project Structure

```text
Voice_Assistant
│
├── core
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── management
│       └── commands
│           └── run_assistant.py
│
├── utils
│   ├── add_command.py
│   ├── close_programs.py
│   ├── find_path.py
│   ├── run_sites.py
│   └── voice_answers.py
│
├── manage.py
├── start_project.py
├── requirements.txt
└── db.sqlite3
```

---

## Application Description

### core

Main application responsible for:

* storing assistant commands;
* database interaction;
* application configuration;
* assistant management.

### utils

Contains utility modules:

* launching applications;
* opening websites;
* generating voice responses;
* searching executable paths;
* closing running programs.

---

## Main Files Description

### run_assistant.py

Main management command used to start the voice assistant.

### add_command.py

Adds and manages assistant commands.

### close_programs.py

Handles closing applications.

### run_sites.py

Opens websites from voice commands.

### find_path.py

Searches executable file paths.

### voice_answers.py

Stores assistant responses and voice output logic.

### models.py

Database models for storing assistant data.

---

## Features

* Voice command recognition
* Opening websites
* Launching desktop applications
* Closing running programs
* Custom command management
* Database-backed command storage

---

## Conclusion

This project provided practical experience in Python development, automation, Django architecture, and voice-controlled applications.

Future improvements may include:

* AI-powered conversations;
* Integration with ChatGPT APIs;
* Smart home control;
* Multilingual support;
* Advanced natural language processing.

---

# Українська версія

## Опис

Voice Assistant — це голосовий помічник, розроблений за допомогою Python та Django. Застосунок дозволяє користувачеві взаємодіяти з комп'ютером за допомогою голосових команд, запускати програми, відкривати вебсайти та виконувати різноманітні автоматизовані дії.

---

## Мета проєкту

Цей проєкт був створений для вивчення:

* розробки застосунків на Python;
* архітектури Django-проєктів;
* обробки голосових команд;
* автоматизації роботи операційної системи;
* роботи з базами даних через ORM;
* створення власних management-команд;
* організації допоміжних модулів та утиліт.

Проєкт демонструє принципи створення голосового асистента засобами Python.

---

## Учасники

* Ваше ім'я — GitHub Profile

---

## Технології та модулі

### Backend

* Python
* Django
* Django ORM
* SQLite
* python-dotenv

### Голосова обробка

* Speech Recognition
* Text-to-Speech
* Система голосових відповідей

### Автоматизація

* Запуск програм
* Відкриття сайтів
* Керування командами
* Автоматизація системних дій

---

## Опис проєкту

### core

Основний додаток, що відповідає за:

* зберігання команд асистента;
* взаємодію з базою даних;
* налаштування застосунку;
* запуск голосового помічника.

### utils

Містить допоміжні модулі для:

* запуску програм;
* відкриття вебсайтів;
* голосових відповідей;
* пошуку шляхів до програм;
* завершення роботи програм.

---

## Висновок

Під час розробки проєкту було отримано практичний досвід роботи з Python, Django, автоматизацією системних процесів та технологіями голосового керування.

У майбутньому проєкт можна розширити інтеграцією штучного інтелекту, підтримкою кількох мов, керуванням розумним будинком та розширеним аналізом природної мови.
