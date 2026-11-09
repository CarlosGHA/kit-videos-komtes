# Ficha de producto confirmada · RG Systems · RG W-FOG (agua nebulizada)

Hechos validados por I+D durante la producción del vídeo «Centros de datos» (oct–nov 2026). Léela antes del guion de cualquier vídeo de RG W-FOG y amplíala con lo que confirme el ingeniero en cada ronda de feedback. Si algo de aquí choca con lo que diga el ingeniero, manda el ingeniero: actualiza la ficha.

## Nomenclatura (nombre comercial · qué es · EN)

| Referencia | Qué es | EN |
|---|---|---|
| W-FOG UAP | Grupo de bombeo (motor eléctrico + bomba de pistones) | pump unit |
| WF-PAV | Válvula de preacción | pre-action valve |
| WF-SV | Válvula de sección | section valve |
| WF-VC | Válvula de control | control valve |
| RG W-FOG UAC | Batería de cilindros de agua + nitrógeno («combi»), anclada a la pared | cylinder bank |
| MM-P51 | Difusor ambiente de centro de datos (cerrado, con ampolla) | data center nozzle |
| MM-P52 / MM-P53 | Difusores de falso suelo (sistema de «área de cobertura») | area of coverage |
| MM-P50 | Difusor para zonas de personal (oficinas, centro de control); misma forma, tamaño y funcionamiento que la MM-P51 | — |
| EMM-416549 | Difusor abierto para espacios de maquinaria (plateado); sus insertos se llaman «Microdifusores» | machinery spaces nozzle |

- La MM-P51 también se usa en falso suelo para sistema de «aplicación local» (local application).
- Todos los difusores son de color acero inoxidable. Sus orificios son agujeros reales, no relieve.
- Difusores cerrados de CPD (techo y falso suelo): solo 2 filas de micro-orificios. El de techo lleva adaptador M32 + embellecedor NS1; el de falso suelo, el adaptador M32 normal, sin embellecedor.

## Aprobaciones

- Se dice **«aprobado por FM» / «FM APPROVED»**, nunca «certificado».
- MM-P50: aprobada por FM para riesgos HC-1. El centro de control (MM-P50 + WF-SV) también es FM Approved.
- **RG W-FOG UAC no tiene aprobación para centro de datos.** Solo se muestra en otros riesgos del edificio (salas de generadores y transformadores).

## Válvulas: montaje e identificación de piezas

- Las tres (WF-PAV, WF-SV, WF-VC) van **en vertical**: el agua (de la bomba o de las botellas) entra por el tubo de la izquierda y sale hacia los colectores por el tubo inferior.
- La palanca de latón con anilla de arriba es el **disparo manual** en las tres.
- **WF-PAV:** lo negro es la solenoide; el presostato es la pieza de latón con el manómetro grande encima; la pieza azul es el interruptor de confirmación de activación.
- **WF-SV:** la pieza gris es el detector de paso de agua.
- **WF-VC:** lo negro de arriba es la solenoide que la abre por señal de la central; la caja negra de la derecha es el presostato que confirma el paso de agua.
- No llamar «preacción» a una válvula de sección o de control.

## Funcionamiento por zona

- **Sala de CPD (WF-PAV + detección electrónica):** tubería húmeda del grupo a la válvula y seca, presurizada con aire, hasta los difusores. Rotura accidental de una ampolla → alarma del presostato y la válvula sigue cerrada. Falsa alarma de detección → no hay descarga. Protege «frente a falsas alarmas y accidentes».
- **Zonas de personal y centro de control (MM-P50 + WF-SV):** tubería húmeda, red llena de agua hasta los difusores cerrados. Al activarse un difusor descarga sin esperar a la detección; la WF-SV (normalmente abierta) detecta el paso de agua, avisa a la central de qué sala ha descargado y permite cerrar el flujo para volver a poner el sistema en servicio.
- **Generadores y transformadores (UAC + WF-VC + EMM):** dos válvulas de control WF-VC junto a la batería, una por sala. Los detectores identifican el incendio y la central abre solo la válvula de esa sala.
- **Arranque del grupo:** «la caída de presión produce el arranque» (no «arranca el grupo»).

## Instalación (lo que debe verse en el 3D)

- Red de falso suelo **por encima de las bandejas de cables**, con los difusores descargando hacia abajo sobre ellas.
- Cada red acaba en su último difusor, con tapón; nada sigue hasta la pared.
- Una válvula por zona o sala; cada red llega solo a los difusores de su sala.
- Cilindros UAC con etiqueta blanca de RG Systems y batería anclada a la pared.

## Textos: sí y no

| Sí | No |
|---|---|
| ambiente y falso suelo | sobre y bajo suelo técnico |
| bandejas de cables | mazos |
| boquilla activada | ampolla rota |
| gases tóxicos | gases corrosivos |
| detectores | detectores de llama |
| actúa por enfriamiento y desplazamiento de oxígeno | sofocar el vapor |
| — | equipos en tensión |
| — | 400 V · 50 Hz (puede ser 60 Hz) |

- En animaciones: agua en azul; nitrógeno y demás gases en rojo.
