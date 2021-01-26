/*
<<hwut-sm_walker:  myWalk1  my_data_t  4   1 >> 
------------------------------------------------------------------------
#include <stdio.h>
typedef struct {
    int x;
    float y;
} my_data_t;
------------------------------------------------------------------------
  
   BEGIN1 ---( goes )------.
     '-------( walkes )--- Frieda

---// EVENTS //---------------------------------------------------------
 
   goes   { printf("I go!\n"); }
   walkes { printf("I walk!\n"); }

   @end { 
      printf("do_event:    { user_data: ((%p)); name: %s; event: %s; }\n", 
             me->subject, state->name, me->base.aux.event_id_db.begin[EventId]);  
   }

---// CONDITIONS //-----------------------------------------------------

   @end { 
        int result = (ConditionId == 1);
        assert(ConditionId != 0);
        printf("condition:   { user_data: ((%p)); name: %s; condition_id: %i; result: %s; }\n", 
               me->subject, state->name, ConditionId, result ? "OK" : "FAIL"); 
        return result;
   }

------------------------------------------------------------------------
*/

/*
<<hwut-sm_walker:  myWalk2 my_data_t 4 1>> 
------------------------------------------------------------------------
------------------------------------------------------------------------

   BEGIN2 ---( goes )--------.
   Erwin -----( walkes )--- Otto
   Otto ------( goes )----- Erwin

---// EVENTS //---------------------------------------------------------

   @end { 
      printf("do_event:    { user_data: ((%p)); name: %s; event: %s; }\n", 
             me->subject, state->name, me->base.aux.event_id_db.begin[EventId]);  
   }

---// CONDITIONS //-----------------------------------------------------

   @end { 
        int result = (ConditionId == 1);
        assert(ConditionId != 0);
        printf("condition:   { user_data: ((%p)); name: %s; condition_id: %i; result: %s; }\n", 
               me->subject, state->name, ConditionId, result ? "OK" : "FAIL"); 
        return result;
   }

------------------------------------------------------------------------
*/

/*
<<hwut-sm_walker:  myWalk3 my_data_t 6 1>> 
------------------------------------------------------------------------
------------------------------------------------------------------------

   Bed ----| WARM |---( BUZZ )------ Garden
     '-----| COLD |---( BUZZ )------ LivingRoom
   Garden ------------( BUZZ )------ LivingRoom
   LivingRoom --------( BUZZ )------ Bed

---// EVENTS //---------------------------------------------------------

   BUZZ {}

   @end { 
      printf("do_event:    { user_data: ((%p)); name: %s; event: %s; }\n", 
             me->subject, state->name, me->base.aux.event_id_db.begin[EventId]);  
   }

---// CONDITIONS //-----------------------------------------------------

   WARM { printf("WARM?\n"); }
   COLD { printf("COLD?\n"); }

   @end { 
        assert(ConditionId != 0);
        printf("condition:   { user_data: ((%p)); name: %s; condition_id: %s; result: %s; }\n", 
               me->subject, state->name, me->base.aux.condition_id_db.begin[ConditionId], "OK"); 
        return 1;
   }

------------------------------------------------------------------------
*/

/*
<<hwut-sm_walker:  myWalk4 my_data_t 4 1>> 
------------------------------------------------------------------------
------------------------------------------------------------------------

    A --( JUMP )-- B
    B --( HOP )--- C
    C --( FLY )--- D

---// EVENTS //---------------------------------------------------------

    JUMP*
    HOP*
    FLY*

------------------------------------------------------------------------
*/

/*
<<hwut-sm_walker:  myWalk5 my_data_t 100 1>> 
------------------------------------------------------------------------
------------------------------------------------------------------------

    A ---( X )---| C0 |-- B
    '----( X )---| C1 |-- C
    
---// EVENTS //---------------------------------------------------------

   X {    
      printf("event:       { user_data: ((%p)); name: %s; event_id: %s; }\n", 
             me->subject, state->name, me->base.aux.event_id_db.begin[EventId]); 
   }

---// CONDITIONS //-----------------------------------------------------

   @begin {
     printf("state: %s; real: %s;\n", 
            state->name, myWalk5_state_is_real(state) ? "true" : "false");
   }

   C0 { 
       printf("condition:   { user_data: ((%p)); name: %s(%i); condition_id: %s; result: %s; }\n", 
               me->subject, state->name, state->pass_n, me->base.aux.condition_id_db.begin[ConditionId], "FAIL"); 
       return 0; 
    }
   C1 { 
       printf("condition:   { user_data: ((%p)); name: %s(%i); condition_id: %s; result: %s; }\n", 
               me->subject, state->name, state->pass_n, me->base.aux.condition_id_db.begin[ConditionId], "OK"); 
       return 1; 
    }

------------------------------------------------------------------------
*/

#include "hwut_unit.h"
#include "myWalk_sm_walker.h"
#include <stdio.h>

static void 
do_init1(myWalk1_t* me) { printf("do_init:    { user_data: ((%p)); }\n", me->subject); }
static void 
do_init2(myWalk2_t* me) { printf("do_init:    { user_data: ((%p)); }\n", me->subject); }
static void 
do_init3(myWalk3_t* me) { printf("do_init:    { user_data: ((%p)); }\n", me->subject); }
static void 
do_init4(myWalk4_t* me) { printf("do_init:    { user_data: ((%p)); }\n", me->subject); }
static void 
do_init5(myWalk5_t* me) { printf("do_init:    { user_data: ((%p)); }\n", me->subject); }

static void 
do_terminal1(myWalk1_t* me, hwut_sm_state_t* state) { printf("do_terminal: { user_data: ((%p)); name: %s; }\n\n", me->subject, state->name); }
static void 
do_terminal2(myWalk2_t* me, hwut_sm_state_t* state) { printf("do_terminal: { user_data: ((%p)); name: %s; }\n\n", me->subject, state->name); }
static void 
do_terminal3(myWalk3_t* me, hwut_sm_state_t* state) { printf("do_terminal: { user_data: ((%p)); name: %s; }\n\n", me->subject, state->name); }
static void 
do_terminal4(myWalk4_t* me, hwut_sm_state_t* state) { printf("do_terminal: { user_data: ((%p)); name: %s; }\n\n", me->subject, state->name); }
static void 
do_terminal5(myWalk5_t* me, hwut_sm_state_t* state) { printf("do_terminal: { user_data: ((%p)); name: %s; }\n\n", me->subject, state->name); }

int
main(int argc, char** argv)
{
    myWalk1_t  me1;
    myWalk2_t  me2;
    myWalk3_t  me3;
    myWalk4_t  me4;
    myWalk5_t  me5;

    my_data_t  my_data = { 0, 3.14 };

    hwut_info("The whole chain;\n"
              "CHOICES: 1, 2, 3, 4, 5;");

    hwut_if_choice("1") { 
        myWalk1_execute(&me1, &my_data, do_init1, do_terminal1);
    }

    hwut_if_choice("2") { 
        myWalk2_execute(&me2, &my_data, do_init2, do_terminal2);
    }

    hwut_if_choice("3") { 
        myWalk3_execute(&me3, &my_data, do_init3, do_terminal3);
    }

    hwut_if_choice("4") { 
        myWalk4_execute(&me4, &my_data, do_init4, do_terminal4);
    }

    hwut_if_choice("5") { 
        myWalk5_execute(&me5, &my_data, do_init5, do_terminal5);
    }

    return 0;
}

