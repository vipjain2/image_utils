#!/usr/bin/env python3

import xmltodict
import urllib
import os
from subprocess import Popen, PIPE
import requests
import sys
import magic

logfile = "./log.txt"

logfd = open( logfile, "a" )
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
            cmd = [ "wget", \
                    "--output-document=%s" % saved_file, \
                    "--timeout=6", \
                    "--tries=1", \
                    "-q", \
                    url ]

            print( url )
            out = Popen( cmd, stdin=PIPE, stdout=PIPE )
            stdout, stderr = out.communicate()

            if os.path.isfile( saved_file ):
                size = os.path.getsize( saved_file )
                mime_type =  magic.from_file( saved_file )

            if size == 0:
                raise Exception( "File is empty!" )
            if ( extension == ".jpg" or extension == ".jpeg" ) and "JPEG image data" not in mime_type:
                raise Exception( "File should be JPEG, but is not!" )
            if extension == ".png" and "PNG image data" not in mime_type:
                raise Exception( "File should be PNG, but is not!" )
            if "HTML" in mime_type:
                raise Exception( "Not an image file." )
            if stderr is not None and "-1 / unknown" in stderr:
                raise Exception( "Something went wrong." )
        except KeyboardInterrupt:
            print( "Breaking." )
            break
        except Exception as e:
            logfd.write( line )
            logfd.flush()
            if os.path.isfile( saved_file ):
                print( "%s Deleting %s\n" % ( e, saved_file ) )
                os.remove( saved_file )
        else:
            print( "Saving: %s\n" % saved_file )
logfd.close()

