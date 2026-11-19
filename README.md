# DinoCode-
El desarrollo de un mini lenguaje de programacion para la UTM, utilizando los conocimiento teoricos obtenidos dentro de la materia de Teoria de la comptacion


# División del Trabajo en Equipo — Parser de DinoCode (versión paralela)

**Idea central:** 6 personas programan cada una en **su propio archivo**, sin esperarse entre sí. La Persona 7 recopila todo, integra y escribe `main.py`.

Para que nadie bloquee a nadie, el día 1 se fija un **contrato común** (lo entrega la Persona 1). Cada módulo se escribe como un **mixin**: una clase que usa los métodos base (`peek`, `advance`, `match`, `expect`, `error`) y llama a los métodos de otros niveles (`self.unary()`, `self.expression()`, `self.block()`) sin importar quién los implemente. Cada persona prueba con un parser simulado (stub) que reemplaza los métodos ajenos.

---

## Contrato del día 1 (Persona 1, obligatorio para todos)

- `ast_nodes.py`: todos los nodos como `dataclass`, con `line` y `col`.
- `parser_base.py`: clase `ParserBase` con `peek()`, `advance()`, `match(*tipos)`, `check(tipo)`, `expect(tipo, msg)`, `error(msg, token)` (reporta línea y columna) y `synchronize()`.
- `GRAMATICA.md`: la BNF con las firmas de cada método (nombre, qué recibe y qué nodo devuelve).

Sin este contrato nadie arranca. Se entrega **antes de que termine el día 1**.

---

## Tareas individuales

### Persona 1 — AST, gramática y base del parser
**Complejidad:** ⭐⭐

**Qué hace:**
- Escribir la gramática BNF y la precedencia de operadores.
- Definir los nodos en `ast_nodes.py`.
- Implementar `ParserBase` (helpers de tokens y reporte de errores).
- Escribir la tabla de errores sintácticos.
- Crear `ejemplos/` con 10 programas válidos y 5 inválidos.

**Entregables:** `ast_nodes.py`, `parser_base.py`, `GRAMATICA.md`, `ejemplos/`, `tests/test_base.py`

**Depende de:** nadie. **Después de entregar el contrato** (día 1), revisa el código de la Persona 2.

---

### Persona 2 — Expresiones de bajo nivel
**Complejidad:** ⭐⭐⭐

**Qué hace:**
- `primary()`: números, cadenas, booleanos, identificadores y paréntesis.
- `unary()`: negación aritmética y lógica.
- `factor()`: `*`, `/`, `%`.
- Manejar paréntesis sin cerrar y operandos faltantes, con línea y columna.

**Entregables:** `parser_expr_bajo.py` (`ExprBajoMixin`), `tests/test_expr_bajo.py`

---

### Persona 3 — Expresiones de alto nivel
**Complejidad:** ⭐⭐⭐

**Qué hace:**
- `term()`: `+`, `-`.
- `comparison()`: `==`, `!=`, `<`, `>`, `<=`, `>=`.
- `conjunction()`: `y`.
- `disjunction()`: `o`.
- `expression()` como punto de entrada.
- Pruebas de precedencia y asociatividad (llamando a `self.factor()` simulado).

**Entregables:** `parser_expr_alto.py` (`ExprAltoMixin`), `tests/test_precedencia.py`

---

### Persona 4 — Sentencias simples
**Complejidad:** ⭐⭐⭐

**Qué hace:**
- `let_stmt()`: `huevo IDENT <- expresion`.
- `assign_stmt()`: `IDENT <- expresion`.
- `const_stmt()`: `huevo IDENT = expresion`.
- `print_stmt()`: `rugir` con y sin paréntesis.
- `increment_stmt()`: `IDENT ++`.
- `expr_stmt()`: expresión suelta.
- Pruebas con `expression()` simulado.

**Entregables:** `parser_sentencias.py` (`SentenciasMixin`), `tests/test_sentencias.py`

---

### Persona 5 — Bloques y condicionales
**Complejidad:** ⭐⭐⭐⭐

**Qué hace:**
- `block()`: `:`, `NEWLINE`, `INDENT`, sentencias, `DEDENT`.
- `if_stmt()`: `si_ve` / `o_ve` / `no_ve` / `fin_si`.
- Pruebas con anidamiento de 2 y 3 niveles (llamando a `statement()` simulado).

**Entregables:** `parser_bloques_if.py` (`BloquesIfMixin`), `tests/test_bloques_if.py`

---

### Persona 6 — Ciclo `for` y recuperación de errores
**Complejidad:** ⭐⭐⭐⭐

**Qué hace:**
- `for_stmt()`: `cazar desde … hasta … avanzar …` / `fin_caza`.
- Recuperación de errores: `synchronize()` y modo pánico para que el parser no aborte en el primer error.
- Manejar casos límite: `EOF` inesperado, `INDENT` sin `DEDENT`, falta de `fin_si` o `fin_caza`.
- Pruebas de `for` anidado y de recuperación.

**Entregables:** `parser_for_recuperacion.py` (`ForRecuperacionMixin`), `tests/test_for.py`, `tests/test_recuperacion.py`

---

### Persona 7 — Recopilación, integración y `main.py`
**Complejidad:** ⭐⭐⭐⭐⭐

**Qué hace:**
- Implementar `program()` y `statement()` (despachador principal).
- Armar `parser.py` con `class Parser(ParserBase, ExprBajoMixin, ExprAltoMixin, SentenciasMixin, BloquesIfMixin, ForRecuperacionMixin)`.
- Resolver conflictos de firmas y precedencia entre módulos.
- Implementar el manejo global de errores sintácticos.
- Escribir `main.py`: archivo → lexer → tokens → parser → AST.
- Escribir `tests/test_integracion.py` (10 válidos) y `tests/test_errores_sintacticos.py` (5 inválidos).
- Reportar bugs a cada dueño con casos reproducibles en `reporte_bugs.md`.

**Entregables:** `parser.py`, `main.py`, `tests/test_integracion.py`, `tests/test_errores_sintacticos.py`, `reporte_bugs.md`

**Mientras espera los módulos** (días 1 a 4): prepara `main.py` con el lexer, escribe los tests de integración con los ejemplos de la Persona 1 y arma el esqueleto de `program()`/`statement()` con métodos simulados.

---

## Resumen

| Persona | Tarea | Archivo | Complejidad |
|---------|-------|---------|-------------|
| 1 | AST, BNF, base y ejemplos | `ast_nodes.py`, `parser_base.py` | ⭐⭐ |
| 2 | `primary`, `unary`, `factor` | `parser_expr_bajo.py` | ⭐⭐⭐ |
| 3 | `term` … `expression` | `parser_expr_alto.py` | ⭐⭐⭐ |
| 4 | Sentencias simples | `parser_sentencias.py` | ⭐⭐⭐ |
| 5 | `block`, `if` | `parser_bloques_if.py` | ⭐⭐⭐⭐ |
| 6 | `for`, recuperación de errores | `parser_for_recuperacion.py` | ⭐⭐⭐⭐ |
| 7 | Integración, `main.py`, pruebas | `parser.py`, `main.py` | ⭐⭐⭐⭐⭐ |

---

## Reglas de coordinación

1. **Un archivo por persona**, sin archivos compartidos, para evitar conflictos de git.
2. El contrato del día 1 (nodos, firmas, `ParserBase`) **no se cambia** sin avisar a todos.
3. Cada módulo es un mixin que **no importa** a los demás; usa `self.metodo()` y se prueba con stubs.
4. El lexer no se modifica. Cualquier token nuevo se pide a la Persona 7.
5. Un módulo sin pruebas no cuenta como terminado.
6. Revisión en anillo: 1 → 2 → 3 → 4 → 5 → 6 → 1. La Persona 7 revisa el código de todos durante la integración.

---

## Cronograma

| Día | Qué pasa |
|-----|----------|
| 1 | Persona 1 entrega el contrato. Todos empiezan en paralelo. |
| 2–4 | Desarrollo individual con stubs y pruebas. |
| 5 | Entrega de módulos 2 a 6 a Persona 7. Revisión en anillo. |
| 6 | Persona 7 integra, ejecuta los tests y reporta bugs. Los dueños corrigen. |
| 7 | Integración final, `main.py` funcionando y documentación completa. |

---

## Criterios de aceptación

- [ ] Los 10 programas válidos producen AST sin errores.
- [ ] Los 5 programas inválidos producen errores con línea y columna.
- [ ] El parser sigue después del primer error (recuperación).
- [ ] `main.py` ejecuta archivo → tokens → AST.
- [ ] Todos los tests pasan en conjunto.
- [ ] No hay reglas duplicadas ni nodos inventados.
- [ ] La documentación está completa.
