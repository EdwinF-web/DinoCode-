# DinoCode-
El desarrollo de un mini lenguaje de programacion para la UTM, utilizando los conocimiento teoricos obtenidos dentro de la materia de Teoria de la comptacion



# División del Trabajo en Equipo — Parser de DinoCode

## Distribución de roles y tareas

El equipo está conformado por **7 integrantes**. Cada uno tiene una tarea específica y un entregable concreto. Las tareas están ordenadas de **menor a mayor complejidad**.

---

### Persona 2 — AST y gramática BNF
**Complejidad:** ⭐

**Qué debe hacer:**
- Escribir la gramática BNF de DinoCode.
- Definir todos los nodos del AST en `ast_nodes.py` como `dataclass`.
- Escribir la tabla de errores sintácticos.
- Crear 10 programas válidos y 5 inválidos en `ejemplos/`.
- Documentar la precedencia de operadores.

**Entregables:**
- `ast_nodes.py`
- `GRAMATICA.md`
- `ejemplos/` (10 válidos + 5 inválidos)

**Depende de:** nadie. **Bloquea a:** todos.

---

### Persona 3 — Parser de expresiones: primario, unario y factor
**Complejidad:** ⭐⭐

**Qué debe hacer:**
- Implementar `primary()`: números, cadenas, booleanos, identificadores y paréntesis.
- Implementar `unary()`: negación aritmética y lógica.
- Implementar `factor()`: multiplicación, división y módulo.
- Escribir pruebas con tokens escritos a mano.
- Reportar errores con línea y columna.

**Entregables:**
- `parser_expresiones.py` con `primary()`, `unary()` y `factor()`
- `tests/test_parser_expresiones.py`

**Depende de:** Persona 2. **Bloquea a:** Persona 4.

---

### Persona 4 — Parser de expresiones: suma, comparación y lógicos
**Complejidad:** ⭐⭐

**Qué debe hacer:**
- Implementar `term()`: suma y resta.
- Implementar `comparison()`: `==`, `!=`, `<`, `>`, `<=`, `>=`.
- Implementar `conjunction()`: operador `y`.
- Implementar `disjunction()`: operador `o`.
- Implementar `expression()` como punto de entrada.
- Escribir pruebas de precedencia.

**Entregables:**
- Contribución a `parser_expresiones.py` (revisión cruzada con Persona 3)
- `tests/test_precedencia.py`

**Depende de:** Persona 3. **Bloquea a:** Personas 5 y 6.

---

### Persona 5 — Parser de sentencias simples
**Complejidad:** ⭐⭐⭐

**Qué debe hacer:**
- Implementar `let_stmt()`: `huevo IDENT <- expresion`.
- Implementar `assign_stmt()`: `IDENT <- expresion`.
- Implementar `const_stmt()`: `huevo IDENT = expresion`.
- Implementar `print_stmt()`: `rugir` con y sin paréntesis.
- Implementar `increment_stmt()`: `IDENT ++`.
- Implementar `expr_stmt()`: expresión suelta.
- Escribir pruebas con simulacros.

**Entregables:**
- `parser_sentencias_simples.py`
- `tests/test_sentencias_simples.py`

**Depende de:** Persona 4. **Bloquea a:** Persona 6.

---

### Persona 6 — Parser de bloques y control de flujo
**Complejidad:** ⭐⭐⭐⭐

**Qué debe hacer:**
- Implementar `block()`: `:`, `NEWLINE`, `INDENT`, `DEDENT`.
- Implementar `if_stmt()`: `si_ve` / `no_ve` / `o_ve` / `fin_si`.
- Implementar `for_stmt()`: `cazar desde … hasta … avanzar …` / `fin_caza`.
- Implementar recuperación de errores en bloques.
- Escribir pruebas con bloques anidados (2 y 3 niveles).

**Entregables:**
- `parser_control.py`
- `tests/test_control_flujo.py`

**Depende de:** Persona 5. **Bloquea a:** Persona 7 y Persona 1.

---

### Persona 7 — Pruebas de integración y errores
**Complejidad:** ⭐⭐⭐⭐

**Qué debe hacer:**
- Escribir `tests/test_integracion.py` con los 10 programas válidos de Persona 2.
- Escribir `tests/test_errores_sintacticos.py` con los 5 programas inválidos.
- Escribir `tests/test_recuperacion.py` para verificar que el parser no aborta en el primer error.
- Probar casos límite: `EOF` inesperado, `INDENT` sin `DEDENT`, paréntesis sin cerrar.
- Reportar errores a Personas 3 a 6 con casos reproducibles.

**Entregables:**
- `tests/test_integracion.py`
- `tests/test_errores_sintacticos.py`
- `tests/test_recuperacion.py`
- `reporte_bugs.md`

**Depende de:** Personas 3 a 6. **Bloquea a:** Persona 1.

---

### Persona 1 — Integración, `main.py` y documentación
**Complejidad:** ⭐⭐⭐⭐⭐

**Qué debe hacer:**
- Revisar y aprobar `ast_nodes.py` y `GRAMATICA.md` el primer día.
- Implementar `program()` y `statement()` (despachador principal).
- Integrar los módulos de Personas 3, 4, 5 y 6 en `parser.py`.
- Resolver conflictos de precedencia.
- Implementar el manejo global de errores sintácticos.
- Escribir `main.py` que une lexer y parser.
- Ejecutar pruebas de integración.
- Documentar el flujo en `README.md` y `docs/parser.md`.
- Revisar el trabajo de Persona 2 y Persona 7.

**Entregables:**
- `parser.py` (integrado)
- `main.py`
- `tests/test_integracion.py`
- `README.md` y `docs/parser.md`

**Depende de:** Personas 2 a 7.

---

## Orden de complejidad

| Orden | Persona | Tarea | Complejidad |
|-------|---------|-------|-------------|
| 1 | Persona 2 | AST + gramática BNF + ejemplos | ⭐ |
| 2 | Persona 3 | `primary`, `unary`, `factor` | ⭐⭐ |
| 3 | Persona 4 | `term`, `comparison`, lógicos | ⭐⭐ |
| 4 | Persona 5 | Sentencias simples | ⭐⭐⭐ |
| 5 | Persona 6 | Bloques y control de flujo | ⭐⭐⭐⭐ |
| 6 | Persona 7 | Pruebas de integración y errores | ⭐⭐⭐⭐ |
| 7 | Persona 1 | Integración, `main.py`, documentación | ⭐⭐⭐⭐⭐ |

---

## Reglas de coordinación

1. Los nodos del AST y la gramática BNF se definen el primer día y se respetan.
2. Un archivo por persona. Personas 3 y 4 comparten `parser_expresiones.py`; Personas 5 y 6 comparten `parser_sentencias.py`. Persona 1 integra en `parser.py`.
3. Cada persona prueba su módulo con tokens escritos a mano antes de la integración.
4. Revisión en anillo: Persona 1 → 2 → 3 → 4 → 5 → 6 → 7 → 1.
5. El lexer no se modifica. Cualquier token nuevo se pide a Persona 1.
6. Un módulo sin pruebas no cuenta como terminado.
7. Integraciones programadas: día 3 (Personas 3 y 4), día 5 (Personas 5 y 6), día 6 (Persona 7), día 7 (Persona 1 integra todo).

---

## Criterios de aceptación globales

- [ ] Los 10 programas válidos producen AST sin errores.
- [ ] Los 5 programas inválidos producen errores con línea y columna.
- [ ] `main.py` ejecuta archivo → tokens → AST.
- [ ] Todos los tests pasan en conjunto.
- [ ] No hay reglas duplicadas ni nodos inventados.
- [ ] La documentación está completa.
