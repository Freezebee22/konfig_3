import re
import toml
import sys

constants = {}  # Глобальный словарь для хранения констант

def parse_value(value):
    # Проверка на число
    if re.match(r'^\d+$', value):
        return int(value)
    # Проверка на строку
    elif value.startswith('q(') and value.endswith(')'):
        return value[2:-1].strip()  # Убираем 'q(' и ')'
    # Проверка на массив
    elif value.startswith('[') and value.endswith(']'):
        elements = re.split(r',\s*', value[1:-1].strip())
        return [parse_value(element.strip()) for element in elements if element.strip() != '']
    # Проверка на словарь
    elif value.startswith('{') and value.endswith('}'):
        return parse_dict(value)
    # Проверка на вычисление константы
    elif re.match(r'^\|([a-z][a-z0-9_]*)\|$', value):
        const_name = re.match(r'^\|([a-z][a-z0-9_]*)\|$', value).group(1)
        if const_name not in constants:
            raise ValueError(f"Константа {const_name} не определена.")
        return constants[const_name]
    else:
        raise ValueError(f"Невалидное значение: {value}")

def parse_dict(value):
    content = value[1:-1].strip()
    dictionary = {}

    current = []  # Для накопления текущей пары "ключ => значение"
    inside_brackets = 0  # Вложенность массивов
    inside_curly = 0  # Вложенность словарей
    inside_string = False  # Вложенность строки
    i = 0

    while i < len(content):
        char = content[i]

        if inside_string:
            if char == ')' and content[i - 1] != '\\':
                inside_string = False
            current.append(char)
        elif char == '[':
            inside_brackets += 1
            current.append(char)
        elif char == ']':
            inside_brackets -= 1
            current.append(char)
        elif char == '{':
            inside_curly += 1
            current.append(char)
        elif char == '}':
            inside_curly -= 1
            current.append(char)
        elif char == 'q' and content[i:i+2] == 'q(':
            inside_string = True
            current.append(char)
        elif char == ',' and inside_brackets == 0 and inside_curly == 0 and not inside_string:
            pair = ''.join(current).strip()
            key_value = pair.split('=>', 1)
            if len(key_value) != 2:
                raise ValueError(f"Невалидный словарь: {pair}")
            key = key_value[0].strip()
            value = parse_value(key_value[1].strip())
            dictionary[key] = value
            current = []
        else:
            current.append(char)

        i += 1

    if current:
        pair = ''.join(current).strip()
        key_value = pair.split('=>', 1)
        if len(key_value) != 2:
            raise ValueError(f"Невалидный словарь: {pair}")
        key = key_value[0].strip()
        value = parse_value(key_value[1].strip())
        dictionary[key] = value

    return dictionary



def parse_config(input_text):
    global constants
    config = {}
    lines = input_text.splitlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match_def = re.match(r'^def\s+([a-z][a-z0-9_]*?)\s*:=\s*(.*)\s*;$', line)
        if match_def:
            name = match_def.group(1)
            value = parse_value(match_def.group(2))
            constants[name] = value
            continue

        match_compute = re.match(r'^\|([a-z][a-z0-9_]*)\|$', line)
        if match_compute:
            name = match_compute.group(1)
            if name not in constants:
                raise ValueError(f"Константа {name} не определена.")
            config[name] = constants[name]
            continue

    return config

def convert_to_toml(parsed_config):
    return toml.dumps(parsed_config)

def main():
    try:
        input_text = sys.stdin.read()
        parsed_config = parse_config(input_text)
        toml_output = convert_to_toml(parsed_config)
        print(toml_output)
    except ValueError as e:
        print(f"Ошибка синтаксиса: {e}")

if __name__ == "__main__":
    main()
