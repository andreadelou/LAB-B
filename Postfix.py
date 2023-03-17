from re import S
import pandas as pd
from graphviz import Digraph

class convertExpression:
    # Constructor to initialize the class variables
    def __init__(self, longitud):
        self.top = -1
        self.longitud = longitud
        # This array is used a stack
        self.array = []
        # precedencia setting
        self.precedencia = {'|': 1, '.': 1, '*': 2,'+':2,'?':2}
        # Aqui se almacena el resultado final
        self.output = []
        self.res = ""

    # funcion para añadir puntos
    def addPuntos(self, regex):
        simbolos = [".", "|", "*", "(", ")","+","?"]
        length = len(regex)
        new_regex = []
        for i in range(length-1):
            new_regex.append(regex[i])
            if regex[i] not in simbolos:
                if regex[i+1] not in simbolos or regex[i+1] == '(':
                    new_regex += "."
            if regex[i] == ")" and regex[i+1] == "(":
                new_regex += "."
            if regex[i] == "*" and regex[i+1] == "(":
                new_regex += "."
            if regex[i] == "?" and regex[i+1] == "(": #se agrega ya que al funcionar como el kleene, hay que tratarlo de la misma manera
                new_regex += "."
            if regex[i] == ")" and regex[i+1] not in simbolos:
                new_regex += "."
            if regex[i] == "*" and regex[i+1] not in simbolos:
                new_regex += "."
            if regex[i] == "+" and regex[i+1] not in simbolos:
                new_regex += "."
            if regex[i] == "?" and regex[i+1] not in simbolos:
                new_regex += "."
        new_regex += regex[length-1]

        return "".join(new_regex)

    # revisar un stack de operaciones

    def vacio(self):
        return True if self.top == -1 else False

    # FUNCIONES DE peek, pop y push
    # retornar el valor al tope del stack
    def peek(self):
        try:
            return self.array[-1]
        except:
            pass

    # pop del stack
    def pop(self):
        if not self.vacio():
            self.top -= 1
            return self.array.pop()
        else:
            return "$"

    # Push del elemento al stack
    def push(self, op):
        self.top += 1
        self.array.append(op)

    # Funcion para chequear si es un operando/letra
    def operando(self, caracter):
        if(caracter.isalpha() or caracter == "ε" or caracter.isnumeric()):
            return True
        else:
            return False

    # Se chequea la procedencia del operador para verificar su posicion en el stack
    def revision(self, i):
        try:
            a = self.precedencia[i]
            b = self.precedencia[self.peek()]
            return True if a <= b else False
        except KeyError:
            return False
    
    def revision2(self, exp):
        bandera = 0
        
        for caracter in exp:
            if caracter == '(' :
                bandera = bandera + 1
            if caracter == ')' :
                bandera = bandera - 1
                if bandera < 0:
                    return False
                
        return bandera ==0
                
        
            
        
     # Funcion principal que retorna la expresion regular a postfix
    def RegexToPostfix(self, exp): 
        
        self.verificar = self.revision2(exp)
        
        if self.verificar == True:
            
            exp = self.addPuntos(exp)
            # se itera sobre cada caracter de la expresion
            for i in exp:

                # si el caracter es un operando/letra, añadirlo al output
                if self.operando(i):
                    if self.peek() == "*":
                        self.output.append(self.pop())
                    self.output.append(i)

                # si es un "(" se manda al stack
                elif i == '(':
                    self.push(i)

                # si es un ")" sacar todo del stack
                elif i == ')':
                    while((not self.vacio()) and
                        self.peek() != '('):
                        a = self.pop()
                        self.output.append(a)
                    if (not self.vacio() and self.peek() != '('):
                        return -1
                    else:
                        self.pop()

                # cuando se encuentra un operador
                else:
                    while(not self.vacio() and self.revision(i)):
                        self.output.append(self.pop())
                    self.push(i)

            # sacar todos los operadores del stack
            while not self.vacio():
                self.output.append(self.pop())

            self.res = "".join(self.output)
            
        else:
            print("Uso incorrecto de parentesis")
            
from re import S
import pandas as pd
from graphviz import Digraph


class PostifixToAFN():
    def __init__(self, postfix):
        self.postfix = postfix
        self.estados = []
        self.estados_list = []
        self.e0 = None
        self.ef = None
        self.transiciones = []
        self.transiciones_splited = []
        self.simbolos = []
        self.afn_final = []
        self.error = False

    def graficar(self, nombre):
        dot = Digraph()
        for i in range(len(self.estados)):
            if self.estados[i] == self.ef:
                dot.node(str(self.estados[i]), shape="doublecircle")
            else:
                dot.node(str(self.estados[i]), shape="circle")
        for transicion in self.transiciones_splited:
            if transicion[1] == "ε":
                dot.edge(str(transicion[0]), str(transicion[2]), label="ε")
            else:
                dot.edge(str(transicion[0]), str(
                    transicion[2]), label=transicion[1])
        dot.render(nombre, format='png', view=True)

    def operando(self, caracter):
        if(caracter.isalpha() or caracter.isnumeric() or caracter == "ε"):
            return True
        else:
            return False

    def reemplazar_interrogacion(self):
        self.postfix = self.postfix.replace('?', 'ε?')

    def conversion(self):
        print("\nPostfix: ", self.postfix)
        self.reemplazar_interrogacion()
        simbolos = []
        postfix = self.postfix
        for i in postfix:
            if self.operando(i):
                if i not in simbolos:
                    simbolos.append(i)

        self.simbolos = sorted(simbolos)

        stack = []
        start = 0
        end = 1

        counter = -1
        c1 = 0
        c2 = 0

        # implementation del algoritmo de thompson

        for i in postfix:
            # si es un simbolo
            if i in simbolos:
                counter = counter+1
                c1 = counter
                if c1 not in self.estados:
                    self.estados.append(c1)
                counter = counter+1
                c2 = counter
                if c2 not in self.estados:
                    self.estados.append(c2)
                self.afn_final.append({})
                self.afn_final.append({})
                stack.append([c1, c2])
                self.afn_final[c1][i] = c2
                self.transiciones_splited.append([c1, i, c2])
            # si es un kleene
            elif i == '*':
                try:
                    r1, r2 = stack.pop()
                    counter = counter+1
                    c1 = counter
                    if c1 not in self.estados:
                        self.estados.append(c1)
                    counter = counter+1
                    c2 = counter
                    if c2 not in self.estados:
                        self.estados.append(c2)
                    self.afn_final.append({})
                    self.afn_final.append({})
                    stack.append([c1, c2])
                    self.afn_final[r2]['ε'] = (r1, c2)
                    self.afn_final[c1]['ε'] = (r1, c2)
                    if start == r1:
                        start = c1
                    if end == r2:
                        end = c2
                    self.transiciones_splited.append([r2, "ε", r1])
                    self.transiciones_splited.append([r2, "ε", c2])
                    self.transiciones_splited.append([c1, "ε", r1])
                    self.transiciones_splited.append([c1, "ε", c2])
                except:
                    self.error = True
                    print("\nError sintaxis en * ")
            # si es una cerradura positiva
            elif i == '+':
                try:
                    r1, r2 = stack.pop()
                    counter = counter+1
                    c1 = counter
                    if c1 not in self.estados:
                        self.estados.append(c1)
                    counter = counter+1
                    c2 = counter
                    if c2 not in self.estados:
                        self.estados.append(c2)
                    self.afn_final.append({})
                    self.afn_final.append({})
                    stack.append([c1, c2])
                    self.afn_final[r2]['ε'] = (r1, c2)
                    if start == r1:
                        start = c1
                    if end == r2:
                        end = c2
                    self.transiciones_splited.append([r2, "ε", r1])
                    self.transiciones_splited.append([r2, "ε", c2])
                    self.transiciones_splited.append([c1, "ε", r1])
                except:
                    self.error = True
                    print("\nError sintaxis en + ")

            # si es una concatenacion
            elif i == '.':
                try:
                    r11, r12 = stack.pop()
                    r21, r22 = stack.pop()
                    stack.append([r21, r12])
                    self.afn_final[r22]['ε'] = r11
                    if start == r11:
                        start = r21
                    if end == r22:
                        end = r12
                    self.transiciones_splited.append([r22, "ε", r11])

                except:
                    self.error = True
                    print(
                        "\nSyntax error")
            # si es un or
            elif i == "|":
                try:
                    counter = counter+1
                    c1 = counter
                    if c1 not in self.estados:
                        self.estados.append(c1)
                    counter = counter+1
                    c2 = counter
                    if c2 not in self.estados:
                        self.estados.append(c2)
                    self.afn_final.append({})
                    self.afn_final.append({})

                    r11, r12 = stack.pop()
                    r21, r22 = stack.pop()
                    stack.append([c1, c2])
                    self.afn_final[c1]['ε'] = (r21, r11)
                    self.afn_final[r12]['ε'] = c2
                    self.afn_final[r22]['ε'] = c2
                    if start == r11 or start == r21:
                        start = c1
                    if end == r22 or end == r12:
                        end = c2
                    self.transiciones_splited.append([c1, "ε", r21])
                    self.transiciones_splited.append([c1, "ε", r11])
                    self.transiciones_splited.append([r12, "ε", c2])
                    self.transiciones_splited.append([r22, "ε", c2])
                except:
                    self.error = True
                    print("\nError sintaxis en | ")
            # si es un uno o cero ?
            elif i == "?":
                try:
                    counter = counter+1
                    c1 = counter
                    if c1 not in self.estados:
                        self.estados.append(c1)
                    counter = counter+1
                    c2 = counter
                    if c2 not in self.estados:
                        self.estados.append(c2)
                    self.afn_final.append({})
                    self.afn_final.append({})

                    r11, r12 = stack.pop()
                    r21, r22 = stack.pop()
                    stack.append([c1, c2])
                    self.afn_final[c1]['ε'] = (r21, r11)
                    self.afn_final[r12]['ε'] = c2
                    self.afn_final[r22]['ε'] = c2
                    if start == r11 or start == r21:
                        start = c1
                    if end == r22 or end == r12:
                        end = c2
                    self.transiciones_splited.append([c1, "ε", r21])
                    self.transiciones_splited.append([c1, "ε", r11])
                    self.transiciones_splited.append([r12, "ε", c2])
                    self.transiciones_splited.append([r22, "ε", c2])
                except:
                    print("Error sintaxis en ?")

        # asignacion de estados finales e iniciales
        self.e0 = start
        self.ef = end

        # Guardar variables para impresión
        df = pd.DataFrame(self.afn_final)
        string_afn = df.to_string()
        for i in range(len(self.transiciones_splited)):
            self.transiciones.append(
                "(" + str(self.transiciones_splited[i][0]) + " - " + str(self.transiciones_splited[i][1]) + " - " + str(self.transiciones_splited[i][2]) + ")")
        self.transiciones = ', '.join(self.transiciones)

        for i in range(len(self.estados)):
            if i == len(self.estados)-1:
                ef = i
            self.estados_list.append(str(self.estados[i]))
        self.estados_list = ", ".join(self.estados_list)

        if self.error == False:

            with open('afn.txt', 'a', encoding="utf-8") as f:
                f.write("AFN  a partir de la Expresión Regular -->")
                f.write("\n")
                f.write("Símbolos: "+', '.join(simbolos))
                f.write("\n")
                f.write("Estados:  " + str(self.estados_list))
                f.write("\n")
                f.write("Estado inicial: { " + str(self.e0) + " }")
                f.write("\n")
                f.write("Estados de aceptación: { " + str(self.ef) + " }")
                f.write("\n")
                f.write("Transiciones: " + str(self.transiciones))
                f.write("\n")
                f.write(string_afn)

            self.graficar('afn_grafico')  
        else:
            print("\nIngrese una expresión Regex válida")

    def cerradura_epsilon(self, estados):
        resultado = estados.copy()
        pila = estados.copy()
        while pila:
            actual = pila.pop()
            epsilon_transiciones = [
                t[2] for t in self.transiciones_splited if t[0] == actual and t[1] == "ε"]
            for e in epsilon_transiciones:
                if e not in resultado:
                    resultado.append(e)
                    pila.append(e)
        return resultado

    def simulacion(self, cadena):
        estados_actuales = self.cerradura_epsilon([self.e0])
        estados_finales = []
        for simbolo in cadena:
            nuevos_estados = []
            for estado in estados_actuales:
                for transicion in self.transiciones_splited:
                    if estado == transicion[0] and simbolo == transicion[1]:
                        nuevos_estados.append(transicion[2])
            if not nuevos_estados:
                return False
            estados_actuales = self.cerradura_epsilon(nuevos_estados)
        estados_finales = self.cerradura_epsilon(estados_actuales)
        return self.ef in estados_finales