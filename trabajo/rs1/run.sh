cd /home/claude
for a in "groom 0" "gnoz 0" "gdoor 0" "gmed 0" "gmed 1" "gfloor 0" "gfloor 1" "gwide 0" "gwide 1"; do set -- $a; python3 siex_scene.py /tmp/claude-0/-home-claude/9170677f-e914-5fad-9582-ded74f623b9a/scratchpad/rs1 $1 80 1.25 $2 2>&1 | grep -E "RENDERED|Error"; done
echo ALLDONE
