# Modulo Gestor de Sistema de Gestion de datos de estudiantes
# con Arboles AVL usando de archivos JSON para persistencia

import json
import os
from Logica.Arboles import NodoAVL
from Logica.Estudiante import Estudiante


class GestorEstudiantes:
    def __init__(self, archivo_json="Archivos/estudiantes.json"):
        """
        Inicializa el gestor de estudiantes con un árbol AVL
        y configura el archivo JSON para persistencia.
        """
        self.raiz = None
        self.archivo_json = archivo_json
        self.total_estudiantes = 0
        
        # Crear directorio si no existe
        directorio = os.path.dirname(archivo_json)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        # Cargar datos existentes del archivo JSON
        self.cargar_desde_json()

    def agregar_estudiante(self, estudiante):
        """
        Agrega un estudiante al árbol AVL.
        """
        nuevo_nodo = NodoAVL(estudiante)
        
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            self.raiz = self.raiz.agregar_hijo(nuevo_nodo)
            # Actualizar la raíz después del balanceo
            while self.raiz.padre is not None:
                self.raiz = self.raiz.padre
        
        self.total_estudiantes += 1
        return True

    def buscar_estudiante(self, id_estudiante):
        """
        Busca un estudiante por su ID en el árbol AVL.
        Retorna el estudiante si lo encuentra, None en caso contrario.
        """
        if self.raiz is None:
            return None
        
        return self._buscar_recursivo(self.raiz, id_estudiante)
    
    def _buscar_recursivo(self, nodo, id_estudiante):
        """
        Búsqueda recursiva en el árbol AVL por ID de estudiante.
        """
        if nodo is None:
            return None
        
        if nodo.valor.id_estudiante == id_estudiante:
            return nodo.valor
        
        # Buscar en el subárbol izquierdo
        if id_estudiante < nodo.valor.id_estudiante:
            return self._buscar_recursivo(nodo.hijos[0], id_estudiante)
        
        # Buscar en el subárbol derecho
        return self._buscar_recursivo(nodo.hijos[1], id_estudiante)

    def eliminar_estudiante(self, id_estudiante):
        """
        Elimina un estudiante del árbol AVL por su ID.
        Retorna True si se eliminó exitosamente, False si no se encontró.
        """
        if self.raiz is None:
            return False
        
        # Crear un estudiante temporal para la comparación
        estudiante_temp = Estudiante("", 0, "", 0, id_estudiante)
        
        nueva_raiz, eliminado = self.raiz.eliminar_nodo(estudiante_temp)
        
        if eliminado:
            self.raiz = nueva_raiz
            if self.raiz is not None:
                self.raiz.padre = None
            self.total_estudiantes -= 1
            return True
        
        return False

    def listar_estudiantes(self):
        """
        Retorna una lista de todos los estudiantes en orden (in-order traversal).
        """
        estudiantes = []
        self._inorden_recursivo(self.raiz, estudiantes)
        return estudiantes
    
    def _inorden_recursivo(self, nodo, lista):
        """
        Recorrido in-order del árbol AVL para obtener estudiantes ordenados por ID.
        """
        if nodo is None:
            return
        
        self._inorden_recursivo(nodo.hijos[0], lista)
        lista.append(nodo.valor)
        self._inorden_recursivo(nodo.hijos[1], lista)

    def actualizar_estudiante(self, id_estudiante, **kwargs):
        """
        Actualiza los datos de un estudiante existente.
        Los campos actualizables son: nombre, edad, carrera, semestre.
        """
        estudiante = self.buscar_estudiante(id_estudiante)
        
        if estudiante is None:
            return False
        
        # Actualizar los campos proporcionados
        if "nombre" in kwargs:
            estudiante.nombre = kwargs["nombre"]
        if "edad" in kwargs:
            estudiante.edad = kwargs["edad"]
        if "carrera" in kwargs:
            estudiante.carrera = kwargs["carrera"]
        if "semestre" in kwargs:
            estudiante.semestre = kwargs["semestre"]
        
        return True

    def guardar_en_json(self):
        """
        Guarda todos los estudiantes en un archivo JSON.
        """
        estudiantes = self.listar_estudiantes()
        datos = {
            "total_estudiantes": self.total_estudiantes,
            "estudiantes": [est.to_dict() for est in estudiantes]
        }
        
        try:
            with open(self.archivo_json, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar en JSON: {e}")
            return False

    def cargar_desde_json(self):
        """
        Carga los estudiantes desde un archivo JSON al árbol AVL.
        """
        if not os.path.exists(self.archivo_json):
            return False
        
        try:
            with open(self.archivo_json, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            estudiantes_data = datos.get("estudiantes", [])
            
            for est_data in estudiantes_data:
                estudiante = Estudiante(
                    nombre=est_data["nombre"],
                    edad=est_data["edad"],
                    carrera=est_data["carrera"],
                    semestre=est_data["semestre"],
                    id_estudiante=est_data["id_estudiante"]
                )
                self.agregar_estudiante(estudiante)
            
            return True
        except Exception as e:
            print(f"Error al cargar desde JSON: {e}")
            return False

    def buscar_por_nombre(self, nombre):
        """
        Busca estudiantes por nombre (búsqueda parcial).
        Retorna una lista de estudiantes que coinciden.
        """
        estudiantes = self.listar_estudiantes()
        return [est for est in estudiantes if nombre.lower() in est.nombre.lower()]

    def buscar_por_carrera(self, carrera):
        """
        Busca estudiantes por carrera.
        Retorna una lista de estudiantes de la carrera especificada.
        """
        estudiantes = self.listar_estudiantes()
        return [est for est in estudiantes if carrera.lower() in est.carrera.lower()]

    def obtener_estadisticas(self):
        """
        Retorna estadísticas básicas del sistema.
        """
        estudiantes = self.listar_estudiantes()
        
        if not estudiantes:
            return {
                "total": 0,
                "edad_promedio": 0,
                "carreras": {}
            }
        
        edad_promedio = sum(est.edad for est in estudiantes) / len(estudiantes)
        
        carreras = {}
        for est in estudiantes:
            carreras[est.carrera] = carreras.get(est.carrera, 0) + 1
        
        return {
            "total": self.total_estudiantes,
            "edad_promedio": round(edad_promedio, 2),
            "carreras": carreras
        }

    def limpiar_datos(self):
        """
        Elimina todos los estudiantes del árbol.
        """
        self.raiz = None
        self.total_estudiantes = 0

    def __str__(self):
        """
        Representación en string del gestor.
        """
        return f"GestorEstudiantes(Total: {self.total_estudiantes}, Archivo: {self.archivo_json})"
