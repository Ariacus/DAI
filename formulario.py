#!/usr/bin/env python

# -*- coding: utf-8 -*-

import web
from web import form
from web.contrib.template import render_mako
from pymongo import MongoClient


client = MongoClient()
db = client.aplicacion
print "Se ha conectado a la BDD"
web.config.debug=False




urls = (
	'/registro', 'registro',
	'/', 'inicio',
	'/login','login'
 	
)

app=web.application(urls,globals())
sesion = web.session.Session(app,
	web.session.DiskStore('session'),
	initializer={'usuario':''})




plantilla = render_mako (
	directories = ['templates'],
	input_encoding = 'utf-8',
	output_encoding = 'utf-8'
	)

dia = range(1,32)
mes = range(1,13)
anio = range(1960,2000)


################     FUNCIONES GLOBALES ####################


def comprueba_identificacion():
	usuario=sesion.usuario
	return usuario



###############################################################



################ FORMULARIOS    ########################
form_logear = form.Form(
	form.Textbox("Usuario", form.notnull),
	form.Password("Contrasenia", form.notnull),
	form.Button("Sign In")
	)



form_registrar = form.Form(
	form.Textbox("Nombre", form.notnull),
	form.Textbox("Apellidos", form.notnull),
	form.Textbox("DNI", form.notnull, form.regexp('^([0-9]{8}[A-Z])$', "Formato de DNI no valido")),
	form.Textbox("email", form.notnull, form.regexp('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', "Formato de correo incorrecto")), 
	form.Textbox("VISA", form.notnull, form.regexp('^([0-9]{4}) ([0-9]{4}) ([0-9]{4}) ([0-9]{4})|([0-9]{4})-([0-9]{4})-([0-9]{4})-([0-9]{4})$', "Formato de tarjeta VISA no valido")),
	form.Dropdown("dia",dia, description="Dia de nacimiento"),
	form.Dropdown("mes",mes, description="Mes de nacimiento"),
	form.Dropdown("anio",anio, description="Anio de nacimiento"),
	form.Textarea("Direccion", form.notnull),
	form.Password("Contrasenia", form.notnull, post = "Su contrasenia debe de tener mas de 7 caracteres"),
	form.Password("Verificacion", form.notnull, pre= "Repita su contraseña"),
	form.Radio("pago", ['Contra reembolso', 'VISA'],form.notnull),
	form.Checkbox("clausulas",form.Validator("Debes aceptar las clausulas de la protección de datos", lambda i: "clausulas" not in i), description="Acepta las clausulas"),
	form.Button("Enviar"),
	validators = [form.Validator("No coinciden las contraseñas", lambda i: i.Contrasenia == i.Verificacion), form.Validator("Longitud de contraseña", lambda i: len(i.Contrasenia)>=7), form.Validator("Fecha de nacimiento no válida.", lambda i: (((int(i.mes) == 2) and ((int(i.dia) <= 28) and ((int(i.anio) % 4) != 0) or (int(i.dia) <= 29) and ((int(i.anio) % 4) == 0))) or ((int(i.dia) <= 30) and ((int(i.mes) == 4) or (int(i.mes) == 6) or (int(i.mes) == 9) or (int(i.mes) == 11)))))]	
)

################################################################




################# CLASES ############################################
class inicio:
	def GET(self):		

		return plantilla.inicio()
	def POST(self):
		return "Inicio por POST"
			

#Clase para logear

class login:
	def GET(self):
		f = form_logear()
		return plantilla.login(f=f.render())
	def POST(self):
		f = form_logear()
		posts=db.posts
		query="Hola"
		if query:
			return "Ha encontrado"
		else:
			return "No ha encontrado nada"
		
		
#Clase para registrarse en el sistema.

class registro:
	def GET(self):
		f = form_registrar()
		
		return plantilla.registro(f=f.render())
	

	def POST(self):
		f = form_registrar()
		if not f.validates():
			
			return plantilla.registro(f=f.render())
		else:
			usr = {"Nombre": f.d.Nombre,
				"Password": f.d.Contrasenia,
				"Apellidos": f.d.Apellidos,
				"DNI": f.d.DNI,
				"Email": f.d.email,
				"VISA": f.d.VISA,
				"dia": f.d.dia,
				"mes": f.d.mes,
				"anio": f.d.anio,
				"Direccion": f.d.Direccion,
				"Pago": f.d.pago}			
			posts=db.posts
			posts.insert(usr)
			print "Se han registrado los datos"
			return plantilla.inicio()
	









if __name__ == "__main__":
    app.run()

