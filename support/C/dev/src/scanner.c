#include <support/C/hwut_scanner.h>

int   
hwut_isspace(char C) 
{ return C == ' ' || C == '\t' || C == '\n' || C == '\r'; }

int 
hwut_isnumber(char C)
{ return C >= '0' && C <= '9'; }

int
hwut_strlen(const char* Begin)
{ 
    const char* end   = Begin;
    while( *end ) ++end; 
    return end - Begin;
}

const char*   
hwut_find(char C, const char* iterator) 
{ while( *iterator != C && *iterator != '\0' ) ++iterator; return iterator; }

const char*   
hwut_find_before(char C, const char* iterator, const char* End) 
{ while( *iterator != C && *iterator != '\0' && iterator != End ) ++iterator; return iterator; }

void   
hwut_skip_whitespace(const char** iterator) 
{ while( hwut_isspace(**iterator) && **iterator != '\0') ++(*iterator); }

void   
hwut_skip_whitespace_backwards(const char** iterator, const char* Limit) 
{ 
    while( *iterator != Limit ) { 
        if( ! hwut_isspace(**iterator) || (**iterator == '\0') ) return;
        --(*iterator);
    }
}

void   
hwut_skip_until_whitespace(char** iterator) 
{ while( ! hwut_isspace(**iterator) && **iterator != '\0') ++(*iterator); }

int
hwut_scan_integer(const char** iterator)
{
    long  result = 0;
    hwut_skip_whitespace(iterator);
    for(result = 0; hwut_isnumber(**iterator); ++(*iterator) ) {
        result *= 10;
        result += **iterator - '0';
    }
    return result;
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>

void
hwut_error(const char* Msg)
{ 
    fprintf(stderr, Msg); 
    exit(-1);
}

void
hwut_memmove(void* drain, void* source, size_t ByteN)
{
    memmove(drain, source, ByteN);
}

void
hwut_memset(void* drain, char Value, size_t ByteN)
{
    void* DrainEnd = drain + ByteN;
    while( drain != DrainEnd ) *((char*)drain++) = Value;
}

void
hwut_memcpy(void* drain, void* source, size_t ByteN)
{
    void* DrainEnd = drain + ByteN;
    while( drain != DrainEnd ) *((char*)drain++) = *((char*)source++);
}

void*
hwut_malloc(size_t ByteN)
{
    void* memory = malloc(ByteN);
    memset(memory, 0xFF, ByteN);
    return memory;
}
