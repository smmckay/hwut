#ifndef __HWUT_INCLUDE_GUARD__SUPPORT_HWUT_SCANNER_H
#define __HWUT_INCLUDE_GUARD__SUPPORT_HWUT_SCANNER_H

#include "stddef.h"

int    hwut_isspace(char C);
int    hwut_isnumber(char C);
int    hwut_strlen(const char* Begin);
const char*  hwut_find(char C, const char* iterator);
const char*  hwut_find_before(char C, const char* iterator, const char* End);
void   hwut_skip_whitespace(const char** iterator);
void   hwut_skip_whitespace_backwards(const char** iterator, const char* Limit);
void   hwut_skip_until_whitespace(char** iterator);
int    hwut_scan_integer(const char** iterator);
long   hwut_get_bit_range(void* value_p, size_t ByteN, size_t Begin, size_t End);

void   hwut_memcpy(void* drain, void* source, size_t byte_n);
void   hwut_memmove(void* drain, void* source, size_t ByteN);
void   hwut_memset(void* drain, char Value, size_t ByteN);
void*  hwut_malloc(size_t ByteN);

void   hwut_append(char** iterator, const char* read_iterator, size_t Size);
void   hwut_append_string(char** iterator, const char* read_iterator);
void   hwut_append_hex(char** iterator, long Value, size_t DigitN);
void   hwut_append_decimal(char** iterator, long Value, size_t DigitN);
void   hwut_append_binary(char** iterator, long Value, size_t BitN);
void   hwut_append_characters(char** iterator, size_t N, char C);

void   hwut_error(const char*);

#endif /* __HWUT_INCLUDE_GUARD__SUPPORT_HWUT_SCANNER_H */
