#!/usr/bin/env bash

# some general bash setup to make working with shell scripts
# less frustrating. To enable tracing: "$ TRACE=1 ./launch.sh"
set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

# usage note
if [[ "${1-}" =~ ^-*h(elp)?$ ]]; then
  echo 'Usage: ./launch.sh'
  echo '       TRACE=1 ./launch.sh'
  echo ''
  echo 'Launches the lab network setup.'
  echo '* Use TRACE for script debuging.'
  echo ''
  exit
fi

# prepare to kill the background processes after we ^c 
# (if we don't, then "zombie" generator processes will continue to
# flood the canbus with traffic)
catch_ctrlc() {

  pkill -SIGTERM -f "nodeA.py"
  pkill -SIGTERM -f "nodeB.py"
  pkill -SIGTERM -f "pto_speed.py"
  echo ""
  echo "simulator background tasks have been halted"
}

trap catch_ctrlc INT

# launch the background processes
echo
echo "sharing public keys in order to generate a shared secret"
echo "                            nodeA        on vcan0"
echo "                            nodeB        on vcan0"
echo

python3 nodeA.py -b vcan0 -s 0x40 &
python3 nodeB.py -b vcan0 -s 0x41 &
echo "launched all nodes for simulator"



sleep infinity

