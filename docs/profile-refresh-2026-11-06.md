# Actualización del perfil · 6 de noviembre de 2026

## Decisiones

- Conservar la firma de terminal animada y la paleta verde/azul del perfil.
- Presentar primero identidad y proyectos; actividad como un bloque compacto inferior.
- Destacar Panter-ai y ZanaLLaima con descripciones basadas en sus README públicos.
- Conservar la invitación a investigación médica y sus límites de casos sintéticos.
- Reunir las descripciones ya públicas de proyectos privados en un desplegable.
- Mantener datos de actividad como registros fechados, sin widgets ni contadores externos.

## Fuentes consultadas

Consulta: **2026-11-06**.

| Información | Fuente |
| --- | --- |
| Panter-ai: coordinación entre aplicaciones, permisos, evidencia y ausencia de inferencia propia | [README público](https://github.com/riquelmechile/Panter-ai/blob/main/README.md), blob `79c7229e992263327a53eb88ea00e518e06beb08` |
| ZanaLLaima: MCP remoto, rama por misión, pruebas en Actions, revisión del commit exacto y E2E real pendiente de observar | [README público](https://github.com/riquelmechile/ZanaLLaima/blob/main/README.md), blob `b45b4b11eefdb2ac95c3e471716e6c0eff94254e` |
| Skills Chile | [README](https://github.com/riquelmechile/Skills-Chile/blob/main/README.md) y [catálogo](https://github.com/riquelmechile/Skills-Chile/blob/main/CATALOG.md) |
| Oráculo Chanchín: interpretación cultural, sin afirmación científica | [README público](https://github.com/riquelmechile/oraculo-chanchin/blob/main/README.md) |
| Integrador ME1: MVP, certificación y contratos pendientes | [README público](https://github.com/riquelmechile/mercadolibre-me1-chile-integrator/blob/main/README.md) |
| Actividad: 7.310 contribuciones; 76% commits, 19% PR, 4% issues, 1% code review | Captura del perfil aportada por su propietario en la conversación del 06-NOV-2026. Es una observación histórica, no una consulta API ni un contador en vivo. |

Los textos de colaboración sanitaria y sistemas privados se conservan a partir de las descripciones ya publicadas en este repositorio. No se incorporaron datos internos ni se investigaron repositorios privados.

## Verificación reproducible

```sh
python scripts/validate_profile.py
python -m unittest discover -s tests -p 'test_*.py' -v
```

Las tarjetas anteriores de actividad permanecen como archivo, sin ocupar la portada. Los nuevos assets llevan nombres distintos para evitar reutilizar su caché. La firma conserva sus valores, tiempos y repetición originales; se añade una versión estática para la preferencia de movimiento reducido.
