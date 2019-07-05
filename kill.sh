#/bin/bash
ps -W | grep "$1" | awk '{print $1}' | xargs kill -f;
