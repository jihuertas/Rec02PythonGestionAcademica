import json
from datetime import datetime

class Asignatura:
    def __init__(self, nombre, codigo, profesor):
        self.nombre = nombre
        self.codigo = codigo
        self.profesor = profesor
        self.alumnos = [] 
    
    def agregar_alumno(self, alumno):
        # Verificar que el alumno no esté ya inscrito y agregarlo (1 punto)
        if alumno not in self.alumnos:
            self.alumnos.append(alumno)
            #alumno.inscribirse(self)
    
    def eliminar_alumno(self, alumno):
        # Verificar que el alumno esté inscrito y eliminarlo (1 punto)
        if alumno in self.alumnos:
            self.alumnos.remove(alumno)
            #alumno.retirarse(self)
    
    def mostrar_info(self):
        print(f"Asignatura: {self.nombre} ({self.codigo}) - Profesor: {self.profesor}")
        print("Alumnos inscritos:")
        for alumno in self.alumnos:
            print(f"- {alumno.nombre} ({alumno.matricula})")
    
    def to_dict(self):
        dict = {
            "nombre": self.nombre,
            "codigo": self.codigo,
            "profesor": self.profesor,
            "alumnos": [alumno.matricula for alumno in self.alumnos]


        }
        return dict

class Alumno:
    def __init__(self, nombre, matricula):
        self.nombre = nombre
        self.matricula = matricula
        self.asignaturas = []
        self.calificaciones = {}
    
    
    def inscribirse(self, asignatura):
        # Agregar la asignatura a la lista de asignaturas del alumno (1 punto)
        if asignatura not in self.asignaturas:
            self.asignaturas.append(asignatura)
           # asignatura.agregar_alumno(self)


    def retirarse(self, asignatura):
        # Verificar que el alumno esté inscrito y eliminar la asignatura de la lista (1 punto)
        if asignatura in self.asignaturas:
            self.asignaturas.remove(asignatura)
           # asignatura.eliminar_alumno(self)

    def ver_calificaciones(self):
        print(f"Calificaciones de {self.nombre}:")
        for examen, calificacion in self.calificaciones.items():
            print(f"{examen}: {calificacion}")
    
    def to_dict(self):
        dict = {
            "nombre": self.nombre,
            "matricula": self.matricula,
            "asignaturas" : [asignatura.codigo for asignatura in self.asignaturas],
            "calificaciones": self.calificaciones
        }
        return dict
        

        

class Examen:
    def __init__(self, nombre, fecha, asignatura):
        self.nombre = nombre
        self.fecha = fecha
        self.asignatura = asignatura
        self.calificaciones = {}
    
    def asignar_calificacion(self, alumno, calificacion):
        # Verificar que el alumno esté inscrito en la asignatura y asignar la calificación (1 punto)
        if alumno in self.asignatura.alumnos:
            self.calificaciones[alumno.matricula] = calificacion
            alumno.calificaciones[self.nombre] = calificacion
    
    def mostrar_calificaciones(self):
        print(f"Calificaciones del examen {self.nombre} ({self.fecha}):")
        for matricula,nota in self.calificaciones.items():
            for alumno in self.asignatura.alumnos:
                if alumno.matricula == matricula:
                    print(f'La calificación del alumno {alumno.nombre} es: {nota}')
                    break
                

    def to_dict(self):
        dict = {
            "nombre": self.nombre,
            "fecha": self.fecha,
            "asignatura" : self.asignatura.codigo,
            "calificaciones": self.calificaciones
        }
        return dict
    

class GestorAcademico:
    def __init__(self):
        self.asignaturas = {}
        self.alumnos = {}
        self.examenes = {}
    
    def agregar_asignatura(self, nombre, codigo, profesor):
        # Agregar la asignatura al diccionario de asignaturas, usando el código como clave (1 punto)
        self.asignaturas[codigo]= Asignatura(nombre,codigo,profesor)

    def agregar_alumno(self, nombre, matricula):
        # Agregar el alumno al diccionario de alumnos, usando la matrícula como clave (1 punto)
        self.alumnos[matricula] = Alumno(nombre, matricula)

    def agregar_alumno_a_asignatura(self, matricula, codigo_asignatura):
        # Verificar que el alumno y la asignatura existan y agregar al alumno a la asignatura (1,5 puntos)
        if matricula in self.alumnos and codigo_asignatura in self.asignaturas:
            alumno = self.alumnos[matricula]
            asignatura = self.asignaturas[codigo_asignatura]
            asignatura.agregar_alumno(alumno)
            alumno.inscribirse(asignatura)
        
    
    def registrar_examen(self, nombre, fecha, codigo_asignatura):
        # Verificar que la asignatura exista y registrar el examen (1,5 puntos)
        if codigo_asignatura in self.asignaturas:
            asignatura=self.asignaturas[codigo_asignatura]
            examen= Examen(nombre,fecha,asignatura)
            self.examenes[nombre]=examen
    
    def asignar_calificaciones(self, examen):
        for alumno in examen.asignatura.alumnos:
            nota = float(input(f"Dame la nota de {alumno.nombre}"))
            examen.asignar_calificacion(alumno, nota)
        examen.mostrar_calificaciones()


    def listar_datos(self):
        print("\nAsignaturas:")
        for asignatura in self.asignaturas.values():
            asignatura.mostrar_info()
        print("\nAlumnos:")
        for alumno in self.alumnos.values():
            print(f"{alumno.nombre} ({alumno.matricula})")
        print("\nExámenes:")
        for examen in self.examenes.values():
            print(f"{examen.nombre} - {examen.fecha} ({examen.asignatura.nombre})")
    
    def guardar_datos(self, archivo):
        datos = {
            "asignaturas": {k: v.to_dict() for k, v in self.asignaturas.items()},
            "alumnos": {k: v.to_dict() for k, v in self.alumnos.items()},
            "examenes": {k: v.to_dict() for k, v in self.examenes.items()}
        }
        with open(archivo, "w") as f:
            json.dump(datos, f)
    

    def cargar_datos(self, archivo):
        try:
            with open(archivo, "r") as f:
                datos = json.load(f)

            # Cargar asignaturas
            for codigo, info in datos["asignaturas"].items():
                asignatura = Asignatura(info["nombre"], codigo, info["profesor"])
                self.asignaturas[codigo] = asignatura

            # Cargar alumnos
            for matricula, info in datos["alumnos"].items():
                alumno = Alumno(info["nombre"], matricula)
                self.alumnos[matricula] = alumno

            # Restaurar relaciones entre alumnos y asignaturas
            for matricula, info in datos["alumnos"].items():
                alumno = self.alumnos[matricula]
                for codigo_asignatura in info["asignaturas"]:
                    if codigo_asignatura in self.asignaturas:
                        asignatura = self.asignaturas[codigo_asignatura]
                        if alumno not in asignatura.alumnos:  # Asegurar que no se repitan
                            asignatura.agregar_alumno(alumno)
                        if asignatura not in alumno.asignaturas:
                            alumno.inscribirse(asignatura)

                # Restaurar calificaciones
                alumno.calificaciones = info["calificaciones"]

            # Restaurar calificaciones en los exámenes
            for nombre, info in datos["examenes"].items():
                if info["asignatura"] in self.asignaturas:
                    asignatura = self.asignaturas[info["asignatura"]]
                    examen = Examen(nombre, info["fecha"], asignatura)
                    examen.calificaciones = info["calificaciones"]
                    self.examenes[nombre] = examen

                print("Datos cargados exitosamente.")

        except FileNotFoundError:
            print("Archivo no encontrado. Se iniciará con datos vacíos.")


### **Interfaz de Usuario Simple (Consola):**
if __name__ == "__main__":
    gestor = GestorAcademico()
    gestor.cargar_datos("datos.json")
    while True:
        print("\nSistema de Gestión Académica")
        print("1. Agregar asignatura")
        print("2. Agregar alumno")
        print("3. Registrar examen")
        print("4. Agregar alumno a asignatura")
        print("5. Calificar examen")
        print("6. Listar datos")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre de la asignatura: ")
            codigo = input("Código de la asignatura: ")
            profesor = input("Nombre del profesor: ")
            gestor.agregar_asignatura(nombre, codigo, profesor)
        elif opcion == "2":
            nombre = input("Nombre del alumno: ")
            matricula = input("Número de matrícula: ")
            gestor.agregar_alumno(nombre, matricula)
        elif opcion == "3":
            nombre = input("Nombre del examen: ")
            fecha = input("Fecha del examen (YYYY-MM-DD): ")
            codigo = input("Código de la asignatura: ")
            gestor.registrar_examen(nombre, fecha, codigo)
        elif opcion == "4":
            matricula = input("Número de matrícula del alumno: ")
            codigo = input("Código de la asignatura: ")
            gestor.agregar_alumno_a_asignatura(matricula, codigo)
        elif opcion == "5":
            nombre_examen = input("Dame el nombre de un examen: ")
            if nombre_examen in gestor.examenes:
                gestor.asignar_calificaciones(gestor.examenes[nombre_examen])
            else:
                print("No existe el examen")
        elif opcion == "6":
            gestor.listar_datos()
        elif opcion == "7":
            gestor.guardar_datos("datos.json")
            print("Datos guardados. Saliendo...")
            break
        else:
            print("Opción no válida, intente nuevamente.")
