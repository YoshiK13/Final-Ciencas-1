# Clase de la informacion del estudiante

class Estudiante:
    def __init__(self, nombre, edad, carrera, semestre, id_estudiante):
        self.nombre = nombre
        self.edad = edad
        self.carrera = carrera
        self.semestre = semestre
        self.id_estudiante = id_estudiante

    def __repr__(self):
        return f"Estudiante(ID: {self.id_estudiante}, Nombre: {self.nombre}, Edad: {self.edad}, Carrera: {self.carrera}, Semestre: {self.semestre})"
    
    def to_dict(self):
        return {
            "id_estudiante": self.id_estudiante,
            "nombre": self.nombre,
            "edad": self.edad,
            "carrera": self.carrera,
            "semestre": self.semestre
        }