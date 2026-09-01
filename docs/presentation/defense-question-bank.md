# Banco de Preguntas para Defensa Oral (Defense Question Bank) — KnowledgeFlow RAG

**Asignatura**: ISY0101 — Ingeniería de Soluciones con IA  
**Propósito**: Preparar a los estudiantes ante posibles preguntas del docente y evaluadores durante la presentación oral (10 minutos), proporcionando la evidencia del repositorio y los puntos fácticos clave que el estudiante debe dominar.

---

## 1. Preguntas sobre el Problema Organizacional y Caso de Estudio

### P1: ¿Por qué una empresa como NovaTech SpA necesita RAG en lugar de consultar directamente un modelo como ChatGPT o Gemini?
- **EVIDENCIA PARA RESPONDER**: [`../../knowledge/internal/`](../../knowledge/internal/), [`../../README.md`](../../README.md).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - Los modelos base no conocen la información privada, reciente ni interna de la organización (políticas de acceso, procedimientos de guardia de NovaTech).
  - Consultar un LLM genérico sin RAG induce alucinaciones y respuestas desalineadas con la normativa corporativa vigente.
  - RAG aporta trazabilidad documental auditable mediante citas verificables `[S#]`.

### P2: ¿Qué diferencia existe entre el conocimiento interno y el externo en este proyecto?
- **EVIDENCIA PARA RESPONDER**: [`../../app/rag/loaders.py`](../../app/rag/loaders.py), [`../../knowledge/`](../../knowledge/).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - `internal`: Directivas privadas específicas de NovaTech (control de accesos, severidades de incidentes, FAQ).
  - `external`: Estándares normativos y guías públicas autoritativas (OWASP Prompt Injection Prevention, NIST SSDF SP 800-218, NIST Privacy Framework).
  - El sistema permite consultar cada ámbito de forma aislada o combinarlos de manera balanceada.

---

## 2. Preguntas sobre Prompts, Grounding y Seguridad

### P3: ¿Cómo asegura el System Prompt que el modelo no responda con información externa inventada?
- **EVIDENCIA PARA RESPONDER**: [`../../app/rag/prompts.py`](../../app/rag/prompts.py).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - El System Prompt establece directivas explícitas de *grounding*: prohibición de suponer hechos y obligación de fundamentar cada afirmación en fragmentos provistos en el bloque `<context>`.
  - Instruye expresamente a abstenerse si el contexto provisto no contiene información suficiente para responder.

### P4: ¿Qué ocurre si un documento del corpus contiene una inyección maliciosa (Prompt Injection indirecto)?
- **EVIDENCIA PARA RESPONDER**: [`../../app/rag/prompts.py`](../../app/rag/prompts.py), [`../../tests/test_security.py`](../../tests/test_security.py).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - Separación de planos de control y datos: los fragmentos se encierran dentro de etiquetas delimitadoras `<context><source id="...">...</source></context>`.
  - El System Prompt instruye al modelo a tratar el contenido recuperado estrictamente como datos de consulta pasivos y no como directivas operativas.

### P5: ¿Qué valida y qué NO valida el validador de citas `[S#]`?
- **EVIDENCIA PARA RESPONDER**: [`../../app/rag/generator.py`](../../app/rag/generator.py).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - **Qué valida**: Que los identificadores citados en el texto existan realmente entre las fuentes inyectadas al contexto y que el formato sintáctico sea correcto.
  - **Qué NO valida**: No certifica la corrección semántica o veracidad lógica absoluta del texto generado por el LLM; mitiga citas fantasma pero no reemplaza la auditoría humana.

---

## 3. Preguntas sobre Embeddings, Vectorstore y FAISS

### P6: ¿Qué es un embedding y por qué se configuró en 768 dimensiones?
- **EVIDENCIA PARA RESPONDER**: [`../../app/rag/embeddings.py`](../../app/rag/embeddings.py), [`../../app/core/config.py`](../../app/core/config.py).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - Un embedding es una representación vectorial densa que captura el significado semántico del texto en un espacio multidimensional.
  - La dimensión 768 es la salida nativa del modelo `gemini-embedding-2`, ofreciendo una resolución semántica adecuada para segmentación de párrafos y consultas técnicas.

### P7: ¿Por qué se utiliza similitud coseno y cómo se implementa en FAISS?
- **EVIDENCIA PARA RESPONDER**: [`../../app/rag/vectorstore.py`](../../app/rag/vectorstore.py).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - La similitud coseno mide el coseno del ángulo entre dos vectores, evaluando la cercanía semántica independientemente de la longitud del texto.
  - En FAISS se utiliza `IndexFlatIP` (Inner Product). Al normalizar previamente los vectores con norma L2 ($||v||=1$), el producto punto resulta idéntico a la similitud coseno.

### P8: ¿Qué ocurre si alguien modifica un archivo del corpus en disco sin reindexar FAISS?
- **EVIDENCIA PARA RESPONDER**: [`../../app/rag/vectorstore.py`](../../app/rag/vectorstore.py) (`verify_index_freshness`), [`../../app/api/routes.py`](../../app/api/routes.py).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - El vectorstore almacena un `IndexManifest` con un fingerprint SHA-256 determinista del corpus y su configuración.
  - Al iniciar una consulta, la función `verify_index_freshness` recalcula el hash. Si no coincide, la API aborta con error HTTP 503 impidiendo entregar respuestas basadas en un índice desfasado.

---

## 4. Preguntas sobre el Agente Enrutador (Source Router)

### P9: ¿Por qué se utilizó un agente con LLM (`SourceRouter`) en lugar de reglas basadas en `if` o palabras clave?
- **EVIDENCIA PARA RESPONDER**: [`../../app/agents/source_router.py`](../../app/agents/source_router.py).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - Las preguntas de los usuarios presentan variaciones lingüísticas, sinónimos y formulaciones complejas que escapan a listas de palabras clave estáticas.
  - El agente evalúa la intención semántica global de la consulta y devuelve un objeto tipado `RouteDecision` con confianza.

### P10: ¿Qué pasa si el Source Router se equivoca o emite un JSON mal formado?
- **EVIDENCIA PARA RESPONDER**: [`../../app/agents/source_router.py`](../../app/agents/source_router.py) (`_parse_decision`), [`../../tests/test_router.py`](../../tests/test_router.py).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - Mecanismo de fallback seguro: ante fallo de parseo JSON, excepción de red o confianza inferior a 0.50, el agente conmuta automáticamente a `source_scope: "all"`.
  - Esto garantiza que nunca se pierda la recuperación de información por un error del clasificador.

### P11: ¿Por qué se desacopló el modelo del router (`gemini-3.5-flash-lite`) del generador (`gemini-3.5-flash`)?
- **EVIDENCIA PARA RESPONDER**: [`../../app/core/config.py`](../../app/core/config.py), [`../../tests/test_model_separation.py`](../../tests/test_model_separation.py).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - La clasificación de ámbito es una tarea liviana que no requiere la capacidad generativa del modelo principal.
  - Permite reducir la latencia de respuesta y optimizar el consumo de solicitudes por modelo en la cuota diaria (RPD).

---

## 5. Preguntas sobre Calibración, Umbrales y Métricas

### P12: ¿Por qué se seleccionó el umbral $\tau = 0.60$ y no un valor más alto como $0.70$ o más bajo como $0.50$?
- **EVIDENCIA PARA RESPONDER**: [`../evidence/evaluation-evidence.md`](../evidence/evaluation-evidence.md), [`../../app/evaluation/threshold_sweep.py`](../../app/evaluation/threshold_sweep.py).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - $\tau = 0.50 / 0.55$: Permite que preguntas fuera de dominio recuperen fragmentos irrelevantes (OOD leakage de 100% y 40% respectivamente).
  - $\tau = 0.75$: Se vuelve hiper-restrictivo y descarta el 40% de las preguntas válidas (falsa abstención).
  - $\tau = 0.60$: Es el menor umbral evaluado que retuvo el 100% de los casos respondibles y produjo 0% de OOD leakage en los 20 casos evaluados.

### P13: ¿Qué significa la métrica Hit@K y qué es el OOD Leakage?
- **EVIDENCIA PARA RESPONDER**: [`../../app/evaluation/metrics.py`](../../app/evaluation/metrics.py), [`../../evaluation/dataset_verified.json`](../../evaluation/dataset_verified.json).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - **Hit@K**: Proporción de consultas válidas en las que al menos un fragmento relevante (*gold label*) está presente entre los Top-K fragmentos recuperados.
  - **OOD Leakage**: Porcentaje de preguntas fuera de dominio (*Out-of-Domain*) en las que el sistema superó indebidamente el umbral de similitud en lugar de abstenerse.

---

## 6. Preguntas sobre la Arquitectura del Pipeline y la Interfaz

### P14: ¿Cómo funciona la compuerta temprana de abstención (*Early Abstention*)?
- **EVIDENCIA PARA RESPONDER**: [`../../app/rag/pipeline.py`](../../app/rag/pipeline.py).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - Si tras la búsqueda vectorial y el filtrado por umbral no queda ningún fragmento con similitud $\ge 0.60$, el pipeline retorna inmediatamente `abstained=True`, `citations=[]`, `sources=[]`.
  - Evita llamar al LLM generativo, ahorrando cuota/costo y erradicando respuestas inventadas cuando no hay respaldo.

### P15: ¿Cómo se garantiza la seguridad en la interfaz web (prevención de XSS)?
- **EVIDENCIA PARA RESPONDER**: [`../../app/ui/static/app.js`](../../app/ui/static/app.js) (`renderGroundedText`).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - No se utiliza `innerHTML` para inyectar las respuestas del modelo.
  - El frontend analiza el texto con expresiones regulares y construye nodos seguros del DOM (`document.createTextNode` y `document.createElement("button")` para las insignias de citas).

---

## 7. Preguntas Difíciles sobre Estado del Proyecto y Limitaciones

### P16: ¿El servidor de UI Preview (`scripts/ui_preview.py`) demuestra que el sistema RAG está funcionando en vivo?
- **EVIDENCIA PARA RESPONDER**: [`../../scripts/ui_preview.py`](../../scripts/ui_preview.py), [`../../README.md`](../../README.md).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - No. El servidor de preview es un entorno de desarrollo offline con fixtures controlados, diseñado para validar estados visuales de la interfaz sin consumir cuota de API.
  - La demostración del motor RAG real se realiza ejecutando `app.main:app` con `GEMINI_API_KEY`.

### P17: ¿Qué parte del proyecto quedó pendiente y cuál fue el motivo técnico?
- **EVIDENCIA PARA RESPONDER**: [`../evidence/evaluation-evidence.md`](../evidence/evaluation-evidence.md).
- **PUNTOS QUE EL ESTUDIANTE DEBERÍA PODER EXPLICAR**:
  - La corrida automatizada oficial generativa end-to-end de los 20 casos quedó en estado `PENDING` debido al límite diario de 20 RPD en Google Gemini Free Tier (`GenerateRequestsPerDayPerProjectPerModel-FreeTier`).
  - Toda la infraestructura de software, dataset, runner y calibración de umbrales está completamente terminada y testeada con 158 pruebas offline.
