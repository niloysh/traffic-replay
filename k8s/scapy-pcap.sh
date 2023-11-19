#!/bin/bash

# This script copies a Scapy Python script from the scripts directory 
# and runs it on a Kubernetes container. It requires a keyword to identify the pod,
# the name of the Scapy script file, and the namespace as command-line arguments.
# It also takes a pcap file as input.

# Command-line arguments
KEYWORD=$1
SCRIPT_FILE=$2
PCAP_FILE=$3
NAMESPACE=$4
SCRIPT_DIR="../scripts"
PCAP_DIR="../pcaps"

function usage {
  echo "Usage: $0 keyword script_file pcap_file namespace"
  echo "       keyword: a string to identify the pod (e.g., part of the pod name)"
  echo "       script_file: the name of the Scapy Python script file in the scripts directory"
  echo "       pcap_file: the name of the pcap file in the pcaps directory"
  echo "       namespace: the Kubernetes namespace where the pod is located"
}

# Check for the correct number of arguments
if [ "$#" -ne 4 ]; then
  usage
  exit 1
fi

# Check if the script file exists
if [ ! -f "$SCRIPT_DIR/$SCRIPT_FILE" ]; then
  echo "Error: Script file '$SCRIPT_FILE' not found in '$SCRIPT_DIR'."
  exit 1
fi

# Check if the pcap file exists
if [ ! -f "$PCAP_DIR/$PCAP_FILE" ]; then
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

# Copy the script file and pcap file to a temporary location in the container
kubectl cp "$SCRIPT_DIR/$SCRIPT_FILE" "$NAMESPACE/$POD:/tmp/$SCRIPT_FILE"
kubectl cp "$PCAP_DIR/$PCAP_FILE" "$NAMESPACE/$POD:/tmp/$PCAP_FILE"

# Execute the script inside the container
kubectl exec -it -n "$NAMESPACE" "$POD" -- bash -c "python3 /tmp/$SCRIPT_FILE /tmp/$PCAP_FILE"
