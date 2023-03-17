from Postfix import *
from AFN import * 
import utils 
from DFA import *
from regex import *

BANDERA = True

while BANDERA == True:
    print('Elija una opcion:')
    print('1. AFN a AFD')
    print('2. AFD directo')
    print('3. Salir')
    print("\n")
    opcion = int(input('>> '))
    
    if opcion == 1: #AFN A AFD
        #ingreso de la expresion
        r =  input("\nIngrese una expresion a convertir: ")
        print("\nRegex: ", r)

        #ε

        #infix a postfix
        conversion = convertExpression(len(r))
        conversion.RegexToPostfix(r)
        if conversion.verificar == True:
            
            #Regex a postfix
            postfix = conversion.res
            print("\nPostfix: ", postfix)

            #Postfix a AFN
            afn = PostifixToAFN(postfix)
            afn.conversion()
            
            #AFN a AFD
            conversionAFD = AFN(afn.e0, afn.ef,afn.estados, afn.simbolos, afn.transiciones_splited)

            conversionAFD.construir_afd()
            
            #Simulacion
            exp = input("\nIngrese una cadena para simular en AFN:\n-> ")
            aceptada = afn.simulacion(exp)
            if aceptada:  # devuelve True
                print(f"\nLa cadena '{exp}' es aceptada por el AFN.")
            else:
                print(f"\nLa cadena '{exp}' NO es aceptada por el AFN.")
            
             # MINIMIZACION DE AFD A PARTIR DE AFN
            minizacionAFD = Minimizar(conversionAFD.e0_afd, conversionAFD.ef_afd, conversionAFD.afd_transiciones, conversionAFD.estados)

            minizacionAFD.minimizar('afd_minimizado_1')
        
        else:
            print("Error en expresion")
    if opcion == 2:
        #ingreso de la expresion
        r =  input("\nIngrese una expresion a convertir: ")
        w =  input("\nIngrese una cadena para simular: ")
        
        my_regex = fix_regex(r, True)
        syntax = DFA(my_regex)

        states = {s.name for s in syntax.states}
        alphabet = {a for a in syntax.symbols}
        alphabet, alphabet_print = utils.get_alphabet(syntax.create_transitions())

        syntax.draw()
        respuesta = syntax.simulate_string(w)

        print(f'\nLa cadena {w} es acpetada en la expresion {r}? -> ', respuesta)
        utils.graph_fa(states, alphabet, syntax.init_state, {s for s in syntax.acc_states}, syntax.create_transitions(), 'graphs/d_dfa')
        
        
    if opcion ==3:
        BANDERA=False
