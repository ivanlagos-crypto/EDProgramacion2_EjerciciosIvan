"""
CHALLENGE 04 - Pila de libros
Cada libro tiene: nombre, ISBN, autor y editorial.
Se llena con datos de prueba, hay un "formulario" para agregar libros
y se imprime la pila en pantalla (el de arriba primero).
"""


# ---------------- Estructura implementada ----------------
class Nodo:
    def __init__(self, valor):
        self.valor = valor      # el dato que guarda el nodo
        self.siguiente = None   # la "flecha" al nodo que está debajo


class Pila:
    def __init__(self):
        self.tope = None    # nodo de arriba (None = pila vacía)
        self.tamano = 0

    def push(self, valor):
        """Agrega un elemento ENCIMA de la pila."""
        nuevo = Nodo(valor)
        nuevo.siguiente = self.tope   # el nuevo apunta al que era el tope
        self.tope = nuevo             # ahora el nuevo es el tope
        self.tamano += 1

    def pop(self):
        """Saca y devuelve el elemento de ARRIBA. Si está vacía devuelve None."""
        if self.is_empty():
            return None
        nodo = self.tope
        self.tope = nodo.siguiente    # el de abajo pasa a ser el tope
        self.tamano -= 1
        return nodo.valor

    def peek(self):
        """Devuelve el elemento de arriba SIN sacarlo."""
        return None if self.is_empty() else self.tope.valor

    def is_empty(self):
        return self.tope is None

    def size(self):
        return self.tamano

    def to_list(self):
        """Devuelve los elementos desde el tope hacia abajo (del más reciente al más antiguo)."""
        elementos = []
        actual = self.tope
        while actual is not None:
            elementos.append(actual.valor)
            actual = actual.siguiente
        return elementos

    def print(self):
        for valor in self.to_list():
            print(valor)
# ---------------------------------------------------------



def mostrar(pila):
    print("\n📚 PILA DE LIBROS (arriba = último agregado)")
    if pila.is_empty():
        print("   (vacía)")
    for i, libro in enumerate(pila.to_list()):
        marca = "⬆ TOPE" if i == 0 else ""
        print(f"   | {libro['nombre']} — {libro['autor']} ({libro['editorial']}) ISBN {libro['isbn']} {marca}")
    print(f"   Total: {pila.size()} libros")


def main():
    libros = Pila()
    datos_prueba = [
        {"nombre": "Cien años de soledad", "isbn": "978-0307474728", "autor": "Gabriel García Márquez", "editorial": "Sudamericana"},
        {"nombre": "Clean Code", "isbn": "978-0132350884", "autor": "Robert C. Martin", "editorial": "Prentice Hall"},
        {"nombre": "Estructuras de datos en Python", "isbn": "978-1118290279", "autor": "Michael Goodrich", "editorial": "Wiley"},
        {"nombre": "El principito", "isbn": "978-0156012195", "autor": "Antoine de Saint-Exupéry", "editorial": "Reynal & Hitchcock"},
    ]
    for libro in datos_prueba:
        libros.push(libro)

    while True:
        mostrar(libros)
        print("\n[1] Agregar libro (push)  [2] Sacar libro de arriba (pop)  [3] Ver libro de arriba (peek)  [0] Salir")
        op = input("> ").strip()
        if op == "1":
            print("--- Formulario nuevo libro ---")
            libro = {
                "nombre": input("Nombre: "),
                "isbn": input("ISBN: "),
                "autor": input("Autor: "),
                "editorial": input("Editorial: "),
            }
            libros.push(libro)
            print("✅ Libro agregado encima de la pila")
        elif op == "2":
            libro = libros.pop()
            print("Sacado:", libro["nombre"] if libro else "la pila está vacía")
        elif op == "3":
            libro = libros.peek()
            print("Arriba está:", libro["nombre"] if libro else "nada")
        elif op == "0":
            break


if __name__ == "__main__":
    main()
