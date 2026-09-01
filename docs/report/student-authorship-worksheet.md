# Guía de Redacción del Informe y Autoría Estudiantil (Authorship Worksheet) — KnowledgeFlow RAG

**Asignatura**: ISY0101 — Ingeniería de Soluciones con IA (Evaluación Parcial N°1)  
**Propósito**: Proveer a los estudiantes una estructura de trabajo, datos fácticos del repositorio, preguntas guía y advertencias conceptuales para que **redacten personalmente** las justificaciones técnicas, conclusiones y reflexiones de su informe académico.

---

## 1. Presupuesto Orientativo de 5 Páginas

Esta distribución es una recomendación para estructurar el informe dentro del límite máximo de 5 páginas exigido por la pauta:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ PÁGINA 1: Introducción, Caso Organizacional (NovaTech) y Objetivos     │
│   • Contexto, dolor organizacional y delimitación de alcance.          │
│   • Inserción sugerida: Tabla de objetivos y requerimientos.           │
├────────────────────────────────────────────────────────────────────────┤
│ PÁGINA 2: Prompt Engineering, Agente Enrutador y RAG Dual-Source       │
│   • Patrones de prompting, aislamiento XML y balanceo multi-fuente.    │
│   • Inserción sugerida: Estructura del prompt de sistema.              │
├────────────────────────────────────────────────────────────────────────┤
│ PÁGINA 3: Arquitectura Técnica de la Solución y Trazabilidad           │
│   • Desglose de componentes, modelos desacoplados y persistencia.      │
│   • Inserción sugerida: Diagrama de Arquitectura Mermaid.              │
├────────────────────────────────────────────────────────────────────────┤
│ PÁGINA 4: Coherencia, Validación de Citas y Barrido de Umbrales        │
│   • Calibración del threshold, compuerta de abstención temprana.       │
│   • Inserción sugerida: Tabla de resultados del Threshold Sweep.       │
├────────────────────────────────────────────────────────────────────────┤
│ PÁGINA 5: Limitaciones, Fundamentación, Conclusiones y Referencias APA │
│   • Matriz de decisiones, reflexiones, declaración de IA y fuentes.    │
│   • Inserción sugerida: Checklist APA y referencias oficiales.         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Bloques de Trabajo por Indicador de Rúbrica (IE1 – IE9)

### Bloque 1: Caso Organizacional y Requerimientos (IE1 — 15%)
- **Preguntas Guía que el Equipo debe Responder**:
  1. ¿Qué problemática concreta de dispersión documental enfrenta la organización simulada NovaTech SpA?
  2. ¿Por qué se requiere un motor que consulte simultáneamente fuentes internas (políticas) y estándares externos (OWASP/NIST) de forma diferenciada?
  3. ¿Cuál es el alcance operacional del sistema y qué elementos quedan explícitamente fuera?
- **Datos Objetivos y Rutas en Repositorio**:
  - Corpus interno pedagógico: [`../../knowledge/internal/politica_accesos.md`](../../knowledge/internal/politica_accesos.md), [`../../knowledge/internal/procedimiento_incidentes.md`](../../knowledge/internal/procedimiento_incidentes.md), [`../../knowledge/internal/faq_interna.txt`](../../knowledge/internal/faq_interna.txt).
  - Descripción general: [`../../README.md`](../../README.md).
- **Presupuesto Sugerido**: 200 – 250 palabras.
- **Errores Conceptuales a Evitar**:
  - *No presentar a NovaTech SpA como una empresa real con clientes reales; es un caso simulado/pedagógico.*
  - *No describir el sistema como un chatbot conversacional genérico; es una mesa de consulta y trazabilidad documental.*
- **Espacio de Redacción Estudiantil**:
> [RESPUESTA DEL EQUIPO: Redactar aquí el planteamiento del problema, contexto organizacional y objetivos del proyecto.]

---

### Bloque 2: Prompt Engineering y Mitigación de Riesgos (IE2 — 10%)
- **Preguntas Guía que el Equipo debe Responder**:
  1. ¿Cómo se estructuraron las instrucciones del System Prompt para forzar la fundamentación estricta (*grounding*)?
  2. ¿Cómo se implementó la separación entre el plano de control (instrucciones) y el plano de datos (fragmentos recuperados)?
  3. ¿Por qué es obligatorio el formato de citas `[S#]` y cómo se instruye al modelo respecto a la abstención?
- **Datos Objetivos y Rutas en Repositorio**:
  - Prompts estructurados: [`../../app/rag/prompts.py`](../../app/rag/prompts.py).
  - Prompt del Router: [`../../app/agents/source_router.py`](../../app/agents/source_router.py).
  - Pruebas de seguridad: [`../../tests/test_security.py`](../../tests/test_security.py).
- **Presupuesto Sugerido**: 200 – 250 palabras.
- **Errores Conceptuales a Evitar**:
  - *No afirmar que los delimitadores XML "garantizan al 100% que no habrá inyecciones"; afirmar que "mitigan el riesgo al aislar los datos recuperados como texto no ejecutable".*
- **Espacio de Redacción Estudiantil**:
> [RESPUESTA DEL EQUIPO: Redactar aquí el análisis del diseño de prompts, directivas de seguridad y control de contexto.]

---

### Bloque 3: Flujos RAG Internos y Externos (IE3 — 10%)
- **Preguntas Guía que el Equipo debe Responder**:
  1. ¿Cómo clasifica el sistema los documentos durante la ingesta y cómo preserva su metadato de procedencia (`source_type`)?
  2. ¿Cómo opera el parámetro `source_scope` en las modalidades `internal`, `external` y `all`?
  3. ¿Por qué es necesario aplicar una estrategia de recuperación balanceada ($k/2$) en consultas comparativas (`all`)?
- **Datos Objetivos y Rutas en Repositorio**:
  - Ingesta y metadatos: [`../../app/rag/loaders.py`](../../app/rag/loaders.py).
  - Lógica de recuperación y balanceo: [`../../app/rag/retriever.py`](../../app/rag/retriever.py), [`../../app/rag/pipeline.py`](../../app/rag/pipeline.py).
- **Presupuesto Sugerido**: 180 – 220 palabras.
- **Errores Conceptuales a Evitar**:
  - *No usar el término "RAG híbrido" si no se utiliza búsqueda léxica (BM25) combinada con vectorial; usar "RAG dual-source" o "recuperación multi-fuente balanceada".*
- **Espacio de Redacción Estudiantil**:
> [RESPUESTA DEL EQUIPO: Redactar aquí la justificación de los flujos RAG internos/externos y el mecanismo de balanceo.]

---

### Bloque 4: Arquitectura de Solución y Diagrama Modular (IE4 — 15%, IE7 — 10%)
- **Preguntas Guía que el Equipo debe Responder**:
  1. ¿Cuáles son las capas principales del pipeline y cuál es la responsabilidad de cada componente?
  2. ¿Por qué se desacopló el Source Router (`gemini-3.5-flash-lite`) del Generador Grounded (`gemini-3.5-flash`)?
  3. ¿Cómo asegura el sistema la frescura y coherencia del índice mediante el fingerprint SHA-256 (`verify_index_freshness`)?
- **Datos Objetivos y Rutas en Repositorio**:
  - Diagrama Mermaid: [`../architecture/architecture.mmd`](../architecture/architecture.mmd).
  - Documentación de arquitectura: [`../architecture/architecture.md`](../architecture/architecture.md).
  - Configuración y vectorstore: [`../../app/core/config.py`](../../app/core/config.py), [`../../app/rag/vectorstore.py`](../../app/rag/vectorstore.py).
- **Presupuesto Sugerido**: 250 – 300 palabras (acompañado del diagrama).
- **Errores Conceptuales a Evitar**:
  - *No describir el fingerprint SHA-256 como una "firma criptográfica de seguridad de los datos"; es un hash de frescura para detectar desalineación entre el índice y los archivos físicos.*
- **Espacio de Redacción Estudiantil**:
> [RESPUESTA DEL EQUIPO: Redactar aquí la descripción técnica de la arquitectura e integración de componentes.]

---

### Bloque 5: Coherencia de Datos, Validación de Citas y Calibración (IE5 — 10%, IE6 — 10%)
- **Preguntas Guía que el Equipo debe Responder**:
  1. ¿Cómo valida el sistema que las afirmaciones generadas se correspondan con los fragmentos recuperados?
  2. ¿Qué pasos realiza el generador cuando detecta una cita inválida (reparación controlada con segunda llamada)?
  3. ¿Cómo se interpretan los resultados del barrido paramétrico y por qué se adoptó el umbral $\tau = 0.60$?
- **Datos Objetivos y Rutas en Repositorio**:
  - Generador y validador de citas: [`../../app/rag/generator.py`](../../app/rag/generator.py).
  - Tabla de barrido de umbrales: [`../evidence/evaluation-evidence.md`](../evidence/evaluation-evidence.md).
  - Dataset verificado: [`../../evaluation/dataset_verified.json`](../../evaluation/dataset_verified.json).
- **Presupuesto Sugerido**: 250 – 300 palabras.
- **Errores Conceptuales a Evitar**:
  - *No afirmar que la presencia de citas `[S1]` "garantiza la verdad absoluta de la respuesta"; valida que el texto cita formalmente una fuente presente en el contexto provisto.*
  - *No usar "umbral óptimo experimental"; indicar que 0.60 fue el menor umbral evaluado que retuvo 100% de casos válidos sin fuga OOD en el dataset de 20 casos.*
- **Espacio de Redacción Estudiantil**:
> [RESPUESTA DEL EQUIPO: Redactar aquí el análisis de coherencia datos-respuestas, validación de citas y calibración del umbral.]

---

## 3. Matriz de Decisiones Técnicas para Fundamentación (IE8 — 10%)

Esta tabla presenta las decisiones de ingeniería adoptadas en el código y las preguntas que el equipo debe argumentar en el informe:

| Decisión Técnica de Ingeniería | Evidencia en Repositorio | Pregunta que el Equipo debe Responder |
| :--- | :--- | :--- |
| **Persistencia Vectorial en FAISS (`IndexFlatIP`)** | [`app/rag/vectorstore.py`](../../app/rag/vectorstore.py) | ¿Por qué utilizar búsqueda exacta por producto punto sobre vectores normalizados L2 en lugar de una base de datos vectorial externa pesada? |
| **Embeddings `gemini-embedding-2` (768d)** | [`app/rag/embeddings.py`](../../app/rag/embeddings.py) | ¿Qué ventajas ofrece la dimensión 768 en términos de expresividad semántica y costo de cómputo para este volumen documental? |
| **Top-K = 4** | [`app/core/config.py`](../../app/core/config.py) | ¿Por qué 4 fragmentos representan un equilibrio adecuado entre cobertura contextual y límite de longitud de ventana del LLM? |
| **Umbral de Similitud $\tau = 0.60$** | [`app/evaluation/threshold_sweep.py`](../../app/evaluation/threshold_sweep.py) | ¿Qué balance experimental sustenta fijar 0.60 frente a umbrales más laxos (0.50/0.55) o más restrictivos (0.75)? |
| **Desacoplamiento Router (Flash-Lite) vs Generator (Flash)** | [`app/agents/source_router.py`](../../app/agents/source_router.py), [`app/rag/generator.py`](../../app/rag/generator.py) | ¿Por qué asignar una tarea de clasificación de baja complejidad a un modelo liviano y reservar el modelo principal para la síntesis fundamentada? |
| **Compuerta Temprana de Abstención** | [`app/rag/pipeline.py`](../../app/rag/pipeline.py) | ¿Qué beneficios operativos y de seguridad aporta cortar el flujo antes de la llamada generativa cuando no hay evidencia suficiente? |
| **Contratos Estrictos Pydantic en FastAPI** | [`app/rag/schemas.py`](../../app/rag/schemas.py), [`app/api/routes.py`](../../app/api/routes.py) | ¿Por qué tipar estrictamente `QueryRequest` y `QueryResponse` en lugar de devolver diccionarios libres? |
| **Interfaz Web Vanilla (Sin frameworks pesados)** | [`app/ui/static/`](../../app/ui/static/) | ¿Por qué servir HTML/CSS/JS nativo directamente desde FastAPI evitando dependencias externas para la mesa de trabajo? |

- **Espacio de Redacción Estudiantil para IE8**:
> [RESPUESTA DEL EQUIPO: Redactar aquí la justificación razonada de las decisiones técnicas seleccionadas frente a los objetivos organizacionales.]

---

## 4. Datos Objetivos del Barrido de Umbrales ($\tau = 0.60$)

Para fundamentar la sección de calibración, el equipo dispone de los siguientes datos medidos sobre los 20 casos de [`../../evaluation/dataset_verified.json`](../../evaluation/dataset_verified.json):

```text
Resultados del Threshold Sweep (Top-K = 4):
• τ = 0.50: 15/15 respondibles retenidos (100%), 0/5 OOD abstenidos (0%), OOD Leakage = 100%.
• τ = 0.55: 15/15 respondibles retenidos (100%), 3/5 OOD abstenidos (60%), OOD Leakage = 40%.
• τ = 0.60: 15/15 respondibles retenidos (100%), 5/5 OOD abstenidos (100%), OOD Leakage = 0%, Hit@K = 100%.
• τ = 0.65: 15/15 respondibles retenidos (100%), 5/5 OOD abstenidos (100%), OOD Leakage = 0%, Hit@K = 100%.
• τ = 0.70: 15/15 respondibles retenidos (100%), 5/5 OOD abstenidos (100%), OOD Leakage = 0%, Hit@K = 100%.
• τ = 0.75:  9/15 respondibles retenidos (60%),  5/5 OOD abstenidos (100%), Falsa Abstención = 40%.
```

- **Preguntas de Análisis que los Estudiantes deben Reflexionar**:
  - ¿Por qué $\tau=0.60$ es preferible a $\tau=0.55$ desde el punto de vista del control de fugas (*leakage*)?
  - ¿Por qué $\tau=0.60$ es preferible a $\tau=0.75$ para evitar descartar información válida (*false abstention*)?
  - ¿Qué limitación metodológica implica calibrar sobre un dataset de 20 casos?

---

## 5. Checklist de Limitaciones Técnicas y Trabajo Futuro

El equipo debe discutir y documentar honestamente las limitaciones del sistema:
- [ ] **Volumen del Corpus**: El corpus interno cuenta con 3 documentos simulados y el externo con 5 resúmenes curados. No representa la escala de un repositorio corporativo masivo.
- [ ] **Dependencia de API Externa**: El sistema depende de la disponibilidad y latencia de los endpoints de Google Gemini.
- [ ] **Restricción de Cuota en Free Tier**: La cuota de 20 RPD observada en `gemini-3.5-flash` (`GenerateRequestsPerDayPerProjectPerModel-FreeTier`) impidió completar la corrida generativa oficial end-to-end de 20 casos consecutivos.
- [ ] **Validación de Citas vs. Verdad Semántica**: La validación de citas confirma que las referencias `[S#]` corresponden a fragmentos inyectados, pero no sustituye la supervisión humana experta sobre la corrección fáctica del texto generado.

---

## 6. Declaración de Uso de Herramientas de IA

Los estudiantes deben completar esta sección de acuerdo con las normativas éticas e institucionales de DuocUC:

- **Herramientas de IA Utilizadas**: `[Completar: ej. Google Antigravity / Gemini / ChatGPT / Copilot]`
- **Actividades en las que se Emplearon**: `[Completar: ej. Generación de código boilerplate, diseño de pruebas unitarias, formateo de tablas, revisión sintáctica]`
- **Actividades Realizadas Exclusivamente por los Estudiantes**: `[Completar: ej. Definición de la arquitectura, selección del caso de estudio, análisis de decisiones técnicas, revisión humana del dataset, redacción de conclusiones y defensa oral]`
- **Declaración de Responsabilidad**: `[Completar: Declaración de autoría y comprensión total del código entregado]`

---

## 7. Checklist de Formato APA y Fichas Bibliográficas

### Fichas Bibliográficas de Fuentes Curadas
1. **OWASP LLM Prompt Injection Prevention Cheat Sheet**:
   - *Autor*: OWASP Foundation
   - *Título*: OWASP LLM Prompt Injection Prevention Cheat Sheet
   - *Año*: 2026 (Consulta: Septiembre 2026)
   - *URL*: `https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html`
2. **NIST SP 800-218 (SSDF Version 1.1)**:
   - *Autor*: National Institute of Standards and Technology (NIST), U.S. Department of Commerce
   - *Título*: Secure Software Development Framework (SSDF) Version 1.1: Recommendations for Mitigating the Risk of Software Vulnerabilities (Special Publication 800-218)
   - *Año*: 2022 (Consulta: Septiembre 2026)
   - *URL*: `https://csrc.nist.gov/pubs/sp/800/218/final`
3. **NIST Privacy Framework Version 1.0**:
   - *Autor*: National Institute of Standards and Technology (NIST)
   - *Título*: NIST Privacy Framework: A Tool for Improving Privacy through Enterprise Risk Management, Version 1.0
   - *Año*: 2020 (Consulta: Septiembre 2026)
   - *URL*: `https://www.nist.gov/privacy-framework/privacy-framework`

### Checklist Final de Entrega del Informe
- [ ] Límite de 5 páginas respetado rigurosamente.
- [ ] Diagrama de arquitectura legible insertado en la página correspondiente.
- [ ] Tabla de resultados de barrido paramétrico formateada de forma clara.
- [ ] Indicadores IE1 al IE9 abordados con evidencia verificable del repositorio.
- [ ] Referencias bibliográficas en formato APA al final del documento.
- [ ] Declaración de uso de IA completada por el equipo.
