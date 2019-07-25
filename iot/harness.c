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
//required to use js modules
#include "duk_module_duktape.h"
//required to read from a config file the name of the module
#include  "ini.h"

//These structure and handler function are for reading configuration
//from an .ini file
typedef struct
{
    const char* id;
    const char* path;
} configuration;

static int handler(void* user, const char* section, const char* name,
                   const char* value)
{
    configuration* pconfig = (configuration*)user;

    #define MATCH(s, n) strcmp(section, s) == 0 && strcmp(name, n) == 0
    if (MATCH("module", "id")) {
        pconfig->id = strdup(value);
    } else if (MATCH("module", "path")) {
        pconfig->path = strdup(value);
    } else {
        return 0;  /* unknown section/name, error */
    }
    return 1;
}

duk_ret_t mod_search(duk_context *ctx) {
    /* Nargs was given as 4 and we get the following stack arguments:
     *   index 0: id
     *   index 1: require
     *   index 2: exports
     *   index 3: module
     */

	configuration config;

    if (ini_parse("module.ini", handler, &config) < 0) {
        printf("WARNING: Can't load 'module.ini'\n");
        return 1;
    }
	printf("INFO: 'module.ini' loaded\n");
	char *src = NULL;
	FILE *f   = NULL;
	//const char *filename = "/home/moar82/benchmark/js_modules/numeral/en-gb.min.js";
	//const char *filename = "/home/moar82/benchmark/js_modules/numeral/numeral.min.js";
	const char *filename = config.path;

	int  rc, len;

	// Pull Arguments
	char *id = duk_require_string(ctx, 0);

	printf("INFO: Duktape stack idx 0 (ID) => %s \n", id);

	/*char *result;
	result = Search_in_File(argv[1], "require(");
	printf("compare result and id: %d\n",strcmp(id, result) );
	*/
	//rc = strcmp(id, "numeral");
	rc = strcmp(id, config.id);
	if(rc == 0)
	{
	    printf("INFO: Module ID from duktape stack matches module.ini id\n");
	    // Read File and calculate its size (as DUKtape examples)
	    printf("INFO: Loading %s js module \n", filename);
	    f = fopen(filename, "rb");
	    fseek(f, 0, SEEK_END);
	    len = (int) ftell(f);

	    // Rewind
	    fseek(f, 0, SEEK_SET);

	    src = malloc(len);
	    fread(src, 1, len,f);
	    fclose(f);
	    duk_push_lstring(ctx, src, len);
	    free(src);
	    return 1;
	  }
	// Error
	    return -1;
}

/* Function declaration */
void modSearch_register(duk_context *ctx) {
    duk_get_global_string(ctx, "Duktape");
    duk_push_c_function(ctx, mod_search, 4 /*nargs*/);
    duk_put_prop_string(ctx, -2, "modSearch");
    duk_pop(ctx);
}

/* For brevity assumes a maximum file length of 17kB. */
static void push_file_as_string(duk_context *ctx, const char *filename) {
    FILE *f;
    size_t len;
    char buf[17384];

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
	
	    duk_module_duktape_init(ctx);
	    printf("top after init: %ld\n", (long) duk_get_top(ctx));
	    modSearch_register(ctx);
	    //push_file_as_string(ctx, "12.10-2-2.js");//here I should parametrize it with the name of the js file
	    printf("INFO: modSearch_register executed \n");
	    push_file_as_string(ctx, argv[1]);//here I should parametrize it with the name of the js file
	    if (duk_peval(ctx) != 0) {
	        printf("Error evaluating js script: %s\n", duk_safe_to_string(ctx, -1));
	        goto finished;
	    }
	    duk_pop(ctx);  /* ignore result */
	    /* when the js function argument is different from 0 we
		* should call the function specified by the argument.
		* Hence, the following lines inside the if are required */	
	    if (strcmp(argv[2],".")!=0){
		duk_push_global_object(ctx);
	    	duk_get_prop_string(ctx, -1 /*index*/, argv[2]);
	    	printf("js function name provided %s \n", argv[2]);
          //    duk_push_string(ctx, line);
	    	if (duk_pcall(ctx, 0 /*nargs*/) != 0) {
	        	printf("Error executing JS function: %s\n", duk_safe_to_string(ctx, -1));
	            } 
	    	/*else {
	                printf("%s\n", duk_safe_to_string(ctx, -1));
	            }*/
	    	duk_pop(ctx);  /* pop result/error */
	    }
	
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


