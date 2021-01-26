#include <stdio.h>
#define  size_t   int
#define  bool     int
#define  uint8_t  int

typedef struct {
    int x; int y;
} mine_t;

/* <<functions>> */
void    my_write(float Id, int Value);
int     my_read(float Id);

uint8_t flag_unset(uint8_t *flag_array, size_t BitIndex);
void    flag_set(uint8_t* flag_array, size_t BitIndex);
bool    flag_get(uint8_t* flag_array, size_t BitIndex);
mine_t  position();
const mine_t  other_position();

void    func();
void    same_func(void);
