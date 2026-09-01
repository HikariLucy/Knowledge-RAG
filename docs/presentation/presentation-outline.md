# Esquema de Presentación Oral (Presentation Outline) — KnowledgeFlow RAG

**Duración Estimada Total**: 10 minutos (8 diapositivas recomendadas).

---

## Estructura de Diapositivas

### Diapositiva 1: Problema y Caso Organizacional
- **Duración sugerida**: 1:00 min
- **Contenido Clave**:
  - Problemática de dispersión documental y desconfianza ante alucinaciones de LLMs en el entorno corporativo.
  - Caso **NovaTech SpA**: Necesidad de responder consultas operativas sobre políticas internas y comparar directivas frente a estándares normativos externos (OWASP, NIST).
- **Evidencia**: Corpus en `knowledge/internal/` y `knowledge/external/`.
- **Apoyo al Orador**:
  > [REQUIERE EXPLICACIÓN DEL EQUIPO: Presentación del equipo y planteamiento inicial del problema.]

---

### Diapositiva 2: Solución Propuesta — KnowledgeFlow RAG
- **Duración sugerida**: 1:00 min
- **Contenido Clave**:
  - Enfoque *Evidence-First*: Respuestas estrictamente fundamentadas con libro mayor de evidencia visible.
  - Separación entre conocimiento institucional (`INT`) y público (`EXT`).
  - Compuerta temprana de abstención ante falta de similitud para erradicar respuestas inventadas.
- **Evidencia**: Consola web editorial y esquema `QueryResponse`.
- **Apoyo al Orador**:
  > [REQUIERE EXPLICACIÓN DEL EQUIPO: Explicación de los principios de diseño y propuesta de valor.]

---

### Diapositiva 3: Arquitectura Técnica y Flujo de Procesamiento
- **Duración sugerida**: 1:30 min
- **Contenido Clave**:
  - Diagrama end-to-end: Web UI $\to$ FastAPI $\to$ Source Router $\to$ FAISS (Embeddings 768d) $\to$ Early Abstention $\to$ Grounded Generator $\to$ Citation Validator.
  - Desacoplamiento de modelos: `gemini-3.5-flash-lite` (Routing) y `gemini-3.5-flash` (Generación fundamentada).
- **Evidencia**: Diagrama Mermaid en [`docs/architecture/architecture.md`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/docs/architecture/architecture.md).
- **Apoyo al Orador**:
  > [REQUIERE EXPLICACIÓN DEL EQUIPO: Recorrido por el flujo de componentes y justificación del pipeline.]

---

### Diapositiva 4: Enrutamiento Inteligente y Recuperación Dual Balanceada
- **Duración sugerida**: 1:15 min
- **Contenido Clave**:
  - Agente `GeminiSourceRouter`: Clasificación semántica hacia `internal`, `external` o `all` con fallback de seguridad.
  - Balanceo de cuotas: Asignación equitativa $k/2$ en consultas comparativas (`all`) para evitar que un dominio sature el contexto.
- **Evidencia**: Implementación en `app/agents/source_router.py` y `app/rag/pipeline.py`.
- **Apoyo al Orador**:
  > [REQUIERE EXPLICACIÓN DEL EQUIPO: Demostración de cómo se resolvió la contaminación cruzada entre fuentes.]

---

### Diapositiva 5: Seguridad, Prompting y Validación Estricta de Citas
- **Duración sugerida**: 1:15 min
- **Contenido Clave**:
  - Aislamiento de planos: Directivas de sistema separadas del contexto de datos en bloques XML (anti-Prompt Injection).
  - Citas obligatorias `[S#]` y rutina de autorreparación ante citas fantasma.
  - Verificación criptográfica SHA-256 de frescura del índice documental (`verify_index_freshness`).
- **Evidencia**: `app/rag/prompts.py`, `app/rag/generator.py`, `tests/test_security.py`.
- **Apoyo al Orador**:
  > [REQUIERE EXPLICACIÓN DEL EQUIPO: Argumentación sobre los mecanismos de integridad y seguridad de la información.]

---

### Diapositiva 6: Calibración Experimental y Compuerta de Abstención
- **Duración sugerida**: 1:30 min
- **Contenido Clave**:
  - Barrido de umbrales sobre dataset verificado de 20 casos (15 answerable, 5 OOD).
  - Justificación del umbral $\tau = 0.60$: 100% retención de casos legítimos y 0% de fuga en preguntas fuera de dominio.
  - Abstención temprana: corte inmediato del flujo si no hay evidencia $\ge 0.60$ (ahorro de cómputo y cero alucinaciones).
- **Evidencia**: Tabla de resultados en [`docs/evidence/evaluation-evidence.md`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/docs/evidence/evaluation-evidence.md).
- **Apoyo al Orador**:
  > [REQUIERE EXPLICACIÓN DEL EQUIPO: Presentación de los datos del barrido paramétrico y fundamentación de la decisión.]

---

### Diapositiva 7: Demostración en Vivo / Consola Web
- **Duración sugerida**: 1:30 min
- **Contenido Clave**:
  - Ejecución en vivo de consulta interna (`[INT]`), consulta externa (`[EXT]`) y consulta fuera de dominio (Abstención).
  - Interacción con citas `[S1]` $\to$ scroll y resaltado en el Evidence Ledger.
  - Despliegue de trazabilidad técnica.
- **Evidencia**: Guía paso a paso en [`docs/evidence/demo-runbook.md`](file:///c:/Users/jiqmo/OneDrive/Documentos/DocumentosDuocUC/ISY0101-IA/KnowledgeFlow%20RAG/docs/evidence/demo-runbook.md).
- **Apoyo al Orador**:
  > [REQUIERE EXPLICACIÓN DEL EQUIPO: Conducción de la demostración visual según el Demo Runbook.]

---

### Diapositiva 8: Limitaciones Identificadas, Lecciones y Cierre
- **Duración sugerida**: 1:00 min
- **Contenido Clave**:
  - Restricciones reales de cuota Free Tier (20 RPD) y estrategia de mitigación mediante desacoplamiento.
  - Suite de 156 pruebas offline automatizadas y harness de preview aislado.
  - Síntesis de aprendizajes en arquitectura RAG de nivel empresarial.
- **Apoyo al Orador**:
  > [REQUIERE EXPLICACIÓN DEL EQUIPO: Conclusiones finales, reflexiones del equipo y sesión de preguntas.]
