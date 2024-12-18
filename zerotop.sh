#!/bin/bash

# Функция для отображения информации о системе
system_info() {
    echo "Info about system:"
    echo "Name of system: $(uname -s)"
    echo "Core version: $(uname -r)"
    echo "CPU architecture: $(uname -m)"
    echo "CPU: $(lscpu | grep 'Model name' | awk -F: '{ $1=""; print $0 }' | xargs)"
    echo "Memory: $(free -h | awk '/^Mem:/ {print $2}')"
    echo "GPU: $(lspci | grep -i vga | awk -F: '{ $1=""; print $0 }' | xargs)"
    echo
}

# Функция для отображения использования процессора
cpu_usage() {
    echo "CPU Usage:"
    top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8 "%"}'
}

# Функция для отображения использования памяти
memory_usage() {
    echo "Memory Usage:"
    free -h | awk '/^Mem:/ {printf "%s/%s (%.2f%%)\n", $3, $2, $3/$2*100}'
}

# Функция для отображения использования диска
disk_usage() {
    echo "Disk Usage:"
    df -h | awk '$NF=="/"{printf "%s/%s (%s)\n", $3, $2, $5}'
}

# Функция для отображения списка процессов
list_processes() {
    echo "CPU list:"
    ps -eo pid,comm,%mem,%cpu --sort=-%mem | head -n 10
}

# Функция для отображения активных сетевых соединений
network_connections() {
    echo "Network connections:"
    ss -tunap | awk 'NR<=1 || $1=="ESTAB" {print $0}'  # Показываем только установленные соединения
}

# Функция для завершения процесса
kill_process() {
    read -p "Enter the PID of the process to complete: " pid
    if kill -0 $pid 2>/dev/null; then
        kill $pid
        echo "Process with PID $pid complete."
    else
        echo "Process with PID $pid not found."
    fi
}

# Функция для выхода из программы
exit_program() {
    echo "Exit..."
    exit 0
}

# Обработка нажатия клавиш F5 и F10
while true; do
    clear
    echo "=== ZEROTOP ==="
    system_info
    cpu_usage
    memory_usage
    disk_usage
    list_processes
    network_connections
    echo "========================="
    echo "Press F5 to complete the process, F10 to exit."
    
    # Ожидание нажатия клавиши
    read -n 1 -s key
    if [[ $key == $'\e' ]]; then
        read -n 2 -s key
        if [[ $key == '[15' ]]; then  # F5
            kill_process
        elif [[ $key == '[21' ]]; then  # F10
            exit_program
        fi
    fi
    
    sleep 5  # Обновление каждые 5 секунд
done

