# Datos Locales Privados

Esta carpeta debe contener el libro fuente local:

```text
PRESUPUESTO-TULUA2.xlsx
```

Ese archivo no se versiona en Git porque contiene información privada y datos operativos del proyecto.

Al preparar un equipo nuevo:

1. Copiar manualmente `PRESUPUESTO-TULUA2.xlsx` en esta carpeta.
2. Mantener el nombre exacto del archivo.
3. Cerrar el archivo en Microsoft Excel antes de guardar cambios desde la app.

Los backups automáticos se generan en:

```text
04_implementation/data/backups/
```

La carpeta de backups también está ignorada por Git.
