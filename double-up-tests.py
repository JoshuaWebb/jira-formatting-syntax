#!/usr/bin/env python
import os
import re

import errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

mkdir_p("generated")
filenames = ["syntax_test_Bold.jira"]
for filename in filenames:
    (filenameWithoutExt, ext) = os.path.splitext(filename)
    file = open(filename, "r")
    header = file.readline()
    # TODO: use some kind of path join method from python?
    outfile = open("generated/" + filenameWithoutExt + "_duped" + ext, "w")
    outfile.write(header + "\n")

    stringUnderTest = ""
    testLines = []
    for line in file:
        match = re.match("   (.+)", line)
        if (match):
            for testLine in testLines:
                outfile.write("// " + testLine + "\n")

            if (stringUnderTest != ""):
                outfile.write("// " + (" " * len(stringUnderTest)) + " ^ - markup\n")

            for testLine in testLines:
                outfile.write("// " + (" " * len(stringUnderTest)) + "   " + testLine + "\n")

            outfile.write("\n")
            stringUnderTest = match.group(1)
            outfile.write("   " + stringUnderTest + " x " + stringUnderTest + "\n")
            testLines = []
            continue

        match = re.match("// (.+)", line)
        if (match):
            testLines.append(match.group(1))
            continue

    file.close()