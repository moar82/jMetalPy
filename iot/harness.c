/*
 *  we test to read js scripts and measure memory footprint
 *  parameters: js file, main js function to execute
 */

/* processlines.c */
#include <stdio.h>
#include <string.h>
#include <malloc.h>
#include <stdlib.h>
#include <string.h>
#include "duktape.h"

/* For brevity assumes a maximum file length of 16kB. */
static void push_file_as_string(duk_context *ctx, const char *filename) {
    FILE *f;
    size_t len;
    char buf[16384];

    f = fopen(filename, "rb");
    if (f) {
        len = fread((void *) buf, 1, sizeof(buf), f);
        fclose(f);
        duk_push_lstring(ctx, (const char *) buf, (duk_size_t) len);
    } else {
        duk_push_undefined(ctx);
    }
}

static int
       get_total_size_of_memory_occupied(void)
       {
           struct mallinfo mi;
           mi = mallinfo();
           return mi.uordblks;
       }


static duk_ret_t native_print(duk_context *ctx) {
	duk_push_string(ctx, " ");
	duk_insert(ctx, 0);
	duk_join(ctx, duk_get_top(ctx) - 1);
	printf("%s\n", duk_safe_to_string(ctx, -1));
	return 0;
}



int main(int argc, const char *argv[]) {
	if ( argc == 3){
	    duk_context *ctx = NULL;
	    //char line[4096];
	    //size_t idx;
	    //int ch;
	
	    (void) argc; (void) argv;
	    ctx = duk_create_heap_default();
	    if (!ctx) {
	        printf("Failed to create a Duktape heap.\n");
	        exit(1);
	    }

	    //these 3 lines are only used for debuggin purposes. Comment otherwise
	    /*duk_push_global_object(ctx);
    	duk_push_c_function(ctx, native_print, DUK_VARARGS);
    	duk_put_prop_string(ctx, -2, "print");*/
	
	    //push_file_as_string(ctx, "12.10-2-2.js");//here I should parametrize it with the name of the js file
	    push_file_as_string(ctx, argv[1]);//here I should parametrize it with the name of the js file
	    if (duk_peval(ctx) != 0) {
	        printf("Error: %s\n", duk_safe_to_string(ctx, -1));
	        goto finished;
	    }
	    duk_pop(ctx);  /* ignore result */
	    duk_push_global_object(ctx);
	    duk_get_prop_string(ctx, -1 /*index*/, argv[2]);
	//    duk_push_string(ctx, line);
	    if (duk_pcall(ctx, 0 /*nargs*/) != 0) {
	        printf("Error: %s\n", duk_safe_to_string(ctx, -1));
	            } 
	    /*else {
	                printf("%s\n", duk_safe_to_string(ctx, -1));
	            }*/
	    duk_pop(ctx);  /* pop result/error */
	    int JS_MemoryUsed = get_total_size_of_memory_occupied();
	    printf("%d",JS_MemoryUsed );
		
		finished:
	    duk_destroy_heap(ctx);    
	}
	else {
		printf("You need to provide: (1) the name of the js to run;\
			(2) the js function to execute"); 
	}
	exit(0);
}


