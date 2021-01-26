#! /usr/bin/env perl
# (C) 2006-2016 Frank-Rene Schaefer, private.
# (C) 2006-2016 Frank-Rene Schaefer, Visteon Innovation&Technology GmbH, 
#     Kerpen, Germany.
# This file is part of HWUT - Project.
# This Source Code Form is subject to the terms of the MIT License (MIT).
#------------------------------------------------------------------------------
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

