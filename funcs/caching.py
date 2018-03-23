import cPickle
from .logging import log

# ------------------------------------------------------------------------
# load_cache
# ------------------------------------------------------------------------
def load_cache(C):
  """
  load the cache and return it

  load_cache(C)

  expects:
    C           configuration

  returns:
    di_cache    dictionary with the loaded cache

  """

  try:
    di_cache = cPickle.load(file(C.CacheFile,"r"))
    log(C, severity="I", msg='result=success msg="cache loaded"')
  except:
    di_cache = {}
    log(C, severity="W", msg='result=failure msg="cache not loaded"')

  return(di_cache)

# ------------------------------------------------------------------------
# save_cache
# ------------------------------------------------------------------------
def save_cache(C, di_cache):
  """
  save the cache

  save_cache(C)

  expects:
    C           configuration
    di_cache    the cache to save

  returns:
    nothing

  """

  try:
    cPickle.dump(di_cache, file(C.CacheFile,"w"))
    log(C, severity="I", msg='result=success msg="cache saved"')
  except:
    log(C, severity="W", msg='result=failure msg="cache not saved"')
