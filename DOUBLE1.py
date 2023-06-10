import subprocess
import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Define as opções do driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# Inicializa o driver com o ChromeDriverManager que irá automaticamente baixar o driver correto
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)

# Define o tempo máximo de espera para o driver
driver_wait_time = 10

# Aguarda até que a página seja carregada
driver.get('https://old.tipminer.com/blaze/double')
time.sleep(5)


# Criação da interface
#root = tk.Tk()
#root.title('Double Sequence')

#bg_color = '#000000'
#fg_color = '#FFFFFF'

# Criar a grade de quadrados
#frame = ttk.Frame(root, padding=15)
#frame.pack(fill='both', expand=True)

# Lista para armazenar os labels dos números e horários
#num_labels = []
#time_labels = []

# Criar a matriz de quadrados
#for i in range(7):
    #row_labels = []
    #row_time_labels = []
    #for j in range(28):
        #square_frame = ttk.Frame(frame, width=30, height=30, relief='raised', borderwidth=1)
        #square_frame.grid(row=i, column=j, padx=0, pady=0)

        #num_label = ttk.Label(square_frame, text='', width=4, anchor='center', font=('arial', 13, 'bold'), background=bg_color, foreground=fg_color)
        #num_label.pack(side='top', pady=0)

        #time_frame = ttk.Frame(square_frame, width=30, height=2, relief='raised', borderwidth=0)
        #time_frame.pack(side='top', pady=1)

        #time_label = ttk.Label(time_frame, text='', width=5, anchor='center', font=('arial', 10, 'bold'), background=bg_color, foreground=fg_color)
        #time_label.pack(side='top', pady=1)

        #row_labels.append(num_label)
        #row_time_labels.append(time_label)

    #num_labels.append(row_labels)
    #time_labels.append(row_time_labels)


def atualizar_sequencia():
    try:
        # Encontra os elementos com os números desejados
        number_elements = WebDriverWait(driver, driver_wait_time).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.roll > div.number'))
        )

        # Extrai os valores dos elementos
        numbers = [element.text.strip() for element in number_elements]
        print(f'Os números são: {numbers}')

        # Encontra os elementos com os horários desejados
        time_elements = WebDriverWait(driver, driver_wait_time).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.time'))
        )

        # Extrai os valores dos elementos
        times = [element.text.strip() for element in time_elements]
        print(f'Os horários são: {times}')

        # Encontrar os índices dos zeros na sequência
        zeros_indices = [i for i, num in enumerate(numbers) if num == '0']

        # Registrar o horário em que cada zero ocorre
        zeros_horarios = [times[i] for i in zeros_indices]

        # Identificar e registrar os três números anteriores e posteriores a cada zero
        zeros_numeros_antecessores = []
        zeros_numeros_sucessores = []

        for zero_index in zeros_indices:
            antecessores = []
            sucessores = []
            count = 0

            # Capturar os três números anteriores ao zero
            for i in range(zero_index - 1, -1, -1):
                if count == 3:
                    break
                if numbers[i] != '0':
                    antecessores.append(numbers[i])
                    count += 1

            count = 0

            # Capturar os três números posteriores ao zero
            for i in range(zero_index + 1, len(numbers)):
                if count == 3:
                    break
                if numbers[i] != '0':
                    sucessores.append(numbers[i])
                    count += 1

            zeros_numeros_antecessores.append(antecessores)
            zeros_numeros_sucessores.append(sucessores)

        # Garantir que nenhum zero esteja presente nos conjuntos de números antecessores e posteriores
        for i, numeros_antecessores in enumerate(zeros_numeros_antecessores):
            zeros_numeros_antecessores[i] = [num for num in numeros_antecessores if num != '0']
        for i, numeros_sucessores in enumerate(zeros_numeros_sucessores):
            zeros_numeros_sucessores[i] = [num for num in numeros_sucessores if num != '0']

        # Em caso de falta de três números anteriores ou posteriores, registrar os números disponíveis
        for i, numeros_antecessores in enumerate(zeros_numeros_antecessores):
            if len(numeros_antecessores) < 3:
                zeros_numeros_antecessores[i] = numbers[zero_index - len(numeros_antecessores):zero_index][
                                                ::-1] + numeros_antecessores[::-1]
        for i, numeros_sucessores in enumerate(zeros_numeros_sucessores):
            if len(numeros_sucessores) < 3:
                zeros_numeros_sucessores[i] = numeros_sucessores + numbers[zero_index + 1:zero_index + 1 + (
                            3 - len(numeros_sucessores))]

        # Não registrar o mesmo zero várias vezes se ocorrerem zeros com o mesmo horário
        zeros_indices_uniq = []
        zeros_horarios_uniq = []
        zeros_numeros_antecessores_uniq = []
        zeros_numeros_sucessores_uniq = []
        for i, horario in enumerate(zeros_horarios):
            if horario not in zeros_horarios_uniq:
                zeros_indices_uniq.append(zeros_indices[i])
                zeros_horarios_uniq.append(horario)
                zeros_numeros_antecessores_uniq.append(zeros_numeros_antecessores[i])
                zeros_numeros_sucessores_uniq.append(zeros_numeros_sucessores[i])

        # Inicializar a lista para armazenar os horários prováveis dos próximos zeros
        zeros_horarios_provaveis = []

        # Calcular as probabilidades e obter os horários prováveis dos próximos zeros
        for i in range(len(zeros_indices_uniq)):
            zero_horario = zeros_horarios_uniq[i]
            numeros_antecessores = zeros_numeros_antecessores_uniq[i]
            numeros_sucessores = zeros_numeros_sucessores_uniq[i]

            # Verificar se a sequência de números antes tem menos de 3 números
            if len(numeros_antecessores) < 3:
                numeros_antecessores = ['0'] * (3 - len(numeros_antecessores)) + numeros_antecessores

            # Verificar se a sequência de números depois tem menos de 3 números
            if len(numeros_sucessores) < 3:
                numeros_sucessores = numeros_sucessores + ['0'] * (3 - len(numeros_sucessores))

            # Calcular as probabilidades
            probabilidades = []

            # Calcular as probabilidades
            probabilidades = []

            # Calcular as probabilidades
            probabilidades = []

            # Função para ajustar as horas e minutos
            def ajustar_horario(horas, minutos):
                horas += minutos // 60
                minutos = minutos % 60
                return horas % 24, minutos

            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[1]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[1]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_sucessores[0]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_sucessores[0]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_sucessores[1]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_sucessores[1]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_antecessores[1]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_antecessores[1]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_sucessores[0]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_sucessores[0]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_sucessores[1]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_sucessores[1]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[1]) + int(numeros_sucessores[0]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[1]) + int(numeros_sucessores[0]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[1]) + int(numeros_sucessores[1]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[1]) + int(numeros_sucessores[1]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_sucessores[0]) + int(numeros_sucessores[1]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_sucessores[0]) + int(numeros_sucessores[1]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_antecessores[1]) + int(numeros_sucessores[0]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_antecessores[1]) + int(numeros_sucessores[0]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_antecessores[1]) + int(numeros_sucessores[1]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_antecessores[1]) + int(numeros_sucessores[1]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[1]) + int(numeros_sucessores[0]) + int(numeros_sucessores[1]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[1]) + int(numeros_sucessores[0]) + int(numeros_sucessores[1]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_sucessores[0]) + int(numeros_sucessores[1]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_sucessores[0]) + int(numeros_sucessores[1]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_antecessores[1]) + int(numeros_sucessores[0]) + int(numeros_sucessores[1]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_antecessores[1]) + int(numeros_sucessores[0]) + int(numeros_sucessores[1]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_antecessores[1]) + int(numeros_sucessores[0]) + int(numeros_sucessores[1]) + int(numeros_antecessores[2]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_antecessores[1]) + int(numeros_sucessores[0]) + int(numeros_sucessores[1]) + int(numeros_antecessores[2]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_antecessores[1]) + int(numeros_sucessores[0]) + int(numeros_sucessores[1]) + int(numeros_sucessores[2]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_antecessores[1]) + int(numeros_sucessores[0]) + int(numeros_sucessores[1]) + int(numeros_sucessores[2]))[1]:02d}")
            probabilidades.append(
                f"{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_antecessores[1]) + int(numeros_sucessores[0]) + int(numeros_sucessores[1]) + int(numeros_sucessores[2]) + int(numeros_antecessores[2]))[0]:02d}:{ajustar_horario(int(zero_horario.split(':')[0]), int(zero_horario.split(':')[1]) + int(numeros_antecessores[0]) + int(numeros_antecessores[1]) + int(numeros_sucessores[0]) + int(numeros_sucessores[1]) + int(numeros_sucessores[2]) + int(numeros_antecessores[2]))[1]:02d}")

            # Armazenar os horários prováveis na lista geral
            zeros_horarios_provaveis.append(probabilidades)

            # Exibir as informações na saída
        for i, indice in enumerate(zeros_indices_uniq):
            print(f"Minuto: {zeros_horarios_uniq[i]}")
            print(f"Números antes: {', '.join(zeros_numeros_antecessores_uniq[i])}")
            print(f"Números depois: {', '.join(zeros_numeros_sucessores_uniq[i])}")
            print("Horários prováveis:")
            for j, horario_provavel in enumerate(zeros_horarios_provaveis[i]):
                print(f"E{j + 1} - {horario_provavel}")
            print()

        with open('D:\\BLAZE\\BLAZE\\Resultados\\resultados.txt', 'w') as f:
            json.dump(numbers, f)
        with open('D:\\BLAZE\\BLAZE\\Resultados\\horarios.txt', 'w') as f:
            json.dump(times, f)


        # Preenche a interface com os valores extraídos

        #for i, number in enumerate(numbers):
            #row = i // 28
            #col = 27 - (i % 28)
#
            #if row >= 7:
                #break

            #num_labels[row][col].config(text=number)

            #if number == '0':
                #num_labels[row][col].config(background='white', foreground='red')
            #elif 1 <= int(number) <= 7:
                #num_labels[row][col].config(background='red', foreground='white')
            #else:
                #num_labels[row][col].config(background='black', foreground='white')

        # Preenche a interface com os horários extraídos
        #for i, time_value in enumerate(times):
            #row = i // 28
            #col = 27 - (i % 28)

            #if row >= 7:
                #break

            #time_labels[row][col].config(text=time_value)

            #if time_value == '0':
                #time_labels[row][col].config(background='white', foreground='red')
            #else:
                #time_labels[row][col].config(background='black', foreground='white')

    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")


    # Aguarda um tempo antes de capturar a próxima sequência
    #root.after(1000, atualizar_sequencia)

# Iniciar o processo de atualização da sequência
#atualizar_sequencia()
script_path = 'D:\pythonProject1\invictus.py'
subprocess.Popen(['python', script_path])
# Loop principal da interface
#root.mainloop()

while True:
    try:
        # Atualiza a sequência a cada segundo
        atualizar_sequencia()
        time.sleep(1)
    except KeyboardInterrupt:
        print("Parando o script...")
        break


# Finaliza o driver
driver.quit()
