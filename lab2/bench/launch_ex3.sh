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

  pkill -SIGTERM -f "ground_speed.py"
  pkill -SIGTERM -f "engine_speed.py"
  pkill -SIGTERM -f "pto_speed.py"
  echo ""
  echo "simulator background tasks have been halted"
}

trap catch_ctrlc INT

# launch the background processes
echo
echo "setting up 1 Hz simulation: text_ic      on vcan0"
echo "                            ground_speed on vcan1"
echo "                            engine_speed on vcan1"
echo "                            pto_speed    on vcan1"
echo

python3 ground_speed.py -b vcan1 -s 0x40 &
python3 engine_speed.py -b vcan1 -s 0x41 &
python3 pto_speed.py    -b vcan1 -s 0x42 &
echo "launched all generators for simulator"

python3 text_ic.py      -b vcan0 & 

sleep infinity

