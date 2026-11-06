# Identidad visual de proyectos

Actualización: 06-NOV-2026. Las tarjetas `*-identity.svg` reemplazan los gráficos genéricos del README. Son SVG autónomos: la mascota está incorporada como vectores, sin imágenes rasterizadas ni referencias externas.

| Tarjeta | Origen del dibujo |
| --- | --- |
| Panter-ai | Mascota original [Panter](https://github.com/riquelmechile/Panter-ai/blob/main/docs/assets/panter-mascot.svg), blob `3f81db87bd6db70719303d6b9fa0845652658634`. SVG original conservado en `assets/projects/source/panter-mascot.svg`; aviso MIT en [licenses/Panter-ai-MIT.txt](licenses/Panter-ai-MIT.txt). |
| ZanaLLaima | [Zanahoria original](https://github.com/riquelmechile/ZanaLLaima/blob/main/assets/brand/zanallaima.svg), blob `c6a8e7eac9d2d20aedf8e6bd32166c87a6aa576d`. SVG original en `assets/projects/source/zanallaima-mascot.svg`; aviso MIT en [licenses/ZanaLLaima-MIT.txt](licenses/ZanaLLaima-MIT.txt). |
| IO | Adaptación del monograma circular del [hero público](https://github.com/riquelmechile/io/blob/main/docs/assets/io-hero-dark.svg), blob `e41bbec105d94be8d321bfa4db82298fd6f3fc32`. |
| zanaX | Interpretación vectorial del robot azul y banana de su [imagen social](https://github.com/riquelmechile/zanaX/blob/main/assets/social-preview.png), blob `ee77126852bda26dc4a2f372a99e84627122bfa8`. No se presenta como SVG original del proyecto. |
| MCP Doctor Chile | Ilustración nueva de estetoscopio y ficha; representa investigación, no acreditación clínica ni marca institucional. |
| Skills Chile | Ilustración nueva de tarjetas de conocimiento, estrella chilena y código, relacionada con su biblioteca de skills. |
| EAUTO-AI | Ilustración nueva de carrito y escudo de aprobación, relacionada con comercio y autoridad. |

Los dibujos nuevos son motivos del portafolio; no se declaran logos oficiales de los proyectos. Los originales antiguos se conservan sin enlazar desde el README para no romper referencias previas.

## Regeneración

```sh
python scripts/build_project_identity.py
python scripts/validate_profile.py
python -m unittest discover -s tests -p 'test_*.py' -v
```

La firma animada del perfil y la sección de actividad no se modifican.
