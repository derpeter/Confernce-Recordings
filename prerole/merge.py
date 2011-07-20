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

parser = argparse.ArgumentParser(description='merge splittet raw dv files')
parser.add_argument('-i', action="store", dest="id", help="talk id")
parser.add_argument('-o', action="store", dest="output", help="output dir", default='')
parser.add_argument('-v', action="store", dest="videodir", help="video dir", default='')
parser.add_argument('-f', action="store", dest="files", help="files to merge. Files are separated with a blank.", nargs="+")

args = parser.parse_args()

def merge():
    #check the inputs filds
    if args.id == None:
        print "id not defined"
        sys.exit(1)
    if args.files == None:
        print "no files defined"
        sys.exit(1)
    
    if os.path.exists(args.output+args.id+".dv"):
        commands.getstatusoutput("rm -f "+args.output+args.id+".dv")
    command=''
    for file in args.files:
        command = command + file+' '
        
    result = commands.getstatusoutput('cat '+command+'> '+args.output+args.id+'.dv')
    if result[0] != 0:
        print "merge failed"
        print result[1]
        sys.exit(1)
merge()