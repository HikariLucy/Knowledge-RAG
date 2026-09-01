# Framework de Evaluación — KnowledgeFlow RAG

Este directorio contiene los datasets de evaluación controlada y los resultados generados por el framework de evaluación sistemática de **KnowledgeFlow RAG**.

---

## 1. Puerta de Revisión Humana (*Human Review Gate*)

El dataset inicial generado automáticamente se encuentra en:
- **`evaluation/dataset_draft.json`**: Todos los registros inician con `"human_reviewed": false`.
- **Aviso**: Las ejecuciones sobre `dataset_draft.json` son de carácter **exploratorio** y no deben presentarse como evidencia final académica.

Para promover un dataset a versión oficial:
1. El equipo revisa analíticamente cada caso en `evaluation/dataset_draft.json`.
2. Se valida la coherencia de `expected_scope`, `expected_files` y `answerable`.
3. Se actualiza cada caso con `"human_reviewed": true`.
4. Se guarda como **`evaluation/dataset_verified.json`**.

---

## 2. Estructura de Casos (`EvaluationCase`)

Cada caso de evaluación responde al siguiente esquema:

```json
{
  "id": "EVAL-001",
  "query": "¿Cómo debo reportar un incidente de seguridad y a qué canales?",
  "category": "internal",
  "expected_scope": "internal",
  "answerable": true,
  "expected_source_types": ["internal"],
  "expected_files": ["procedimiento_incidentes.md"],
  "expected_behavior": "grounded_answer",
  "notes": "Procedimiento de notificación por correo o ticket.",
  "human_reviewed": false
}
```

Para consultas fuera de dominio (`out_of_domain`):
- `expected_scope`: `null` (no participa en accuracy del router).
- `answerable`: `false`.
- `expected_files`: `[]`.
- `expected_behavior`: `"abstain"`.

---

## 3. Comandos de Evaluación

### Ejecución Exploratoria
```powershell
python -m app.evaluation.runner --dataset evaluation/dataset_draft.json
```

### Ejecución Oficial Estricta (Requiere dataset revisado y working tree limpio)
```powershell
python -m app.evaluation.runner --dataset evaluation/dataset_verified.json --require-reviewed --require-clean
```

### Barrido de Umbrales de Similitud (*Threshold Sweep*)
```powershell
python -m app.evaluation.threshold_sweep --dataset evaluation/dataset_draft.json
```

---

## 4. Métricas Calculadas

- **Source Router Accuracy**: Exactitud y matriz de confusión $3 \times 3$ sobre casos con alcance esperado explícito.
- **Retrieval Hit@K**: Proporción de casos donde al menos un archivo esperado apareció en Top-K.
- **Mean Reciprocal Rank (MRR)**: Posición inversa media de la primera fuente relevante ($1/r$).
- **Expected Source Recall@K**: Fracción de fuentes esperadas recuperadas a nivel de archivo.
- **Source Scope Compliance**: Cumplimiento del filtro estricto por procedencia.
- **Dual Source Coverage**: Cobertura combinada (interna y externa) en consultas de alcance `all`.
- **Abstention Metrics**: Exactitud, precisión y recall considerando la abstención como clase positiva.
- **Citation Integrity & Traceability**: Verificación de presencia de citas válidas y trazabilidad contractual de la respuesta generada.
