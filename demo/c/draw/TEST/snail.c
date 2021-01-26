#include <stdio.h>
const int X_SIZE = 60;
const int Y_SIZE = 20;


void display(char screen[Y_SIZE][X_SIZE]);
void init(char screen[Y_SIZE][X_SIZE]);

void draw_line(char screen[Y_SIZE][X_SIZE], int X0, int Y0, int X1, int Y1);
void draw_box(char screen[Y_SIZE][X_SIZE], int TopRight_X, int TopRight_Y, int BottomLeft_X, int BottomLeft_Y);
void draw_circle(char screen[Y_SIZE][X_SIZE], int X0, int X1, int Radius);

int
main(int argc, char** argv)
{
    char  screen[Y_SIZE][X_SIZE];

    init(screen);
    // draw_line(screen, 5, 5, 56, 17);
    // draw_circle(screen, 10, 10, 5);
    draw_box(screen, 10, 10, 25, 17);
    display(screen);
    
}

void init(char screen[Y_SIZE][X_SIZE])
{
    int x = -1;
    int y = -1;

    for(x=0; x<X_SIZE; ++x) { 
        for(y=0; y<Y_SIZE; ++y) { 
            screen[y][x] = ' ';
        }
    }
}

void display(char screen[Y_SIZE][X_SIZE])
{
    int x = -1;
    int y = -1;

    for(y=0; y<Y_SIZE; ++y) { 
        printf("%02i:", y);
        for(x=0; x<X_SIZE; ++x) { 
            printf("%c", screen[y][x]);
        }
        printf("\n");
    }
}

#include <assert.h>
#include <math.h>
static void __safe_set(char screen[Y_SIZE][X_SIZE], int x, int y)
{ 
    if( x < 0 || x >= X_SIZE ) return;
    if( y < 0 || y >= Y_SIZE ) return;

    screen[y][x] = '*';
}

void draw_line(char screen[Y_SIZE][X_SIZE], int X0, int Y0, int X1, int Y1)
{
    int x = -1;
    int y = -1;
    float slope = 0.0;
    
    if( X0 == X1 ) { 
        for(y=Y0; y <= Y1; ++y) {
            __safe_set(screen, X0, y);
        }
    }
    else { 
        slope = (float)(Y1 - Y0) / (float)(X1 - X0);
        for(x=X0; x <= X1; ++x) { 
            y = Y0 + (int)(slope * (float)(x - X0));
            __safe_set(screen, x, y);
        }

    }
}

void draw_box(char screen[Y_SIZE][X_SIZE], int TopRight_X, int TopRight_Y, int BottomLeft_X, int BottomLeft_Y)
{
    int x = -1;
    int y = -1;
    assert(BottomLeft_Y >= TopRight_Y);
    assert(BottomLeft_X >= TopRight_X);

    for(x=TopRight_X; x<=BottomLeft_X; ++x) {
        __safe_set(screen, x, TopRight_Y); 
        __safe_set(screen, x, BottomLeft_Y); 
    }
    for(y=TopRight_Y; y<=BottomLeft_Y; ++y) {
        __safe_set(screen, TopRight_X, y); 
        __safe_set(screen, BottomLeft_X, y); 
    }
}

void draw_circle(char screen[Y_SIZE][X_SIZE], int X0, int Y0, int Radius)
{
    int x = 0.0;
    int x_distance_to_origin = 0.0;
    int y_distance_to_origin = 0.0;
    int height = 0;
    int y = 0;

    for(x=X0-Radius; x <= X0+Radius; ++x) { 
        if( x < 0 || x >= X_SIZE ) continue;
        x_distance_to_origin = abs(x - X0);
        height = abs((int)((float)Radius * cos( (float)(x_distance_to_origin) / (float)(Radius) )));
        for(y=Y0-height; y<=Y0+height; ++y) { 
            __safe_set(screen, x, y); 
        }
    }
}
