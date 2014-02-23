#    Copyright (C) 2011  derpeter
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
import argparse
import fileinput
import commands
import sys
import os

parser = argparse.ArgumentParser(description='VOC Control - post processing and publishing the 1337 way')
parser.add_argument('-i', action="store", dest="id", help="talk id")
parser.add_argument('-o', action="store", dest="output", help="output dir", default='')
parser.add_argument('-v', action="store", dest="videodir", help="video dir", default='')
parser.add_argument('-t', action="store", dest="title", help="talk title")
parser.add_argument('-s', action="store", dest="subtitle", help="talk subtitle")
parser.add_argument('-p', action="store", dest="speakers", help="person(s). Persons are separated with a blank.", nargs="+")
parser.add_argument('-d', action="store", dest="date", help="date of the talk")
parser.add_argument('-b', action="store", dest="begin", help="begin of the talk")

args = parser.parse_args()



#check the inputs filds
if args.id == None:
    print "id not defined"
    sys.exit(1)
if args.title == None:
    print "title not defined"
    sys.exit(1)
if args.speakers == None:
    print "person not defined"
    sys.exit(1)
if args.date == None:
    print "date not defined"    
    sys.exit(1)
if args.begin == None:
    print "begin not defined"
    sys.exit(1)        

# build the speaker name
if len(args.speakers) == 1:
    speaker = args.speakers[0]
elif len(args.speakers) == 2:
    speaker = args.speakers[0] + ' ' + args.speakers[1]
elif len(args.speakers) == 3:
    speaker = args.speakers[0] + ' - ' + args.speakers[1] + ' - ' + args.speakers[2]
elif len(args.speakers) == 4:
    speaker = args.speakers[0] + ' - ' + args.speakers[1] + ' - ' + args.speakers[2] + ' - ' + args.speakers[3]
# in the rare case that we have more than 4 speaker we replace the last speakers with et al.
elif len(args.speakers) > 4:
    speaker = args.speakers[0] + ' - ' + args.speakers[1] + ' - ' + args.speakers[2] + ' - ' + args.speakers[3] + ' - et al.'

def encTheora():
    if os.path.exists(args.videodir+args.id+".dv"):
        commands.getstatusoutput("rm -f "+args.videodir+args.id+".dv")
    result = commands.getstatusoutput('ffmpeg2theora '+ args.videodir+args.id +'.dv  --artist "'+ speaker +'" --title "'+ args.title +'" --date "'+ args.date +' '+ args.begin +'" --deinterlace -o '+ args.output+args.id+'.mp4')
    if result[0] != 0:
        print "theora encoding failed"
        print result[1]
        sys.exit(1)
    
encTheora()