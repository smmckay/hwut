#ifndef INCLUDE_GUARD_HWUT_BITFIELD_H
#define INCLUDE_GUARD_HWUT_BITFIELD_H
#include <inttypes.h>
#include <stddef.h>

extern int  hwut_bitfield_encode(uint8_t* array, size_t array_size, ...);
extern int  hwut_bitfield_decode(const uint8_t* array, size_t array_size, ...);
extern void hwut_bitfield_print_bytes(const uint8_t* array, size_t ArraySize);
extern void hwut_bitfield_print_numeric(const uint8_t* array, size_t ArraySize, const int Base, ...);
extern void hwut_bitfield_print_borders(const uint8_t* array, size_t ArraySize, ...);

#endif /* INCLUDE_GUARD_HWUT_BITFIELD_H */
