#! /usr/bin/env bash
if [ "$1" = "--hwut-info" ]; then
    echo "Oversizer;";
    echo "CHOICES: quicky, slow-starter, stalker;"
    exit 0
fi

case $1 in
    quicky)
    # start blowing without hesitation
    ;;
    slow-starter)
    # wait a second before blowing
    sleep 1
    ;;
    stalker)
    sleep 1
    for i in $(seq 0 100); do 
        echo "123456789"
    done
    # approach the 1MB slowly, then blast
    for i in $(seq 0 90000); do 
        echo "123456789"
    done
    echo "Done less than 1MB"
    # The output has not yet a size of 1 MB.
    # Sleep to simulate slowliness
    sleep 1
    # Then flush brutally.
    ;;
esac

# Write something that is 20MB large.
# Recall: HWUT_OUTPUT_FILE_MAX_SIZE = 1MB
for i in $(seq 0 327680); do
    echo "01234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" # 64 byte
done
