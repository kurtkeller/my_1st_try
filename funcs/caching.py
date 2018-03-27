import cPickle
from common import settings as C
from common import logging as L

# KK: should to file locking...

# ------------------------------------------------------------------------
# load_cache
# ------------------------------------------------------------------------
def load_cache():
  """
  load the cache and return it

  load_cache()

  expects:

  returns:
    di_cache    dictionary with the loaded cache

  """

  try:
    di_cache = cPickle.load(file(C.CacheFile,"r"))
    L.log(severity="I", msg='result=success msg="cache loaded"')
  except:
    di_cache = {}
    L.log(severity="W", msg='result=failure msg="cache not loaded"')

  return(di_cache)

# ------------------------------------------------------------------------
# save_cache
# ------------------------------------------------------------------------
def save_cache(di_cache):
  """
  save the cache

  save_cache(di_cache)

  expects:
    di_cache    the cache to save

  returns:
    nothing

  """

  try:
    cPickle.dump(di_cache, file(C.CacheFile,"w"))
    L.log(severity="I", msg='result=success msg="cache saved"')
  except:
    L.log(severity="W", msg='result=failure msg="cache not saved"')
