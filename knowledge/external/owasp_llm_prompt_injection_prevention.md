# OWASP LLM Prompt Injection Prevention Cheat Sheet

> **Aviso de Procedencia**: Documento técnico de procedencia externa real.
> **Organización / Autores**: OWASP (Open Web Application Security Project) Cheat Sheet Series.
> **URL de Origen**: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html
> **Fecha de Acceso**: 2026-09-01
> **Temática**: Prevención de inyección directa e indirecta de prompts en aplicaciones basadas en Large Language Models (LLM).

## 1. Definición y Tipos de Prompt Injection
La inyección de prompts ocurre cuando un atacante manipula las entradas hacia un modelo de lenguaje para alterar su comportamiento previsto, eludir restricciones de seguridad o forzar la ejecución de acciones no autorizadas.
- **Inyección Directa (Jailbreaking)**: El usuario introduce instrucciones maliciosas directamente en el prompt del sistema o de usuario.
- **Inyección Indirecta**: El modelo procesa contenido externo no confiable (páginas web, correos electrónicos, documentos RAG recuperados) que contiene instrucciones maliciosas incrustadas para secuestrar el flujo conversacional.

## 2. Separación de Planos de Control y Datos
Para mitigar la inyección de prompts:
- Trate todo contexto recuperado o entrada externa como datos no confiables y jamás como instrucciones ejecutables.
- Utilice delimitadores estructurales claros (bloques etiquetados de contexto) para separar los datos documentales del System Prompt.
- Sanitice y valide las entradas antes de procesarlas, filtrando secuencias de control o instrucciones de override ("ignora instrucciones previas").

## 3. Principio de Menor Privilegio y Salidas Estructuradas
- Restrinja el acceso del LLM a herramientas y funciones (function calling) únicamente a las operaciones indispensables para su propósito.
- Valide y codifique las respuestas generadas antes de entregarlas a clientes o integraciones aguas abajo para evitar Cross-Site Scripting (XSS) o ejecución indebida.
