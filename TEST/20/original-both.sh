if [ "$1" = "--hwut-info" ]; then
    echo "$0 has been interviewed" >> $(cat interview_file_name.txt)
    echo "both;"
    echo "CHOICES: good, bad;"
    echo "SAME;"
    exit 0
fi
echo $1
