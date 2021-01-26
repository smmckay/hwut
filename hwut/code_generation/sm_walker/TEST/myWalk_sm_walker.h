#ifndef INCLUDE_GUAGE_HWUT_GENERATOR_myWalk_sm_walker_h
#define INCLUDE_GUAGE_HWUT_GENERATOR_myWalk_sm_walker_h
#include <stdio.h>
typedef struct {
    int x;
    float y;
} my_data_t;

#ifndef INCLUDE_GUARD_SM_WALKER_myWalk4_H
#define INCLUDE_GUARD_SM_WALKER_myWalk4_H
/* This file has been generated with HWUT $$HWUT_VERSION$$.
 *___________________________________________________________________________*/

#include <hwut_sm_walker.h>  /* Use: -I<<HWUT_PATH>>/support/C               */

/* Event Definitions ________________________________________________________*/
typedef enum {
    myWalk4_JUMP = 0,
    myWalk4_FLY  = 1,
    myWalk4_HOP  = 2,
} myWalk4_event_id_t;


/* Condition Definitions ____________________________________________________*/
/* No conditions */

/* State Declarations _______________________________________________________
 * (Use those to compare expected states with current states)                */
typedef enum {
    myWalk4_A          = 0,
    myWalk4_C          = 1,
    myWalk4_B          = 2,
    myWalk4_D          = 3,
    myWalk4___BeyondId = 4, /* Any state below is 'real' */
} myWalk4_state_id_t;

typedef struct myWalk4_t_tag {
    /* Inheritance __________________________________________________________*/
    hwut_sm_walker_t    base;

    /* The user's unit under test ___________________________________________*/
    my_data_t* subject;

    /* Memory for the 'aux' component of the walker _________________________*/
    struct { 
        hwut_sm_condition_coverage_t  condition_coverage[1]; 
        hwut_sm_condition_norm_t      condition_norm[1];
        const char*                   condition_norm_comment[1];

        hwut_state_coverage_t         state_coverage[4]; 
        hwut_state_forbidden_t        state_forbidden[4];
        const char*                   state_forbidden_comment[4];
    } memory;

    /* User data related callbacks __________________________________________*/
    void   (*do_init)(struct myWalk4_t_tag* me);
    void   (*do_terminal)(struct myWalk4_t_tag* me, hwut_sm_state_t* state_p);
} myWalk4_t;

/* API ______________________________________________________________________*/
void
myWalk4_execute(myWalk4_t* me,
                my_data_t* the_subject,
                void   (*do_init)(myWalk4_t* me),
                void   (*do_terminal)(myWalk4_t* me, hwut_sm_state_t*));
int
myWalk4_state_is_real(const hwut_sm_state_t* State);

#endif /* INCLUDE_GUARD_SM_WALKER_myWalk4_H */

#ifndef INCLUDE_GUARD_SM_WALKER_myWalk5_H
#define INCLUDE_GUARD_SM_WALKER_myWalk5_H
/* This file has been generated with HWUT $$HWUT_VERSION$$.
 *___________________________________________________________________________*/

#include <hwut_sm_walker.h>  /* Use: -I<<HWUT_PATH>>/support/C               */

/* Event Definitions ________________________________________________________*/
typedef enum {
    myWalk5_X = 3,
} myWalk5_event_id_t;


/* Condition Definitions ____________________________________________________*/
typedef enum {
    myWalk5_C0 = 1,
    myWalk5_C1 = 2,
} myWalk5_condition_id_t;


/* State Declarations _______________________________________________________
 * (Use those to compare expected states with current states)                */
typedef enum {
    myWalk5_A          = 4,
    myWalk5_C          = 5,
    myWalk5_B          = 6,
    myWalk5_A_post0    = 7,
    myWalk5_A_post1    = 8,
    myWalk5___BeyondId = 7, /* Any state below is 'real' */
} myWalk5_state_id_t;

typedef struct myWalk5_t_tag {
    /* Inheritance __________________________________________________________*/
    hwut_sm_walker_t    base;

    /* The user's unit under test ___________________________________________*/
    my_data_t* subject;

    /* Memory for the 'aux' component of the walker _________________________*/
    struct { 
        hwut_sm_condition_coverage_t  condition_coverage[2]; 
        hwut_sm_condition_norm_t      condition_norm[2];
        const char*                   condition_norm_comment[2];

        hwut_state_coverage_t         state_coverage[5]; 
        hwut_state_forbidden_t        state_forbidden[5];
        const char*                   state_forbidden_comment[5];
    } memory;

    /* User data related callbacks __________________________________________*/
    void   (*do_init)(struct myWalk5_t_tag* me);
    void   (*do_terminal)(struct myWalk5_t_tag* me, hwut_sm_state_t* state_p);
} myWalk5_t;

/* API ______________________________________________________________________*/
void
myWalk5_execute(myWalk5_t* me,
                my_data_t* the_subject,
                void   (*do_init)(myWalk5_t* me),
                void   (*do_terminal)(myWalk5_t* me, hwut_sm_state_t*));
int
myWalk5_state_is_real(const hwut_sm_state_t* State);

#endif /* INCLUDE_GUARD_SM_WALKER_myWalk5_H */

#ifndef INCLUDE_GUARD_SM_WALKER_myWalk1_H
#define INCLUDE_GUARD_SM_WALKER_myWalk1_H
/* This file has been generated with HWUT $$HWUT_VERSION$$.
 *___________________________________________________________________________*/

#include <hwut_sm_walker.h>  /* Use: -I<<HWUT_PATH>>/support/C               */

/* Event Definitions ________________________________________________________*/
typedef enum {
    myWalk1_walkes = 4,
    myWalk1_goes   = 5,
} myWalk1_event_id_t;


/* Condition Definitions ____________________________________________________*/
/* No conditions */

/* State Declarations _______________________________________________________
 * (Use those to compare expected states with current states)                */
typedef enum {
    myWalk1_BEGIN1     = 9,
    myWalk1_Frieda     = 10,
    myWalk1___BeyondId = 11, /* Any state below is 'real' */
} myWalk1_state_id_t;

typedef struct myWalk1_t_tag {
    /* Inheritance __________________________________________________________*/
    hwut_sm_walker_t    base;

    /* The user's unit under test ___________________________________________*/
    my_data_t* subject;

    /* Memory for the 'aux' component of the walker _________________________*/
    struct { 
        hwut_sm_condition_coverage_t  condition_coverage[1]; 
        hwut_sm_condition_norm_t      condition_norm[1];
        const char*                   condition_norm_comment[1];

        hwut_state_coverage_t         state_coverage[2]; 
        hwut_state_forbidden_t        state_forbidden[2];
        const char*                   state_forbidden_comment[2];
    } memory;

    /* User data related callbacks __________________________________________*/
    void   (*do_init)(struct myWalk1_t_tag* me);
    void   (*do_terminal)(struct myWalk1_t_tag* me, hwut_sm_state_t* state_p);
} myWalk1_t;

/* API ______________________________________________________________________*/
void
myWalk1_execute(myWalk1_t* me,
                my_data_t* the_subject,
                void   (*do_init)(myWalk1_t* me),
                void   (*do_terminal)(myWalk1_t* me, hwut_sm_state_t*));
int
myWalk1_state_is_real(const hwut_sm_state_t* State);

#endif /* INCLUDE_GUARD_SM_WALKER_myWalk1_H */

#ifndef INCLUDE_GUARD_SM_WALKER_myWalk2_H
#define INCLUDE_GUARD_SM_WALKER_myWalk2_H
/* This file has been generated with HWUT $$HWUT_VERSION$$.
 *___________________________________________________________________________*/

#include <hwut_sm_walker.h>  /* Use: -I<<HWUT_PATH>>/support/C               */

/* Event Definitions ________________________________________________________*/
typedef enum {
    myWalk2_goes   = 6,
    myWalk2_walkes = 7,
} myWalk2_event_id_t;


/* Condition Definitions ____________________________________________________*/
/* No conditions */

/* State Declarations _______________________________________________________
 * (Use those to compare expected states with current states)                */
typedef enum {
    myWalk2_BEGIN2     = 11,
    myWalk2_Erwin      = 12,
    myWalk2_Otto       = 13,
    myWalk2___BeyondId = 14, /* Any state below is 'real' */
} myWalk2_state_id_t;

typedef struct myWalk2_t_tag {
    /* Inheritance __________________________________________________________*/
    hwut_sm_walker_t    base;

    /* The user's unit under test ___________________________________________*/
    my_data_t* subject;

    /* Memory for the 'aux' component of the walker _________________________*/
    struct { 
        hwut_sm_condition_coverage_t  condition_coverage[1]; 
        hwut_sm_condition_norm_t      condition_norm[1];
        const char*                   condition_norm_comment[1];

        hwut_state_coverage_t         state_coverage[3]; 
        hwut_state_forbidden_t        state_forbidden[3];
        const char*                   state_forbidden_comment[3];
    } memory;

    /* User data related callbacks __________________________________________*/
    void   (*do_init)(struct myWalk2_t_tag* me);
    void   (*do_terminal)(struct myWalk2_t_tag* me, hwut_sm_state_t* state_p);
} myWalk2_t;

/* API ______________________________________________________________________*/
void
myWalk2_execute(myWalk2_t* me,
                my_data_t* the_subject,
                void   (*do_init)(myWalk2_t* me),
                void   (*do_terminal)(myWalk2_t* me, hwut_sm_state_t*));
int
myWalk2_state_is_real(const hwut_sm_state_t* State);

#endif /* INCLUDE_GUARD_SM_WALKER_myWalk2_H */

#ifndef INCLUDE_GUARD_SM_WALKER_myWalk3_H
#define INCLUDE_GUARD_SM_WALKER_myWalk3_H
/* This file has been generated with HWUT $$HWUT_VERSION$$.
 *___________________________________________________________________________*/

#include <hwut_sm_walker.h>  /* Use: -I<<HWUT_PATH>>/support/C               */

/* Event Definitions ________________________________________________________*/
typedef enum {
    myWalk3_BUZZ = 8,
} myWalk3_event_id_t;


/* Condition Definitions ____________________________________________________*/
typedef enum {
    myWalk3_WARM = 3,
    myWalk3_COLD = 4,
} myWalk3_condition_id_t;


/* State Declarations _______________________________________________________
 * (Use those to compare expected states with current states)                */
typedef enum {
    myWalk3_Bed        = 14,
    myWalk3_LivingRoom = 15,
    myWalk3_Garden     = 16,
    myWalk3___BeyondId = 17, /* Any state below is 'real' */
} myWalk3_state_id_t;

typedef struct myWalk3_t_tag {
    /* Inheritance __________________________________________________________*/
    hwut_sm_walker_t    base;

    /* The user's unit under test ___________________________________________*/
    my_data_t* subject;

    /* Memory for the 'aux' component of the walker _________________________*/
    struct { 
        hwut_sm_condition_coverage_t  condition_coverage[2]; 
        hwut_sm_condition_norm_t      condition_norm[2];
        const char*                   condition_norm_comment[2];

        hwut_state_coverage_t         state_coverage[3]; 
        hwut_state_forbidden_t        state_forbidden[3];
        const char*                   state_forbidden_comment[3];
    } memory;

    /* User data related callbacks __________________________________________*/
    void   (*do_init)(struct myWalk3_t_tag* me);
    void   (*do_terminal)(struct myWalk3_t_tag* me, hwut_sm_state_t* state_p);
} myWalk3_t;

/* API ______________________________________________________________________*/
void
myWalk3_execute(myWalk3_t* me,
                my_data_t* the_subject,
                void   (*do_init)(myWalk3_t* me),
                void   (*do_terminal)(myWalk3_t* me, hwut_sm_state_t*));
int
myWalk3_state_is_real(const hwut_sm_state_t* State);

#endif /* INCLUDE_GUARD_SM_WALKER_myWalk3_H */


#endif /* INCLUDE_GUAGE_HWUT_GENERATOR_myWalk_sm_walker_h */
