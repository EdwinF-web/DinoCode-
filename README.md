# División del Trabajo en Equipo — Parser de DinoCode (versión paralela)

> Este documento son las **órdenes del equipo**. Léelo completo una vez, y después vuelve solo a la sección de tu persona.

---

## 1. Cómo vamos a trabajar (idea general)

Somos **7 personas**. Seis programan al mismo tiempo, **cada una en su propio archivo**, sin esperar a las demás. La **Persona 7** recoge todo al final, lo une y escribe `main.py`.

Para que esto funcione, el **día 1** la Persona 1 entrega un **contrato**: un conjunto de reglas y archivos base que todos usamos. Gracias a eso, cada quien sabe cómo se llaman las cosas y qué devuelve cada función, aunque la parte de otro compañero todavía no exista.

**Regla de oro:** nadie modifica el contrato sin avisar a todo el equipo.

---

## 2. El contrato del día 1 (explicado paso a paso)

### 2.1 ¿Qué es y por qué existe?

Imagina que la Persona 3 escribe `term()` (la suma) y necesita llamar a `factor()` (que escribe la Persona 2). Si `factor()` aún no existe, la Persona 3 no sabe:

- cómo se llama el nodo que representa una suma,
- cómo se pide el siguiente token,
- qué devuelve `factor()`,
- cómo se reporta un error.

Si cada quien inventa sus propios nombres, **al juntar el código nada va a encajar**. El contrato evita eso: se acuerdan los nombres **antes** de programar.

> **Sin este contrato nadie arranca. La Persona 1 lo entrega antes de que termine el día 1.**

### 2.2 Qué entrega la Persona 1 (3 archivos)

| Archivo | Para qué sirve | Analogía |
|---------|----------------|----------|
| `ast_nodes.py` | Define las "piezas" del árbol (suma, número, if, for...) | Las piezas de LEGO |
| `parser_base.py` | Herramientas para leer tokens y reportar errores | La caja de herramientas |
| `GRAMATICA.md` | Las reglas del lenguaje y la firma de cada método | El manual de instrucciones |

---

### 2.3 `ast_nodes.py` — las piezas del árbol

**Qué es el AST:** el resultado final del parser. Es un árbol que representa el programa. Por ejemplo, `2 + 3 * 4` se convierte en:

```
BinaryOp(+)
├── Number(2)
└── BinaryOp(*)
    ├── Number(3)
    └── Number(4)
```

**Qué debe hacer la Persona 1:** crear una clase `dataclass` por cada tipo de nodo. **Todos** los nodos llevan `line` y `col` (línea y columna donde empiezan), para poder reportar errores con ubicación.

Ejemplo de cómo debe verse:

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Number:
    value: float
    line: int
    col: int

@dataclass
class BinaryOp:
    left: object      # otro nodo
    op: str           # "+", "-", "*", "==", "y", "o", ...
    right: object     # otro nodo
    line: int
    col: int
```

**Lista mínima de nodos** (la Persona 1 puede ajustar nombres el día 1, pero una vez publicados **ya no se cambian**):

| Grupo | Nodos |
|-------|-------|
| Expresiones | `Number`, `String`, `Boolean`, `Identifier`, `UnaryOp`, `BinaryOp` |
| Sentencias simples | `LetStmt`, `AssignStmt`, `ConstStmt`, `PrintStmt`, `IncrementStmt`, `ExprStmt` |
| Control de flujo | `Block`, `IfStmt`, `ForStmt` |
| Raíz | `Program` |

**Orden para todos:** usa **solo** estos nodos. No inventes nodos nuevos. Si crees que falta uno, pídelo a la Persona 1.

---

### 2.4 `parser_base.py` — la caja de herramientas

Contiene la clase `ParserBase`. Guarda la lista de tokens y la posición actual. **Todos los demás módulos usan estos métodos**; nadie recorre la lista de tokens "a mano".

| Método | Qué hace | Ejemplo de uso |
|--------|----------|----------------|
| `peek()` | Mira el token actual **sin consumirlo** | `if self.peek().type == "PLUS":` |
| `advance()` | Consume el token actual y devuelve el que consumió | `tok = self.advance()` |
| `check(tipo)` | Pregunta si el token actual es de ese tipo (no consume) | `if self.check("RPAREN"):` |
| `match(*tipos)` | Si el token actual es de alguno de esos tipos, **lo consume** y devuelve `True`; si no, devuelve `False` | `while self.match("PLUS", "MINUS"):` |
| `expect(tipo, msg)` | Exige un token de ese tipo. Si está, lo consume y lo devuelve. Si no, reporta error con `msg` | `self.expect("RPAREN", "Se esperaba ')'")` |
| `error(msg, token)` | Registra un error sintáctico con **línea y columna** del token | `self.error("Operando faltante", tok)` |
| `synchronize()` | Después de un error, salta tokens hasta un punto seguro (inicio de la siguiente sentencia) | Lo usa la recuperación de errores |

Esqueleto que la Persona 1 debe completar:

```python
class ParserBase:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []          # lista de errores encontrados

    def peek(self): ...
    def advance(self): ...
    def check(self, tipo): ...
    def match(self, *tipos): ...
    def expect(self, tipo, msg): ...
    def error(self, msg, token): ...   # guarda (msg, token.line, token.col)
    def synchronize(self): ...
```

> **Importante:** la Persona 1 debe revisar el lexer y escribir en `GRAMATICA.md` la **lista exacta de nombres de tokens** (por ejemplo `NUMBER`, `STRING`, `IDENT`, `PLUS`, `INDENT`, `DEDENT`...). Todos usan esos nombres, tal cual.

---

### 2.5 `GRAMATICA.md` — el manual del equipo

Debe contener:

1. La **gramática BNF** de DinoCode.
2. La **tabla de precedencia** de operadores (de menor a mayor).
3. La **lista de tokens** del lexer.
4. La **firma de cada método**: nombre, qué recibe y qué devuelve.

Ejemplo de la tabla de firmas:

| Método | Recibe | Devuelve | Dueño |
|--------|--------|----------|-------|
| `primary()` | nada | `Number`, `String`, `Boolean`, `Identifier` o la expresión entre paréntesis | Persona 2 |
| `unary()` | nada | `UnaryOp` o lo que devuelva `primary()` | Persona 2 |
| `factor()` | nada | `BinaryOp` (`*`, `/`, `%`) o lo que devuelva `unary()` | Persona 2 |
| `term()` | nada | `BinaryOp` (`+`, `-`) o lo que devuelva `factor()` | Persona 3 |
| `comparison()` | nada | `BinaryOp` o lo que devuelva `term()` | Persona 3 |
| `conjunction()` | nada | `BinaryOp` (`y`) o lo que devuelva `comparison()` | Persona 3 |
| `disjunction()` | nada | `BinaryOp` (`o`) o lo que devuelva `conjunction()` | Persona 3 |
| `expression()` | nada | cualquier nodo de expresión | Persona 3 |
| `let_stmt()` | nada | `LetStmt` | Persona 4 |
| `assign_stmt()` | nada | `AssignStmt` | Persona 4 |
| `const_stmt()` | nada | `ConstStmt` | Persona 4 |
| `print_stmt()` | nada | `PrintStmt` | Persona 4 |
| `increment_stmt()` | nada | `IncrementStmt` | Persona 4 |
| `expr_stmt()` | nada | `ExprStmt` | Persona 4 |
| `block()` | nada | `Block` (lista de sentencias) | Persona 5 |
| `if_stmt()` | nada | `IfStmt` | Persona 5 |
| `for_stmt()` | nada | `ForStmt` | Persona 6 |
| `statement()` | nada | cualquier nodo de sentencia | Persona 7 |
| `program()` | nada | `Program` | Persona 7 |

Con esta tabla, la Persona 3 sabe que `self.factor()` existirá y qué devolverá, **aunque la Persona 2 no haya terminado**.

---

## 3. Cómo trabajar sin esperar: mixins y stubs

### 3.1 Mixin

Cada persona escribe su parte como una **clase mixin**: una clase que **no hereda de nada** y que usa `self.peek()`, `self.match()`, `self.factor()`, etc. como si ya existieran. Al final, la Persona 7 las junta en una sola clase `Parser`.

```python
# parser_expr_alto.py  (Persona 3)
from ast_nodes import BinaryOp

class ExprAltoMixin:
    def term(self):
        left = self.factor()                 # lo implementa la Persona 2
        while self.match("PLUS", "MINUS"):
            op = self.tokens[self.pos - 1]
            right = self.factor()
            left = BinaryOp(left, op.value, right, op.line, op.col)
        return left
```

**Reglas del mixin:**
- **No** importes los archivos de otros compañeros.
- **No** dupliques métodos de otra persona.
- Para lo que no es tuyo, llama a `self.metodo()` y confía en la tabla de firmas.

### 3.2 Stub (parser simulado para pruebas)

Un **stub** es una clase falsa que sustituye lo que aún no existe, solo para tus pruebas. Ejemplo: para probar `term()` sin tener `factor()`:

```python
# tests/test_precedencia.py  (Persona 3)
from parser_base import ParserBase
from parser_expr_alto import ExprAltoMixin
from ast_nodes import Number

class ParserDePrueba(ParserBase, ExprAltoMixin):
    def factor(self):                 # STUB: solo lee un número
        tok = self.advance()
        return Number(float(tok.value), tok.line, tok.col)
```

Así pruebas tu código con tokens escritos a mano, sin esperar a nadie.

---

## 4. Órdenes por persona

> Cada persona entrega: **código + pruebas**. Un módulo sin pruebas **no cuenta como terminado**.

---

### Persona 1 — AST, gramática y base del parser
**Complejidad:** ⭐⭐ | **Depende de:** nadie

**Tu prioridad es entregar el contrato el día 1.** Todos esperan por ti al inicio.

**Qué debes hacer, en orden:**
1. Revisar el lexer y anotar los nombres exactos de los tokens.
2. Escribir `ast_nodes.py` con todos los nodos (ver 2.3).
3. Escribir `parser_base.py` con `ParserBase` (ver 2.4).
4. Escribir `GRAMATICA.md` con BNF, precedencia, tokens y tabla de firmas (ver 2.5).
5. **Avisar al equipo:** el contrato está listo (fin del día 1).
6. Después: escribir la tabla de errores sintácticos y crear `ejemplos/` con **10 programas válidos y 5 inválidos** (cada inválido debe indicar qué error se espera y en qué línea).
7. Revisar el código de la Persona 2.

**Entregables:** `ast_nodes.py`, `parser_base.py`, `GRAMATICA.md`, `ejemplos/`, `tests/test_base.py`

---

### Persona 2 — Expresiones de bajo nivel
**Complejidad:** ⭐⭐⭐ | **Depende de:** el contrato (día 1)

**Qué debes hacer:**
1. `primary()`: números, cadenas, booleanos, identificadores y paréntesis `( expresion )`. Para el paréntesis llama a `self.expression()` (lo hace la Persona 3).
2. `unary()`: negación aritmética (`-x`) y lógica. Debe permitir encadenar (`--x`). Llama a `self.primary()`.
3. `factor()`: `*`, `/`, `%`, asociativo a la izquierda. Llama a `self.unary()`.
4. Errores con línea y columna para: paréntesis sin cerrar, operando faltante (`3 *`), token inesperado.
5. Pruebas con tokens escritos a mano.

**Entregables:** `parser_expr_bajo.py` (`class ExprBajoMixin`), `tests/test_expr_bajo.py`

---

### Persona 3 — Expresiones de alto nivel
**Complejidad:** ⭐⭐⭐ | **Depende de:** el contrato (día 1)

**Qué debes hacer:**
1. `term()`: `+` y `-`. Llama a `self.factor()`.
2. `comparison()`: `==`, `!=`, `<`, `>`, `<=`, `>=`. Llama a `self.term()`.
3. `conjunction()`: operador `y`. Llama a `self.comparison()`.
4. `disjunction()`: operador `o`. Llama a `self.conjunction()`.
5. `expression()`: punto de entrada, llama a `self.disjunction()`.
6. Pruebas de **precedencia** (`2 + 3 * 4` ≠ `(2 + 3) * 4`) y **asociatividad** (`10 - 3 - 2` = `(10 - 3) - 2`). Usa un stub de `factor()`.

**Entregables:** `parser_expr_alto.py` (`class ExprAltoMixin`), `tests/test_precedencia.py`

---

### Persona 4 — Sentencias simples
**Complejidad:** ⭐⭐⭐ | **Depende de:** el contrato (día 1)

**Qué debes hacer:**
1. `let_stmt()`: `huevo IDENT <- expresion`.
2. `assign_stmt()`: `IDENT <- expresion`.
3. `const_stmt()`: `huevo IDENT = expresion`.
4. `print_stmt()`: `rugir` con paréntesis y sin paréntesis.
5. `increment_stmt()`: `IDENT ++`.
6. `expr_stmt()`: una expresión suelta como sentencia.
7. Todas llaman a `self.expression()` (lo hace la Persona 3). En tus pruebas usa un stub de `expression()`.
8. Errores con línea y columna (por ejemplo, `huevo <- 5` sin nombre).

**Entregables:** `parser_sentencias.py` (`class SentenciasMixin`), `tests/test_sentencias.py`

---

### Persona 5 — Bloques y condicionales
**Complejidad:** ⭐⭐⭐⭐ | **Depende de:** el contrato (día 1)

**Qué debes hacer:**
1. `block()`: `:` → `NEWLINE` → `INDENT` → sentencias → `DEDENT`. Cada sentencia se obtiene con `self.statement()` (lo hace la Persona 7).
2. `if_stmt()`: `si_ve` / `o_ve` (puede haber varios) / `no_ve` (opcional) / `fin_si`. La condición se obtiene con `self.expression()`.
3. Pruebas con anidamiento de **2 y 3 niveles**. En tus pruebas usa un stub de `statement()` y de `expression()`.
4. Errores con línea y columna (falta `:`, falta `INDENT`, falta `fin_si`).

**Entregables:** `parser_bloques_if.py` (`class BloquesIfMixin`), `tests/test_bloques_if.py`

---

### Persona 6 — Ciclo `for` y recuperación de errores
**Complejidad:** ⭐⭐⭐⭐ | **Depende de:** el contrato (día 1)

**Qué debes hacer:**
1. `for_stmt()`: `cazar IDENT desde expr hasta expr avanzar expr` + bloque + `fin_caza`. Usa `self.expression()` y `self.block()`.
2. **Recuperación de errores:** que el parser **no se detenga en el primer error**. Implementa el modo pánico: al detectar un error, registrarlo, llamar a `self.synchronize()` y continuar con la siguiente sentencia. (Puedes ampliar `synchronize()` en tu mixin si coordinas con la Persona 1.)
3. Casos límite:
   - `EOF` inesperado,
   - `INDENT` sin `DEDENT`,
   - falta `fin_si` o `fin_caza`.
4. Pruebas de `for` anidado y de recuperación (un archivo con 3 errores debe reportar los 3).

**Entregables:** `parser_for_recuperacion.py` (`class ForRecuperacionMixin`), `tests/test_for.py`, `tests/test_recuperacion.py`

---

### Persona 7 — Recopilación, integración y `main.py`
**Complejidad:** ⭐⭐⭐⭐⭐ | **Depende de:** todos (al final)

**Mientras esperas los módulos (días 1 a 4):**
1. Escribe `program()` y `statement()` (el despachador: según el token actual decide si llama a `let_stmt`, `if_stmt`, `for_stmt`, etc.). Pruébalos con stubs.
2. Prepara `main.py`: leer archivo → lexer → tokens → parser → AST.
3. Escribe `tests/test_integracion.py` (10 programas válidos) y `tests/test_errores_sintacticos.py` (5 inválidos) usando los `ejemplos/` de la Persona 1.

**Cuando lleguen los módulos (días 5 a 7):**
4. Arma `parser.py`:
   ```python
   class Parser(ParserBase, ExprBajoMixin, ExprAltoMixin,
                SentenciasMixin, BloquesIfMixin, ForRecuperacionMixin):
       def program(self): ...
       def statement(self): ...
   ```
5. Ejecuta todos los tests. Si algo falla, **reporta el bug en `reporte_bugs.md`** con un caso reproducible y avisa al dueño del módulo.
6. Resuelve conflictos de firmas o precedencia entre módulos.
7. Implementa el manejo global de errores sintácticos.
8. Deja `main.py` funcionando de punta a punta.

**Entregables:** `parser.py`, `main.py`, `tests/test_integracion.py`, `tests/test_errores_sintacticos.py`, `reporte_bugs.md`

---

## 5. Resumen

| Persona | Tarea | Archivo | Complejidad |
|---------|-------|---------|-------------|
| 1 | AST, BNF, base y ejemplos | `ast_nodes.py`, `parser_base.py`, `GRAMATICA.md` | ⭐⭐ |
| 2 | `primary`, `unary`, `factor` | `parser_expr_bajo.py` | ⭐⭐⭐ |
| 3 | `term` … `expression` | `parser_expr_alto.py` | ⭐⭐⭐ |
| 4 | Sentencias simples | `parser_sentencias.py` | ⭐⭐⭐ |
| 5 | `block`, `if` | `parser_bloques_if.py` | ⭐⭐⭐⭐ |
| 6 | `for`, recuperación de errores | `parser_for_recuperacion.py` | ⭐⭐⭐⭐ |
| 7 | Integración, `main.py`, pruebas | `parser.py`, `main.py` | ⭐⭐⭐⭐⭐ |

---

## 6. Reglas de coordinación

1. **Un archivo por persona**, sin archivos compartidos, para evitar conflictos de git.
2. El contrato del día 1 (nodos, firmas, `ParserBase`) **no se cambia** sin avisar a todos.
3. Cada módulo es un mixin que **no importa** a los demás; usa `self.metodo()` y se prueba con stubs.
4. El lexer no se modifica. Cualquier token nuevo se pide a la Persona 7.
5. Un módulo sin pruebas no cuenta como terminado.
6. Revisión en anillo: 1 → 2 → 3 → 4 → 5 → 6 → 1. La Persona 7 revisa el código de todos durante la integración.
7. Si tienes una duda sobre qué devuelve un método ajeno, **la respuesta está en la tabla de firmas** de `GRAMATICA.md`. Si no está ahí, pregunta a la Persona 1.

---

## 7. Cronograma

| Día | Qué pasa |
|-----|----------|
| 1 | Persona 1 entrega el contrato. Todos empiezan en paralelo. |
| 2–4 | Desarrollo individual con stubs y pruebas. |
| 5 | Entrega de módulos 2 a 6 a Persona 7. Revisión en anillo. |
| 6 | Persona 7 integra, ejecuta los tests y reporta bugs. Los dueños corrigen. |
| 7 | Integración final, `main.py` funcionando y documentación completa. |

---

## 8. Criterios de aceptación

- [ ] Los 10 programas válidos producen AST sin errores.
- [ ] Los 5 programas inválidos producen errores con línea y columna.
- [ ] El parser sigue después del primer error (recuperación).
- [ ] `main.py` ejecuta archivo → tokens → AST.
- [ ] Todos los tests pasan en conjunto.
- [ ] No hay reglas duplicadas ni nodos inventados.
- [ ] La documentación está completa.
