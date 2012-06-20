#!/bin/sh
cd /home/student/mezuza
cp /shared/*.png img/. > /dev/null 2>&1
s='{"images": ['
for f in img/*.png; do
    s=$s'"'$f'"',
done
s=$(echo $s | sed '$s/.$//')']}'

echo "Content-Type: application/json

$s
"
exit 0
