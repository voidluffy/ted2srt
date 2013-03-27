#!/usr/bin/python
# -*- encoding:utf-8 -*-

"""
https://github.com/yasondinalt/ted2srt

Translate TED's Transcript into srt file.

Takes TED's transcript filename as argument (.json extension required).

NB: to get transcript, use this URL:
http://www.ted.com/talks/subtitles/id/VIDEO_ID/lang/en
"""

# srt example
"""1
00:00:3,000 --> 00:00:5,000
And I'm happy most of the time"""

# TED's transcript example (first tags)
"""{"duration":2000,"content":"And I'm happy most of the time,","startOfParagraph":false,"startTime":3000}"""

import re, sys

# Pattern to identify a subtitle and grab start, duration and text.

def parseLine(text):
    """Parse a subtitle."""
    text = text.replace('\\"','&amp;quot;')
    pat = re.compile(r'.*?\"duration\"\:([\.\d]+?),\"content\"\:\"(.*?)\".*?\"startTime\":([\.\d]*)', re.DOTALL|re.U|re.I|re.S)
    m = re.match(pat, text)
    if m:
        return (m.group(3), m.group(1), m.group(2))
    else:
        return None

def formatSrtTime(secTime):
    """Convert a time in seconds (TED's transcript) to srt time format."""
    sec = int(secTime)/1000+16
    micro = 0
    m, s = divmod(int(sec), 60)
    h, m = divmod(m, 60)
    return "{:02}:{:02}:{:02},{}".format(h,m,s,micro)

def convertHtml(text):
    """A few HTML encodings replacements.
    &amp;#39; to '
    &amp;quot; to "
    """
    text = text.decode('unicode-escape', 'replace').encode('utf-8', 'replace')
    return text.replace('&amp;#39;', "'").replace('&amp;quot;', '"')

def printSrtLine(i, elms):
    """Print a subtitle in srt format."""
    return "{}\n{} --> {}\n{}\n\n".format(i, formatSrtTime(elms[0]), formatSrtTime(float(elms[0])+float(elms[1])), convertHtml(elms[2]))

fileName = sys.argv[1]

def main(fileName):
    """Parse TED's transcript and write the converted data in srt format."""
    with open(sys.argv[1], 'r') as infile:
        buf = []
        for line in infile:
            buf.append(line)
    # Split the buffer to get one string per tag.
    buf = "".join(buf).split('},{')
    i = 0
    srtfileName = fileName.replace('.json', '.srt')
    with open(srtfileName, 'w') as outfile:
        for text in buf:
            parsed = parseLine(text)
            if parsed:
                i += 1
                outfile.write(printSrtLine(i, parsed))
            print i
            print text
            print parsed
    print('DONE ({})'.format(srtfileName))

if __name__ == "__main__":
    main(fileName)
