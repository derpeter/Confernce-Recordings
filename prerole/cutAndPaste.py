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

parser = argparse.ArgumentParser(description='Cut the rawdv an paste prerole: make sure you have ffmpeg $PATH')
parser.add_argument('-i', action="store", dest="id", help="talk id")
parser.add_argument('-o', action="store", dest="output", help="output dir", default='')
parser.add_argument('-v', action="store", dest="videodir", help="video dir", default='')
parser.add_argument('-p', action="store", dest="preroledir", help="prerole dir", default='')
parser.add_argument('-t', action="store", dest="threads", help="threads to use by ffmpeg")
parser.add_argument('-s', action="store", dest="start", help="start time format hh:mm:ss")
parser.add_argument('-e', action="store", dest="end", help="end time format hh:mm:ss")
args = parser.parse_args()

#check the inputs filds
if args.id == None:
    print "id not defined"
    sys.exit(1)
if args.start == None:
    print "start time not defined"
    sys.exit(1)
if args.id == None:
    print "end time defined"
    sys.exit(1)

def paste():
    if os.path.exists(args.output+args.id+".dv"):
        commands.getstatusoutput("rm -f "+args.output+args.id+".dv")
    result = commands.getstatusoutput('cat '+args.preroledir+args.id+'prerole.dv '+ args.videodir+args.id +"dv > "+args.output+args.id+".dv")
    if result[0] != 0:
        print "cut failed"
        sys.exit(1)
def cut():
    to=args.end - args.start 
    result = commands.getstatusoutput('ffmpeg -i '+args.videodir+args.id+'.dv -ss '+args.start+' -t '+to+' -vcodec copy -acodec copy -target dv cutted '+args.id+'.dv') 
    if result[0] !=0:
        print "cutting failed"
        sys.ecit(1)
        
cut()
paste()
    