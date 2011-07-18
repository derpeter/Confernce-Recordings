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

parser = argparse.ArgumentParser(description='Encode a dv file to h264: make sure you have ffmpeg $PATH')
parser.add_argument('-i', action="store", dest="id", help="talk id")
parser.add_argument('-o', action="store", dest="output", help="output dir", default='')
parser.add_argument('-v', action="store", dest="videodir", help="video dir", default='')
parser.add_argument('-t', action="store", dest="threads", help="threads to use by ffmpeg")
args = parser.parse_args()

#check the inputs filds
if args.id == None:
    print "id not defined"
    sys.exit(1)
        
if args.threads == None:
    args.threads = 0

def encWebM():
    if os.path.exists(args.videodir+args.id+".dv"):
        commands.getstatusoutput("rm -f "+args.videodir+args.id+".dv")
    result = commands.getstatusoutput('ffmpeg -i '+ args.id +'.dv -vpre libvpx-720p -threads '+ str(args.threads) +' -pass 1 -an -f webm -y /dev/null > '+ args.id +'.log')
    if result[0] != 0:
        print "webM encoding pass1 failed"
        print result[1]
        sys.exit(1)
        
    result = commands.getstatusoutput('fmpeg -i '+ args.id +'.dv -vpre libvpx-720p -threads '+ str(args.threads) +' -pass 2 -acodec libvorbis -ab 100k -f webm -y '+ args.output+args.id +'.webm >> '+ args.id +'.log')
    if result[0] != 0:
        print "webM encoding pass2 failed"
        print result[1]
        sys.exit(1)
    
encWebM()