from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.uix.button import Button

from salvar import read, add, clear
from engine import avaliar


class CalcButton(Button):
    pass

class CalculadoraScreen(Screen):
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
        if self.erro == True:
            self.lmp()

        if self.display[-1] in self.operadores and resp in self.operadores:
            return

        if self.display[-1] in self.operadores and resp == ")":
            return

        if self.display[-1] == "." and resp == ".":
            return

        if len(self.display) == 1 and self.display[0] == "0" and resp == "(":
            self.display = "("
            return

        if self.display[-1] not in self.operadores and resp == "(":
            if self.display[-1] != "(" and resp == "(":
                self.display += "x"
                self.display += "("
                return
        
        if resp == ")":
            rptc_dspl = Counter(self.display)
            rptc_abr_prts = rptc_dspl["("]
            rptc_fch_prts = rptc_dspl[")"]
            if rptc_abr_prts - rptc_fch_prts <= 0:
                return

        if resp in self.operadores and self.display[-1] == "(":
            return

        if resp == "." and self.display[-1] != ".":
            self.display += str(resp)
            return

        if resp == "=":
            if self.display != "0":
                add('historico.json', self.display)
                rstd, erro_avl = avaliar(self.display)

                self.erro = erro_avl
                
                self.display = rstd
                self.ult_btn = "="
                return
            else:
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

    def rem(self):
        self.display = self.display[:-1]

        if len(self.display) == 0:
            self.display = '0'


    def lmp(self):
        self.display = "0"
        self.erro = False


class HistoricoScreen(Screen):
    def abrir(self):
        self.ids.lista.data = [
            {
                "text":
                expr,
                "on_press": lambda x=expr: self.carregar(x)
            }
            for expr in read("historico.json")
        ]
    def carregar(self, expr):
        self.manager.current = "calc"
        calc = self.manager.get_screen("calc")
        calc.display = expr

    def limpar(self):
        clear("historico.json")
        self.abrir()

class Root(ScreenManager):
    pass


kv = Builder.load_file("calculadora.kv")

class CalculadoraApp(App):
    def build(self):
        return kv
        
CalculadoraApp().run()