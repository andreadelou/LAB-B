from graphviz import Digraph


class AFN:
    def __init__(self, e0, ef, estados, simbolos, transiciones):
        self.e0 = e0
        self.ef = ef
        self.estados = estados
        self.simbolos = simbolos
        self.transiciones = transiciones
        self.afd_estados = []
        self.afd_transiciones = []

    def cerradura_epsilon(self, estados):
        
        resultado = estados.copy()
        pila = estados.copy()
        while pila:
            actual = pila.pop()
            epsilon_transiciones = [
                t[2] for t in self.transiciones if t[0] == actual and t[1] == "ε"]
            for e in epsilon_transiciones:
                if e not in resultado:
                    resultado.append(e)
                    pila.append(e)
        return resultado

    def mover(self, estados, simbolo): #Obtiene estados alcanzados
        resultado = []
        for estado in estados:
            simbolo_transiciones = [
                t[2] for t in self.transiciones if t[0] == estado and t[1] == simbolo]
            resultado.extend(simbolo_transiciones)
        return resultado

    def construir_afd(self):
        e0_cerradura = self.cerradura_epsilon([self.e0])
        self.afd_estados.append(e0_cerradura)
        cola = [e0_cerradura]
        while cola:
            actual = cola.pop(0)
            for simbolo in self.simbolos:
                alcanzables = (self.cerradura_epsilon(
                    self.mover(actual, simbolo)))
                if alcanzables not in self.afd_estados and simbolo != "ε":
                    self.afd_estados.append(alcanzables)
                    self.afd_transiciones.append((self.afd_estados.index(
                        actual), simbolo, self.afd_estados.index(alcanzables)))
                    cola.append(alcanzables)
                elif alcanzables in self.afd_estados and len(self.mover(actual, simbolo)) != 0 and simbolo != "ε":
                    self.afd_transiciones.append((self.afd_estados.index(
                        actual), simbolo, self.afd_estados.index(alcanzables)))

        dot = Digraph()
        for i, estado in enumerate(self.afd_estados):
            dot.node(str(i), label=str(chr(i+65)))
            if self.ef in estado:
                dot.node(str(i), shape='doublecircle')
        for transicion in self.afd_transiciones:
            dot.edge(str(transicion[0]), str(
                transicion[2]), label=str(transicion[1]))
        dot.render('afd', format='png', view=True)

        estado_inicial = None
        self.e0_afd = None
        estados_finales = []
        self.ef_afd = []
        self.estados = []
        for i, estado in enumerate(self.afd_estados):
            if i == 0:
                estado_inicial = str(chr(i+65))
                self.e0_afd = i
            if self.ef in estado:
                estados_finales.append(str(chr(i+65)))
                self.ef_afd.append(i)
            self.estados.append(i)

        with open('afd.txt', 'a', encoding="utf-8") as f:
            f.write("AFD a partir de un AFN -->")
            f.write("\n")
            f.write("Símbolos: "+', '.join(self.simbolos))
            f.write("\n")
            f.write("Estados:  " + str(self.afd_estados))
            f.write("\n")
            f.write("Estado inicial: { " + str(estado_inicial) + " }")
            f.write("\n")
            f.write("Estados de aceptación: { " + str(estados_finales) + " }")
            f.write("\n")
            f.write("Transiciones: " + str(self.afd_transiciones))
        
class Minimizar:
    def __init__(self, e0, ef, transiciones, estados):
        self.e0 = e0
        self.ef = ef
        self.transiciones = transiciones
        self.estados = estados
        self.grupos = []

    def minimizar(self, filename):
        self.initialize_groups()
        self.split_groups()
        self.graficar(self.build_new_afd(), filename)
        self.escribir(filename)

    def initialize_groups(self):
        no_final = [x for x in self.estados if x not in self.ef]
        self.grupos = [no_final, self.ef]

    def split_groups(self):
        while True:
            new_groups = []
            for group in self.grupos:
                if len(group) == 1:
                    new_groups.append(group)
                    continue
                grouped_by_transitions = {}
                for state in group:
                    transition_key = self.get_transition_key(state)
                    if transition_key in grouped_by_transitions:
                        grouped_by_transitions[transition_key].append(state)
                    else:
                        grouped_by_transitions[transition_key] = [state]
                new_groups.extend(grouped_by_transitions.values())
            if new_groups == self.grupos:
                break
            self.grupos = new_groups

    def get_transition_key(self, state):
        transition_key = []
        for symbol in self.get_symbols():
            next_state = self.get_next_state(state, symbol)
            for i, group in enumerate(self.grupos):
                if next_state in group:
                    transition_key.append(i)
                    break
        return tuple(transition_key)

    def get_symbols(self):
        symbols = set()
        for transition in self.transiciones:
            symbols.add(transition[1])
        return symbols

    def get_next_state(self, state, symbol):
        for transition in self.transiciones:
            if transition[0] == state and transition[1] == symbol:
                return transition[2]
        return None

    def build_new_afd(self):
        self.new_states = [str(i) for i in range(len(self.grupos))]
        new_e0 = self.get_new_initial_state()
        new_ef = self.get_new_final_states()
        new_transitions = self.get_new_transitions()
        return Minimizar(new_e0, new_ef, new_transitions, self.new_states)

    def get_new_initial_state(self):
        for i, group in enumerate(self.grupos):
            if self.e0 in group:
                return str(i)
        return None

    def get_new_final_states(self):
        new_ef = []
        for i, group in enumerate(self.grupos):
            for state in group:
                if state in self.ef:
                    new_ef.append(str(i))
                    break
        return new_ef

    def get_new_transitions(self):
        new_transitions = []
        for i, group in enumerate(self.grupos):
            for symbol in self.get_symbols():
                next_state = self.get_next_state(group[0], symbol)
                for j, other_group in enumerate(self.grupos):
                    if next_state in other_group:
                        new_transitions.append([str(i), symbol, str(j)])
                        break
        return new_transitions

    def graficar(self, minimizador_afd, filename):
        graph = Digraph()
        graph.attr(rankdir='LR')

        # Agregar estados
        for estado in minimizador_afd.estados:
            if estado in minimizador_afd.ef:
                graph.node(estado, shape='doublecircle')
            else:
                graph.node(estado, shape='circle')

        # Agregar transiciones
        for transicion in minimizador_afd.transiciones:
            graph.edge(transicion[0], transicion[2], label=transicion[1])

        graph.render(filename, format='png', view=True)

    def escribir(self, filename):
        with open(filename+'.txt', 'a', encoding="utf-8") as f:
            f.write("AFD Minimizado a partir de un AFD generado por AFN -->")
            f.write("\n")
            f.write("Estados:  " + str(self.new_states))
            f.write("\n")
            f.write("Estado inicial: { " +
                    str(self.get_new_initial_state()) + " }")
            f.write("\n")
            f.write(
                "Estados de aceptación: { " + str(self.get_new_final_states()) + " }")
            f.write("\n")
            f.write("Transiciones: " + str(self.get_new_transitions()))

    def simular_cadena(self, cadena):
        current_state = self.e0
        for symbol in cadena:
            next_state = self.get_next_state(current_state, symbol)
            if next_state is None:
                return False
            current_state = next_state
        if current_state in self.ef:
            return True
        else:
            return False