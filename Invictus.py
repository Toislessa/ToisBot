import os
import ast
from selenium.common.exceptions import NoSuchElementException
from kivy.clock import Clock
from kivy.uix.label import Label
from selenium.webdriver.common.by import By
from kivy.properties import StringProperty
from kivy.clock import Clock
from Blaze import Bot
import pandas as pd
import random
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Line
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
import time
import json
kv = '''
Screen:
    FloatLayout:
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: 'D:\\DOWNLOADS\\invictusfundo.png'

        Image:
            source: 'D:\\DOWNLOADS\\invictus.jpg'
            size_hint: (.45, .45)
            pos_hint: {"center_x": 0.5, "center_y": .82}


        BoxLayout:
            orientation: 'vertical'
            BoxLayout:

                orientation: 'horizontal'
                size_hint_y: 0.3

                FloatLayout:
                    BoxLayout:

                        canvas.before:
                            Color:
                                rgba: 1, 0, 0, 1  # Define a cor da borda como vermelho
                            Line:
                                width: 2.  # Define a espessura da borda
                                rectangle: (self.x, self.y, self.width, self.height)

                        orientation: 'horizontal'
                        size_hint: (.6, .9)
                        pos_hint: {"center_x": .4, "center_y": .5}
                        GridLayout:
                            cols: 2
                            size_hint: (1, 1)
                            spacing:15

                            MDLabel:
                                text: "BANCA INICIAL"
                                theme_text_color: "Custom"
                                font_size: "16sp"
                                bold: True 
                                text_color: 1, 1, 1, 1


                            MDTextField:
                                id: banca
                                theme_text_color: "Custom"
                                text_color: 0, 0, 0, 1  # RGB + alpha
                                font_style: "H6"  # H6 é a fonte mais próxima de 18pt
                                bold: True
                                max_text_length: 10
                                mode: "round"
                                multiline: False
                                font_color: 0, 0, 0, 1
                                background_color: 1, 1, 1, 1
                                halign: "center"
                                font_size: "18sp"    

                            MDLabel:
                                text: "ENTRADA INICIAL"
                                theme_text_color: "Custom"
                                bold: True    
                                font_size: "16sp" 
                                text_color: 1, 1, 1, 1
                            MDTextField:
                                id: entrada
                                theme_text_color: "Custom"
                                text_color: 0, 0, 0, 1
                                font_style: "H6"
                                bold: True
                                max_text_length: 10
                                mode: "round"
                                multiline: False
                                font_color: 0, 0, 0, 1
                                background_color: 1, 1, 1, 1
                                halign: "center"
                                font_size: "18sp"     

                            MDLabel:
                                text: "meta"
                                theme_text_color: "Custom"
                                bold: True  
                                font_size: "16sp" 
                                text_color: 1, 1, 1, 1
                            MDTextField:
                                id: meta
                                theme_text_color: "Custom"
                                text_color: 0, 0, 0, 1
                                font_style: "H6"
                                bold: True
                                max_text_length: 10
                                mode: "round"
                                multiline: False
                                font_color: 0, 0, 0, 1
                                background_color: 1, 1, 1, 1
                                halign: "center"
                                font_size: "18sp"   

                            MDLabel:
                                text: "GREENS"
                                theme_text_color: "Custom"
                                bold: True 
                                font_size: "16sp"    
                                text_color: 1, 1, 1, 1
                            MDTextField:
                                id: GREEN
                                theme_text_color: "Custom"
                                text_color: 0, 1, 0, 1  # Verde
                                font_style: "H6"
                                bold: True
                                max_text_length: 10
                                mode: "round"
                                multiline: False
                                font_color: 0, 0, 0, 1
                                background_color: 1, 1, 1, 1
                                halign: "center"
                                font_size: "18sp"

                FloatLayout:
                    BoxLayout:

                        canvas.before:
                            Color:
                                rgba: 1, 0, 0, 1  # Define a cor da borda como vermelho
                            Line:
                                width: 2.  # Define a espessura da borda
                                rectangle: (self.x, self.y, self.width, self.height)

                        orientation: 'vertical'
                        size_hint: (.7, .8)
                        pos_hint: {"center_x": 0.6, "center_y": .5}
                        spacing: 20

                        MDLabel:
                            text: "BANCA ATUAL"
                            theme_text_color: "Custom"
                            bold: True 
                            font_size: "18sp"
                            halign: "center"
                            text_color: 1, 1, 1, 1
                        MDTextField:
                            id: banca_atual
                            text: app.balance  # Vincule a propriedade balance ao texto
                            max_text_length: 10
                            mode: "round"
                            multiline: False
                            font_color: 0, 0, 0, 1
                            background_color: 1, 1, 1, 1
                            halign: "center"
                            font_size: "18sp" 

                        MDLabel:
                            text: "VALOR DA APOSTA"
                            theme_text_color: "Custom"
                            bold: True 
                            font_size: "18sp"
                            halign: "center"
                            text_color: 1, 1, 1, 1
                        MDTextField:
                            id: valor
                            max_text_length: 10
                            mode: "round"
                            multiline: False
                            font_color: 0, 0, 0, 1
                            background_color: 1, 1, 1, 1
                            halign: "center"
                            font_size: "18sp" 

                        MDLabel:
                            text: "G1"
                            theme_text_color: "Error"
                            bold: True 
                            font_size: "18sp"
                            halign: "center"
                            font_color: 1, 1, 1, 1

                    BoxLayout:
                        canvas.before:
                                    
                        orientation: 'horizontal'
                        size_hint: (.7, .8)
                        pos_hint: {"center_x": 0.6, "center_y": .5}
                        spacing: 20
                        MDRectangleFlatButton:
                            id: INICIAR_APOSTA  # Add this line
                            text: "Iniciar"
                            on_release: app.start_bet()  # Vinculando o botão à função start_bet
                            pos_hint: {"center_x": 0.5}
                            halign: "center"
                            md_bg_color: 1, 0, 0, 1  # Vermelho
                            elevation: 20
                            font_color: 1, 1, 1, 1
                            text_color: 1, 1, 1, 1
                            bold: True 
                        MDRaisedButton:
                            id: INICIAR_PROGRAMA  # Add this line
                            text:'Aposta'
                            on_release: app.start_and_place_bet()
                            pos_hint: {"center_x": 0.5}
                            halign: "center"
                            md_bg_color: 1, 0, 0, 1  # Vermelho
                            elevation: 10
                            font_color: 1, 1, 1, 1
                            text_color: 1, 1, 1, 1
                            bold: True 
                            #pos_hint: {"center_x": 0.5, "center_y": .1}
                            disabled: True  # Inicialmente, o botão estará desativado
                            md_bg_color: app.theme_cls.primary_color  # A cor de fundo do botão será a cor primária por padrão
                        MDRaisedButton:
                            id: FECHAR  # Add this line
                            text: 'Fechar'
                            on_release: app.stop()  # Parar a aplicação
                            pos_hint: {"center_x": 0.7}
                            halign: "center"
                            md_bg_color: 1, 0, 0, 1  # Vermelho
                            elevation: 10
                            font_color: 1, 1, 1, 1
                            text_color: 1, 1, 1, 1
                            bold: True 
                            
                            
            BoxLayout:
                canvas.before:
                    Color:
                        rgba: 1, 0, 0, 1  # Define a cor da borda como vermelho
                    Line:
                        width: 1.  # Define a espessura da borda
                        rectangle: (self.x, self.y, self.width, self.height)
                size_hint_y: 0.5
                canvas.before:
                    Color:
                        rgba: 1, 0, 0, 1  # Define a cor da borda como vermelho
                    Line:
                        width: 1.  # Define a espessura da borda
                        rectangle: (self.x, self.y, self.width, self.height)
                GridLayout:
                    id: grid_layout
                    cols: 25
                    rows: 8


'''


class CustomButton(Button):
    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.background_color = [1, 1, 1, 1]
class TimeButton(Button):
    def __init__(self, **kwargs):
        super(TimeButton, self).__init__(**kwargs)
        self.size_hint_y = 0.3  # Aqui foi alterado para size_hint_y
        self.background_color = [0, 0, 0, 1]
        self.font_size = '12sp'
        self.bold = True



class MainApp(MDApp):
    balance = StringProperty("0.00")  # Inicializando o balance como um atributo da classe

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Blaze = None
        #Clock.schedule_interval(self.update_balance, 5)  # atualiza o saldo a cada 5 segundos
        self.apostou = False  # adicionando uma nova variável de controle para saber quando a aposta foi feita
        self.monitorando = False  # Atributo monitorando definido aqui

    def monitor_game_status(self, dt):
        if self.Blaze is None:
            return

        confirm_button_xpath = '//*[@id="roulette-controller"]/div[1]/div[3]/button'
        button_text = self.Blaze.driver.find_element(By.XPATH, confirm_button_xpath).text

        print(self.root.ids)  # Add this line to check the contents of self.root.ids

        if 'INICIAR_PROGRAMA' in self.root.ids:  # Check if 'iniciar_programa' is in self.root.ids before accessing it
            start_button = self.root.ids.INICIAR_PROGRAMA
            if button_text == "Começar o jogo":
                start_button.disabled = False
                start_button.md_bg_color = [1, 0, 0, 1]  # Vermelho
                print(button_text)
            else:
                start_button.disabled = True
                start_button.md_bg_color = [0.5, 0.5, 0.5, 1]  # Cinza
            #return False  # Para interromper a chamada de retorno de chamada programada

    def verificar_ganho(self, dt):
        if self.monitorando and self.apostou:  # só entra aqui se tiver monitorando e a aposta tiver sido feita
            try:
                with open(r'D:\BLAZE\BLAZE\Resultados\Resultados.txt', 'r') as f:
                    dados_string = f.read().strip()
                    dados = ast.literal_eval(dados_string)
                    dados = [int(num) for num in dados]
                    confirm_button_xpath = '//*[@id="roulette-controller"]/div[1]/div[3]/button'
                    button_text = self.Blaze.driver.find_element(By.XPATH, confirm_button_xpath).text

                    if button_text == 'Esperando':  # verifica se a aposta foi realizada
                        self.apostou = False  # para de verificar a aposta
                        greens = self.root.ids.GREEN
                        if dados[0] == 0:
                            greens.text = 'GREEN'
                        else:
                            greens.text = 'LOSS'
            except (FileNotFoundError, ValueError, NoSuchElementException):
                return

    def build(self):
        Window.bind(on_resize=self.on_window_resize)
        self.root = Builder.load_string(kv)
        self.create_button_pairs()
        self.load_excel_data()  # Load data from Excel
        self.root.ids['INICIAR_APOSTA'].bind(on_press=self.start_bet)  # Add this line
        Clock.schedule_interval(self.atualizar_botoes, 1)  # Atualizar os botões a cada segundo
        Clock.schedule_interval(self.monitor_game_status, 1)  # Schedule monitor_game_status to be called every second
        Clock.schedule_interval(self.verificar_ganho, 1)
        return self.root


    def on_window_resize(self, window, width, height):
        # Este método será chamado sempre que a janela for redimensionada
        print(f'Window resized to: {width}, {height}')

    def load_excel_data(self):
        df = pd.read_excel(r'D:\Downloads\Gerenciamento Invictus LIVE.xlsx')

        banca = df.iloc[10, 1]  # Get value at B12
        entrada = df.iloc[9, 1]  # Get value at B11
        meta = df.iloc[11, 1]  # Get value at B13

        # Formatando os valores
        banca = "{:.2f}".format(banca)
        entrada = "{:.2f}".format(entrada)
        meta = int(meta)  # Converte para inteiro

        self.root.ids.banca.text = str(banca)
        self.root.ids.entrada.text = str(entrada)
        self.root.ids.meta.text = str(meta)

    def create_button_pairs(self):
        grid_layout = self.root.ids.grid_layout
        for i in range(200):
            # num = str(random.randint(0,14))  # Comentei esta linha
            button_text = ""  # Texto do botão vazio
            button = CustomButton(text=button_text, bold=True)
            # Configuração das cores iniciais. Você pode ajustá-las conforme necessário.
            button.background_color = [1, 1, 1, 1]  # Background branco
            button.color = [1, 1, 1, 1]  # Texto preto

            button.bind(pos=self.update_rect, size=self.update_rect)

            time_button = TimeButton(text="00:00")
            time_button.bind(pos=self.update_rect, size=self.update_rect)

            pair_layout = BoxLayout(orientation='vertical')
            pair_layout.add_widget(button)
            pair_layout.add_widget(time_button)

            grid_layout.add_widget(pair_layout)

    def update_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(1, 1, 1, 1)  # Borda cinza
            Line(width=1, rectangle=(instance.x, instance.y, instance.width, instance.height))



    def start_bet(self, instance=None):
        if self.Blaze is None:
            self.Blaze = Bot()
            self.Blaze.Start()
            self.Blaze.Login("toislessa5@gmail.com", "Perola2010@")

            if self.Blaze:
                balance = self.Blaze.Get_Balance()
                self.balance = str(balance)  # Atualize a propriedade balance
                print("Balance updated")
                self.monitorando = True
                self.apostou = True  # indica que a aposta foi realizada

    def place_bet(self, instance=None):
        if self.Blaze:
            # Obtem o valor de aposta do campo de texto
            bet_value = self.root.ids.valor.text

            bet_input_xpath = '//*[@id="roulette-controller"]/div[1]/div[2]/div[1]/div/div[1]/input'
            bet_button_xpath = '//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[2]'
            confirm_button_xpath = '//*[@id="roulette-controller"]/div[1]/div[3]/button'

            # Encontra o campo de entrada de aposta, limpa e insere o valor de aposta
            bet_input = self.Blaze.driver.find_element(By.XPATH, bet_input_xpath)
            bet_input.clear()
            bet_input.send_keys(bet_value)

            # Clica no botão de aposta e depois no botão de confirmação
            bet_button = self.Blaze.driver.find_element(By.XPATH, bet_button_xpath)
            bet_button.click()
            confirm_button = self.Blaze.driver.find_element(By.XPATH, confirm_button_xpath)
            confirm_button.click()

            print("Bet placed")

            # Pausa a execução do script por 2 segundos
            time.sleep(2)
            # Atualiza o saldo após a aposta
            self.update_balance()

    def start_and_place_bet(self, instance=None):
        self.start_bet()
        self.place_bet()


    def update_balance(self, dt=None):  # dt é o tempo desde a última chamada
        if self.Blaze:
            balance = self.Blaze.Get_Balance()
            self.balance = str(balance)

    def on_balance(self, instance, value):
        print('Balance updated to', value)

    def start_bot(self, instance=None):
        if self.Blaze is None:
            self.Blaze = BlazeBot()  # Substitua "BlazeBot" pelo nome real da sua classe bot
            self.update_balance()

    def stop_bet(self, instance):  # Adicionado instance
        if self.Blaze:
            self.Blaze.Stop()
            self.Blaze = None

    def atualizar_botoes(self, *args):
        try:
            with open(r'D:\BLAZE\BLAZE\Resultados\Resultados.txt', 'r') as f:
                dados_string = f.read().strip()
        except FileNotFoundError:
            return  # O arquivo ainda não foi criado, então apenas ignore o erro

        # Tente converter a string de volta para uma lista
        try:
            dados = ast.literal_eval(dados_string)
        except ValueError as e:
            print(f"Erro ao converter string para lista: {e}")
            return  # Se houver um erro ao converter a string para uma lista, pare a execução do método aqui

        # Tente converter a lista de strings para uma lista de inteiros
        try:
            dados = [int(num) for num in dados]
        except ValueError as e:
            print(f"Erro na conversão para inteiro: {e}")
            return  # Se houver um erro na conversão para inteiros, pare a execução do método aqui

        grid_layout = self.root.ids.grid_layout

        for i, num in enumerate(dados):
            # Calcular a posição do botão com base no índice
            linha = i // 25
            coluna = i % 25

            # Calcular o índice do widget correspondente na lista de children do grid_layout
            widget_index = (7 - linha) * 25 + coluna  # Substitua 7 por qualquer número de linhas - 1
            button = grid_layout.children[widget_index].children[1]  # Ajuste o índice se necessário

            # Atualizar o texto e a cor do botão como antes
            button.text = str(num) if num != 0 else "0"
            if num == 0:
                button.background_color = [1, 1, 1, 1]  # Background branco
                button.color = [1, 0, 0, 1]  # Texto vermelho
            elif 1 <= num <= 7:
                button.background_color = [1, 0, 0, 1]  # Background vermelho
                button.color = [1, 1, 1, 1]  # Texto branco
            else:
                button.background_color = [0, 0, 0, 1]  # Background preto
                button.color = [1, 1, 1, 1]  # Texto branco

if __name__ == '__main__':
    MainApp().run()