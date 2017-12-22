#define HELLO 3

typedef struct
{
    double x;
    double y;
    double z;
    char* label;
}Vec3;

Vec3* getVec3(double x, double y, double z, char* label);
void printVec3(Vec3* v);
void addScalar(Vec3* v, double s);
void subScalar(Vec3* v, double s);
void mulScalar(Vec3* v, double s);
void divScalar(Vec3* v, double s);
void extendVec3(Vec3* v, char c, double s);
void deleteVec3(Vec3* v);