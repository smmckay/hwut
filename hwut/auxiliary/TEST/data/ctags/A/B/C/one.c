#define one_something(X) X
#define one_something_else(X) X

extern int one_function(void);
static int one_static_function(void);
int        one_implemented_function(void) { return 0; }

static int one_static;
extern int one_extern;
int        one_global;
int zz_all(void) { return 0; }
