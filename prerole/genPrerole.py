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

parser = argparse.ArgumentParser(description='Generate prerole file: make sure you have ffmpeg and inkscape in $PATH')
parser.add_argument('-f', action="store", dest="background", help="background SVG. Default background.svg", default='background.svg' )
parser.add_argument('-t', action="store", dest="title", help="talk title")
parser.add_argument('-s', action="store", dest="subtitle", help="talk subtitle")
parser.add_argument('-p', action="store", dest="speakers", help="person(s). Persons are separated with a blank.", nargs="+")
parser.add_argument('-d', action="store", dest="date", help="date of the talk")
parser.add_argument('-b', action="store", dest="begin", help="begin of the talk")
parser.add_argument('-i', action="store", dest="id", help="talk id")
parser.add_argument('-o', action="store", dest="output", help="output dir", default='')
parser.add_argument('-w', action="store", dest="workdir", help="working dir", default='')

args = parser.parse_args()
output=[]

# replace the string in a given svg
def build_svg():
    
    #check the inputs filds
    if args.id == None:
        print "id not defined"
        sys.exit(1)
    if args.title == None:
        print "title not defined"
        sys.exit(1)
    if len(args.title) > 45:
        print "title to long"
        sys.exit(1)
    if args.subtitle == None:
        print "subtitle not defined"
        args.subtitle = ''
    if len(args.subtitle) > 63:
        print "subtitle to long"
        sys.exit(1)
    if args.speakers == None:
        print "person not defined"
        sys.exit(1)
    if args.date == None:
        print "date not defined"    
        args.date=''
    if args.begin == None:
        print "begin not defined"
        args.begin = ''

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
        
    # replace the strings in the svg
    # add here some filtering to precent to long names
    for line in fileinput.FileInput(args.background,inplace=0):
        if "%title%" in line:
            line=line.replace('%title%',args.title)
            output.append(line)
        elif "%subtitle%" in line:
            line=line.replace('%subtitle%', args.subtitle)
            output.append(line)    
        elif "%speaker%" in line:
            line=line.replace('%speaker%', speaker)
            output.append(line)    
        elif "%date%" in line:
            line=line.replace('%date%', args.date+' '+args.begin)
            output.append(line)
        else:
            output.append(line)    
            
    outfileName = args.workdir+args.id+".svg"        
    outfile = file(outfileName, 'w')
    outfile.writelines(output)

# create a png out of the svg
def build_png():
    result = commands.getstatusoutput("inkscape "+ args.workdir+args.id +".svg -e "+args.workdir+args.id+".png")
    if result[0] != 0:
        print "png not created"
        print result[1] 
        sys.exit(1)

# build the dv file            
def build_dv():
    # check if tmp file already present and remove it
    if os.path.exists(args.workdir+args.id+".tmp"):
        commands.getstatusoutput("rm -f "+args.workdir+args.id+".tmp")
    result = commands.getstatusoutput("ffmpeg -qscale 3 -loop_input -i "+ args.workdir+args.id +".png -target dv-pal "+args.workdir+args.id+".tmp -t 10 -r 25 -an -threads 2")
    if result[0] != 0:
        print "inital dv file not created"
        print result[1]
        sys.exit(1)
    
    #check if silence file is present, if not generate it
    if not os.path.exists('silence'):
        os.system('dd if=/dev/zero of=silence ibs=10240 count=10240')
    
    #check if prerole file is present if yes delete it        
    if os.path.exists(args.output+args.id+"prerole.dv"):
        commands.getstatusoutput("rm -f "+args.output+args.id+"prerole.dv") 
        
    result = commands.getstatusoutput("ffmpeg -f dv -target pal-dv -i "+args.workdir+args.id+".tmp -f u16le -i silence -vcodec copy -t 10s "+args.output+args.id+"prerole.dv")
    #if result[0] == 1:
    # no idea why ffmpeg is not returning 0 at this call
    if True:    
        commands.getstatusoutput("rm -f "+args.workdir+args.id+".tmp")
    else:
        print "audio fix not applied"
        print result[1]
        sys.exit(1)
    #clean up
    commands.getstatusoutput("rm -f "+args.workdir+args.id+".png")
    commands.getstatusoutput("rm -f "+args.workdir+args.id+".svg")
    
build_svg()
build_png()
build_dv()
sys.exit(0)