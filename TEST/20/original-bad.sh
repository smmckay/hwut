if [ "$1" = "--hwut-info" ]; then
    echo "$0 has been interviewed" >> $(cat interview_file_name.txt)
fi
echo bad
