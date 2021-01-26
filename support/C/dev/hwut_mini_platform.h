#ifndef __HWUT_INCLUDE_GUARD__MINI_PLATTFORM__
#define __HWUT_INCLUDE_GUARD__MINI_PLATTFORM__

#ifndef   HWUT_TYPE_CLIENT_ID
#  define HWUT_TYPE_CLIENT_ID   int
#endif

#ifndef HWUT_TYPE_MESSAGE
   typedef struct Ttag_HwutMessage {
      HWUT_TYPE_CLIENT_ID    source;
      HWUT_TYPE_CLIENT_ID    target;

      char*                  data;
      size_t                 size;
   } T_HwutMessage;
#  define HWUT_TYPE_MESSAGE              T_HwutMessage
#  define HWUT_TYPE_MESSAGE_DESTRUCT(X)  free((X)->data) 
#  define HWUT_TYPE_MESSAGE_TARGET_ID(X) (X)->target
#  define HWUT_TYPE_MESSAGE_SOURCE_ID(X) (X)->source
#  define HWUT_TYPE_MESSAGE_BROADCAST_ID (0)
#else
#  ifndef HWUT_TYPE_MESSAGE_DESTRUCT
#     error "Macro HWUT_TYPE_MESSAGE_DESTRUCT must be defined, i.e." \
            "it must be defined how to free the content of a message."
#  endif
#  ifndef   HWUT_TYPE_MESSAGE_TARGET_ID
#    define HWUT_TYPE_MESSAGE_TARGET_ID(X) (0)
#  endif
#  ifndef   HWUT_TYPE_MESSAGE_SOURCE_ID
#    define HWUT_TYPE_MESSAGE_SOURCE_ID(X) (0)
#  endif
#  ifndef   HWUT_TYPE_MESSAGE_BROADCAST_ID
#    define HWUT_TYPE_MESSAGE_BROADCAST_ID (0)
#  endif

#endif

extern HWUT_TYPE_CLIENT_ID  hwut_connect(const char* Name);
extern HWUT_TYPE_CLIENT_ID  hwut_map_client_name_to_id(const char* Name);
extern const char*          hwut_map_client_id_to_name(HWUT_TYPE_CLIENT_ID ID);

extern void                 hwut_send(HWUT_TYPE_MESSAGE*   Msg);
extern HWUT_TYPE_MESSAGE*   hwut_receive(HWUT_TYPE_CLIENT_ID  Me, 
                                         HWUT_TYPE_TIME       TimeOut);
extern void                 hwut_transmission_time_set(HWUT_TYPE_TIME DeltaT);
extern void                 hwut_transmission_time_random_set(unsigned         RamdonSeed, 
                                                              HWUT_TYPE_TIME   DeltaT_Min, 
                                                              HWUT_TYPE_TIME   DeltaT_Max);

extern HWUT_TYPE_TIME       hwut_time_get();
extern void                 hwut_set_timer(HWUT_TYPE_TIME  Time, 
                                           void            (*callback)(HWUT_TYPE_TIME, void*));

#endif
