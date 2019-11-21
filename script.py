import subprocess, platform, shutil, csv, pandas
from tempfile import NamedTemporaryFile

#Informacion de Hospitales
hospitales = [
  {'Codigo': '1', 'Nombre': 'Hospital Universitario Juan Segundo', 'Cupo Pacientes': 15, 'Cantidad Pacientes': 0},
  {'Codigo': '2', 'Nombre': 'Hospital San Carlos', 'Cupo Pacientes': 10, 'Cantidad Pacientes': 0},
  {'Codigo': '3', 'Nombre': 'HHospital Piloto', 'Cupo Pacientes': 10, 'Cantidad Pacientes': 0}
]
#Funciones
def cargarConfig():
  for hospital in hospitales:
    hospital['Cantidad Pacientes'] = 0
  archivoBd = 'bd.csv'
  camposBd = ['Codigo', 'Nombre', 'Identificacion','Causa de Ingreso','Hospital Origen','Hospital Actual']
  with open(archivoBd, 'r', encoding='ascii') as archivo:
    lector = csv.DictReader(archivo, fieldnames=camposBd)
    for fila in lector:
      if fila['Hospital Actual'] == hospitales[0]['Codigo']:
        hospitales[0]['Cantidad Pacientes'] = hospitales[0]['Cantidad Pacientes'] + 1
        pass
      elif fila['Hospital Actual'] == hospitales[1]['Codigo']:
        hospitales[1]['Cantidad Pacientes'] = hospitales[1]['Cantidad Pacientes'] + 1
        pass
      elif fila['Hospital Actual'] == hospitales[2]['Codigo']:
        hospitales[2]['Cantidad Pacientes'] = hospitales[2]['Cantidad Pacientes'] + 1
def ingresoPaciente():
  print("\nA que hospital desea ingresarlo: \n1: Hospital Universitario Juan Segundo\n2: Hospital San Carlos\n3: Hospital Piloto")
  codigoHospital = int(input("Seleccion: "))
  while codigoHospital > 3:
    codigoHospital = int(input("Ingrese un codigo de hospital valido: "))
  if hospitales[codigoHospital-1]['Cantidad Pacientes'] < hospitales[codigoHospital-1]['Cupo Pacientes']:
    codigoPaciente = input("Ingrese el codigo del paciente: ")
    nombre = input("Ingrese los Nombres y Apellidos del paciente: ")
    identificacion = input("Ingrese el numero de Identificacion del paciente: ")
    causa = input("Ingrese la Causa de Ingreso del paciente: ")
    hospitalOrigen = '0'
    hospitalActual = str(codigoHospital)
    string = codigoPaciente+","+nombre+","+identificacion+","+causa+","+hospitalOrigen+","+hospitalActual+"\n"
    f=open("bd.csv", "a+")
    f.write(string)
    f.close()
    cargarConfig()
    print('Paciente agregado con exito al sistema.')
  else:
    print('No hay cupo para el paciente en el hospital ', codigoHospital)
  input()
def verPacientes():
  print ("\n\nLista de Pacientes")
  pacientes = pandas.read_csv('bd.csv')
  print(pacientes.to_string(index = False))
  input()
def trasladoPaciente():
  codigoPaciente = input("\nIngrese el código del paciente que desea trasladar: ")
  camposPacientes = ['Codigo', 'Nombre', 'Identificacion','Causa', 'Hospital Origen','Hospital Actual']
  archivoTemporal = NamedTemporaryFile(mode='w', delete=False)
  archivoBD = 'bd.csv'
  pacienteExiste = False
  with open(archivoBD, 'r', encoding='UTF-8') as archivo:
    lector = csv.DictReader(archivo, fieldnames=camposPacientes)
    for fila in lector:
      if fila['Codigo'] == codigoPaciente:
        pacienteExiste = True
        break
  if pacienteExiste == True:
    with open(archivoBD, 'r', encoding='UTF-8') as archivo, archivoTemporal:
      lector = csv.DictReader(archivo, fieldnames=camposPacientes)
      escritor = csv.DictWriter(archivoTemporal, fieldnames=camposPacientes) 
      for fila in lector:
        if fila['Codigo'] == codigoPaciente:
          print("\nEl paciente actualmente se encuentra en el hospital ", fila['Hospital Actual'])
          print("A que hospital desea trasladar al paciente " + codigoPaciente)
          if fila['Hospital Actual'] != '1':
            print("1: Hospital Universitario Juan Segundo")
          if fila['Hospital Actual'] != '2':
            print("2: Hospital San Carlos")
          if fila['Hospital Actual'] != '3':
            print("3: Hospital Piloto")
          codigoNuevoHospital = int(input("Seleccion: "))
          while codigoNuevoHospital > 3 or codigoNuevoHospital == fila['Hospital Actual']:
            codigoNuevoHospital = int(input("Ingrese un codigo de hospital valido: "))
          codigoHospitalOrigen = fila['Hospital Actual']
          fila['Hospital Actual'], fila['Hospital Origen']= codigoNuevoHospital, codigoHospitalOrigen
        fila = { 'Codigo': fila['Codigo'], 'Nombre': fila['Nombre'], 'Identificacion': fila['Identificacion'], 'Causa': fila['Causa'], 'Hospital Origen': fila['Hospital Origen'], 'Hospital Actual': fila['Hospital Actual']}
        escritor.writerow(fila)
    shutil.move(archivoTemporal.name, archivoBD)
    cargarConfig()
    print('El paciente ' + codigoPaciente + ' fue trasladado correctamente.')
  else:
    print('No existe un paciente con el codigo ', codigo)
  input()
def verificarCupo():
  codigoHospital = int(input("\nIngrese el código del hospital que desea verificar: "))
  cupo = hospitales[codigoHospital-1]['Cupo Pacientes'] - hospitales[codigoHospital-1]['Cantidad Pacientes']
  if cupo > 0:
    print('El hospital ' + str(codigoHospital) + ' tiene ' + str(cupo) + ' cupos disponibles.')
  else: 
    print('El hospital ' + str(codigoHospital) + ' no tiene cupos disponibles.')
  input()
def limpiarConsola():
  if platform.system()=="Windows":
    subprocess.Popen("cls", shell=True).communicate() 
  else: 
    print("\033c", end="")

#Programa
cargarConfig()
opcion = ''
while opcion!='e':
  limpiarConsola()
  print ("TRASLADO DE PACIENTES\n[a] Ingreso del Paciente\n[b] Ver Pacientes\n[c] Trasladar Paciente\n[d] Verficiar Cupo\n[e] Salir")
  opcion = str(input("\tOpcion: "))
  if(opcion == 'a'):
    ingresoPaciente()
  elif(opcion == 'b'):
    verPacientes()
  elif(opcion == 'c'):
    trasladoPaciente()
  elif(opcion == 'd'):
    verificarCupo()
  elif(opcion == 'e'):
    limpiarConsola()
  else:
    print('Digite una opcion valida.')
    input()
