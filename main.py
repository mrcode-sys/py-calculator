from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import StringProperty, BooleanProperty, ListProperty

class CalcButton(Button):
    pass

class Calculadora(BoxLayout):

    buttons = [
        "C", "(", ")", "<-",
        "7", "8", "9", "+",
        "4", "5", "6", "-",
        "1", "2", "3", "x",
        ".", "0", "=", "/",

    ]
    operadores = ['+','-','x','/']

    erro = BooleanProperty(False)
    display = StringProperty('0')
    rstd_c = ListProperty([1, 1, 1, 1])
    ult_btn = None

    ult_num = None
    ult_expr = None

    def on_kv_post(self, base_widget):
        grid = self.ids.grid_btn

        for txt in self.buttons:
            btn = CalcButton(text = txt)
            btn.bind(on_press=self.btnTxtForm)
            
            if txt == "=":
                btn.font_size = 24
                btn.color = [0.3, 0.3, 1, 1]

            elif txt == "C":
                btn.color = [1, 0.8, 0, 1]
            
            elif txt == "<-":
                btn.color = [1, 0.3, 0.3, 1]

            grid.add_widget(btn)

    def on_erro(self, instance, valor):
        if valor == False:
            self.rstd_c = [1, 1, 1, 1]
        else:
            self.rstd_c = [1, 0, 0, 1]
    
    def btnTxtForm(self, btn):
        self.form(btn.text)

    def form(self, resp):

        if self.display[-1] in self.operadores and resp in self.operadores:
            return

        if self.display[-1] in self.operadores and resp == ")":
            return

        if self.display[-1] not in self.operadores and resp == "(":
            if self.display[-1] != "(" and resp == "(":
                return

        if resp == "=":
            self.brain()
            self.ult_btn = resp
            return

        else:
            self.ult_btn = resp

        if resp == "C":
            self.lmp()
            return
        elif resp == "<-":
            self.rem()
            return


        if self.display == '0':
            self.display = str(resp)

        else:
            self.display += str(resp)
        
    def calc(self, n1, exp, n2):
        self.ult_num = n2
        self.ult_expr = exp

        if exp == '+':
            rstd = n1 + n2

        elif exp == '-':
            rstd = n1 - n2

        elif exp == 'x':
            rstd = n1 * n2

        elif exp == '/':
            if n2 != 0:
                rstd = n1 / n2
            else:
                self.display = "Err"
                return False

        return rstd

    def rem(self):
        self.display = self.display[:-1]

        if len(self.display) == 0:
            self.display = '0'

    def brain(self):
        rstd = None
        if self.display != '0':

            form = []
            countbox = list(self.display)
            mult_sub = []

            if self.ult_btn == '=':
                rstd = self.calc(float(self.display), self.ult_expr, self.ult_num)

            for character in countbox:
                if not character in self.operadores and character != "(" and character != ")":

                    if not form:
                        form.append(character)
                        continue

                    if not form[-1].isnumeric():
                        form.append(character)
                        continue

                    if form:
                        form[-1] = form[-1] + character


                else:
                    if character != "(" and character != ")":

                        float_number = False
                        ind_flt = -1
                        if form:
                            while not float_number:
                                try:
                                    form[-1] = float(form[ind_flt])
                                    float_number = True

                                except ValueError:
                                    ind_flt -= 1

                    exp = character
                    form.append(exp)

            if len(form) <= 2:
                print(form)
                if form[0] in self.operadores:
                    self.display = form[-1]
                return

            ult_num = False
            ind_ult_num = -1
            while ult_num != True:
                if form[ind_ult_num] == ")":
                    ind_ult_num -= 1

                elif not form[ind_ult_num] in self.operadores:
                    form[ind_ult_num] = float(form[ind_ult_num])
                    ult_num = True

            if isinstance(form[-1], str) and form[-1] != ")":
                self.lmp()
                return

            run = False

            inic_prts = []
            fim_prts = []

            ind_prts = 0
            if "(" in form or ")" in form:
                for character in form:
                    if character == "(":
                        inic_prts.append(ind_prts)

                    if character == ")":
                        fim_prts.append(ind_prts)

                    ind_prts += 1

                if len(fim_prts) != len(inic_prts):
                    prts_adic = len(inic_prts) - len(fim_prts)

                    while prts_adic > 0:
                        fim_prts.append(len(form))

                        form.append(")")
                        prts_adic -= 1
                    
                if inic_prts and fim_prts:
                    while len(fim_prts) > 0:
#                        inic_prts[-1] += 1 não sei para que era usado
                        if inic_prts[-1] != fim_prts[-1]:

                            if 'x' in form[inic_prts[-1]:fim_prts[-1]] or '/' in form[inic_prts[-1]:fim_prts[-1]]:
                                ind1 = inic_prts[-1]
                                
                                for character in form[inic_prts[-1]:fim_prts[-1]]:
                                    if not character == "(" and not character == ")":
                                        if character == '/' or character == 'x':
                                            mult_sub.insert(-1, ind1)

                                    ind1 += 1

                            if mult_sub:
                                for character in mult_sub:
                                    num1 = form[character - 1]
                                    num2 = form[character + 1]
                                    expr = form[character]


                                    rstd = self.calc(num1, expr, num2)

                                    if rstd == False:
                                        return

                                    form.pop(character + 1)
                                    form.pop(character)
                                    form[character - 1] = rstd

                                    fim_prts[-1] -= 2
                            
                            num1 = None
                            expr = None
                            num2 = None
                            print(form[inic_prts[-1]:fim_prts[-1]])
                            print(inic_prts[-1])
                            print(fim_prts[-1])
                            
                            while len(form[inic_prts[-1]:fim_prts[-1]]) > 1:
    
                                if 'x' in form[inic_prts[-1]:fim_prts[-1]] or '/' in form[inic_prts[-1]:fim_prts[-1]]:
                                    ind1 = inic_prts[-1]
                                    
                                    for character in form[inic_prts[-1]:fim_prts[-1]]:
                                        if not character == "(" and not character == ")":
                                            if character == '/' or character == 'x':
                                                mult_sub.insert(-1, ind1)

                                        ind1 += 1

                                if mult_sub:
                                    for character in mult_sub:
                                        num1_m_s = form[character - 1]
                                        num2_m_s = form[character + 1]
                                        expr_m_s = form[character]


                                        rstd = self.calc(num1_m_s, expr_m_s, num2_m_s)

                                        if rstd == False:
                                            return

                                        form.pop(character + 1)
                                        form.pop(character)
                                        form[character - 1] = rstd

                                        fim_prts[-1] -= 2

                                ind = inic_prts[-1] + 1
                                print(ind)
                                print(form[inic_prts[-1]:fim_prts[-1]])
                                print(form[ind])
                                print(form[ind+2])
                                if form[ind-1] != "(" and form[ind + 1]!= ")":
                                    if not num1:
                                        num1 = form[ind]
                                        ind += 1
                                        print(num1)
                                    if not expr:
                                        expr = form[ind]
                                        ind += 1
                                        print(expr)
                                    if not num2:
                                        num2 = form[ind]
                                        print(num2)

                                    rstd = self.calc(num1, expr, num2)

                                    form.pop(ind)
                                    form.pop(ind - 1)
                                    print(form)
                                    print(inic_prts)
                                    print(fim_prts)
                                    fim_prts[-1] -= 2

                                    form[ind - 2] = rstd

                                    num1 = None
                                    num2 = None
                                    expr = None
                                print(form)
                                print(inic_prts)
                                print(fim_prts)

                
                                form.pop(inic_prts[-1])
                                if fim_prts[-1] < len(form):
                                    form.pop(fim_prts[-1] -1)
                                    fim_prts.pop(-1)

                                else:

                                    ind_prts_fim = 0
                                    continuar_while = True

                                    while continuar_while == True:
                                        ind_prts_fim += 1
                                        print(ind_prts_fim)
                                        if ind_prts_fim > 40:
                                            return
                                        if fim_prts[-1] - ind_prts_fim < len(form) and form[fim_prts[-1] -ind_prts_fim] == ')':
                                            form.pop(fim_prts[-1] - ind_prts_fim)
                                            fim_prts.pop(-1)
                                            continuar_while = False

                                inic_prts.pop(-1)
                                print(fim_prts)
                                print(inic_prts)
                                print(form)

                                if not inic_prts and not fim_prts:
                                    break

                ind = 0
                mult_sub = []

            if 'x' in form or '/' in form:

                ind1 = 0

                for character in form:

                    if character == '/' or character == 'x':
                        mult_sub.insert(-1, ind1)

                    ind1 += 1

            if mult_sub:
                for character in mult_sub:
                    num1 = form[character - 1]
                    num2 = form[character + 1]
                    expr = form[character]

                    rstd = self.calc(num1, expr, num2)
                    if rstd == False:
                        return

                    form.pop(character + 1)
                    form.pop(character)
                    form[character - 1] = rstd
            
            num1 = None
            expr = None
            num2 = None

            while len(form) > 2:
                ind = 0
                if not num1:
                    num1 = form[ind]
                    ind += 1

                if not expr:
                    expr = form[ind]
                    ind += 1

                if not num2:

                    num2 = form[ind]
                print(form)

                rstd = self.calc(num1, expr, num2)

                form.pop(2)
                form.pop(1)

                form[0] = rstd

                if form[-1] in self.operadores:
                    form.pop(-1)

                num1 = None
                num2 = None
                expr = None

            form[0] = rstd

            if form[0].is_integer():
                self.display = str(int(form[0]))

            else:
                self.display = str(form[0])

    def lmp(self):
        self.display = "0"
        self.erro = False

class CalculadoraApp(App):
    def build(self):
        return Calculadora()
CalculadoraApp().run()