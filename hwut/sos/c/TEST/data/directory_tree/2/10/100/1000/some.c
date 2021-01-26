#include "c.h"
#include "b.h"
#include "a.h"
#include <some.h>

int some(void);
int some(void) { return 1; }

extern int nothing(void);
int anything(void);
int anything(void) { return nothing(); }

