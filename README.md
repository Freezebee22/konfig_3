# Конвертер конфигураций в TOML  

Эта программа позволяет конвертировать файлы пользовательского формата конфигураций в формат TOML.

### Основные функции:  
- Поддержка констант, массивов, словарей и строк.  
- Возможность ссылаться на ранее определённые константы.  
- Автоматическая проверка корректности синтаксиса.
- Простая работа через стандартный ввод и вывод. 

## 2. Описание функций  

### Основные функции  

#### `validate_name(name: str)`  
Проверяет, соответствует ли имя правилам `[a-z][a-z0-9_]*` (начинается с прописной латинской буквы, далее могут быть прописные латинские символы, цифры и нижнее подчеркивание). Вызывает исключение `ValueError`, если имя некорректное.  

#### `parse_value(value: str)`  
Анализирует строку `value` и возвращает Python-объект в зависимости от типа:  
- Число → `int`  
- Строка (формат `q(строка)`) → `str`  
- Массив (формат `[элемент1, элемент2]`) → `list`  
- Словарь (формат `{ключ => значение}`) → `dict`  
- Константа (формат `|имя|`) → значение из глобального словаря.  

#### `parse_dict(value: str)`  
Парсит строку-словарь и возвращает Python-словарь. Поддерживает вложенные массивы и словари.  

#### `parse_config(input_text: str)`  
Обрабатывает текстовый ввод, определяет константы и вычисляет их значения. Возвращает итоговый словарь конфигурации.  

#### `convert_to_toml(parsed_config: dict)`  
Конвертирует Python-словарь в формат TOML.  

### Глобальные настройки  
- Константы хранятся в глобальном словаре `constants`.  
- Формат TOML-выходных данных полностью соответствует стандарту.  

## 3. Описание команд для сборки проекта  

### Установка зависимостей  
Проект использует модуль `toml`. Для его установки выполните:  
```bash  
pip install toml
```

После установки необходимых зависимостей программу можно запустить командой:
```bash
python main.py < code.txt
```
code.txt - файл с кодом на учебном конфигурационном языке.

Для вывода в отдельный файл (например, output.txt), можно использовать команду:
```bash
python main.py < code.txt > output.txt
```

## Пример использования

   Ввод команды в консоль:
   
   ![image](https://github.com/user-attachments/assets/53212019-8e50-43e6-a75b-e5cea8122408)

   Входные данные:

   ![image](https://github.com/user-attachments/assets/1938936c-39b0-430c-8764-98e6b1e84d75)

   Выходные данные:

   ![image](https://github.com/user-attachments/assets/bd357267-bcd9-46b5-9a1c-b3d76fe7fb2a)

  
## Результаты прогона тестов

Для проверки корректности работы программы предусмотрены тесты, которые можно выполнить с помощью unittest командой:
```bash
python -m unittest tests.py
```

Признаком корректной работы программы является такой вывод после прогона тестов:

   ![image](https://github.com/user-attachments/assets/4f4e1a98-c80e-4971-8b7a-e6da16c870ca)
