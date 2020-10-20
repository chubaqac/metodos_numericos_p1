import math
import sympy as sy
from prettytable import PrettyTable

global ecuacion
global x
global aproximacion_estado
global aproximacion_valor

# ecuacion= (x**3)+(4*(x**2))-10
# ecuacion= sy.exp(x)+x
# ecuacion= (x**2)+x-5
# ecuacion= x-sy.cos(x)
# ecuacion= sy.log(x)+x
# ecuacion= (x**3)+(3*x**2)-4
# ecuacion= x-sy.sin(2*x)
# ecuacion= sy.exp(x)-x-1

x=sy.symbols("x")

ecuacion= (x**3)+(3*x**2)-4

aproximacion_estado= False
aproximacion_valor= 9

def aprox(valor):
	if(aproximacion_estado):
		return round(valor,aproximacion_valor)
	else:
		return valor

def xor(x,y):
	if(x==y):
		return True
	else:
		return False

def signo_boolean(valor):
	if(valor>0):
		return True
	else:
		return False

def signo_string(valor):
	if(valor>0):
		return "+"
	else:
		return "-"

def solve(ecuacion,valor):
	f = lambda x: eval(ecuacion)
	# return aprox(f(valor))
	return f(valor)


def reemplazarMath(valor):
	valor= valor.replace("sin","math.sin")
	valor= valor.replace("cos","math.cos")
	valor= valor.replace("tan","math.tan")
	valor= valor.replace("asin","math.asin")
	valor= valor.replace("acos","math.acos")
	valor= valor.replace("atan","math.atan")
	valor= valor.replace("exp","math.exp")
	valor= valor.replace("log","math.log")

	return valor

def biseccion():
	tabla = PrettyTable()
	tabla.field_names = ["N", "an", "f(an)", "bn", "f(bn)","pn","f(pn)"]

	str_ecuacion= str(ecuacion)
	str_ecuacion= reemplazarMath(str_ecuacion)

	an= float(input("INTERVALO A INICIAL: "))
	bn= float(input("INTERVALO B INICIAL: "))

	modo_n= False

	if(modo_n):
		epsilon=float(input("INGRESAR EPSILON: "))
		numero=((math.log((bn-an)/epsilon))/(math.log(2)))-1
		print("N:",numero)
		numero= round(numero)

	else:
		numero=int(input("NUMERO DE ITERACIONES: "))

	for i in range(numero):
		f_an= solve(str_ecuacion,an)
		f_bn= solve(str_ecuacion,bn)
		pn= (an+bn)/2
		f_pn= solve(str_ecuacion,pn)

		# tabla.add_row([i+1,an,f_an,bn,f_bn,pn,f_pn])
		tabla.add_row([i+1,aprox(an),aprox(f_an),aprox(bn),aprox(f_bn),aprox(pn),aprox(f_pn)])

		if(xor(signo_boolean(f_an),signo_boolean(f_pn))):
			an=pn
		elif(xor(signo_boolean(f_bn),signo_boolean(f_pn))):
			bn=pn

	print()
	print("f(x)=",str_ecuacion)
	print(tabla)
	print()

def newton_raphson():
	tabla=PrettyTable()
	tabla.field_names = ["N", "pn", "|pn - pn-1|"]

	ecuacion_d1= sy.diff(ecuacion,x)

	pn= float(input("INGRESE VALOR P INICIAL: "))
	numero=int(input("INGRESE NUMERO DE INTERACION: "))

	modo_precision= False
	precision_valor= 0.0000001

	str_ecuacion= str(ecuacion)
	str_ecuacion= reemplazarMath(str_ecuacion)

	str_ecuacion_d1= str(ecuacion_d1)
	str_ecuacion_d1= reemplazarMath(str_ecuacion_d1)

	for i in range(numero+1):
		if(i==0):
			tabla.add_row([i,pn,"-"])
			continue
		aux=pn
		pn=aux-((solve(str_ecuacion,pn))/(solve(str_ecuacion_d1,pn)))

		error= abs(pn-aux)

		tabla.add_row([i,aprox(pn),aprox(error)])

		if(modo_precision):
			if(error<precision_valor):
				break

	print()
	print("f(x)=",str_ecuacion)
	print("f'(x)=",str_ecuacion_d1)
	print(tabla)
	print()

def newton_raphson_chute_inicial():
	tabla=PrettyTable()
	tabla.field_names = ["N", "f(x)", "f(x)'", "f(x)''"]

	ecuacion_d1= sy.diff(ecuacion,x)
	ecuacion_d2= sy.diff(ecuacion,x,x)

	str_ecuacion= str(ecuacion)
	str_ecuacion= reemplazarMath(str_ecuacion)

	str_ecuacion_d1= str(ecuacion_d1)
	str_ecuacion_d1= reemplazarMath(str_ecuacion_d1)

	str_ecuacion_d2= str(ecuacion_d2)
	str_ecuacion_d2= reemplazarMath(str_ecuacion_d2)

	an= float(input("INTERVALO A INICIAL: "))
	bn= float(input("INTERVALO B INICIAL: "))
	numero=int(input("INGRESE NUMERO DE INTERACION: "))

	n=an
	while(n<=bn):
		tabla.add_row([n,signo_string(solve(str_ecuacion,n)),signo_string(solve(str_ecuacion_d1,n)),signo_string(solve(str_ecuacion_d2,n))])
		n=round((n+((bn-an)/numero)),1)

	print()
	print("f(x)=",str_ecuacion)
	print("f'(x)=",str_ecuacion_d1)
	print("f''(x)=",str_ecuacion_d2)
	print(tabla)
	print()


def newton_raphson_modificado():
	tabla=PrettyTable()
	tabla.field_names = ["N", "pn", "|pn - pn-1|"]

	ecuacion_d1= sy.diff(ecuacion,x)
	ecuacion_d2= sy.diff(ecuacion,x,x)

	str_ecuacion= str(ecuacion)
	str_ecuacion= reemplazarMath(str_ecuacion)

	str_ecuacion_d1= str(ecuacion_d1)
	str_ecuacion_d1= reemplazarMath(str_ecuacion_d1)

	str_ecuacion_d2= str(ecuacion_d2)
	str_ecuacion_d2= reemplazarMath(str_ecuacion_d2)

	pn= float(input("INGRESE VALOR P INICIAL: "))
	numero=int(input("INGRESE NUMERO DE INTERACION: "))

	modo_precision= False
	precision_valor= 0.0000001

	for i in range(numero+1):
		if(i==0):
			tabla.add_row([i,pn,"-"])
			continue
		aux=pn
		numerador= solve(str_ecuacion,aux)*solve(str_ecuacion_d1,aux)
		denominador= (solve(str_ecuacion_d1,aux)**2)-solve(str_ecuacion,aux)*solve(str_ecuacion_d2,aux)
		pn=pn-(numerador/denominador)

		error=abs(pn-aux)
		tabla.add_row([i,aprox(pn),aprox(error)])

		if(modo_precision):
			if(error<precision_valor):
				break

	print()
	print("f(x)=",str_ecuacion)
	print("f'(x)=",str_ecuacion_d1)
	print("f''(x)=",str_ecuacion_d2)
	print(tabla)
	print()


def main():
	while(True):
		print("[1]: BISECCION | [2]: NEWTON RHAPSON | [3]: NEWTON MEJORADO | [4]: CHUTE INICIAL")
		opcion=input("INGRESE OPCION: ")
		if(opcion=="1"):
			biseccion()
		elif(opcion=="2"):
			newton_raphson()
		elif(opcion=="3"):
			newton_raphson_modificado()
		elif(opcion=="4"):
			newton_raphson_chute_inicial()
		else:
			break

if __name__ == "__main__":
	main()