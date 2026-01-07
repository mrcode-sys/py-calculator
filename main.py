from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import StringProperty, BooleanProperty, ListProperty

class Calculadora(BoxLayout):
    erro = BooleanProperty(False)
    display = StringProperty('0')
    rstd_c = ListProperty([1, 1, 1, 1])
    ult_btn = None
    def on_erro(self, instance, valor):
        if valor == False:
            self.rstd_c = [1, 1, 1, 1]
        else:
            self.rstd_c = [1, 0, 0, 1]

    def form(self, resp):
        if self.ult_btn == "=":
            self.lmp()

        self.ult_btn = resp

        if resp == "=":
            self.brain()
            return

        if self.display == '0':
            self.display = str(resp)

        else:
            self.display += str(resp)

        if not isinstance(resp, str):
            pass
    
    def calc(self, n1, exp, n2):
        if exp == '+':
            rstd = n1 + n2

        elif exp == '-':
            rstd = n1 - n2

        elif exp == 'x':
            rstd = n1 * n2

        elif exp == '/':
            rstd = n1 / n2

        return rstd


    def brain(self):
        rstd = None
        if self.display != '0':

            form = [0]
            countbox = list(self.display)
            mult_sub = []

            prox_num = False
            for character in countbox:
                try:
                    num = int(character)

                    if prox_num:
                        form.append(num)
                        prox_num = False
                        continue
                    if form:
                        form[-1] = str(int(form[-1])) + str(num)
                        form[-1] = int(form[-1])

                    else:
                        form.append(num)

                except ValueError:
                    if prox_num == False:
                        exp = character
                        prox_num = True
                        form.append(exp)
                        
            if isinstance(form[-1], str):
                self.lmp()
                return
            if 'x' in form or '/' in form:

                ind = 0

                for character in form:

                    if character == '/' or character == 'x':
                        mult_sub.insert(-1, ind)

                    ind += 1

            if mult_sub:
                for character in mult_sub:
                    num1 = form[character - 1]
                    num2 = form[character + 1]
                    expr = form[character]
                    rstd = self.calc(num1, expr, num2)

                    form.pop(character + 1)
                    form.pop(character)
                    form[character - 1] = rstd
            
            num1 = None
            expr = None
            num2 = None
            print(form)
            while len(form) > 1:
                ind = 0
                if not num1:
                    num1 = form[ind]
                    ind += 1

                if not expr:
                    expr = form[ind]
                    ind += 1

                if not num2:
                    num2 = form[ind]

                rstd = self.calc(num1, expr, num2)

                form.pop(2)
                form.pop(1)

                form[0] = rstd

                num1 = None
                num2 = None
                expr = None

            self.display = str(form[0])

    def lmp(self):
        self.display = "0"
        self.erro = False

class CalculadoraApp(App):
    def build(self):
        return Calculadora()
CalculadoraApp().run()
