import subprocess
import datetime
import unidecode as unidecode

# Запускаем команду 'tasklist' с помощью subprocess и считываем вывод
output = subprocess.check_output(['tasklist', '/V'], universal_newlines=True).encode('cp1251').decode('cp866')

# Инициализируем счетчики
total_processes = 0
user_processes = {}
total_memory_used = 0.0
max_memory_process = ('', 0)

# Разбиваем вывод на строки и обрабатываем каждую строку
mask = output.splitlines()[2]

for line in output.splitlines()[3:]:
    fields = []
    temp = ""
    for id, i in enumerate(mask):
        if i == "=":
            temp = temp + line[id]
        else:
            fields.append(unidecode.unidecode(temp.strip()))
            temp = ""

    user = fields[6]
    if fields[4] == "N/D":
        memory = 0
    else:
        memory = int(fields[4].replace(' ', '').replace("KB", ""))
    process_name = fields[0]

    total_processes += 1
    user_processes[user] = user_processes.get(user, 0) + 1
    total_memory_used += memory

    if memory > max_memory_process[1]:
        max_memory_process = (process_name, memory)

# Получаем текущую дату и время
current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%d-%m-%Y-%H-%M")

# Создаем имя файла на основе текущей даты и времени
file_name = f"{formatted_datetime}-scan.txt"

# Открываем файл для записи отчета
with open(file_name, 'w') as file:
    # Записываем отчет в файл
    file.write("Отчёт о состоянии системы:\n")
    file.write("Пользователи системы: " + ', '.join(user_processes.keys()) + '\n')
    file.write("Процессов запущено: " + str(total_processes) + '\n')
    file.write("Пользовательских процессов:\n")
    for user, processes in user_processes.items():
        file.write(f"{user}: {processes}\n")

    file.write(f"Всего памяти используется: {total_memory_used / 1024:.1f} mb\n")
    file.write("Всего CPU используется: Н/Д\n")
    file.write(f"Больше всего памяти использует: {max_memory_process[0]}\n")
    file.write("Больше всего CPU использует: Н/Д\n")

# Выводим сообщение о сохранении файла
print(f"Отчет сохранен в файле: {file_name}")
