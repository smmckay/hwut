int 
mini2() 
{ 
    static int virginity_f = 1; 
    if( ! virginity_f ) return; 
    virginity_f = 0;
    return mini0(); 
}
