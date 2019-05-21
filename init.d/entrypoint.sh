#!/bin/bash +e
# catch signals as PID 1 in a container

# SIGNAL-handler
term_handler() {

  echo "terminating scan process ..."
  /etc/init.d/startotscan.sh stop

  echo "terminating ssh ..."
  /etc/init.d/ssh stop

  exit 143; # 128 + 15 -- SIGTERM
}

# on callback, stop all started processes in term_handler
trap 'kill ${!}; term_handler' SIGINT SIGKILL SIGTERM SIGQUIT SIGTSTP SIGSTOP SIGHUP

# run applications in the background
echo "starting ssh ..."
/etc/init.d/ssh start

# create netx "cifx0" ethernet network interface 
/opt/cifx/cifx0daemon

#bring "cifx0" to state up
ip link set cifx0 up

#set "cifx0" ip and broadcast address based on given environment variables the container was started with (readme.txt)
ip addr add $FIELDBUS_IP/24 broadcast ${FIELDBUS_IP%.*}.255 dev cifx0

#start python scanning script 
echo "starting scanning process..."
export PYTHONPATH=${PYTHONPATH}:/opt/scan/profinet
/etc/init.d/startotscan.sh start

# wait forever not to exit the container
while true
do
  tail -f /dev/null & wait ${!}
done

exit 0
