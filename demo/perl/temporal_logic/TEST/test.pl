#! /usr/bin/env perl
use TheDude;

if( shift eq "--hwut-info" ) {
    printf("TheDude: Temporal Logic Tests;\n");
    printf("LOGIC:   dude.tlr;\n");
    exit;
}

$joe = TheDude::new();
for($time=0; $time < 24; ++$time) {
    if( TheDude::on_clock($joe, $time) ) {
        printf("%02i: BUZZ;\n", $time);
    }
    printf("%02i: %s(nfs=%0.1f, w=%s);\n", $time, 
           $joe->{state}, $joe->{need_for_sleep}, $joe->{work_time}); 
}

