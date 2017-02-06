#include <stdlib.h>
#include "string.h"


void rain_to_string(box *ret, box *val) {
  box key;
  box to_str;

  switch(val->type) {
    case ITYP_NULL:
      rain_set_str(ret, "null");
      break;

    case ITYP_INT:
      sprintf(fmt_buf, "%ld", val->data.si);
      rain_set_strcpy(ret, fmt_buf, strlen(fmt_buf));
      break;

    case ITYP_FLOAT:
      sprintf(fmt_buf, "%f", val->data.f);
      rain_set_strcpy(ret, fmt_buf, strlen(fmt_buf));
      break;


    case ITYP_BOOL:
      rain_set_str(ret, val->data.ui ? "true" : "false");
      break;

    case ITYP_STR:
      rain_set_strcpy(ret, val->data.s, val->size);
      break;

    case ITYP_TABLE:
      rain_set_str(&key, "_str");
      rain_get(&to_str, val, &key);
      if(BOX_IS(&to_str, FUNC) && to_str.size == 1) {
        void (*func_ptr)(box *, box *) = (void (*)(box *, box *))(to_str.data.vp);
        func_ptr(ret, val);
        break;
      }

      sprintf(fmt_buf, "table 0x%08lx", val->data.ui);
      rain_set_strcpy(ret, fmt_buf, strlen(fmt_buf));
      break;

    case ITYP_FUNC:
      sprintf(fmt_buf, "func 0x%08lx", val->data.ui);
      rain_set_strcpy(ret, fmt_buf, strlen(fmt_buf));
      break;

    case ITYP_CDATA:
      sprintf(fmt_buf, "cdata 0x%08lx", val->data.ui);
      rain_set_strcpy(ret, fmt_buf, strlen(fmt_buf));
      break;
  }
}

void rain_fmt(box *ret, box *val, box *fmt) {
  if(BOX_ISNT(fmt, STR)) {
    return;
  }

  switch(val->type) {
    case ITYP_INT:
      sprintf(fmt_buf, fmt->data.s, val->data.si);
      rain_set_strcpy(ret, fmt_buf, strlen(fmt_buf));
      break;

    case ITYP_FLOAT:
      sprintf(fmt_buf, fmt->data.s, val->data.f);
      rain_set_strcpy(ret, fmt_buf, strlen(fmt_buf));
      break;

    default:
      rain_to_string(ret, val);
  }
}

void rain_string_to_int(box *ret, box *str) {
  rain_set_int(ret, atoi(str->data.s));
}
