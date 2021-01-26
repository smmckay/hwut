# (C) 2006-2016 Frank-Rene Schaefer, private.
# (C) 2006-2016 Frank-Rene Schaefer, Visteon Innovation&Technology GmbH, 
#     Kerpen, Germany.
# This file is part of HWUT - Project.
# This Source Code Form is subject to the terms of the MIT License (MIT).
#------------------------------------------------------------------------------
package TheDude;

%behavior = (
    BED  => { tired => "BED",  buzz => "HOME" },
    HOME => { tired => "BED",  buzz => "WORK" },
    WORK => { tired => "HOME", buzz => "HOME" }
);

sub new {
    return { state => "BED", need_for_sleep => 5, work_time => 0 };
}

sub on_tired { 
    my ($dude) = @_;

    $dude->{state} = %{$behavior{$dude->{state}}}->{tired}; 
}

sub on_buzz { 
    my ($dude) = @_;

    $before        = $dude->{"state"};
    $dude->{state} = %{$behavior{$dude->{state}}}->{buzz}; 
    if( $before == "BED" && $dude->{need_for_sleep} < 0 ) {
        $dude->{need_for_sleep} = 0;
    }
}

sub on_clock {
# Performs TheDude's state change upon one hour increment. When the 'need for 
# sleep' limit is exceeded, the 'on_tired' event handler is called. The buzz
# handler is called at dedicated hours, and in case that he slept too much.
#
# RETURNS: 1 -- if a buzz event occured.
#          0 -- else.
    my ($dude, $time) = @_;

    $hour = $time % 24;   
    $dude->{need_for_sleep} += 1   if( $dude->{state} eq "WORK" );
    $dude->{need_for_sleep} += 0.5 if( $dude->{state} eq "HOME" );
    $dude->{need_for_sleep} -= 1   if( $dude->{state} eq "BED" );
    $dude->{work_time} += 1        if( $dude->{state} eq "WORK" );
    $dude->{work_time} = 0         if( not $dude->{state} eq "WORK" );

    if( $dude->{need_for_sleep} > 11 ) {
        on_tired($dude);
    }
    if( $hour == 6 || $hour == 7 || $hour == 16 || $dude->{need_for_sleep} < -3 ) { 
        on_buzz($dude);
        return 1;
    }
    return 0;
}

1;
