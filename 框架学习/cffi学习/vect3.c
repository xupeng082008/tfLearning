#include <stdio.h>
#include <stdlib.h>
//#include <malloc.h>
#include "vect3.h"

Vec3* getVec3(double x, double y, double z, char* label){
    Vec3* v = (Vec3*)malloc(sizeof(Vec3));
    v->x = x;
    v->y = y;
    v->z = z;
    v->label = label;
    return v;
}

void deleteVec3(Vec3* v){
    if (v==NULL) return;
    free(v);
    v = NULL;
}

void printVec3(Vec3* v){
    if(v==NULL)return;
    printf("x = %.4f, y = %.4f, z = %.4f, label=%s\n", v->x,v->y,v->z,v->label);
}

void addScalar(Vec3* v, double s){
    if (v==NULL) return;
    v->x += s;
    v->y += s;
    v->z += s;
}

void subScalar(Vec3* v, double s){
    if(v==NULL) return;
    addScalar(v, -s);
}

void mulScalar(Vec3* v, double s){
    if(v==NULL) return;
    v->x *= s;
    v->y *= s;
    v->z *= s;
}

void divScalar(Vec3* v, double s){
    if (v==NULL||!s) return;
    v->x /= s;
    v->y /= s;
    v->z /= s;
}

void extendVec3(Vec3* v, char c, double s){
    if (v == NULL ) return;
    switch (c){
        case '+':
          addScalar(v, s);
          break;
        case '-':
          subScalar(v ,s);
          break;
        case '*':
          mulScalar(v, s);
          break;
        case '/':
          divScalar(v, s);
          break;
    }
}


int main(int argc, char const *argv[])
{
    double x, y, z;
    x = 1.0;
    y = 2.0;
    z = 3.0;
    char* label = "ssdf";
    Vec3* v = getVec3(x,y,z,label);
    printVec3(v);
    addScalar(v, 3.7);
    printVec3(v);
    deleteVec3(v);
    return 0;
}