from urllib.request import Request, urlopen # abre una url
from re import findall # expresiones regulares
import sys, time

#Funcion para obtener el valor de la UTM del mes actual
def get_UTM():
    req = Request("https://www.indicadoreschile.com/valor-utm.html")
    html = urlopen(req).read()
    html = html.decode('utf-8')
    data = findall(r'\s*<p class="valor">([0-9]+)\.([0-9]+),00 pesos chilenos</p>\s*', html)
    utm = int(data[0][0] + data[0][1])

    return utm

#Funcion para obtener el valor del porcentaje del AFP segun la seleccion del usuario
def get_AFP():
    # Capital, Cuprum, Habitat, PlanVital, ProVida, Modelo
    afps = [0.1144, 0.1144, 0.1127, 0.1116, 0.1145, 0.10770] #Porcentajes

    while True:
        option = int(input("Seleccione su AFP: \n" #Opciones de AFP para el usuario
                "1 - Capital \n"
                "2 - Cuprum \n"
                "3 - Habitat \n"
                "4 - PlanVital \n"
                "5 - ProVida \n"
                "6 - Modelo \n"
                "7 - Salir\n=> "))
        print()

        if(option == 7):
            thanks()
        elif (option > 0 and option < 7):
            return afps[option - 1]
        else:
            print("La opción ingresada no es válida \n")
            time.sleep(1) #Lapso de tiempo de espera del programa

#Funcion que retorna los porcentajes de descuento que son constantes para el sueldo bruto
def get_variables():
    sis = 0.0153    # Seguro de Invalidez y Sobrevivencia (1.53%)
    sd = 0.07    # Salud (7%)
    aio = 0.0411    # Aporte de Indemnización obligatoria (4.11%)
    sc = 0.03       # Seguro Cesantía (3%)
    at = 0.0093     # Accidentes del trabajo (0.93%)
    tasa_afp = get_AFP() # AFP

    return sis, sd, aio, sc, at, tasa_afp

# Funcion que retorna el descuento del impuesto a la renta
# segun el sueldo imponible ingresado en esta
def get_impuesto_segunda_categoria(sueldo):
    """
        Recibe el sueldo en UTM.
        Retorna el valor del impuesto en UTM
    """
    if sueldo >= 0 and sueldo <= 13.5:
        return 0
    elif sueldo > 13.5 and sueldo <= 30:
        return sueldo * 0.04 - 0.54
    elif sueldo > 30 and sueldo <= 50:
        return sueldo * 0.08 - 1.74
    elif sueldo > 50 and sueldo <= 70:
        return sueldo * 0.135 - 4.49
    elif sueldo > 70 and sueldo <= 90:
        return sueldo * 0.23 - 11.14
    elif sueldo > 90 and sueldo <= 120:
        return sueldo * 0.304 - 17.8
    elif sueldo > 120:
        return sueldo * 0.35 - 23.32

# Funcion que retorna el factor y la cantidad a rebajar del impuesto a la renta
# segun el sueldo liquido ingresado en esta
def get_factor_cantRebajar(sueldo):
    """
        Recibe el sueldo en UTM.
        Retorna el valor del impuesto en UTM
    """
    if sueldo >= 0 and sueldo <= 13.5:
        return 0, 0
    elif sueldo > 13.5 and sueldo <= 29.34:
        return 0.04, 0.54
    elif sueldo > 29.34 and sueldo <= 47.74:
        return 0.08, 1.74
    elif sueldo > 47.74 and sueldo <= 65.04:
        return 0.135, 4.49
    elif sueldo > 65.04 and sueldo <= 80.44:
        return 0.23, 11.14
    elif sueldo > 80.44 and sueldo <= 101.32:
        return 0.304, 17.8
    elif sueldo > 101.32:
        return 0.35, 23.32

#-------------------------------------------------------------------------------
#Funcion que calcula el sueldo liquido a partir del sueldo bruto ingresado
def bruto_liq(sueldo_bruto, valor_utm):
    sis, sd, aio, sc, at, afp = get_variables()
    sueldo_liquido_imponible = sueldo_bruto - sueldo_bruto * (sis + sd + aio + sc + at + afp)
    sueldo_liquido = sueldo_liquido_imponible - imp_liq(valor_utm, sueldo_liquido_imponible)

    return sueldo_liquido

#Funcion que aplica el impuesto de segunda categoria al sueldo imponible ingresado
#y retorna el respectivo descuento
def imp_liq(utm, sueldo_liquido_imponible):
    sueldo_utm = sueldo_liquido_imponible / utm
    dcto_utm = get_impuesto_segunda_categoria(sueldo_utm)
    dcto = dcto_utm * utm

    return dcto

#-------------------------------------------------------------------------------
#Funcion que calcula el sueldo bruto a partir del sueldo liquido ingresado
def liq_bruto(sueldo_liquido, valor_utm):
    sis, sd, aio, sc, at, afp = get_variables()
    sueldo_liquido_imponible = liq_imp(valor_utm, sueldo_liquido)
    sueldo_bruto = sueldo_liquido_imponible / (1 - (sis + sd + aio + sc + at + afp))

    return sueldo_bruto

#Funcion que busca el factor y la cantidad a rebajar que se le aplico al sueldo
#liquido ingresado, retornando el sueldo liquido imponible
def liq_imp(utm, sueldo_liquido):
    sueldo_utm = sueldo_liquido / utm
    factor_utm, cant_reb_utm = get_factor_cantRebajar(sueldo_utm)
    sueldo_liquido_imponible = (sueldo_utm - cant_reb_utm) / (1 - factor_utm)

    return sueldo_liquido_imponible * utm

#-------------------------------------------------------------------------------
#Ofrece al usuario realizar otra operacion despues de realizar los calculos
def otra_operacion():
    while True:
        option = int(input("Desea realizar otra operación?\n"
            "1 - Sí\n"
            "2 - No\n=> "))

        if option == 1:
            print()
            print()
            return
        elif option == 2:
            thanks()
        else:
            print("La opción ingresada no es válida\n")
            time.sleep(1) #Lapso de tiempo de espera del programa

#Funcion de agradecimiento (imprime)
def thanks():
    print("Gracias por usar la Calculadora de Sueldos DiJo!")
    sys.exit(0) #Termina el programa

if __name__ == '__main__':
    print("Iniciando Calculadora...\n\n")
    valor_utm = get_UTM() #obtiene el valor UTM

    while True: #Ejecuta el codigo hasta que el usuario se salga
        option = int(input("Ingrese el numero correspondiente a la opción deseada: \n"
            "1 - Cálculo de sueldo bruto \n"
            "2 - Cálculo de sueldo líquido \n"
            "3 - Salir\n"
            "=> "))
        print()

        if (option == 1): #opcion para calcular el sueldo bruto a base de un liquido
            while True:
                sueldo_liquido = int(input("Ingrese el sueldo líquido:\n=> "))
                if sueldo_liquido <= 0:
                    print("Ingrese un sueldo positivo por favor!\n")
                    time.sleep(1) #Lapso de tiempo de espera del programa
                else:
                    break
            print()
            ans = round(liq_bruto(sueldo_liquido, valor_utm))
            print("El sueldo bruto que obtendrá con", sueldo_liquido, "de sueldo líquido es:", ans)
            print()
            otra_operacion()

        elif (option == 2): #opcion para calcular el sueldo liquido a base de un bruto
            while True:
                sueldo_bruto = int(input("Ingrese el sueldo bruto:\n=> "))
                if sueldo_bruto <= 0:
                    print("Ingrese un sueldo positivo por favor!\n")
                    time.sleep(1) #Lapso de tiempo de espera del programa
                else:
                    break
            print()
            ans = round(bruto_liq(sueldo_bruto, valor_utm))
            print("El sueldo líquido que obtendrá con", sueldo_bruto, "de sueldo bruto es:", ans)
            print()
            otra_operacion()

        elif (option == 3):
            thanks() #Agradecimiento

        else:
            print("La opción ingresada no es válida\n")
            time.sleep(1) #Lapso de tiempo de espera del programa
