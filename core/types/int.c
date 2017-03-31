#include "rain.h"

void rain_ext_int_float(box *ret, box *value) {
  if(BOX_ISNT(value, INT)) {
    rain_throw(rain_exc_arg_mismatch);
  }

  rain_set_float(ret, (double)value->data.si);
}
