# CV Research Dashboard

Dashboard interactivo en Python para presentar el perfil profesional, la experiencia, la formación, las competencias y la actividad investigadora de Jose Francisco Pedrero Sánchez.

## Propuesta funcional

- Portada profesional con foto, perfil, métricas científicas y enlaces.
- Pestañas para experiencia laboral, formación académica y mapa de aptitudes.
- Investigación con filtros por entidad financiadora y años.
- Visualización de proyectos por año, financiador y temática.
- Sección preparada para publicaciones agrupadas por temática, revista y cuartil.
- Datos de proyectos leídos desde `Info/proyectos_IBV_experiencia_investigadora.md`.

## Ejecutar con Docker

```bash
docker compose up --build
```

Después abre:

```text
http://localhost:8502
```

## Ejecutar en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Próximas iteraciones recomendadas

- Convertir publicaciones a un archivo estructurado con título, año, DOI, revista, temática, JCR/SJR y cuartil.
- Añadir modo público/privado para ocultar teléfono o email según despliegue.
- Añadir exportación a PDF o una vista compacta tipo CV tradicional.
- Conectar Google Scholar, ORCID o Scopus si se quiere refresco automático de métricas.
