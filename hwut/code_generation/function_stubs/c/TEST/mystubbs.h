#ifndef  INCLUDE_GUARD_HWUT_STUB_H
#define INCLUDE_GUARD_HWUT_STUB_H


#include <stdio.h>
#define  size_t   int
#define  bool     int
#define  uint8_t  int
typedef struct {
int x; int y;
} mine_t;
/* FUNCTION: flag_get __________________________________________________________
 *                                                                            */
typedef bool (*flag_get_FUNC)(uint8_t* flag_array, size_t BitIndex);
typedef bool (*flag_get_FUNCS)(int CallCount, uint8_t* flag_array, size_t BitIndex);

extern void flag_get_RETURN(bool ReturnValue);
extern void flag_get_RETURNS(int N, ...);
extern void flag_get_CALL(flag_get_FUNC FuncP);
extern void flag_get_CALLS(flag_get_FUNCS FuncP);

/* FUNCTION: flag_set __________________________________________________________
 *                                                                            */
typedef void (*flag_set_FUNC)(uint8_t* flag_array, size_t BitIndex);
typedef void (*flag_set_FUNCS)(int CallCount, uint8_t* flag_array, size_t BitIndex);

/* NOT: 'flag_set_RETURN(...)' because function returns 'void' */
extern void flag_set_CALL(flag_set_FUNC FuncP);
extern void flag_set_CALLS(flag_set_FUNCS FuncP);

/* FUNCTION: flag_unset ________________________________________________________
 *                                                                            */
typedef uint8_t    (*flag_unset_FUNC)(uint8_t *flag_array, size_t BitIndex);
typedef uint8_t    (*flag_unset_FUNCS)(int CallCount, uint8_t *flag_array, size_t BitIndex);

extern void    flag_unset_RETURN(uint8_t ReturnValue);
extern void    flag_unset_RETURNS(int N, ...);
extern void    flag_unset_CALL(flag_unset_FUNC FuncP);
extern void    flag_unset_CALLS(flag_unset_FUNCS FuncP);

/* FUNCTION: func ______________________________________________________________
 *                                                                            */
typedef void (*func_FUNC)();
typedef void (*func_FUNCS)(int CallCount);

/* NOT: 'func_RETURN(...)' because function returns 'void' */
extern void func_CALL(func_FUNC FuncP);
extern void func_CALLS(func_FUNCS FuncP);

/* FUNCTION: my_read ___________________________________________________________
 *                                                                            */
typedef int (*my_read_FUNC)(float Id);
typedef int (*my_read_FUNCS)(int CallCount, float Id);

extern void my_read_RETURN(int ReturnValue);
extern void my_read_RETURNS(int N, ...);
extern void my_read_CALL(my_read_FUNC FuncP);
extern void my_read_CALLS(my_read_FUNCS FuncP);

/* FUNCTION: my_write __________________________________________________________
 *                                                                            */
typedef void (*my_write_FUNC)(float Id, int Value);
typedef void (*my_write_FUNCS)(int CallCount, float Id, int Value);

/* NOT: 'my_write_RETURN(...)' because function returns 'void' */
extern void my_write_CALL(my_write_FUNC FuncP);
extern void my_write_CALLS(my_write_FUNCS FuncP);

/* FUNCTION: position __________________________________________________________
 *                                                                            */
typedef mine_t   (*position_FUNC)();
typedef mine_t   (*position_FUNCS)(int CallCount);

extern void   position_RETURN(mine_t* ReturnValue);
extern void   position_RETURNS(int N, ...);
extern void   position_CALL(position_FUNC FuncP);
extern void   position_CALLS(position_FUNCS FuncP);

/* FUNCTION: same_func _________________________________________________________
 *                                                                            */
typedef void (*same_func_FUNC)(void);
typedef void (*same_func_FUNCS)(int CallCount);

/* NOT: 'same_func_RETURN(...)' because function returns 'void' */
extern void same_func_CALL(same_func_FUNC FuncP);
extern void same_func_CALLS(same_func_FUNCS FuncP);


#define hwut_stub_RETURN(F, V)       do { F ##_RETURN(V); } while(0)
#define hwut_stub_RETURNS(F, N, ...) do { F ##_RETURNS(N, ## __VA_ARGS__); } while(0)
#define hwut_stub_CALL(F, FP)        do { F ##_CALL(FP); } while(0)
#define hwut_stub_CALLS(F, FP)       do { F ##_CALLS(FP); } while(0)

#endif  /* INCLUDE_GUARD_HWUT_STUB_H */
