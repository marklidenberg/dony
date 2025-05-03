

sshpass -p $SERVER_PASSWORD                       rsync --archive --verbose --compress --progress                         "$SERVER_USERNAME@$SERVER_HOST:/root/home/data/umalat/2025-04-28"                         app/data/dynamic/
sshpass -p "$SERVER_PASSWORD"               ssh -o StrictHostKeyChecking=no "$SERVER_USERNAME@$SERVER_HOST"               'for i in {0..7}; do
     d=$(date -d "$i days ago" +%Y-%m-%d)
     ls -d /root/home/data/umalat/${d}* 2>/dev/null
   done                | grep -v "\.git"                | grep -Ev "_[0-9]+(_[0-9]+)?$"'
