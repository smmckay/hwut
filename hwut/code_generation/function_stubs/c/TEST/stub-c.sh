if [ "--hwut-info" == "$1" ]; then
    echo "HWUT Stub Festival: C"
else
    rm -f hwut_stub.*
    
    # Compatibility Windows etc.
    python ../../../../../hwut-exe.py stub stub-description.c -o hwut_stub
    echo hwut_stub.h: lines, words, bytes
    echo
    wc hwut_stub.h
    echo
    echo hwut_stub.c: lines, words, bytes
    echo
    wc hwut_stub.c
    echo 
    echo "Compiling (no output is good output)"
    echo 
    gcc hwut_stub.c -c -o a.o
    ls a.o
    rm a.o
    
    # rm hwut_stub.c
    # rm hwut_stub.h
fi
