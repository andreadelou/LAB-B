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