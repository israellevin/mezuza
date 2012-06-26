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

# One day we may want to get only x newest files
#[ "$1" ] && limit=$1 || limit=100
#for f in $(stat -c "%Y %n" img/*.png | sort -rn | tail -n $limit | cut -d ' ' -f 1 --complement); do
