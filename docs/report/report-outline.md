# Estructura de Informe Académico (Report Outline) — KnowledgeFlow RAG

Este esquema define la estructura, evidencias técnicas, figuras sugeridas y archivos de respaldo para la redacción del informe técnico-académico del proyecto (límite recomendado: 5 páginas).

---

## Sección 1: Caso Organizacional y Definición de la Necesidad

### 1.1. Objetivo de la Sección
Contextualizar la problemática de dispersión documental y falta de trazabilidad en las organizaciones, presentando el caso de estudio de **NovaTech SpA**.

### 1.2. Evidencias Técnicas Disponibles
- Corpus de políticas internas de acceso, procedimientos de respuesta a incidentes y preguntas frecuentes institucionales.
- Necesidad de consultar estándares normativos externos (OWASP, NIST) sin mezclar arbitrariamente las directivas internas con las directrices públicas.

### 1.3. Archivos del Repositorio Asociados
- [`knowledge/internal/politica_accesos.md`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/knowledge/internal/politica_accesos.md)
- [`knowledge/internal/procedimiento_incidentes.md`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/knowledge/internal/procedimiento_incidentes.md)
- [`knowledge/internal/faq_interna.txt`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/knowledge/internal/faq_interna.txt)

### 1.4. Redacción Pendiente
> [REQUIERE REDACCIÓN DEL EQUIPO: Contexto específico de la organización, delimitación del alcance operativo y justificación de la necesidad de negocio.]

---

## Sección 2: Diseño de la Solución y Enfoque Metodológico

### 2.1. Objetivo de la Sección
Describir la estrategia de solución basada en un sistema RAG de precisión con enrutamiento inteligente de fuentes y compuertas de seguridad.

### 2.2. Evidencias Técnicas Disponibles
- Separación funcional entre conocimiento institucional (`internal`) y marcos de referencia públicos (`external`).
- Esquema de recuperación dual balanceada para consultas comparativas (`all`).
- Enfoque *Evidence-First* en la presentación de resultados.

### 2.3. Tablas y Figuras Sugeridas
- Tabla comparativa entre RAG genérico (caja negra) vs. KnowledgeFlow RAG (trazable y fundamentado).

### 2.4. Archivos del Repositorio Asociados
- [`app/rag/pipeline.py`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/app/rag/pipeline.py)
- [`app/rag/schemas.py`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/app/rag/schemas.py)

### 2.5. Redacción Pendiente
> [REQUIERE REDACCIÓN DEL EQUIPO: Argumentación sobre la elección de la arquitectura desacoplada frente a otras alternativas evaluadas.]

---

## Sección 3: Prompt Engineering, Agente de Enrutamiento y RAG

### 3.1. Objetivo de la Sección
Detallar el diseño de prompts seguros, la lógica del agente clasificador de ámbito y los mecanismos de generación fundamentada con citas.

### 3.2. Evidencias Técnicas Disponibles
- **Agente Enrutador**: `GeminiSourceRouter` operando con `gemini-3.5-flash-lite`, salida tipada JSON `RouteDecision` y manejo de baja confianza.
- **Aislamiento de Planos**: Delimitadores estructurales XML en prompts de usuario y sistema para impedir secuestro por Prompt Injection indirecto.
- **Validación de Citas**: Expresión regular `\[S\d+\]`, mapeo con identificadores en contexto y módulo de autorreparación de citas en el generador (`gemini-3.5-flash`).

### 3.3. Archivos del Repositorio Asociados
- [`app/agents/source_router.py`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/app/agents/source_router.py)
- [`app/rag/prompts.py`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/app/rag/prompts.py)
- [`app/rag/generator.py`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/app/rag/generator.py)

### 3.4. Redacción Pendiente
> [REQUIERE REDACCIÓN DEL EQUIPO: Análisis de los patrones de prompting seleccionados y justificación del desacoplamiento de modelos.]

---

## Sección 4: Arquitectura del Sistema, Vectorstore y Trazabilidad

### 4.1. Objetivo de la Sección
Exponer el flujo end-to-end desde la interfaz web hasta la capa de persistencia vectorial y API.

### 4.2. Evidencias Técnicas Disponibles
- Diagrama de arquitectura Mermaid con 7 subsistemas articulados.
- Persistencia FAISS con embeddings normalizados `gemini-embedding-2` (768d).
- Mecanismo de validación criptográfica `verify_index_freshness` (SHA-256) contra desalineación del corpus.
- Contrato estricto `QueryResponse` en FastAPI y consola web sin uso de `innerHTML`.

### 4.3. Tablas y Figuras Sugeridas
- Diagrama Mermaid de Arquitectura ([`docs/architecture/architecture.mmd`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/docs/architecture/architecture.mmd)).

### 4.4. Archivos del Repositorio Asociados
- [`docs/architecture/architecture.md`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/docs/architecture/architecture.md)
- [`app/rag/vectorstore.py`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/app/rag/vectorstore.py)
- [`app/api/routes.py`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/app/api/routes.py)

### 4.5. Redacción Pendiente
> [REQUIERE REDACCIÓN DEL EQUIPO: Justificación técnica de las decisiones de diseño sobre el vectorstore y la seguridad de la interfaz.]

---

## Sección 5: Evaluación Experimental, Calibración y Limitaciones

### 5.1. Objetivo de la Sección
Presentar los resultados empíricos del barrido de umbrales, la calibración de la compuerta de abstención temprana, las limitaciones de cuota encontradas y las líneas de trabajo futuro.

### 5.2. Evidencias Técnicas Disponibles
- **Barrido Paramétrico**: Resultados con $Top\text{-}K=4$ sobre 20 casos revisados humanamente ($\tau=0.60$ como óptimo experimental con 100% de retención y 0% de fuga OOD).
- **Limitación de Cuota Identificada**: Límite de 20 RPD en Free Tier de Google Gemini (`GenerateRequestsPerDayPerProjectPerModel-FreeTier`) y estrategia de desacoplamiento aplicada.
- **Suite de Pruebas**: 156 tests automatizados 100% offline.

### 5.3. Tablas y Figuras Sugeridas
- Tabla de resultados del Threshold Sweep ([`docs/evidence/evaluation-evidence.md`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/docs/evidence/evaluation-evidence.md#12-tabla-de-resultados-empíricos-del-barrido)).

### 5.4. Archivos del Repositorio Asociados
- [`app/evaluation/threshold_sweep.py`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/app/evaluation/threshold_sweep.py)
- [`evaluation/dataset_verified.json`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/evaluation/dataset_verified.json)

### 5.5. Redacción Pendiente
> [REQUIERE REDACCIÓN DEL EQUIPO: Conclusiones académicas finales, análisis crítico del impacto de las limitaciones de cuota, reflexiones individuales y propuestas de escalabilidad.]
