# NIST Privacy Framework: Data Minimization and Protection Guidelines

> **Aviso de Procedencia**: Documento técnico de procedencia externa real.
> **Organización / Autores**: National Institute of Standards and Technology (NIST).
> **URL de Origen**: https://www.nist.gov/privacy-framework/privacy-framework
> **Fecha de Acceso**: 2026-09-01
> **Temática**: Directrices de minimización de datos, expiración de registros y protección criptográfica.

## 1. Principio y Práctica de Minimización de Datos (CT.DM-P)
La categoría CT.DM del marco de privacidad de NIST establece que las organizaciones deben limitar la recopilación, almacenamiento y procesamiento de datos personales e institucionales exclusivamente a lo indispensable para el propósito operacional legítimo.
- **Recolección Proporcional**: Se debe restringir la ingesta de información sensible o PII a los campos estrictamente requeridos.
- **Prevención de Sobre-Retención**: Los sistemas deben auditar regularmente los conjuntos de datos persistidos para evitar la acumulación injustificada de información histórica.

## 2. Políticas de Retención, Expiración y Purga (CT.DP-P)
Para garantizar la privacidad y cumplimiento normativo:
- **Expiración Automatizada**: Implementar mecanismos automáticos de expiración para datos temporales, registros de sesiones y tokens.
- **Purga y Destrucción Segura**: Aplicar eliminación criptográfica y sobreescritura segura una vez que los datos cumplan su período de retención legal u operativo.

## 3. Protección de Datos en Reposo y en Tránsito (PR.DS-P)
- **Cifrado en Tránsito**: Todas las transmisiones a través de redes públicas o internas deben utilizar TLS 1.3 con conjuntos de cifrado modernos.
- **Cifrado en Reposo**: La persistencia de bases de datos, almacenamiento de objetos y respaldos debe implementar algoritmos estándar como AES-256.
