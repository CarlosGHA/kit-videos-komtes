#!/bin/bash
# uso: bash rg_lane.sh es_45 [es_169 en_45 en_169]  · renderiza los vídeos RG W-FOG Centros de datos (locución v6)
K=$(cd "$(dirname "$0")/.." && pwd); cd $K/codigo; mkdir -p $K/trabajo/out
for job in "$@"; do
  lg=${job%_*}; asp=${job#*_}
  vo=$K/trabajo/vo/v6c_es.mp3; [ $lg = en ] && vo=$K/trabajo/vo/v6c_en.mp3
  W=1080x1350; [ $asp = 169 ] && W=1920x1080
  out=$K/trabajo/out/RG-WFOG_DataCenter_${lg^^}_$W.mp4
  python3 cpd_master.py $lg $vo $asp $out 2>&1 | grep -a -E "^done|rror|Trace" -A3
  rm -f $out.noaudio.mp4* $out.vo.wav; echo "JOB_DONE $job $(date +%H:%M)"
done
