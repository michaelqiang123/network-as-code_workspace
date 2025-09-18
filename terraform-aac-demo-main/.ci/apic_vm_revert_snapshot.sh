#!/bin/bash
DATA='{"action": "revert"}'
curl --data "$DATA" --silent --user $MIQ_USERNAME:$MIQ_PASSWORD --insecure --header "Content-Type: application/json" --request POST $MIQ_URL/api/vms/$MIQ_VM/snapshots/$MIQ_SNAPSHOT