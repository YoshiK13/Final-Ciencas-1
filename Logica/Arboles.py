# Modulo de Arboles Binarios y AVL

# --------------Clase base para los arboles -----------------
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []
        self.padre = None

    def agregar_hijo(self, hijo):
        hijo.padre = self
        self.hijos.append(hijo)

    def eliminar_nodo(self, hijo):
        hijo.padre = None
        self.hijos.remove(hijo)

# --------------Clase para arboles binarios -----------------
class NodoBinario(Nodo):

    def __init__(self, valor):
        super().__init__(valor)
        self.hijos = [None, None] # Inicializa con dos hijos vacios

    def agregar_hijo(self, hijo):
        # Si el valor del hijo es menor o igual al nodo actual, va al hijo izquierdo (indice 0)
        # Si es mayor, va al hijo derecho (indice 1)
        # Y se hace de manera recursiva
        
        # Comparación segura para objetos
        try:
            hijo_comparable = hijo.valor.id_estudiante if hasattr(hijo.valor, 'id_estudiante') else hijo.valor
            nodo_comparable = self.valor.id_estudiante if hasattr(self.valor, 'id_estudiante') else self.valor
        except:
            hijo_comparable = hijo.valor
            nodo_comparable = self.valor
        
        # Insercion izquierda
        if hijo_comparable <= nodo_comparable:

            if self.hijos[0] is None:
                self.hijos[0] = hijo
                hijo.padre = self

            else:
                # Dejar que el subarbol hijo gestione la inserción y recoger
                # la posible nueva raíz del subárbol (por rotaciones)
                nuevo_sub = self.hijos[0].agregar_hijo(hijo)

                if nuevo_sub is not None:
                    self.hijos[0] = nuevo_sub
                    nuevo_sub.padre = self

        # Inserción derecha
        else:

            if self.hijos[1] is None:
                self.hijos[1] = hijo
                hijo.padre = self

            else:
                nuevo_sub = self.hijos[1].agregar_hijo(hijo)

                if nuevo_sub is not None:
                    self.hijos[1] = nuevo_sub
                    nuevo_sub.padre = self

        # Devolver la raiz actual del subarbol para que el padre pueda reasignarla
        return self

    # Se busca entre los hijos de manera recursiva segun el valor
    def buscar_nodo(self, valor):
        nodos_encontrados = []
        
        # Comparación segura para objetos
        try:
            valor_comparable = valor.id_estudiante if hasattr(valor, 'id_estudiante') else valor
            nodo_comparable = self.valor.id_estudiante if hasattr(self.valor, 'id_estudiante') else self.valor
        except:
            valor_comparable = valor
            nodo_comparable = self.valor
    
        if nodo_comparable == valor_comparable:
            nodos_encontrados.append(self)

        # Buscar en el subarbol izquierdo si el valor es menor o igual
        # (los valores iguales se insertan a la izquierda)
        if self.hijos[0] is not None and valor_comparable <= nodo_comparable:
            nodos_encontrados.extend(self.hijos[0].buscar_nodo(valor))

        # Buscar en el subarbol derecho si el valor es mayor
        if self.hijos[1] is not None and valor_comparable > nodo_comparable:
            nodos_encontrados.extend(self.hijos[1].buscar_nodo(valor))
    
        return nodos_encontrados

    # Funcion nesesaria para eliminar nodos con dos hijos, busca el sucesor
    def encontrar_maximo_izq(self):
        nodo_actual = self

        while nodo_actual.hijos[1] is not None:
            nodo_actual = nodo_actual.hijos[1]

        return nodo_actual

    def eliminar_nodo(self, valor):
        nodos_encontrados = self.buscar_nodo(valor)

        # Si no se encontro el nodo, retornar None
        if not nodos_encontrados:
            return None
        
        # Tomar el primer nodo encontrado
        nodo_eliminar = nodos_encontrados[0]

        # Caso 1: Nodo sin hijos
        if nodo_eliminar.hijos[0] is None and nodo_eliminar.hijos[1] is None:

            if nodo_eliminar.padre is not None:

                if nodo_eliminar.padre.hijos[0] == nodo_eliminar:
                    nodo_eliminar.padre.hijos[0] = None

                else:
                    nodo_eliminar.padre.hijos[1] = None
                nodo_eliminar.padre = None
            
            return nodo_eliminar

        # Caso 2: Nodo con un solo hijo
        elif nodo_eliminar.hijos[0] is None or nodo_eliminar.hijos[1] is None:
            hijo = nodo_eliminar.hijos[0] if nodo_eliminar.hijos[0] is not None else nodo_eliminar.hijos[1]
            
            if nodo_eliminar.padre is not None:

                if nodo_eliminar.padre.hijos[0] == nodo_eliminar:
                    nodo_eliminar.padre.hijos[0] = hijo

                else:
                    nodo_eliminar.padre.hijos[1] = hijo

                hijo.padre = nodo_eliminar.padre
            
            else:
                hijo.padre = None # Si el nodo a eliminar es la raiz, su hijo se convierte en la nueva raiz
            
            nodo_eliminar.padre = None
            return nodo_eliminar

        # Caso 3: Nodo con dos hijos
        else:
            # Encontrar el maximo en el subarbol izquierdo
            sucesor = nodo_eliminar.hijos[0].encontrar_maximo_izq()
            valor_sucesor = sucesor.valor
            self.eliminar_nodo(sucesor.valor)
            nodo_eliminar.valor = valor_sucesor
            
            return nodo_eliminar
        
# --------------Clase para el arbol avl -----------------
class NodoAVL(NodoBinario):
    def __init__(self, valor):
        super().__init__(valor)
        self.altura = 1  # Altura del nodo para balanceo
        self.factor_balance = 0  # Factor de balanceo

    # Refrescar altura y factor de balanceo del nodo
    def actualizar_altura_balanceo(self):
        altura_izquierda = self.hijos[0].altura if self.hijos[0] is not None else 0
        altura_derecha = self.hijos[1].altura if self.hijos[1] is not None else 0
        self.altura = 1 + max(altura_izquierda, altura_derecha)
        self.factor_balance = altura_izquierda - altura_derecha
    
    # Rotaciones para balancear el arbol:
    # Rotacion derecha
    def rotar_derecha(self):
        nueva_raiz = self.hijos[0]
        self.hijos[0] = nueva_raiz.hijos[1]

        if nueva_raiz.hijos[1] is not None:
            nueva_raiz.hijos[1].padre = self

        nueva_raiz.hijos[1] = self
        nueva_raiz.padre = self.padre
        self.padre = nueva_raiz
        self.actualizar_altura_balanceo()
        nueva_raiz.actualizar_altura_balanceo()

        return nueva_raiz

    # Rotacion izquierda
    def rotar_izquierda(self):
        nueva_raiz = self.hijos[1]
        self.hijos[1] = nueva_raiz.hijos[0]

        if nueva_raiz.hijos[0] is not None:
            nueva_raiz.hijos[0].padre = self

        nueva_raiz.hijos[0] = self
        nueva_raiz.padre = self.padre
        self.padre = nueva_raiz
        self.actualizar_altura_balanceo()
        nueva_raiz.actualizar_altura_balanceo()

        return nueva_raiz

    # Balancear el nodo
    def balancear(self):
        self.actualizar_altura_balanceo()

        # Rotacion derecha
        if self.factor_balance > 1:
            if self.hijos[0] is not None and self.hijos[0].factor_balance < 0:
                self.hijos[0] = self.hijos[0].rotar_izquierda()

            return self.rotar_derecha()
        
        # Rotacion izquierda
        if self.factor_balance < -1:
            if self.hijos[1] is not None and self.hijos[1].factor_balance > 0:
                self.hijos[1] = self.hijos[1].rotar_derecha()

            return self.rotar_izquierda()
        
        return self

    # Agregar un hijo y balancear el árbol
    def agregar_hijo(self, hijo):
        super().agregar_hijo(hijo)
        return self.balancear()
    
    def eliminar_nodo(self, valor):
        # Comparación segura para objetos
        try:
            valor_comparable = valor.id_estudiante if hasattr(valor, 'id_estudiante') else valor
            nodo_comparable = self.valor.id_estudiante if hasattr(self.valor, 'id_estudiante') else self.valor
        except:
            valor_comparable = valor
            nodo_comparable = self.valor

        # Búsqueda recursiva por el valor
        if valor_comparable < nodo_comparable:
            if self.hijos[0] is None:
                return (self, False)

            nuevo_izq, eliminado = self.hijos[0].eliminar_nodo(valor)
            self.hijos[0] = nuevo_izq
            if nuevo_izq is not None:
                nuevo_izq.padre = self

            if not eliminado:
                return (self, False)

        elif valor_comparable > nodo_comparable:
            if self.hijos[1] is None:
                return (self, False)

            nuevo_der, eliminado = self.hijos[1].eliminar_nodo(valor)
            self.hijos[1] = nuevo_der
            if nuevo_der is not None:
                nuevo_der.padre = self

            if not eliminado:
                return (self, False)

        else:
            # Encontramos el nodo a eliminar
            # Caso 1: sin hijos
            if self.hijos[0] is None and self.hijos[1] is None:
                return (None, True)

            # Caso 2: un solo hijo
            if self.hijos[0] is None:
                derecho = self.hijos[1]
                derecho.padre = self.padre
                return (derecho, True)

            if self.hijos[1] is None:
                izquierdo = self.hijos[0]
                izquierdo.padre = self.padre
                return (izquierdo, True)

            # Caso 3: dos hijos (se usa el sucesor por la izquierda)
            sucesor = self.hijos[0].encontrar_maximo_izq()
            self.valor = sucesor.valor
            # Eliminar el sucesor en el subarbol izquierdo
            nuevo_izq, _ = self.hijos[0].eliminar_nodo(sucesor.valor)
            self.hijos[0] = nuevo_izq

            if nuevo_izq is not None:
                nuevo_izq.padre = self

        # Se hace rebalanceo tras la eliminacion, para mantener asegurar el equilibrio AVL
        nueva_raiz = self.balancear()
        return (nueva_raiz, True)