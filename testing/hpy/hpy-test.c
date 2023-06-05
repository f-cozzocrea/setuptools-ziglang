#include "hpy.h"

HPyDef_METH(say_hello, "say_hello", HPyFunc_NOARGS)
static HPy say_hello_impl(HPyContext *ctx, HPy self)
{
    return HPyUnicode_FromString(ctx, "Hello world");
}

HPyDef_METH(add, "add", HPyFunc_VARARGS)
static HPy add_impl(HPyContext *ctx, HPy self, const HPy *args, size_t nargs)
{
  long a, b;
  if (!HPyArg_Parse(ctx, NULL, args, nargs, "ll", &a, &b))
    return HPy_NULL;
  return HPyLong_FromLong(ctx, a+b);
}

static HPyDef *HPyTestMethods[] = {
  &say_hello,
  &add,  
  NULL,
};

static HPyModuleDef hpy_test_def = {
  .doc = "HPy Quickstart Example",
  .defines = HPyTestMethods,
};

HPy_MODINIT(hpy_test, hpy_test_def)
