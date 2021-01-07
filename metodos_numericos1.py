import math
import sympy as sy
from prettytable import PrettyTable

__author__ = "prepuciano"
__credits__ = ["prepuciano", "wilson"]

global ecuacion
global x
global aproximacion_estado
global aproximacion_valor
global precision_estado

#algunosss ejemploss de como construir tu ecuacion
# ecuacion= (x**3)+(4*(x**2))-10
# ecuacion= sy.exp(x)+x
# ecuacion= (x**2)+x-5
# ecuacion= x-sy.cos(x)
# ecuacion= sy.log(x)+x
# ecuacion= (x**3)+(3*x**2)-4
# ecuacion= x-sy.sin(2*x)
# ecuacion= sy.exp(x)-x-1
# ecuacion= (x**3)-x+1
# ecuacion= (x**3)+(6*x**2)+(12*x)-(28)
# ecuacion= (80*sy.exp(-2*x)+(20*sy.exp(-0.5*x))-93)

x=sy.symbols("x")

#aca se tiene que construir tu ecuacion
ecuacion= (80*sy.exp(-2*x)+(20*sy.exp(-0.5*x))-93)+sy.sin(x)+sy.log(10*x)

#CONFIGURACION PREDETERMINADA
#TRUE: se activa para que los valores entregados sean aproximados
#FALSE: se desactiva para que los valores entregados sean aproximados
aproximacion_estado= False
#numero de decimales a proximar
aproximacion_valor= 8

precision_estado= False

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
	elif(valor<0):
		return "-"
	else:
		return "*"

def solve(ecuacion,valor):
	f = lambda x: eval(ecuacion)
	# return aprox(f(valor))
	return f(valor)


def reemplazarMath(valor):
	valor= str(valor)

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

	str_ecuacion= reemplazarMath(ecuacion)

	an= float(input("INTERVALO A INICIAL: "))
	bn= float(input("INTERVALO B INICIAL: "))


	#TRUE: se activa para que se detenga de forma automatica al ingresar tu valor de precision
	#FALSE: se desactiva para que se detenga de forma automatica al ingresar tu valor de precision
	precision_estado_biseccion= precision_estado

	if(precision_estado_biseccion):
		epsilon= float(input("INGRESAR EPSILON: "))
		numero=((math.log((bn-an)/epsilon))/(math.log(2)))-1
		print("N:",numero)
		numero= round(numero)
	else:
		numero=int(input("INGRESE NUMERO DE INTERACION: "))

	for i in range(numero):
		f_an= solve(str_ecuacion,an)
		f_bn= solve(str_ecuacion,bn)
		pn= (an+bn)/2
		f_pn= solve(str_ecuacion,pn)

		# tabla.add_row([i+1,an,f_an,bn,f_bn,pn,f_pn])
		tabla.add_row([i+1,aprox(an),aprox(f_an),aprox(bn),aprox(f_bn),aprox(pn),aprox(f_pn)])

		#BUG: iteraba a pesar de que los 2 f_an y f_bn tenian el mismo signo
		if(f_an*f_bn>0):
			print()
			print("SE DETUVO PORQUE f(an) y f(bn) MISMO SIGNO")
			break

		if(f_pn*f_bn >0):
			bn=pn
		elif(f_pn*f_an >0):
			an=pn
		else:
			break

		# if(xor(signo_boolean(f_an),signo_boolean(f_pn))):
		# 	an=pn
		# elif(xor(signo_boolean(f_bn),signo_boolean(f_pn))):
		# 	bn=pn

	print()
	print("f(x)=",str(ecuacion))
	print(tabla)

def newton_raphson():
	tabla=PrettyTable()
	tabla.field_names = ["N", "pn", "|pn - pn-1|"]

	ecuacion_d1= sy.diff(ecuacion,x)

	pn= float(input("INGRESE VALOR P INICIAL: "))
	

	#TRUE: se activa para que se detenga de forma automatica al ingresar tu valor de precision
	#FALSE: se desactiva para que se detenga de forma automatica al ingresar tu valor de precision
	precision_estado_newton_raphson= precision_estado

	if(precision_estado_newton_raphson):
		# precision_valor= 0.0000001
		precision_valor= float(input("INGRESAR VALOR PRECISION: "))
		numero=100
	else:
		numero=int(input("INGRESE NUMERO DE INTERACION: "))

	str_ecuacion= reemplazarMath(ecuacion)

	str_ecuacion_d1= reemplazarMath(ecuacion_d1)

	for i in range(numero+1):
		if(i==0):
			tabla.add_row([i,pn,"-"])
			continue
		aux=pn
		pn=aux-((solve(str_ecuacion,pn))/(solve(str_ecuacion_d1,pn)))

		error= abs(pn-aux)

		tabla.add_row([i,aprox(pn),aprox(error)])

		if(precision_estado_newton_raphson):
			if(error<precision_valor):
				break

	print()
	print("f(x)=",str(ecuacion))
	print("f'(x)=",str(ecuacion_d1))
	print(tabla)

def newton_raphson_chute_inicial():
	tabla=PrettyTable()
	tabla.field_names = ["N", "f(x)", "f(x)'", "f(x)''"]

	ecuacion_d1= sy.diff(ecuacion,x)
	ecuacion_d2= sy.diff(ecuacion,x,x)

	str_ecuacion= reemplazarMath(ecuacion)

	str_ecuacion_d1= reemplazarMath(ecuacion_d1)

	str_ecuacion_d2= reemplazarMath(ecuacion_d2)

	an= float(input("INTERVALO A INICIAL: "))
	bn= float(input("INTERVALO B INICIAL: "))
	numero=int(input("INGRESE NUMERO DE INTERACION: "))

	n=an
	while(n<=bn):
		tabla.add_row([n,signo_string(solve(str_ecuacion,n)),signo_string(solve(str_ecuacion_d1,n)),signo_string(solve(str_ecuacion_d2,n))])
		n=round((n+((bn-an)/numero)),1)

	print()
	print("f(x)=",str(ecuacion))
	print("f'(x)=",str(ecuacion_d1))
	print("f''(x)=",str(ecuacion_d2))
	print(tabla)

def newton_raphson_modificado():
	tabla=PrettyTable()
	tabla.field_names = ["N", "pn", "|pn - pn-1|"]

	ecuacion_d1= sy.diff(ecuacion,x)
	ecuacion_d2= sy.diff(ecuacion,x,x)

	str_ecuacion= reemplazarMath(ecuacion)

	str_ecuacion_d1= reemplazarMath(ecuacion_d1)

	str_ecuacion_d2= reemplazarMath(ecuacion_d2)

	pn= float(input("INGRESE VALOR P INICIAL: "))
	

	#TRUE: se activa para que se detenga de forma automatica al ingresar tu valor de precision
	#FALSE: se desactiva para que se detenga de forma automatica al ingresar tu valor de precision
	precision_estado_newton_raphson_modificado= precision_estado
	
	if(precision_estado_newton_raphson_modificado):
		# precision_valor= 1e-7
		precision_valor= float(input("INGRESAR VALOR PRECISION: "))
		numero=100
	else:
		numero=int(input("INGRESE NUMERO DE INTERACION: "))

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

		if(precision_estado_newton_raphson_modificado):
			if(error<precision_valor):
				break

	print()
	print("f(x)=",str(ecuacion))
	print("f'(x)=",str(ecuacion_d1))
	print("f''(x)=",str(ecuacion_d2))
	print(tabla)

def configuracion():
	global aproximacion_estado, aproximacion_valor, precision_estado
	
	print("-------------------------")
	print("APROXIMACION_ESTADO:",str(aproximacion_estado))
	print("APROXIMACION_VALOR:",str(aproximacion_valor))
	print("PRECISION_ESTADO:",str(precision_estado))
	print("-------------------------")

	print("[1]: APROXIMACION | [2]: PRECISION")
	opt1= input("INGRESAR OPCION: ")
	if(opt1=="1"):
		print("[1]: ACTIVAR | [2]: DESACTIVAR")
		opt2= input("INGRESAR OPCION: ")
		if(opt2=="1"):
			aproximacion_estado= True
			opt3= int(input("INGRESAR NUMERO DE DECIMALES: "))
			aproximacion_valor= opt3
		elif(opt2=="2"):
			aproximacion_estado= False

	elif(opt1=="2"):
		print("[1]: ACTIVAR | [2]: DESACTIVAR")
		opt2= input("INGRESAR OPCION: ")
		if(opt2=="1"):
			precision_estado= True
		elif(opt2=="2"):
			precision_estado= False
	else:
		return

def multiderivada():
	numero_derivada=int(input("INGRESAR NUMERO DE DERIVADAS: "))
	numero_evaluar=int(input("INGRESE NUMERO PARA EVALUAR: "))

	tabla=PrettyTable()
	tabla.field_names = ["N°", "d/dx", "EVALUADO"]
	ecuacion_d=ecuacion
	for i in range(numero_derivada+1):
		if(i==0):
			tabla.add_row([i,ecuacion_d,solve(str(ecuacion_d),numero_evaluar)])
			continue

		ecuacion_d= sy.diff(ecuacion_d,x)
		tabla.add_row([i,ecuacion_d,solve(str(ecuacion_d),numero_evaluar)])
	print()	
	print(tabla)

def main():
	global ecuacion
	try:
		while(True):
			print("ECUACION:",ecuacion)
			print("[0]: INGRESAR ECUACION")
			print("[1]: BISECCION | [2]: NEWTON RHAPSON | [3]: NEWTON MEJORADO | [4]: EXTRA")
			opcion=input("INGRESE OPCION: ")
			if(opcion=="1"):
				biseccion()
			elif(opcion=="2"):
				newton_raphson()
			elif(opcion=="3"):
				newton_raphson_modificado()
			elif(opcion=="4"):
				print("[1]: CHUTE INICIAL | [2]: DERIVAR | [3]: CONFIGURACION")
				opcion1=input("INGRESE OPCION: ")
				if(opcion1=="1"):
					newton_raphson_chute_inicial()
				elif(opcion1=="2"):
					multiderivada()
				elif(opcion1=="3"):
					configuracion()
			elif(opcion=="0"):
				# ecuacion= (x**3)+(3*x**2)-4
				# ecuacion= x-sin(2*x)
				ecuacion_nuevo=input("INGRESAR ECUACION: ")
				ecuacion= sy.parse_expr(ecuacion_nuevo)
			else:
				break
			print()
	except:
		print()
		print("UPS... ALGO SALIO MAL")
		input("PRESS ENTER TO EXIT")

if __name__ == "__main__":
	main()
