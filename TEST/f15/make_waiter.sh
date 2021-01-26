sleep_t=$1
claim_sleep_t=$1
printf "if [ \"\$1\" = \"--hwut-info\" ]; then\n"
printf "    echo \"Sleep $claim_sleep_t [sec]\"\n"
printf "else\n"
printf "    sleep $sleep_t\n"
printf "    echo Hallo\n"
printf "fi\n"
