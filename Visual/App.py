# Implementacion del gestor de estudiantes con arboles AVL
# de manera visual por consola

# Integrantes:
# Davidson Esfleider Sanchez Gordillo - 20231020183
# Diego Felipe Diaz Roa - 20201020147
# Dania Lizeth Guzmán Triviño - 20221020061
# Joshoa Alarcon Sanchez - 20221020013

import os
from Logica.Estudiante import Estudiante
from Logica.Gestor import GestorEstudiantes
from Logica.Arboles import NodoAVL

# Códigos ANSI para colores
CYAN = "\033[36m"
RESET = "\033[0m"


class AplicacionGestorEstudiantes:
    def __init__(self):
        """Inicializa la aplicación con el gestor de estudiantes."""
        self.gestor = GestorEstudiantes()
        
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def pausar(self):
        """Pausa la ejecución hasta que el usuario presione Enter."""
        input("\nPresione Enter para continuar...")
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal de la aplicación."""
        print("\n" + "="*60)
        print("   SISTEMA DE GESTIÓN DE ESTUDIANTES - ÁRBOL AVL")
        print("="*60)
        print(f"Total de estudiantes registrados: {self.gestor.total_estudiantes}")
        print("\n1.  Agregar estudiante")
        print("2.  Buscar estudiante por ID")
        print("3.  Buscar estudiantes por nombre")
        print("4.  Buscar estudiantes por carrera")
        print("5.  Listar todos los estudiantes")
        print("6.  Actualizar datos de estudiante")
        print("7.  Eliminar estudiante")
        print("8.  Visualizar estructura del árbol AVL")
        print("9.  Mostrar estadísticas")
        print("10. Guardar datos en archivo")
        print("11. Cargar datos desde archivo")
        print("12. Limpiar todos los datos")
        print("0.  Salir")
        print("="*60)
    
    def agregar_estudiante_menu(self):
        """Menú para agregar un nuevo estudiante."""
        self.limpiar_pantalla()
        print("\n" + "="*60)
        print("   AGREGAR NUEVO ESTUDIANTE")
        print("="*60)
        
        try:
            id_estudiante = int(input("\nID del estudiante: "))
            
            # Verificar si ya existe
            if self.gestor.buscar_estudiante(id_estudiante) is not None:
                print(f"\n[ERROR] Ya existe un estudiante con el ID {id_estudiante}")
                self.pausar()
                return
            
            nombre = input("Nombre completo: ").strip()
            if not nombre:
                print("\n[ERROR] El nombre no puede estar vacío")
                self.pausar()
                return
            
            edad = int(input("Edad: "))
            if edad <= 0:
                print("\n[ERROR] La edad debe ser mayor a 0")
                self.pausar()
                return
            
            carrera = input("Carrera: ").strip()
            if not carrera:
                print("\n[ERROR] La carrera no puede estar vacía")
                self.pausar()
                return
            
            semestre = int(input("Semestre: "))
            if semestre <= 0:
                print("\n[ERROR] El semestre debe ser mayor a 0")
                self.pausar()
                return
            
            # Crear y agregar estudiante
            estudiante = Estudiante(nombre, edad, carrera, semestre, id_estudiante)
            
            if self.gestor.agregar_estudiante(estudiante):
                print(f"\n[OK] Estudiante agregado exitosamente!")
                print(f"   {estudiante}")
            else:
                print(f"\n[ERROR] No se pudo agregar el estudiante")
                
        except ValueError:
            print("\n[ERROR] Entrada inválida. Verifique los datos numéricos.")
        except Exception as e:
            print(f"\n[ERROR] Error inesperado: {e}")
        
        self.pausar()
    
    def buscar_estudiante_por_id_menu(self):
        """Menú para buscar un estudiante por ID."""
        self.limpiar_pantalla()
        print("\n" + "="*60)
        print("   BUSCAR ESTUDIANTE POR ID")
        print("="*60)
        
        try:
            id_estudiante = int(input("\nIngrese el ID del estudiante: "))
            estudiante, pasos = self.gestor.buscar_estudiante(id_estudiante, contar_pasos=True)
            
            if estudiante:
                print("\n[OK] Estudiante encontrado:")
                print(f"\n{estudiante}")
                print(f"\n[INFO] Búsqueda completada en {pasos} paso(s)")
                print(f"[INFO] Complejidad del árbol AVL: O(log n)")
            else:
                print(f"\n[ERROR] No se encontró ningún estudiante con el ID {id_estudiante}")
                print(f"[INFO] Nodos visitados durante la búsqueda: {pasos}")
                
        except ValueError:
            print("\n[ERROR] El ID debe ser un número entero")
        except Exception as e:
            print(f"\n[ERROR] {e}")
        
        self.pausar()
    
    def buscar_por_nombre_menu(self):
        """Menú para buscar estudiantes por nombre."""
        self.limpiar_pantalla()
        print("\n" + "="*60)
        print("   BUSCAR ESTUDIANTES POR NOMBRE")
        print("="*60)
        
        nombre = input("\nIngrese el nombre o parte del nombre: ").strip()
        
        if not nombre:
            print("\n[ERROR] Debe ingresar un nombre")
            self.pausar()
            return
        
        estudiantes, pasos = self.gestor.buscar_por_nombre(nombre, contar_pasos=True)
        
        if estudiantes:
            print(f"\n[OK] Se encontraron {len(estudiantes)} estudiante(s):")
            for est in estudiantes:
                print(f"\n{est}")
            print(f"\n[INFO] Búsqueda lineal completada en {pasos} paso(s)")
            print(f"[INFO] Complejidad: O(n) - Se revisaron todos los {pasos} estudiantes")
            if len(estudiantes) == 1:
                print(f"[INFO] Nota: Búsqueda por ID sería más eficiente: O(log n)")
        else:
            print(f"\n[ERROR] No se encontraron estudiantes con el nombre '{nombre}'")
            print(f"[INFO] Se revisaron {pasos} estudiante(s) en total")
        
        self.pausar()
    
    def buscar_por_carrera_menu(self):
        """Menú para buscar estudiantes por carrera."""
        self.limpiar_pantalla()
        print("\n" + "="*60)
        print("   BUSCAR ESTUDIANTES POR CARRERA")
        print("="*60)
        
        carrera = input("\nIngrese la carrera: ").strip()
        
        if not carrera:
            print("\n[ERROR] Debe ingresar una carrera")
            self.pausar()
            return
        
        estudiantes, pasos = self.gestor.buscar_por_carrera(carrera, contar_pasos=True)
        
        if estudiantes:
            print(f"\n[OK] Se encontraron {len(estudiantes)} estudiante(s) en {carrera}:")
            for est in estudiantes:
                print(f"\n{est}")
            print(f"\n[INFO] Búsqueda lineal completada en {pasos} paso(s)")
            print(f"[INFO] Complejidad: O(n) - Se revisaron todos los {pasos} estudiantes")
        else:
            print(f"\n[ERROR] No se encontraron estudiantes en la carrera '{carrera}'")
            print(f"[INFO] Se revisaron {pasos} estudiante(s) en total")
        
        self.pausar()
    
    def listar_estudiantes_menu(self):
        """Menú para listar todos los estudiantes."""
        self.limpiar_pantalla()
        print("\n" + "="*60)
        print("   LISTA DE TODOS LOS ESTUDIANTES")
        print("="*60)
        
        estudiantes = self.gestor.listar_estudiantes()
        
        if estudiantes:
            print(f"\n[OK] Total de estudiantes: {len(estudiantes)}")
            print("\n(Ordenados por ID)")
            for i, est in enumerate(estudiantes, 1):
                print(f"\n{i}. {est}")
        else:
            print("\n[INFO] No hay estudiantes registrados en el sistema")
        
        self.pausar()
    
    def actualizar_estudiante_menu(self):
        """Menú para actualizar los datos de un estudiante."""
        self.limpiar_pantalla()
        print("\n" + "="*60)
        print("   ACTUALIZAR DATOS DE ESTUDIANTE")
        print("="*60)
        
        try:
            id_estudiante = int(input("\nIngrese el ID del estudiante a actualizar: "))
            estudiante, pasos = self.gestor.buscar_estudiante(id_estudiante, contar_pasos=True)
            
            if not estudiante:
                print(f"[INFO] Búsqueda realizada en {pasos} paso(s)")
            
            if not estudiante:
                print(f"\n[ERROR] No se encontró ningún estudiante con el ID {id_estudiante}")
                self.pausar()
                return
            
            print("\nDatos actuales:")
            print(f"{estudiante}")
            
            print("\n(Presione Enter para mantener el valor actual)")
            
            nombre = input(f"\nNombre [{estudiante.nombre}]: ").strip()
            edad_str = input(f"Edad [{estudiante.edad}]: ").strip()
            carrera = input(f"Carrera [{estudiante.carrera}]: ").strip()
            semestre_str = input(f"Semestre [{estudiante.semestre}]: ").strip()
            
            # Preparar datos para actualizar
            datos_actualizar = {}
            
            if nombre:
                datos_actualizar['nombre'] = nombre
            
            if edad_str:
                try:
                    edad = int(edad_str)
                    if edad > 0:
                        datos_actualizar['edad'] = edad
                    else:
                        print("\n[ADVERTENCIA] Edad inválida, se mantendrá el valor actual")
                except ValueError:
                    print("\n[ADVERTENCIA] Edad inválida, se mantendrá el valor actual")
            
            if carrera:
                datos_actualizar['carrera'] = carrera
            
            if semestre_str:
                try:
                    semestre = int(semestre_str)
                    if semestre > 0:
                        datos_actualizar['semestre'] = semestre
                    else:
                        print("\n[ADVERTENCIA] Semestre inválido, se mantendrá el valor actual")
                except ValueError:
                    print("\n[ADVERTENCIA] Semestre inválido, se mantendrá el valor actual")
            
            if datos_actualizar:
                if self.gestor.actualizar_estudiante(id_estudiante, **datos_actualizar):
                    print("\n[OK] Estudiante actualizado exitosamente!")
                    estudiante_actualizado = self.gestor.buscar_estudiante(id_estudiante)
                    print(f"\nNuevos datos:")
                    print(f"{estudiante_actualizado}")
                else:
                    print("\n[ERROR] Error al actualizar el estudiante")
            else:
                print("\n[INFO] No se realizaron cambios")
                
        except ValueError:
            print("\n[ERROR] El ID debe ser un número entero")
        except Exception as e:
            print(f"\n[ERROR] {e}")
        
        self.pausar()
    
    def eliminar_estudiante_menu(self):
        """Menú para eliminar un estudiante."""
        self.limpiar_pantalla()
        print("\n" + "="*60)
        print("   ELIMINAR ESTUDIANTE")
        print("="*60)
        
        try:
            id_estudiante = int(input("\nIngrese el ID del estudiante a eliminar: "))
            estudiante, pasos = self.gestor.buscar_estudiante(id_estudiante, contar_pasos=True)
            
            print(f"[INFO] Búsqueda realizada en {pasos} paso(s)")
            
            if not estudiante:
                print(f"\n[ERROR] No se encontró ningún estudiante con el ID {id_estudiante}")
                self.pausar()
                return
            
            print("\nDatos del estudiante:")
            print(f"{estudiante}")
            
            confirmacion = input("\n[ADVERTENCIA] ¿Está seguro de eliminar este estudiante? (s/n): ").strip().lower()
            
            if confirmacion == 's':
                if self.gestor.eliminar_estudiante(id_estudiante):
                    print("\n[OK] Estudiante eliminado exitosamente")
                else:
                    print("\n[ERROR] Error al eliminar el estudiante")
            else:
                print("\n[INFO] Operación cancelada")
                
        except ValueError:
            print("\n[ERROR] El ID debe ser un número entero")
        except Exception as e:
            print(f"\n[ERROR] {e}")
        
        self.pausar()
    
    def visualizar_arbol_menu(self):
        """Menú para visualizar la estructura del árbol AVL."""
        self.limpiar_pantalla()
        print("\n" + "="*60)
        print("   VISUALIZACIÓN DEL ÁRBOL AVL")
        print("="*60)
        
        if self.gestor.raiz is None:
            print("\n[INFO] El árbol está vacío")
        else:
            print(f"\nÁrbol AVL con factores de balance mostrados en {CYAN}cian{RESET}.")
            print(f"Total de nodos: {self.gestor.total_estudiantes}\n")
            self._mostrar_arbol_recursivo(self.gestor.raiz, "", None)
        
        self.pausar()
    
    def _mostrar_arbol_recursivo(self, nodo, prefijo, es_izquierdo):
        """Función recursiva para mostrar el árbol de forma visual."""
        if nodo is None:
            return
        
        # Formatear la representación del nodo con ID y factor de balanceo
        if isinstance(nodo, NodoAVL):
            # Mostrar ID del estudiante y factor de balanceo en cian
            nombre_corto = nodo.valor.nombre[:15] + "..." if len(nodo.valor.nombre) > 15 else nodo.valor.nombre
            repr_nodo = f"ID:{nodo.valor.id_estudiante} ({nombre_corto}) [{CYAN}FB:{nodo.factor_balance}{RESET}]"
        else:
            repr_nodo = f"ID:{nodo.valor.id_estudiante} ({nodo.valor.nombre})"
        
        if es_izquierdo is None:
            # Es la raíz
            print(f"{repr_nodo}")
        elif es_izquierdo:
            print(f"{prefijo}├── {repr_nodo}")
        else:
            print(f"{prefijo}└── {repr_nodo}")
        
        # Preparar el nuevo prefijo para los hijos
        if es_izquierdo is None:
            nuevo_prefijo = ""
        elif es_izquierdo:
            nuevo_prefijo = prefijo + "│   "
        else:
            nuevo_prefijo = prefijo + "    "
        
        # Mostrar hijos (primero izquierdo, luego derecho)
        if nodo.hijos[0] is not None or nodo.hijos[1] is not None:
            if nodo.hijos[0] is not None:
                self._mostrar_arbol_recursivo(nodo.hijos[0], nuevo_prefijo, True)
            else:
                print(f"{nuevo_prefijo}├──  ⃠")
            
            if nodo.hijos[1] is not None:
                self._mostrar_arbol_recursivo(nodo.hijos[1], nuevo_prefijo, False)
            else:
                print(f"{nuevo_prefijo}└──  ⃠")
    
    def mostrar_estadisticas_menu(self):
        """Menú para mostrar estadísticas del sistema."""
        self.limpiar_pantalla()
        print("\n" + "="*60)
        print("   ESTADÍSTICAS DEL SISTEMA")
        print("="*60)
        
        stats = self.gestor.obtener_estadisticas()
        
        print(f"\nTotal de estudiantes: {stats['total']}")
        print(f"Edad promedio: {stats['edad_promedio']} años")
        
        if stats['carreras']:
            print("\nEstudiantes por carrera:")
            for carrera, cantidad in sorted(stats['carreras'].items()):
                print(f"   - {carrera}: {cantidad} estudiante(s)")
        else:
            print("\n[INFO] No hay estudiantes registrados")
        
        self.pausar()
    
    def guardar_datos_menu(self):
        """Menú para guardar los datos en archivo JSON."""
        self.limpiar_pantalla()
        print("\n" + "="*60)
        print("   GUARDAR DATOS EN ARCHIVO")
        print("="*60)
        
        print(f"\nArchivo: {self.gestor.archivo_json}")
        confirmacion = input("\n¿Desea guardar los datos actuales? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            if self.gestor.guardar_en_json():
                print("\n[OK] Datos guardados exitosamente")
            else:
                print("\n[ERROR] Error al guardar los datos")
        else:
            print("\n[INFO] Operación cancelada")
        
        self.pausar()
    
    def cargar_datos_menu(self):
        """Menú para cargar datos desde archivo JSON."""
        self.limpiar_pantalla()
        print("\n" + "="*60)
        print("   CARGAR DATOS DESDE ARCHIVO")
        print("="*60)
        
        print(f"\nArchivo: {self.gestor.archivo_json}")
        print("\n[ADVERTENCIA] Esto reemplazará todos los datos actuales")
        print("[INFO] El árbol AVL se reconstruirá automáticamente desde los datos")
        confirmacion = input("\n¿Desea continuar? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            print("\nCargando datos...")
            if self.gestor.cargar_desde_json(mostrar_progreso=True):
                print("\n[OK] Datos cargados exitosamente")
                print(f"Total de estudiantes en el árbol: {self.gestor.total_estudiantes}")
            else:
                print("\n[ERROR] Error al cargar los datos o el archivo no existe")
        else:
            print("\n[INFO] Operación cancelada")
        
        self.pausar()
    
    def limpiar_datos_menu(self):
        """Menú para limpiar todos los datos del sistema."""
        self.limpiar_pantalla()
        print("\n" + "="*60)
        print("   LIMPIAR TODOS LOS DATOS")
        print("="*60)
        
        print(f"\n[ADVERTENCIA] Se eliminarán todos los {self.gestor.total_estudiantes} estudiantes")
        print("[ADVERTENCIA] Esta acción no se puede deshacer")
        confirmacion = input("\n¿Está seguro? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            segunda_confirmacion = input("Escriba 'CONFIRMAR' para proceder: ").strip()
            if segunda_confirmacion == 'CONFIRMAR':
                self.gestor.limpiar_datos()
                print("\n[OK] Todos los datos han sido eliminados")
            else:
                print("\n[INFO] Operación cancelada")
        else:
            print("\n[INFO] Operación cancelada")
        
        self.pausar()
    
    def ejecutar(self):
        """Ejecuta el bucle principal de la aplicación."""
        while True:
            self.limpiar_pantalla()
            self.mostrar_menu_principal()
            
            try:
                opcion = input("\nSeleccione una opción: ").strip()
                
                if opcion == '1':
                    self.agregar_estudiante_menu()
                elif opcion == '2':
                    self.buscar_estudiante_por_id_menu()
                elif opcion == '3':
                    self.buscar_por_nombre_menu()
                elif opcion == '4':
                    self.buscar_por_carrera_menu()
                elif opcion == '5':
                    self.listar_estudiantes_menu()
                elif opcion == '6':
                    self.actualizar_estudiante_menu()
                elif opcion == '7':
                    self.eliminar_estudiante_menu()
                elif opcion == '8':
                    self.visualizar_arbol_menu()
                elif opcion == '9':
                    self.mostrar_estadisticas_menu()
                elif opcion == '10':
                    self.guardar_datos_menu()
                elif opcion == '11':
                    self.cargar_datos_menu()
                elif opcion == '12':
                    self.limpiar_datos_menu()
                elif opcion == '0':
                    self.limpiar_pantalla()
                    print("\n" + "="*60)
                    print("   ¡Gracias por usar el Sistema de Gestión de Estudiantes!")
                    print("="*60 + "\n")
                    break
                else:
                    print("\n[ERROR] Opción inválida. Por favor, seleccione una opción del menú.")
                    self.pausar()
                    
            except KeyboardInterrupt:
                self.limpiar_pantalla()
                print("\n\n[INFO] Programa interrumpido por el usuario")
                print("   ¡Hasta pronto!\n")
                break
            except Exception as e:
                print(f"\n[ERROR] Error inesperado: {e}")
                self.pausar()