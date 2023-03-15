from Postfix import *
from AFN import * 

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
    afn = AFN(postfix)
    afn.conversion()
    
    #Simulacion
    exp = input("\nIngrese una cadena para simular en AFN:\n-> ")
    aceptada = afn.simulacion(exp)
    if aceptada:  # devuelve True
        print(f"\nLa cadena '{exp}' es aceptada por el AFN.")
    else:
        print(f"\nLa cadena '{exp}' NO es aceptada por el AFN.")
    
else:
    print("Error en expresion")