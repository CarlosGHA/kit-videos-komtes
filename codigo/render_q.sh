#!/bin/bash
# Uso: ./render_q.sh <n>   (renderiza UN vídeo de referencia por llamada; ver lista)
cd "$(dirname "$0")"
T=${KOMTES_WORK:-$(cd ../trabajo && pwd)}
SL=(x Incendio-rack Preaccion Falso-suelo Generadores)
case $1 in
1) python3 cpd_master.py es $T/vo/es_v3.mp3 45 $T/out/RG-WFOG_DataCenter_ES_1080x1350.mp4 ;;
2) python3 cpd_master.py en $T/vo/en_v2.mp3 45 $T/out/RG-WFOG_DataCenter_EN_1080x1350.mp4 ;;
3) python3 cpd_master.py es $T/vo/es_v3.mp3 169 $T/out/RG-WFOG_DataCenter_ES_1920x1080.mp4 ;;
4) python3 cpd_master.py en $T/vo/en_v2.mp3 169 $T/out/RG-WFOG_DataCenter_EN_1920x1080.mp4 ;;
5) python3 siex2_master.py es $T/vo_siex2/es_v4.mp3 45 $T/out_siex2/SIEX_DataCenter_ES_1080x1350.mp4 ;;
6) python3 siex2_master.py en $T/vo_siex2/en_fixed.mp3 45 $T/out_siex2/SIEX_DataCenter_EN_1080x1350.mp4 ;;
7) python3 siex2_master.py es $T/vo_siex2/es_v4.mp3 169 $T/out_siex2/SIEX_DataCenter_ES_1920x1080.mp4 ;;
8) python3 siex2_master.py en $T/vo_siex2/en_fixed.mp3 169 $T/out_siex2/SIEX_DataCenter_EN_1920x1080.mp4 ;;
9|10|11|12) p=$(( $1 - 8 )); mkdir -p $T/out/linkedin
   PIEZA=$p python3 cpd_master.py es $T/vo/es_v3.mp3 45 $T/out/linkedin/RG-WFOG_DataCenter_ES_1080x1350_LinkedIn${p}_${SL[$p]}.mp4 ;;
*) echo "1-4 RG (ES/EN x 4:5/16:9) · 5-8 SIEX · 9-12 piezas LinkedIn RG (4:5)"; exit 1 ;;
esac
