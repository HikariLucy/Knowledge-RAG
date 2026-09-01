# NIST SP 800-218: Secure Software Development Framework (SSDF)

> **Aviso de Procedencia**: Documento técnico de procedencia externa real.
> **Organización / Autores**: National Institute of Standards and Technology (NIST), U.S. Department of Commerce.
> **URL de Origen**: https://csrc.nist.gov/pubs/sp/800/218/final
> **Fecha de Acceso**: 2026-09-01
> **Temática**: Prácticas fundamentales de desarrollo seguro de software y mitigación de vulnerabilidades.

## 1. Protección del Software y Gestión de Secretos (Protect Software - PS)
La práctica PS.1 exige salvaguardar todas las formas de código fuente, configuración y componentes de software frente a accesos no autorizados y manipulaciones maliciosas.
- **Gestión Segura de Secretos**: Las claves de API, tokens de autenticación y contraseñas nunca deben almacenarse en repositorios de código versionado.
- **Variables de Entorno Centralizadas**: Se debe utilizar inyección de configuración basada en variables de entorno seguras y plantillas controladas (.env.example).
- **Control de Integridad**: Emplear firmas criptográficas y hashes para verificar la autenticidad e integridad de dependencias y binarios antes de su despliegue.

## 2. Producción de Software Bien Asegurado (Produce Well-Secured Software - PW)
La práctica PW.8 instruye la verificación rigurosa de la seguridad del software mediante estrategias de prueba automatizadas:
- **Estrategia de Pruebas**: Construir pirámides de testing donde las pruebas unitarias rápidas y deterministas cubran las reglas de negocio críticas sin dependencias de red inestables.
- **Análisis Estático y Dinámico**: Implementar linters y análisis de seguridad continuo para detectar vulnerabilidades comunes antes del paso a producción.

## 3. Respuesta a Vulnerabilidades e Incidentes (Respond to Vulnerabilities - RV)
La práctica RV.1 define que las organizaciones deben monitorear continuamente vulnerabilidades reportadas, investigar incidentes y documentar informes post-mortem estructurados para prevenir reincidencias.
