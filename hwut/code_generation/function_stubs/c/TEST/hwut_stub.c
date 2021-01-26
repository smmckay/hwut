#include "hwut_stub.h"
#include <stdarg.h>
#include <malloc.h>

#include <string.h>

static struct {
    int            call_count;
    flag_get_FUNC  call;
    flag_get_FUNCS call_with_call_count;
    bool           return_value;
    bool*          return_value_list;
    int            return_value_list_size;
} self_flag_get = { 0, 0, 0, 0, 0, 0 };

static struct {
    int            call_count;
    flag_set_FUNC  call;
    flag_set_FUNCS call_with_call_count;
} self_flag_set = { 0, 0, 0 };

static struct {
    int              call_count;
    flag_unset_FUNC  call;
    flag_unset_FUNCS call_with_call_count;
    uint8_t          return_value;
    uint8_t*         return_value_list;
    int              return_value_list_size;
} self_flag_unset = { 0, 0, 0, 0, 0, 0 };

static struct {
    int        call_count;
    func_FUNC  call;
    func_FUNCS call_with_call_count;
} self_func = { 0, 0, 0 };

static struct {
    int           call_count;
    my_read_FUNC  call;
    my_read_FUNCS call_with_call_count;
    int           return_value;
    int*          return_value_list;
    int           return_value_list_size;
} self_my_read = { 0, 0, 0, 0, 0, 0 };

static struct {
    int            call_count;
    my_write_FUNC  call;
    my_write_FUNCS call_with_call_count;
} self_my_write = { 0, 0, 0 };

static struct {
    int                  call_count;
    other_position_FUNC  call;
    other_position_FUNCS call_with_call_count;
    const mine_t*        return_value;
    const mine_t**       return_value_list;
    int                  return_value_list_size;
} self_other_position = { 0, 0, 0, 0, 0, 0 };

static struct {
    int            call_count;
    position_FUNC  call;
    position_FUNCS call_with_call_count;
    mine_t*        return_value;
    mine_t**       return_value_list;
    int            return_value_list_size;
} self_position = { 0, 0, 0, 0, 0, 0 };

static struct {
    int             call_count;
    same_func_FUNC  call;
    same_func_FUNCS call_with_call_count;
} self_same_func = { 0, 0, 0 };



/* Default objects for aggregated types.                                     */
mine_t self_default_object_mine_t;

static void self_flag_get_RESET() {
    self_flag_get.call_count             = 0;
    self_flag_get.call_with_call_count   = (void*)0;
    self_flag_get.call                   = (void*)0;
    if( self_flag_get.return_value_list != (void*)0 ) {
         free(self_flag_get.return_value_list);
    }
    self_flag_get.return_value_list      = (void*)0;
    self_flag_get.return_value_list_size = 0;
    self_flag_get.return_value           = 0;
}

void flag_get_RETURN(bool ReturnValue) {
    self_flag_get_RESET();
    self_flag_get.return_value = ReturnValue;
}

void flag_get_RETURNS(int N, ...) {
    va_list  arg_p;
    int      i;

    self_flag_get_RESET();
    self_flag_get.return_value_list      = (bool*)malloc(sizeof(bool)*N);
    self_flag_get.return_value_list_size = N;
    va_start(arg_p, N);
    for(i=0; i<N; ++i) { self_flag_get.return_value_list[i] = (bool)va_arg(arg_p, int); }
    va_end(arg_p);
}

void flag_get_CALL(flag_get_FUNC FuncP) {
    self_flag_get_RESET();
    self_flag_get.call = FuncP;
}

void flag_get_CALLS(flag_get_FUNCS FuncP) {
    self_flag_get_RESET();
    self_flag_get.call_with_call_count = FuncP;
}

static void self_flag_set_RESET() {
    self_flag_set.call_count             = 0;
    self_flag_set.call_with_call_count   = (void*)0;
    self_flag_set.call                   = (void*)0;
}

void flag_set_CALL(flag_set_FUNC FuncP) {
    self_flag_set_RESET();
    self_flag_set.call = FuncP;
}

void flag_set_CALLS(flag_set_FUNCS FuncP) {
    self_flag_set_RESET();
    self_flag_set.call_with_call_count = FuncP;
}

static void self_flag_unset_RESET() {
    self_flag_unset.call_count             = 0;
    self_flag_unset.call_with_call_count   = (void*)0;
    self_flag_unset.call                   = (void*)0;
    if( self_flag_unset.return_value_list != (void*)0 ) {
         free(self_flag_unset.return_value_list);
    }
    self_flag_unset.return_value_list      = (void*)0;
    self_flag_unset.return_value_list_size = 0;
    self_flag_unset.return_value           = 0;
}

void flag_unset_RETURN(uint8_t ReturnValue) {
    self_flag_unset_RESET();
    self_flag_unset.return_value = ReturnValue;
}

void flag_unset_RETURNS(int N, ...) {
    va_list  arg_p;
    int      i;

    self_flag_unset_RESET();
    self_flag_unset.return_value_list      = (uint8_t*)malloc(sizeof(uint8_t)*N);
    self_flag_unset.return_value_list_size = N;
    va_start(arg_p, N);
    for(i=0; i<N; ++i) { self_flag_unset.return_value_list[i] = (uint8_t)va_arg(arg_p, unsigned); }
    va_end(arg_p);
}

void flag_unset_CALL(flag_unset_FUNC FuncP) {
    self_flag_unset_RESET();
    self_flag_unset.call = FuncP;
}

void flag_unset_CALLS(flag_unset_FUNCS FuncP) {
    self_flag_unset_RESET();
    self_flag_unset.call_with_call_count = FuncP;
}

static void self_func_RESET() {
    self_func.call_count             = 0;
    self_func.call_with_call_count   = (void*)0;
    self_func.call                   = (void*)0;
}

void func_CALL(func_FUNC FuncP) {
    self_func_RESET();
    self_func.call = FuncP;
}

void func_CALLS(func_FUNCS FuncP) {
    self_func_RESET();
    self_func.call_with_call_count = FuncP;
}

static void self_my_read_RESET() {
    self_my_read.call_count             = 0;
    self_my_read.call_with_call_count   = (void*)0;
    self_my_read.call                   = (void*)0;
    if( self_my_read.return_value_list != (void*)0 ) {
         free(self_my_read.return_value_list);
    }
    self_my_read.return_value_list      = (void*)0;
    self_my_read.return_value_list_size = 0;
    self_my_read.return_value           = 0;
}

void my_read_RETURN(int ReturnValue) {
    self_my_read_RESET();
    self_my_read.return_value = ReturnValue;
}

void my_read_RETURNS(int N, ...) {
    va_list  arg_p;
    int      i;

    self_my_read_RESET();
    self_my_read.return_value_list      = (int*)malloc(sizeof(int)*N);
    self_my_read.return_value_list_size = N;
    va_start(arg_p, N);
    for(i=0; i<N; ++i) { self_my_read.return_value_list[i] = (int)va_arg(arg_p, int); }
    va_end(arg_p);
}

void my_read_CALL(my_read_FUNC FuncP) {
    self_my_read_RESET();
    self_my_read.call = FuncP;
}

void my_read_CALLS(my_read_FUNCS FuncP) {
    self_my_read_RESET();
    self_my_read.call_with_call_count = FuncP;
}

static void self_my_write_RESET() {
    self_my_write.call_count             = 0;
    self_my_write.call_with_call_count   = (void*)0;
    self_my_write.call                   = (void*)0;
}

void my_write_CALL(my_write_FUNC FuncP) {
    self_my_write_RESET();
    self_my_write.call = FuncP;
}

void my_write_CALLS(my_write_FUNCS FuncP) {
    self_my_write_RESET();
    self_my_write.call_with_call_count = FuncP;
}

static void self_other_position_RESET() {
    self_other_position.call_count             = 0;
    self_other_position.call_with_call_count   = (void*)0;
    self_other_position.call                   = (void*)0;
    if( self_other_position.return_value_list != (void*)0 ) {
         free(self_other_position.return_value_list);
    }
    self_other_position.return_value_list      = (void*)0;
    self_other_position.return_value_list_size = 0;
    self_other_position.return_value           = &self_default_object_mine_t;
    memset((void*)&self_default_object_mine_t, 0, sizeof(mine_t));
}

void other_position_RETURN(const mine_t* ReturnValue) {
    self_other_position_RESET();
    self_other_position.return_value = ReturnValue;
}

void other_position_RETURNS(int N, ...) {
    va_list  arg_p;
    int      i;

    self_other_position_RESET();
    self_other_position.return_value_list      = (const mine_t**)malloc(sizeof(const mine_t*)*N);
    self_other_position.return_value_list_size = N;
    va_start(arg_p, N);
    for(i=0; i<N; ++i) { self_other_position.return_value_list[i] = va_arg(arg_p, const mine_t*); }
    va_end(arg_p);
}

void other_position_CALL(other_position_FUNC FuncP) {
    self_other_position_RESET();
    self_other_position.call = FuncP;
}

void other_position_CALLS(other_position_FUNCS FuncP) {
    self_other_position_RESET();
    self_other_position.call_with_call_count = FuncP;
}

static void self_position_RESET() {
    self_position.call_count             = 0;
    self_position.call_with_call_count   = (void*)0;
    self_position.call                   = (void*)0;
    if( self_position.return_value_list != (void*)0 ) {
         free(self_position.return_value_list);
    }
    self_position.return_value_list      = (void*)0;
    self_position.return_value_list_size = 0;
    self_position.return_value           = &self_default_object_mine_t;
    memset((void*)&self_default_object_mine_t, 0, sizeof(mine_t));
}

void position_RETURN(mine_t* ReturnValue) {
    self_position_RESET();
    self_position.return_value = ReturnValue;
}

void position_RETURNS(int N, ...) {
    va_list  arg_p;
    int      i;

    self_position_RESET();
    self_position.return_value_list      = (mine_t**)malloc(sizeof(mine_t*)*N);
    self_position.return_value_list_size = N;
    va_start(arg_p, N);
    for(i=0; i<N; ++i) { self_position.return_value_list[i] = va_arg(arg_p, mine_t*); }
    va_end(arg_p);
}

void position_CALL(position_FUNC FuncP) {
    self_position_RESET();
    self_position.call = FuncP;
}

void position_CALLS(position_FUNCS FuncP) {
    self_position_RESET();
    self_position.call_with_call_count = FuncP;
}

static void self_same_func_RESET() {
    self_same_func.call_count             = 0;
    self_same_func.call_with_call_count   = (void*)0;
    self_same_func.call                   = (void*)0;
}

void same_func_CALL(same_func_FUNC FuncP) {
    self_same_func_RESET();
    self_same_func.call = FuncP;
}

void same_func_CALLS(same_func_FUNCS FuncP) {
    self_same_func_RESET();
    self_same_func.call_with_call_count = FuncP;
}

bool
flag_get(uint8_t* flag_array, size_t BitIndex) {
    self_flag_get.call_count += 1;
    if( self_flag_get.call_with_call_count != (void*)0 ) {
        return self_flag_get.call_with_call_count(self_flag_get.call_count, flag_array, BitIndex);
    } else if( self_flag_get.call != (void*)0 ) {
        return self_flag_get.call(flag_array, BitIndex);
    } else if( self_flag_get.return_value_list != (void*)0 ) {
        if( self_flag_get.call_count >= self_flag_get.return_value_list_size ) {
            self_flag_get.call_count = 0;
        }
        return self_flag_get.return_value_list[self_flag_get.call_count];
    } else {
        return self_flag_get.return_value;
    }
}

void
flag_set(uint8_t* flag_array, size_t BitIndex) {
    self_flag_set.call_count += 1;
    if( self_flag_set.call_with_call_count != (void*)0 ) {
        self_flag_set.call_with_call_count(self_flag_set.call_count, flag_array, BitIndex); 
    } else if( self_flag_set.call != (void*)0 ) {
        self_flag_set.call(flag_array, BitIndex); 
    } else {
        return;
    }
}

uint8_t
flag_unset(uint8_t *flag_array, size_t BitIndex) {
    self_flag_unset.call_count += 1;
    if( self_flag_unset.call_with_call_count != (void*)0 ) {
        return self_flag_unset.call_with_call_count(self_flag_unset.call_count, flag_array, BitIndex);
    } else if( self_flag_unset.call != (void*)0 ) {
        return self_flag_unset.call(flag_array, BitIndex);
    } else if( self_flag_unset.return_value_list != (void*)0 ) {
        if( self_flag_unset.call_count >= self_flag_unset.return_value_list_size ) {
            self_flag_unset.call_count = 0;
        }
        return self_flag_unset.return_value_list[self_flag_unset.call_count];
    } else {
        return self_flag_unset.return_value;
    }
}

void
func() {
    self_func.call_count += 1;
    if( self_func.call_with_call_count != (void*)0 ) {
        self_func.call_with_call_count(self_func.call_count); 
    } else if( self_func.call != (void*)0 ) {
        self_func.call(); 
    } else {
        return;
    }
}

int
my_read(float Id) {
    self_my_read.call_count += 1;
    if( self_my_read.call_with_call_count != (void*)0 ) {
        return self_my_read.call_with_call_count(self_my_read.call_count, Id);
    } else if( self_my_read.call != (void*)0 ) {
        return self_my_read.call(Id);
    } else if( self_my_read.return_value_list != (void*)0 ) {
        if( self_my_read.call_count >= self_my_read.return_value_list_size ) {
            self_my_read.call_count = 0;
        }
        return self_my_read.return_value_list[self_my_read.call_count];
    } else {
        return self_my_read.return_value;
    }
}

void
my_write(float Id, int Value) {
    self_my_write.call_count += 1;
    if( self_my_write.call_with_call_count != (void*)0 ) {
        self_my_write.call_with_call_count(self_my_write.call_count, Id, Value); 
    } else if( self_my_write.call != (void*)0 ) {
        self_my_write.call(Id, Value); 
    } else {
        return;
    }
}

const mine_t
other_position() {
    self_other_position.call_count += 1;
    if( self_other_position.call_with_call_count != (void*)0 ) {
        return self_other_position.call_with_call_count(self_other_position.call_count);
    } else if( self_other_position.call != (void*)0 ) {
        return self_other_position.call();
    } else if( self_other_position.return_value_list != (void*)0 ) {
        if( self_other_position.call_count >= self_other_position.return_value_list_size ) {
            self_other_position.call_count = 0;
        }
        return *self_other_position.return_value_list[self_other_position.call_count];
    } else {
        return *self_other_position.return_value;
    }
}

mine_t
position() {
    self_position.call_count += 1;
    if( self_position.call_with_call_count != (void*)0 ) {
        return self_position.call_with_call_count(self_position.call_count);
    } else if( self_position.call != (void*)0 ) {
        return self_position.call();
    } else if( self_position.return_value_list != (void*)0 ) {
        if( self_position.call_count >= self_position.return_value_list_size ) {
            self_position.call_count = 0;
        }
        return *self_position.return_value_list[self_position.call_count];
    } else {
        return *self_position.return_value;
    }
}

void
same_func(void) {
    self_same_func.call_count += 1;
    if( self_same_func.call_with_call_count != (void*)0 ) {
        self_same_func.call_with_call_count(self_same_func.call_count); 
    } else if( self_same_func.call != (void*)0 ) {
        self_same_func.call(); 
    } else {
        return;
    }
}

