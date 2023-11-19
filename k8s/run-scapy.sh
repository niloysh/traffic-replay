#!/bin/bash

# This script copies a Scapy Python script from the scripts directory 
# and runs it on a Kubernetes container. It requires a keyword to identify the pod,
# the name of the Scapy script file, and the namespace as command-line arguments.

# Command-line arguments
KEYWORD=$1
SCRIPT_FILE=$2
NAMESPACE=$3
SCRIPT_DIR="../scripts"

function usage {
  echo "Usage: $0 keyword pcap_file namespace"
  echo "       keyword: a string to identify the pod (e.g., part of the pod name)"
  echo "       script_file: the name of the Scapy Python script file in the scripts directory"
  echo "       namespace: the Kubernetes namespace where the pod is located"
}

# Check for the correct number of arguments
if [ "$#" -ne 3 ]; then
  usage
  exit 1
fi

# Check if the script file exists
if [ ! -f "$SCRIPT_DIR/$SCRIPT_FILE" ]; then
  echo "Error: Script file '$SCRIPT_FILE' not found in '$SCRIPT_DIR'."
  exit 1
fi

# Get the pod name using the keyword
POD=$(kubectl get pods -n "$NAMESPACE" | grep "$KEYWORD" | awk '{print $1}')

# Check if the pod exists
if [ -z "$POD" ]; then
  echo "Error: Pod with keyword '$KEYWORD' not found in namespace '$NAMESPACE'."
  exit 1
fi

# Copy the script file to a temporary location in the container
kubectl cp "$SCRIPT_DIR/$SCRIPT_FILE" "$NAMESPACE/$POD:/tmp/$SCRIPT_FILE"

# Execute the script inside the container
kubectl exec -it -n "$NAMESPACE" "$POD" -- bash -c "python3 /tmp/$SCRIPT_FILE"
