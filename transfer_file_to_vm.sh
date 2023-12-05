if [ $# -ne 2 ]; then
    echo "Usage: $0 <source_file> <destination_file>"
    exit 1
fi

gcloud compute scp $1 sardibarnabas@isolated-test-vm:$2 --zone europe-west3-c