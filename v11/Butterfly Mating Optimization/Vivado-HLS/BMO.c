#include <stdio.h>
#include <stdint.h>

#define NBT 4
#define FIXED_POINT_FRACTIONAL_BITS 16
#define FIXED_POINT_ONE (1 << FIXED_POINT_FRACTIONAL_BITS)

// Fixed-point type definition
typedef int32_t fixed_point_t;

// Convert floating-point to fixed-point
fixed_point_t float_to_fixed(float value) {
    return (fixed_point_t)(value * FIXED_POINT_ONE);
}

// Convert fixed-point to floating-point
float fixed_to_float(fixed_point_t value) {
    return (float)value / FIXED_POINT_ONE;
}

// Fixed-point square root function
fixed_point_t custom_sqrt(fixed_point_t x) {
    if (x <= 0)
        return 0;

    fixed_point_t root = x;
    fixed_point_t root_prev;

    do {
        root_prev = root;
        root = (root!= 0) ? ((root + (((int64_t)x << FIXED_POINT_FRACTIONAL_BITS) / root)) >> 1) :0;
    } while (root != root_prev);
    return root;
}

void bmo_fixed(int it, fixed_point_t xpos[NBT + 1], fixed_point_t ypos[NBT + 1], fixed_point_t ux, fixed_point_t uy, fixed_point_t final_xpos[NBT], fixed_point_t final_ypos[NBT])
{

#pragma HLS INTERFACE s_axilite port=return
#pragma HLS INTERFACE s_axilite port=xpos
#pragma HLS INTERFACE s_axilite port=it
#pragma HLS INTERFACE s_axilite port=ypos
#pragma HLS INTERFACE s_axilite port=ux
#pragma HLS INTERFACE s_axilite port=uy
#pragma HLS INTERFACE s_axilite port=final_xpos
#pragma HLS INTERFACE s_axilite port=final_ypos


    fixed_point_t uv[NBT] = {0};
    fixed_point_t uvd[NBT * NBT] = {0};
    int lm[NBT] = {0};
    fixed_point_t f, w, x, y,xx,yy;
    fixed_point_t tmp1,tmp2,dx_square,dy_square;
    fixed_point_t nx,ny;
    int iteration, i, j, k, a;
//    fixed_point_t dx_square;
//    fixed_point_t dy_square;
//    fixed_point_t w;
    fixed_point_t d[NBT * NBT] = {0};
    fixed_point_t xi;
	fixed_point_t yi;
	fixed_point_t xj;
	fixed_point_t yj;
	fixed_point_t dx;
	fixed_point_t dy;
	fixed_point_t dx_square1;
	fixed_point_t dy_square2;
	fixed_point_t sqrt_inp;
	fixed_point_t uvval2;
	fixed_point_t uvval;
	fixed_point_t temp1[NBT], temp2[NBT];
	fixed_point_t xpos_dup[NBT], ypos_dup[NBT],uv_dup[NBT];
	fixed_point_t temp;
	fixed_point_t nx_square1;
	fixed_point_t ny_square2;
	fixed_point_t sqrt_inp2;
	fixed_point_t dinom;
    for (iteration = 1; iteration <= it; iteration++) {
        printf("Iteration %d:\n", iteration);
        for (i = 0; i < NBT; i++) {
            x = xpos[i];
            y = ypos[i];
            tmp1 = x - ux;
            tmp2 = y - uy;
    // Multiply the differences by themselves, ensuring no overflow
            dx_square = ((int64_t)tmp1 * tmp1) >> FIXED_POINT_FRACTIONAL_BITS;
            dy_square = ((int64_t)tmp2 * tmp2) >> FIXED_POINT_FRACTIONAL_BITS;
    // Add the squares together
            w = dx_square + dy_square;
            //tmp1 =(int64_t)((x - ux) * (x - ux));
            //tmp2 = (int64_t)((y - uy) * (y - uy));
            //w = (( tmp1 >>FIXED_POINT_FRACTIONAL_BITS ) + (tmp2>> FIXED_POINT_FRACTIONAL_BITS));
           // printf("w= %.4f \n",fixed_to_float(w));
            f = (FIXED_POINT_ONE - w + (((w * w) >> FIXED_POINT_FRACTIONAL_BITS) >> 1) - (((((w * w) >> FIXED_POINT_FRACTIONAL_BITS)*w)>>FIXED_POINT_FRACTIONAL_BITS) >> 2));
            uv[i] = (f > 0) ? f : 0; // Max function equivalent for fixed-point
           // printf("uv[%d] = %.4f \n", i ,fixed_to_float(uv[i]) );


//        for (i = 0; i < NBT; i++) {
            for (j = 0; j < NBT; j++) {
                 xi = xpos[i];
                 yi = ypos[i];
                 xj = xpos[j];
                 yj = ypos[j];
                 dx = xj - xi;
                 dy = yj - yi;
                 dx_square1 = ((int64_t)dx * dx) >> FIXED_POINT_FRACTIONAL_BITS;
                 dy_square2 = ((int64_t)dy * dy) >> FIXED_POINT_FRACTIONAL_BITS;
    // Add the squares together
                 sqrt_inp = dx_square1 + dy_square2;
               // printf("sqrt_inp= %.4f \n", fixed_to_float(sqrt_inp));
                d[i * NBT + j] = custom_sqrt(sqrt_inp);
               // printf("dx=%f\n",fixed_to_float((dx * dx + dy * dy)));
              // d[i * NBT + j] = custom_sqrt(((((int64_t)dx * dx) +((int64_t)dy * dy) ) >> FIXED_POINT_FRACTIONAL_BITS ));
                //d[i * NBT + j] = custom_sqrt((dx * dx + dy * dy) >> (FIXED_POINT_FRACTIONAL_BITS - 1));
               //printf("d[%d] = %.4f \n", i * NBT + j,fixed_to_float(d[i * NBT + j]));
            }
    	//}

        //for (i = 0; i < NBT; i++) {
            for (j = 0; j < NBT; j++) {
                if (i != j) {
                    fixed_point_t sm = 0;
                    for (a = 0; a < NBT; a++) {
                        if (i != a) {
                            //printf("sm1= %.4f \n", fixed_to_float(sm));

                            sm += ((int64_t)FIXED_POINT_ONE << FIXED_POINT_FRACTIONAL_BITS) / d[i * NBT + a];
                             //sm += ((d[i * NBT + a] != 0) ? (((int64_t)FIXED_POINT_ONE << FIXED_POINT_FRACTIONAL_BITS) / d[i * NBT + a]):0);

                            // printf("sm= %.4f \n", fixed_to_float(sm));
                        }
                    }
                     uvval2 = (uv[i] * ((int64_t)FIXED_POINT_ONE << FIXED_POINT_FRACTIONAL_BITS) / d[i * NBT + j]);
                   //fixed_point_t uvval2 = ((d[i * NBT + a] != 0) ? (uv[i] * ((int64_t)FIXED_POINT_ONE << FIXED_POINT_FRACTIONAL_BITS) / d[i * NBT + j]) : 0);

                 //  printf("uvval2 = %.4f \n", fixed_to_float(uvval2));


                    uvval = (sm!=0) ? (((int64_t)uvval2 << FIXED_POINT_FRACTIONAL_BITS)  / sm) : 0;

                    uvd[i * NBT + j] = uvval;
                   // printf("uvd1[%d] = %.4f \n", i * NBT + j,fixed_to_float(uvd[i * NBT + j]));
                }
            }
        //}

        //for (i = 0; i < NBT; i++) {

            for (k = 0; k < NBT; k++) {
                temp1[k] = uvd[k * NBT + i];
                temp2[k] = (int32_t)k;
                xpos_dup[k] = xpos[i];
				ypos_dup[k] = ypos[i];
				uv_dup[k] = uv[i];
               // printf("  tempjkml2[%d]=%d \n",  k,(temp2[k]));
            }
            for (j = 0; j < NBT - 1; j++) {
                for (k = 0; k < NBT - j - 1; k++) {
                    if (temp1[k] < temp1[k + 1]) {
                         temp = temp1[k];
                        temp1[k] = temp1[k + 1];
                        temp1[k + 1] = temp;
                        temp = temp2[k];
                        temp2[k] = temp2[k + 1];
                        temp2[k + 1] = temp;
                        temp = xpos_dup[k];
                        xpos_dup[k] = xpos_dup[k + 1];
                        xpos_dup[k + 1] = temp;
                        temp = ypos_dup[k];
                        ypos_dup[k] = ypos_dup[k + 1];
                        ypos_dup[k + 1] = temp;
                        temp = uv_dup[k];
                        uv_dup[k] = uv_dup[k + 1];
                        uv_dup[k + 1] = temp;


                    }
                }
            }
            // printf(" temp1[%d]=%.4f \n temp2[%d]=%d \n", i,fixed_to_float(temp1[i]), i,(temp2[i]));


            if (temp2[0] == 0)
            {

                  nx = xpos[NBT] - xpos[i];
                  ny = (uy - y);
            }
            else
			{             if (uv[i] < uv_dup[0])
						{
                            nx = xpos_dup[0] - x;
                            ny = ypos_dup[0] - y;
						}
						else
                         {
                            nx = ux - x;
                            ny = uy - y;
                         }
			}

        //}

        //for (i = 0; i < NBT; i++) {
//            fixed_point_t nx = xpos[lm[i]] - xpos[i];
//            fixed_point_t ny = ypos[lm[i]] - ypos[i];

             nx_square1 = ((int64_t)nx * nx) >> FIXED_POINT_FRACTIONAL_BITS;
             ny_square2 = ((int64_t)ny * ny) >> FIXED_POINT_FRACTIONAL_BITS;
    // Add the squares together
             sqrt_inp2 = nx_square1 + ny_square2;
             // printf(".15 value= %d \n", float_to_fixed(0.15));


             dinom = custom_sqrt(sqrt_inp2);
            //printf("dinom=%.4f\n ",fixed_to_float(dinom));

          //  xpos[i] += (9830 * (((int64_t)nx << FIXED_POINT_FRACTIONAL_BITS) / dinom)) >> FIXED_POINT_FRACTIONAL_BITS; // 0.15 in fixed-point
           // ypos[i] += (9830 * (((int64_t)ny << FIXED_POINT_FRACTIONAL_BITS) / dinom)) >> FIXED_POINT_FRACTIONAL_BITS;
            xpos[i] += ((dinom!=0)?((9830 * (((int64_t)nx << FIXED_POINT_FRACTIONAL_BITS) / dinom)) >> FIXED_POINT_FRACTIONAL_BITS) : 0); // 0.15 in fixed-point
            ypos[i] += ((dinom!=0)?((9830 * (((int64_t)ny << FIXED_POINT_FRACTIONAL_BITS) / dinom)) >> FIXED_POINT_FRACTIONAL_BITS) : 0); // 0.15 in fixed-point
           // printf("Bot %d: xpos=%.4f, ypos=%.4f\n", i + 1, fixed_to_float(xpos[i]), fixed_to_float(ypos[i]));

        //}

        // Print bot positions for this iteration
        //for (i = 0; i < NBT; i++) {
          printf("Bot %d: xpos=%.4f, ypos=%.4f\n", i + 1, fixed_to_float(xpos[i]), fixed_to_float(ypos[i]));
         // printf("Bot %d: xpos=%d, ypos=%dn", i + 1, (xpos[i]), (ypos[i]));

        //}
        }
    }

    for (i = 0; i < NBT; i++) {
    	final_xpos[i] = xpos[i];
    	final_ypos[i] = ypos[i];
    }

}
