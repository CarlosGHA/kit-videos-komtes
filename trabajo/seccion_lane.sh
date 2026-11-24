#!/bin/bash
# uso: bash seccion_lane.sh 1 [2 3 4 5]  · episodios de la sección «Riesgo a riesgo» (4:5, voz EN + textos ES)
K=$(cd "$(dirname "$0")/.." && pwd); cd $K/codigo; mkdir -p $K/trabajo/out_seccion
for p in "$@"; do
  slug=$(python3 -c "import sys;sys.argv=['x','es'];import cpd_final as F;print(F.PIECES[$p-1]['slug'])" 2>/dev/null | tail -1)
  out=$K/trabajo/out_seccion/RG-WFOG_DataCenter_RiesgoARiesgo_${slug}_VozEN-SubES_1080x1350.mp4
  PIEZA=$p SUB_LANG=es python3 cpd_master.py en $K/trabajo/vo/v6c_en.mp3 45 $out 2>&1 | grep -a -E "^done|rror|Trace" -A3
  rm -f $out.noaudio.mp4* $out.vo.wav; echo "JOB_DONE $p $(date +%H:%M)"
done
