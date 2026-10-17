"""
CHALLENGE 11 - Buscador inteligente + Top resultados
- Los productos se guardan en un TRIE (búsqueda por prefijo).
- Un HEAP devuelve los K productos más populares que coinciden con el prefijo.
Cada producto: {"name": "air max", "popularity": 95}
"""


# ---------------- Estructura implementada ----------------
class MaxHeap:
    def __init__(self, prioridad=None):
        self.datos = []
        # Si no nos dan función de prioridad, se compara el valor directamente
        self.prioridad = prioridad if prioridad is not None else (lambda x: x)

    # ---------- helpers ----------
    def _padre(self, i):
        return (i - 1) // 2

    def _izq(self, i):
        return 2 * i + 1

    def _der(self, i):
        return 2 * i + 2

    def _mayor(self, i, j):
        """True si el elemento en i tiene MÁS prioridad que el de j."""
        return self.prioridad(self.datos[i]) > self.prioridad(self.datos[j])

    def _swap(self, i, j):
        self.datos[i], self.datos[j] = self.datos[j], self.datos[i]

    # ---------- reordenar ----------
    def _percolate_up(self, i):
        """Sube el elemento mientras sea más importante que su padre."""
        while i > 0 and self._mayor(i, self._padre(i)):
            self._swap(i, self._padre(i))
            i = self._padre(i)

    def _percolate_down(self, i):
        """Baja el elemento mientras alguno de sus hijos sea más importante."""
        n = len(self.datos)
        while True:
            mayor = i
            izq, der = self._izq(i), self._der(i)
            if izq < n and self._mayor(izq, mayor):
                mayor = izq
            if der < n and self._mayor(der, mayor):
                mayor = der
            if mayor == i:      # ya está en su lugar
                break
            self._swap(i, mayor)
            i = mayor

    # ---------- métodos públicos ----------
    def push(self, valor):
        """Inserta al final y lo sube a su lugar."""
        self.datos.append(valor)
        self._percolate_up(len(self.datos) - 1)

    def pop(self):
        """Saca el de MAYOR prioridad (la raíz) y reordena."""
        if self.is_empty():
            return None
        self._swap(0, len(self.datos) - 1)   # el último pasa a la raíz
        maximo = self.datos.pop()            # sacamos el que era la raíz
        if not self.is_empty():
            self._percolate_down(0)
        return maximo

    def peek(self):
        return None if self.is_empty() else self.datos[0]

    def heapify(self, lista):
        """Convierte una lista cualquiera en heap."""
        self.datos = list(lista)
        for i in range(len(self.datos) // 2 - 1, -1, -1):
            self._percolate_down(i)

    def top_k(self, k):
        """Devuelve los k de mayor prioridad SIN modificar el heap original."""
        copia = MaxHeap(self.prioridad)
        copia.datos = list(self.datos)
        resultado = []
        while len(resultado) < k and not copia.is_empty():
            resultado.append(copia.pop())
        return resultado

    def is_empty(self):
        return len(self.datos) == 0

    def size(self):
        return len(self.datos)

    def to_array(self):
        return list(self.datos)
# ---------------------------------------------------------



class NodoTrie:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.popularity = 0


class BuscadorProductos:
    def __init__(self):
        self.root = NodoTrie()

    def insert(self, name, popularity):
        actual = self.root
        for letra in name.lower():
            if letra not in actual.children:
                actual.children[letra] = NodoTrie()
            actual = actual.children[letra]
        actual.is_end_of_word = True
        actual.popularity = popularity

    def search(self, name):
        nodo = self._nodo(name)
        return nodo is not None and nodo.is_end_of_word

    def _nodo(self, texto):
        actual = self.root
        for letra in texto.lower():
            if letra not in actual.children:
                return None
            actual = actual.children[letra]
        return actual

    def _por_prefijo(self, prefijo):
        """Todos los productos que empiezan con el prefijo (DFS desde ese nodo)."""
        inicio = self._nodo(prefijo)
        encontrados = []
        if inicio is None:
            return encontrados
        pila = [(inicio, prefijo.lower())]
        while pila:
            nodo, palabra = pila.pop()
            if nodo.is_end_of_word:
                encontrados.append({"name": palabra, "popularity": nodo.popularity})
            for letra, hijo in nodo.children.items():
                pila.append((hijo, palabra + letra))
        return encontrados

    def search_top_k(self, prefijo, k):
        heap = MaxHeap(prioridad=lambda p: p["popularity"])
        heap.heapify(self._por_prefijo(prefijo))
        return [heap.pop() for _ in range(min(k, heap.size()))]


if __name__ == "__main__":
    tienda = BuscadorProductos()
    tienda.insert("air max", 90)
    tienda.insert("air force", 95)
    tienda.insert("air jordan", 85)
    tienda.insert("adidas boost", 80)
    tienda.insert("adidas samba", 88)
    tienda.insert("asics gel", 70)

    print('searchTopK("air", 2):')
    print(tienda.search_top_k("air", 2))   # -> air force (95), air max (90)

    while True:
        texto = input("\nBuscar (prefijo) o 'salir': ")
        if texto.strip().lower() == "salir":
            break
        try:
            k = int(input("¿Cuántos resultados (K)? "))
        except ValueError:
            k = 3
        resultados = tienda.search_top_k(texto, k)
        if not resultados:
            print("Sin resultados")
        for i, p in enumerate(resultados, start=1):
            print(f"  {i}. {p['name']} ⭐ {p['popularity']}")
