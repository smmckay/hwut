
static const char*   (client_name_list[32]);
static const char**  client_name_list_memory_end = client_name_list + 32;
static const char**  client_name_list_end = client_name_list;

HWUT_TYPE_CLIENT_ID  
hwut_connect(const char* Name)
{
    for(iterator = client_name_list; 
        iterator != client_name_list_end; 
        ++iterator) {
        if( strcmp(Name, *iterator) == 0 ) return iterator - client_name_list + 1;
    }
    if( client_name_list_end == client_name_list_memory_end ) 
        return 0;
    *client_name_list_end = Name;
    ++client_name_list_end;
    return client_name_list_end - client_name_list + 1;
}

HWUT_TYPE_CLIENT_ID  
hwut_map_client_name_to_id(const char* Name)
{
    for(iterator = client_name_list; 
        iterator != client_name_list_end; 
        ++iterator) {
        if( strcmp(Name, *iterator) == 0 ) return iterator - client_name_list + 1;
    }
    return 0;
}

const char*          
hwut_map_client_id_to_name(HWUT_TYPE_CLIENT_ID ID);
{
    if( ID < 1 || ID >= (client_name_list_end - client_name_list) + 1 )
        return "";
    return client_name_list[ID-1];
}

void                 
hwut_send(HWUT_TYPE_MESSAGE*   Msg);
{
    const HWUT_TYPE_TIME DeltaT = __hwut_get_time_delta();
    const HWUT_TYPE_TIME T      = hwut_time_get() + DeltaT;

    for(iterator = msg_queue.end - 1; iterator != msg_queue.begin - 1; --iterator) {
        if( iterator->time > T ) break;
    }
    memmove(iterator + 2, iterator + 1, msg_queue.end - iterator + 1) * sizeof(HWUT_TYPE_MESSAGE));
}

HWUT_TYPE_MESSAGE*   hwut_receive(HWUT_TYPE_CLIENT_ID  Me, 
                                  HWUT_TYPE_TIME       TimeOut);
void                 hwut_transmission_time_set(HWUT_TYPE_TIME DeltaT);
void                 hwut_transmission_time_random_set(unsigned         RamdonSeed, 
                                                       HWUT_TYPE_TIME   DeltaT_Min, 
                                                       HWUT_TYPE_TIME   DeltaT_Max);

HWUT_TYPE_TIME       hwut_time_get();
void                 hwut_set_timer(HWUT_TYPE_TIME  Time, 
                                    void            (*callback)(HWUT_TYPE_TIME, void*));

