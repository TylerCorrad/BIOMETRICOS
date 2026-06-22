# BIOMETRICOS
Proyecto de automatización de reportes de asistencia laboral
##  Arquitectura del flujo

```mermaid
graph
I[usuarios registran asistencia]-->
A[Excel Huelleros ] -- Carpeta en red --> B[Script en Python]
B --> C[Archivo base limpio]
C --> D[Plantilla de excel con Power Query]
D --> E[reporte final con tablas dinámicas]
```

##  Dependencias

Para el correcto funcionamiento de esta automatización se requiere tener instalados en el computador donde se ejecutarán los reportes:
### python v 3.x
---
**librerias:**
- pandas 
- openpyxl
- oracledb

### Oracle Instant Client v.19.30
---
Una vez instalado mover la carpeta a **"C:\Oracle"**. Asegurarse de que la carpeta tenga como nombre ***"instantclient_19_30"***

---
## Estructura del proyecto
	/BIOMETRICOS
		|-Huelleros/ 	-Archivos de entrada (DIT, CASETA,ADMIN)
		|-SQL/ 			-Script SQL
		|-Scripts/		-Código Python
		|-Excel/		-Archivos de excel (archivo base y plantilla)
		|-README.md
