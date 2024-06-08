#include <stdio.h>
#include <stdint.h>

#define NBT 4
#define FIXED_POINT_FRACTIONAL_BITS 16
#define FIXED_POINT_ONE (1 << FIXED_POINT_FRACTIONAL_BITS)

typedef int32_t fixed_point_t;

// Convert floating-point to fixed-point
fixed_point_t float_to_fixed1(float value) {
    return (fixed_point_t)(value * FIXED_POINT_ONE);
}

// Convert fixed-point to floating-point
float fixed_to_float1(fixed_point_t value) {
    return (float)value / FIXED_POINT_ONE;
}

int main() {
    float xpos_f[NBT + 1] = {3.4741, 4.7511, 2.1937, 3.8276, 0.4857};
    float ypos_f[NBT + 1] = {1.5855, 0.1722, 1.9078, 3.9760, 4.1173};

   // float xpos_f[NBT + 1] ={2.0090 ,  1.1996 ,0.9195 ,2.0863 ,   1.7548};
    //float ypos_f[NBT + 1] ={0.3798 ,   0.6166  ,  1.1998 ,   0.2483 ,   2.5662};

    //float xpos_f[NBT + 1]  = {2.2279,3.5468,1.3801,3.2755,0.5950,4.7987,2.9263,3.7563,2.5298,4.4545,0.9344};
	//float ypos_f[NBT + 1] = {3.2316,3.7734,3.3985,0.8131,2.4918,1.7019,1.1191,1.2755,3.4954,4.7965,2.4488};

    fixed_point_t xpos[NBT + 1], ypos[NBT + 1], final_xpos[NBT], final_ypos[NBT];
    fixed_point_t ux, uy;

    // Convert float to fixed-point
    for (int i = 0; i < NBT + 1; i++) {
        xpos[i] = float_to_fixed1(xpos_f[i]);
        ypos[i] = float_to_fixed1(ypos_f[i]);
    }

    ux = xpos[NBT];
    uy = ypos[NBT];
    int it = 30;

    // Call the function
    bmo_fixed(it, xpos, ypos, ux, uy, final_xpos, final_ypos);

    printf("--------- > final Bot locations <-------- \n");
    for (i = 0; i < NBT; i++)
    {
    	//printf("Bot %d: xpos=%.4f, ypos=%.4f\n", i + 1, fixed_to_float1(final_xpos[i]), fixed_to_float1(final_ypos[i]));
    	printf("Bot %d: xpos=%d, ypos=%d\n", i + 1, (final_xpos[i]), (final_ypos[i]));
    }

   // printf("\n source xpos=%.4f, ypos=%.4f\n",fixed_to_float(ux),fixed_to_float(uy));
    printf("\n source xpos=%d, ypos=%d\n",(ux),(uy));
    printf("--------- >--------------------<-------- \n");

    return 0;
}
