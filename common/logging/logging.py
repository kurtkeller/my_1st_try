import sys
import time
from common import settings as C
# KK: add file locking

# ----------------------------------------------------------------------
# settings
DI_severity = {
  "X":    [ 9, "eXtreme"    ],  # write every possible log message
  "D":    [ 8, "Debug"      ],
  "I":    [ 7, "Info"       ],
  "N":    [ 6, "Notice"     ],
  "W":    [ 5, "Warning"    ],
  "E":    [ 4, "Error"      ],
  "C":    [ 3, "Critical"   ],
  "A":    [ 2, "Alert"      ],
  "P":    [ 1, "Emergency"  ],  # Panic
  "S":    [ 0, "Silent"     ],  # no logging at all
  # S is not valid for passing as levels of log lines, it is only valid
  #   for C.LogLevel in order to suppress all logging
  # X is not valid for passing as levels of log lines, it is only valid
  #   for C.LogLevel in order to write all possible logging to the
  #   logfile, even DEBUG (which usually goes to STDERR)
}

# ------------------------------------------------------------------------
# log
# ------------------------------------------------------------------------
def log(msg="no message given",
        severity="W", out=None, date=None):

  """
  write a log entry if C.LogLevel is at or above the level of the message

  If C.LogLevel is "S" (=Silent), no logging will ever be written to the
  logfile.

  If C.LogLevel is "X" (=eXtreme), all logging will be written to the
  logfile, also Debug, which usually would go to STDERR.

  log(C, msg, [severity], [out], [date])

    msg         type:       string
                description:
                    the messae to write to the log

    severity    type:       string
                default:    W
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
  # if debug set, it overrules any lower C.LogLevel
  if C.LogLevel == "X":
      tmp_LogLevel = C.LogLevel
  elif C.DEBUG:
      tmp_LogLevel = "D"
  else:
      tmp_LogLevel = C.LogLevel

  # ----------------------------------------------------------------------
  # defaults
  if tmp_LogLevel == "S":
    return                      # shortcut, no logging here
  if not out:
    out=C.LogFile
  if not date:
    date=int(time.time())

  # debug output goes to STDERR, not the logfile, unless tmp_LogLevel is "X"
  if (severity == "D") and (tmp_LogLevel != "X"):
    out=sys.stderr

  # ----------------------------------------------------------------------
  # check for valid severity
  if (not severity in DI_severity.keys()) or \
     (severity == "S") or \
     (severity == "X"):
    print >>sys.stderr, "%s %s: %s" % (
                          time.strftime("%Y-%m-%dT%H:%M:%S",time.localtime(date)),
                          DI_severity["W"][1],
                          "severity-code %s not valid, using W instead" % severity)
    severity="W"

  # ----------------------------------------------------------------------
  # skip if the severity of the logline is above tmp_LogLevel
  if DI_severity[severity][0] > DI_severity[tmp_LogLevel][0]:
    return

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
                            DI_severity["W"][1],
                            "can not open logfile %s for writing" % out)
      fi_out = sys.stderr

  # ----------------------------------------------------------------------
  # write the logline
  print >>fi_out, "%s %s: %s" % (
                 time.strftime("%Y-%m-%dT%H:%M:%S",time.localtime(date)),
                 DI_severity[severity][1], msg.encode("UTF-8"))
  # do not close the file, because it could be sys.stdout or sys.stderr
  # but flush it to immediately see what is going on
  fi_out.flush()
