# Checklist Operacional para el Día de la Demostración (Demo Day Checklist) — KnowledgeFlow RAG

Este documento provee una lista de verificación paso a paso para asegurar que el entorno de demostración se encuentre listo, libre de bloqueos de puerto y con un plan de contingencia claro antes de exponer frente a la comisión evaluadora.

---

## 1. Verificación Previa (30 minutos antes de la presentación)

- [ ] **1.1. Repositorio y Rama**:
  - Asegurar que el working tree esté limpio en la rama `main`:
    ```powershell
    git checkout main
    git status
    ```
- [ ] **1.2. Clave de API y Entorno**:
  - Confirmar que el archivo `.env` contiene la variable `GEMINI_API_KEY` válida y sin comillas adicionales.
- [ ] **1.3. Liberación del Puerto 8010**:
  - Comprobar que no existan procesos huérfanos escuchando en el puerto 8010:
    ```powershell
    netstat -ano | findstr :8010
    ```
  - Si aparece un PID activo, finalizar el proceso:
    ```powershell
    taskkill /PID <PID_NUMERO> /F
    ```
- [ ] **1.4. Comprobación de Salud de la API**:
  - Iniciar brevemente el servidor de pruebas y verificar `GET /health`:
    ```powershell
    # Debe responder: {"status":"ok","service":"KnowledgeFlow RAG"}
    ```
- [ ] **1.5. Estado del Navegador**:
  - Abrir una pestaña limpia en `http://127.0.0.1:8010/` y verificar que el diseño editorial y el selector segmentado se rendericen con claridad.

---

## 2. Plan A: Demostración en Vivo Real (Recomendado)

> **Condición**: Cuota de Google Gemini disponible y conexión de red estable.

### Comando de Inicio:
```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8010
```

### Secuencia de Consultas para la Demo Real:
1. **Consulta 1 (Interna)**: `¿Qué requisitos deben cumplir las contraseñas internas?`
   - *Demostrar*: Clasificación `internal`, cita `[S1]`, clic interactivo con scroll y resaltado de `politica_accesos.md` en el Evidence Ledger.
2. **Consulta 2 (Externa)**: `¿Cómo se previene Prompt Injection según OWASP?`
   - *Demostrar*: Clasificación `external`, procedencia verde bosque `[EXT]`, recomendaciones autoritativas de OWASP.
3. **Consulta 3 (Comparativa Dual)**: `Compara el procedimiento interno de incidentes con buenas prácticas externas.`
   - *Demostrar*: Recuperación balanceada multi-fuente `INT` + `EXT` con fuentes combinadas en el Evidence Ledger.
4. **Consulta 4 (Abstención Controlada)**: `¿Cuál es la velocidad de la luz en el vacío?`
   - *Demostrar*: Tarjeta de **"EVIDENCIA INSUFICIENTE"** al no superar el umbral $\tau \ge 0.60$, cortando el flujo antes de generar para evitar alucinaciones.

---

## 3. Plan B: Demostración Offline de Respaldo (Contingencia)

> **Condición de Activación**: Fallo de conectividad a internet en la sala, error HTTP 429 (límite de cuota alcanzado) o caída de los servidores de Google Gemini.

> [!WARNING]
> **Aclaración Obligatoria ante la Comisión Evaluadora**:
> Si se activa este modo, el equipo debe declarar de forma transparente:  
> *"Por indisponibilidad temporal de la API externa / red, estamos activando nuestro harness de UI Preview offline con fixtures locales para demostrar la interacción de la interfaz y la trazabilidad del contrato."*  
> **EL PREVIEW OFFLINE NO CONSTITUYE EVIDENCIA DE RENDIMIENTO DEL MOTOR RAG.**

### Comando de Inicio de Respaldo:
```powershell
python -m uvicorn scripts.ui_preview:app --reload --host 127.0.0.1 --port 8010
```

### Consultas Compatibles con el Harness de Preview:
- **Interna**: `¿Qué requisitos deben cumplir las contraseñas internas?`
- **Externa**: `¿Cómo se previene Prompt Injection según OWASP?`
- **Mixta**: `Compara el procedimiento interno de incidentes con buenas prácticas externas.`
- **Abstención**: `¿Cuál es la velocidad de la luz en el vacío?`
- **Alta Densidad**: `Auditoría integral de accesos, incidentes, inyección de prompts y desarrollo seguro`
- **Error 500**: `PREVIEW_ERROR_500`

---

## 4. Checklist Post-Demostración

- [ ] Detener el servidor con <kbd>Ctrl</kbd>+<kbd>C</kbd> en la terminal.
- [ ] Cerrar las pestañas del navegador.
- [ ] Abrir el espacio de preguntas y tener a mano el documento [`defense-question-bank.md`](defense-question-bank.md) para respaldar técnicamente cada respuesta.
