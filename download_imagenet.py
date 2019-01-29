#!/usr/bin/env python3

import xmltodict
import urllib
import os
from subprocess import Popen, PIPE
import requests
import sys
import magic

logfile = "./log.txt"

logfd = open( logfile, "w" )
input_file = sys.argv[ 1 ] 

with open( input_file ) as fd:
    for line in fd:
        name, url = line.split( None, 1 )
        wnid, num = name.split( '_' )
        url = url.rstrip()
        basename = os.path.basename( url )
        extension = os.path.splitext( basename )[ 1 ]
        saved_file = "%s/%s" % ( wnid, basename )

        if not os.path.isdir( wnid ):
            print( "Creating dir: %s" % wnid )
            os.mkdir( wnid )
            
        try:
            args = [ "wget", "--output-document=%s" % saved_file, "--timeout=15", "--tries=3", url ]
            out = Popen( args, stdin=PIPE, stdout=PIPE )
            stdout, stderr = out.communicate()
            size = os.path.getsize( saved_file )
            ftype =  magic.from_file( saved_file )

            if size == 0:
                raise Exception( "File is empty!" )
            if extension == ".jpg" and "JPEG image data" not in ftype:
                raise Exception( "File should be JPEG, but is not!" )
            if "HTML" in magic.from_file( saved_file ):
                raise Exception( "Not an image file." )
            if stderr is not None and "-1 / unknown" in stderr:
                raise Exception( "Something went wrong." )
        except Exception as e:
            logfd.write( line )
            logfd.flush()
            if os.path.isfile( saved_file ):
                print( "%s Deleting %s" % ( e, saved_file ) )
                os.remove( saved_file )
logfd.close()

