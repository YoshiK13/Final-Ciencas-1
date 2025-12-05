# Modulo Gestor de Sistema de Gestion de datos de estudiantes
# con Arboles AVL usando de archivos JSON para persistencia

import json
import os
from Logica.Arboles import NodoAVL
from Logica.Estudiante import Estudiante


class GestorEstudiantes:
    def __init__(self, archivo_json="Archivos/estudiantes.json", cargar_automatico=True):
        """
        Inicializa el gestor de estudiantes con un arbol AVL
        y configura el archivo JSON para persistencia.
        
        Args:
            archivo_json: Ruta del archivo JSON para persistencia
            cargar_automatico: Si es True, carga automáticamente los datos del JSON
        """
        self.raiz = None
        self.archivo_json = archivo_json
        self.total_estudiantes = 0
        
        # Crear directorio si no existe
        directorio = os.path.dirname(archivo_json)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        # Cargar datos existentes del archivo JSON si se solicita
        if cargar_automatico:
            self.cargar_desde_json()

    def agregar_estudiante(self, estudiante):
        """
        Agrega un estudiante al árbol AVL.
        """
        # No permitir IDs duplicados
        estudiante_existente = self.buscar_estudiante(estudiante.id_estudiante)
        if estudiante_existente is not None:
            return False

        nuevo_nodo = NodoAVL(estudiante)

        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            # agregar_hijo ya devuelve la nueva raíz correcta después del balanceo
            self.raiz = self.raiz.agregar_hijo(nuevo_nodo)

        self.total_estudiantes += 1
        return True

    def buscar_estudiante(self, id_estudiante, contar_pasos=False):
        """
        Busca un estudiante por su ID en el árbol AVL.
        
        Args:
            id_estudiante: ID del estudiante a buscar
            contar_pasos: Si es True, retorna (estudiante, pasos), sino solo estudiante
            
        Returns:
            Si contar_pasos=False: estudiante o None
            Si contar_pasos=True: tupla (estudiante, pasos)
        """
        if self.raiz is None:
            return (None, 0) if contar_pasos else None
        
        resultado, pasos = self._buscar_recursivo(self.raiz, id_estudiante)
        
        if contar_pasos:
            return resultado, pasos
        return resultado
    
    def _buscar_recursivo(self, nodo, id_estudiante, pasos=0):
        """
        Búsqueda recursiva en el árbol AVL por ID de estudiante.
        Retorna una tupla (estudiante, pasos) donde pasos es el número de nodos visitados.
        """
        if nodo is None:
            return None, pasos
        
        pasos += 1
        
        # Verificar que el nodo tenga un valor válido
        if nodo.valor is None or not hasattr(nodo.valor, 'id_estudiante'):
            return None, pasos
        
        if nodo.valor.id_estudiante == id_estudiante:
            return nodo.valor, pasos
        
        # Buscar en el subárbol izquierdo
        if id_estudiante < nodo.valor.id_estudiante:
            if nodo.hijos and len(nodo.hijos) > 0:
                return self._buscar_recursivo(nodo.hijos[0], id_estudiante, pasos)
            return None, pasos
        
        # Buscar en el subárbol derecho
        if nodo.hijos and len(nodo.hijos) > 1:
            return self._buscar_recursivo(nodo.hijos[1], id_estudiante, pasos)
        return None, pasos

    def eliminar_estudiante(self, id_estudiante):
        """
        Elimina un estudiante del arbol AVL por su ID.
        Retorna True si se elimino exitosamente, False si no se encontro.
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
        Recorrido in-order del arbol AVL para obtener estudiantes ordenados por ID.
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
        Solo guarda los datos de los estudiantes, no la estructura del árbol.
        El árbol AVL se reconstruirá automáticamente al cargar.
        """
        estudiantes = self.listar_estudiantes()
        
        # Usar el total de estudiantes listados para asegurar consistencia
        total_real = len(estudiantes)
        
        # Sincronizar el contador si hay discrepancia
        if self.total_estudiantes != total_real:
            print(f"[ADVERTENCIA] Sincronizando contador: {self.total_estudiantes} -> {total_real}")
            self.total_estudiantes = total_real
        
        datos = {
            "total_estudiantes": total_real,
            "estudiantes": [est.to_dict() for est in estudiantes]
        }
        
        try:
            with open(self.archivo_json, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar en JSON: {e}")
            return False

    def cargar_desde_json(self, mostrar_progreso=False):
        """
        Carga los estudiantes desde un archivo JSON al arbol AVL.
        Reconstruye el árbol AVL insertando cada estudiante individualmente.
        El árbol se auto-balancea durante la inserción.
        
        Args:
            mostrar_progreso: Si es True, muestra información detallada de la carga
            
        Returns:
            True si la carga fue exitosa, False en caso contrario
        """
        if not os.path.exists(self.archivo_json):
            if mostrar_progreso:
                print(f"Archivo {self.archivo_json} no existe")
            return False
        
        try:
            with open(self.archivo_json, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            estudiantes_data = datos.get("estudiantes", [])
            total_en_json = datos.get("total_estudiantes", len(estudiantes_data))
            
            if mostrar_progreso:
                print(f"Cargando {len(estudiantes_data)} estudiantes desde JSON...")
            
            # Reiniciar árbol y contador: el archivo JSON es la fuente de la carga
            self.raiz = None
            self.total_estudiantes = 0
            insertados = 0
            omitidos = 0

            for i, est_data in enumerate(estudiantes_data):
                try:
                    estudiante = Estudiante(
                        nombre=est_data["nombre"],
                        edad=est_data["edad"],
                        carrera=est_data["carrera"],
                        semestre=est_data["semestre"],
                        id_estudiante=est_data["id_estudiante"]
                    )
                    inserted = self.agregar_estudiante(estudiante)
                    if inserted:
                        insertados += 1
                        if mostrar_progreso and (i + 1) % 10 == 0:
                            print(f"  Cargados {insertados}/{len(estudiantes_data)}...")
                    else:
                        omitidos += 1
                        print(f"[ADVERTENCIA] Duplicado omitido: ID {estudiante.id_estudiante}")
                except Exception as e:
                    omitidos += 1
                    print(f"[ERROR] No se pudo cargar estudiante {i+1}: {e}")
                    continue

            if mostrar_progreso:
                print(f"\nCarga completada:")
                print(f"  - Insertados: {insertados}")
                print(f"  - Omitidos: {omitidos}")
                print(f"  - Total en árbol: {self.total_estudiantes}")
            
            # Verificar consistencia
            if self.total_estudiantes != insertados:
                print(f"[ERROR] Inconsistencia: contador={self.total_estudiantes}, insertados={insertados}")
                self.total_estudiantes = insertados

            return True
        except Exception as e:
            print(f"Error al cargar desde JSON: {e}")
            import traceback
            traceback.print_exc()
            return False

    def buscar_por_nombre(self, nombre, contar_pasos=False):
        """
        Busca estudiantes por nombre (búsqueda parcial).
        Utiliza búsqueda lineal O(n) sobre la lista ordenada.
        
        Args:
            nombre: Nombre o parte del nombre a buscar
            contar_pasos: Si es True, retorna (lista_estudiantes, pasos)
            
        Returns:
            Si contar_pasos=False: lista de estudiantes que coinciden
            Si contar_pasos=True: tupla (lista_estudiantes, pasos)
        """
        estudiantes = self.listar_estudiantes()
        coincidencias = []
        pasos = 0
        
        for est in estudiantes:
            pasos += 1
            if nombre.lower() in est.nombre.lower():
                coincidencias.append(est)
        
        if contar_pasos:
            return coincidencias, pasos
        return coincidencias

    def buscar_por_carrera(self, carrera, contar_pasos=False):
        """
        Busca estudiantes por carrera.
        Utiliza búsqueda lineal O(n) sobre la lista ordenada.
        
        Args:
            carrera: Carrera o parte de la carrera a buscar
            contar_pasos: Si es True, retorna (lista_estudiantes, pasos)
            
        Returns:
            Si contar_pasos=False: lista de estudiantes de la carrera
            Si contar_pasos=True: tupla (lista_estudiantes, pasos)
        """
        estudiantes = self.listar_estudiantes()
        coincidencias = []
        pasos = 0
        
        for est in estudiantes:
            pasos += 1
            if carrera.lower() in est.carrera.lower():
                coincidencias.append(est)
        
        if contar_pasos:
            return coincidencias, pasos
        return coincidencias

    def obtener_estadisticas(self):
        """
        Retorna estadisticas basicas del sistema.
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
