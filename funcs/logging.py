import sys
import time

# ----------------------------------------------------------------------
# settings
DI_severity = {
  "D":    "Debug",
  "I":    "Info",
  "N":    "Notice",
  "W":    "Warning",
  "E":    "Error",
  "C":    "Critical",
  "A":    "Alert",
  "P":    "Emergency"     # Panic
}

# ------------------------------------------------------------------------
# log
# ------------------------------------------------------------------------
def log(C, msg="no message given",
        severity="I", out=None, date=None):

  """
  write a log entry

  log(C, msg, [severity], [out], [date])

    C           the global config
    msg         type:       string
                description:
                    the messae to write to the log

    severity    type:       string
                default:    I
                description:
                    the code for severity of the message
                    D / I / N / W / E / C / A / P
                    for
                    Debug / Info / Notice / Warning / Error /
                    Critical / Alert / Emergency (Panic)

    out         type:       filename
                default:    LogFile
                description:
                    the full path to a writable file which
                    will be opened in append mode and the
                    log entry written to it

    date        type:       Integer (unix epoch time)
                default:    current time
                description:
                    timestamp to use for logging; the value
                    will be converted to ISO-8601 format
  """


  # ----------------------------------------------------------------------
  # defaults
  if not out:
    out=C.LogFile
  if not date:
    date=int(time.time())

  # debug outut always goes to STDERR
  if severity == "D":
    out=sys.stderr

  # ----------------------------------------------------------------------
  # check for valid severity
  if not severity in DI_severity.keys():
    print >>sys.stderr, "%s %s: %s" % (
                          time.strftime("%Y-%m-%dT%H:%M:%S",time.localtime(date)),
                          DI_severity["W"],
                          "severity-code %s not valid, using W instead" % severity)
    severity="W"

  # ----------------------------------------------------------------------
  # check for valid output file
  try:
    scr=out.fileno
    fi_out=out
  except AttributeError:
    try:
      fi_out=open(out,"a")
    except:
      print >>sys.stderr, "%s %s: %s" % (
                            time.strftime("%Y-%m-%dT%H:%M:%S",time.localtime(date)),
                            DI_severity["W"],
                            "can not open logfile %s for writing" % out)
      fi_out = sys.stderr

  # ----------------------------------------------------------------------
  # write the logline
  print >>fi_out, "%s %s: %s" % (
                        time.strftime("%Y-%m-%dT%H:%M:%S",time.localtime(date)),
                        DI_severity[severity], msg)
  # do not close the file, because it could be sys.stdout or sys.stderr

  # flush while debugging to immediately see what is going on
  if C.DEBUG:
    fi_out.flush()

