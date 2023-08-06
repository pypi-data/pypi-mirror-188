
#####################################################################
#
# s_util.py
#
# Project   : SAPIADAPTER
# Author(s) : Zafar Iqbal < zaf@sparc.space >
# Copyright : (C) 2023 SPARC PC < https://sparc.space/ >
#
# All rights reserved. No warranty, explicit or implicit, provided.
# SPARC PC is and remains the owner of all titles, rights
# and interests in the Software.
#
#####################################################################

import os
import sys
import time
import json
import pickle
import uuid
import hashlib
import base64
import shutil
import gzip
import inspect
import glob
import traceback
import random
import sqlite3
import copy

import atexit

import threading

from datetime import datetime , timedelta , timezone

import datetime as _dt

from subprocess import Popen, PIPE

from pathlib import Path
from traceback import format_exception

import urllib.parse

from . import get_version , s_log , s_config , s_net , s_db

#####################################################################


#class JsonEncoder( json.JSONEncoder ) :
#    def default( self , z ) :
#        if isinstance( z , datetime.date ) :
#            return ( str( z ) )
#        else :
#            return super( ).default( z )


#class CustomJSONEncoder(json.JSONEncoder):
#    def default(self, obj):
#        if isinstance(obj, datetime):
#            return obj.isoformat()
#        if isinstance(obj, np.ndarray):
#           return obj.tolist()
#        if isinstance(obj, OrderedDict):
#           return "{" + ",".join([self.encode(k) + ":" + self.encode(v) for (k, v) in obj.iteritems()]) + "}"
#        return json.JSONEncoder.default(self, obj)

class JsonEncoder( json.JSONEncoder ) :

    def default( self , obj ) :
        #if isinstance( obj , numpy.integer ) :
        #    return int( obj )
        #elif isinstance( obj, numpy.floating ) :
        #    return float( obj)
        #elif isinstance( obj, numpy.ndarray ) :
        #    return obj.tolist( )
        #if isinstance( obj , datetime.datetime ) :
        #    return ( str( obj ) )
        if isinstance( obj , _dt.date ) :
            return str( obj ) 
        return json.JSONEncoder.default( self , obj )

def json_encode( data ) :
    return json.dumps( data , cls = JsonEncoder )

def json_save( fn , data ) :

    #with open( fn , 'w', encoding='utf-8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)

    with open( fn , "w" ) as file :
        file.write( json_encode( data ) )

def json_load( fn ) :
    with open( fn ) as f :
        j = json.load( f )
    return( j )

def json_loads( str ) :
    return( json.loads( str ) )

def json_stdin( ) :

    data_in_list = sys.stdin.readlines( )
    data_in_json = "".join( data_in_list )

    data_in = json_loads( data_in_json )

    return( data_in )

def json_dumps( inputs ) :
    return( json.dumps( inputs , cls = JsonEncoder ) )

#def json_pretty( json_in ) :
#    data = json.loads(json_in)
#    pretty_object = json.dumps(data, indent=4)
#    print(pretty_object)

def json_prettyprint( data ) :
    pretty_object = json.dumps( data , indent = 4 ,  cls = JsonEncoder )
    print( pretty_object )

#####################################################################


def sdb_init( db_fp ) :
    if not os.path.exists( db_fp ) :

        db_con = sqlite3.connect( db_fp )

        if( db_con.total_changes != 0 ) :
            print( "ERROR db_con.total_changes ! 0 " )
            time.sleep( 10 )
            sys.exit( )

        db_cur = db_con.cursor( )
        db_cur.execute( "pragma journal_mode=wal" )

        db_con.commit( )
        db_con.close( )
        return(False)
    return(True)

def sdb_execute( db_fp , sql , params_tuple = False ) :

    db_con = sqlite3.connect( db_fp , isolation_level = None )
    db_cur = db_con.cursor( )
    db_cur.execute( "pragma synchronous=NORMAL" )
    if params_tuple == False :
        db_cur.execute( sql )
    else :
        db_cur.execute( sql , params_tuple )
    db_con.commit( )
    db_con.close( )

def sdb_execute_fetch( db_fp , sql , fetch_all = False , params_tuple=False) :

    #s_log.write( sql )

    dbcon = sqlite3.connect( db_fp , isolation_level = None  )
    dbcon.row_factory = lambda C , R : { c[ 0 ] : R[ i ] for i , c in enumerate( C.description ) }
    db_cur = dbcon.cursor( )
    db_cur.execute( "pragma synchronous=NORMAL" )

    if params_tuple == False :
        db_cur.execute( sql )
    else :
        db_cur.execute( sql , params_tuple )

    #db_cur.execute( sql )

    if fetch_all : 
        rows = db_cur.fetchall( )
        dbcon.close( )
        return( rows )
    else :
        row = db_cur.fetchone( )
        dbcon.close( )
        if( not row ) : return( False )
        return( row )


#####################################################################

def copy_deep( x ) :
    return( copy.deepcopy( x ) )

#####################################################################

def is_number(n):
    is_number = True
    try:
        num = float(n)
        is_number = num == num   
    except ValueError:
        is_number = False
    return is_number

def atexit_register( f ) :
    atexit.register( f )

def get_chunks(l, n):
    """Yield n number of striped chunks from l."""
    for i in range(0, n):
        yield l[i::n]

# Can be array
def rnd_choice( i = "-|/\\"  ) :
    return( random.choice( i ) )

def get_ver( ) :
    return( get_version( ) )

def num_randomlist( s = 10 ) :
    random_list = [ random.random( ) for i in range( s ) ]
    return( random_list )

def rnd_binary( s = 1024 ) :
    return( os.urandom( s ) )

# Get arg from position and use default
def argv_get( p , d = None ) :
    al = len( sys.argv ) - 1
    #print( al )
    if( p > al ) : return( d )
    return( sys.argv[ p ] )

# FIXME TODO aaarrggghhh!!!
def time_getisoformat( ) :

    dt = datetime.now( datetime.now( ).astimezone( ).tzinfo ).isoformat( )

    return( dt )

#>>> now = datetime.now()
#>>> now
#datetime.datetime(2010, 11, 29, 11, 55, 27, 172480)
#>>> now.tzname()
#>>> from dateutil import tz
#>>> now = datetime.now(tz=tz.tzlocal())
#>>> now
#datetime.datetime(2010, 11, 29, 11, 56, 21, 316679, tzinfo=tzlocal())
#>>> now.tzname()

def pickle_load( datakey , fromtmp = False ) :

    fn = "local_" + datakey + ".pkl"

    if(fromtmp):
        fn="/tmp/"+fn

    if( os.path.isfile( fn ) ) :
        with open( fn , "rb" ) as f :
            return( pickle.load( f ) )
    else :
        return None
        
def pickle_save( datakey , data , mvtotmp = False ) :
    fn = "local_" + datakey + ".pkl"
    f = open( fn , "wb" )
    pickle.dump( data , f )
    f.close( )

    if( mvtotmp ) :
        os.rename( fn , "/tmp/" + fn )

def get_cwd( ) :
    directory_path = os.getcwd()
    return(directory_path)

 
def pathnotallowed( p ) :

    #s_log.write( p )

    p1 = os.path.normpath(p)
    #s_log.write( p1 )

    p2 = os.path.realpath(p1)
    #s_log.write( p2 )

    base_dir = s_config.get_key( "/config/cwd" , "/tmp")

    path_test = ( Path( base_dir ) / p2 ).resolve( ) 

    s_log.write(str(Path(base_dir).resolve()))
    s_log.write(str(path_test.parent))

    if( str( path_test.parent ).startswith( base_dir ) ) :
        return( False )

    s_log.write("pathnotallowed "+p)
    s_log.write(str(Path(base_dir).resolve()))
    s_log.write(str(path_test.parent))

    return( True )



def get_hashkeycontentdir( ) :
    # FIXME TODO should be coming from config
    fd = "/tmp/sapiadapter/sessions/"

    # FIXME TODO have this as a convenience function
    if environ_isdockerrunning( ) and dir_exists( "/data/" ) :
        fd = "/data/sessions/"

    return( fd )

def save_hashkeycontent( fk , fc ) :
    
    fd = get_hashkeycontentdir( )

    path_mkdirs( fd )

    hk = fk + s_config.get_key( "endpoint/token" )

    fp = fd + hash( hk ) + ".session"

    with open( fp , "w" ) as file :
        file.write( fc )

def load_hashkeycontent( fk ) :
    
    fd = get_hashkeycontentdir( )

    fp = fd + hash( fk ) + ".session"

    if( file_exists( fp ) ) :
        return( file_read( fp ) )
    return( False )



def uhash( prefix = "" ) :
    return( prefix + hashlib.sha256( str( uuid.uuid4( ) ).encode( "utf-8" )  ).hexdigest( ) )

# FIXME TODO bytes coming in ?!?!?
def hash( str , prefix = "" ) :
    return( prefix + hashlib.sha256( str.encode( "utf-8" ) ).hexdigest( ) )

def hash_file_md5( fp ) :
    return( hashlib.md5( open( fp , "rb" ).read( ) ).hexdigest( ) )

# FIXME TODO add encode...??? especially images...
def base64_decode( str ) :
    m = base64.b64decode( str ).decode( "utf-8" )
    return( m )


def is_ip( address ) :
    if( not address ) : return( False )
    return( not address.split( "." )[ -1 ].isalpha( ) )
    

def uptime( ) :
    return( time.time( ) - s_config.get_key( "/config/init/time" ) )


def uptime_lap( ) :

    tn = time.time( )

    tlp = s_config.get_key( "/config/init/time_lap" )  

    tl = tn - tlp 

    s_config.set_key( "/config/init/time_lap" , tn )

    return( tl )


def printexit( msg ) :
    print( "PREXIT: " + str(msg) )
    sys.exit( )


def LEGACYprintexception( e = False ) :
    if e :
        print( "EXCEPTION" + str( e ) )
    etype , value, tb = sys.exc_info( )
    info , error = format_exception( etype , value , tb )[ -2: ]
    print( f'Exception in:\n{info}\n{error}' )
    print( full_stack( ) )

def full_stack():
    exc = sys.exc_info()[0]
    if exc is not None:
        f = sys.exc_info()[-1].tb_frame.f_back
        stack = traceback.extract_stack(f)
    else:
        stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if exc is not None:
        # FIXME TODO WARNING this removes "chars"!
        stackstr += '  ' + traceback.format_exc().lstrip(trc)
    return stackstr


def print_exception():
    etype, value, tb = sys.exc_info()
    info, error = format_exception(etype, value, tb)[-2:]
    print(f'Exception in:\n{info}\n{error}')



heartbeat_last = 0
def heartbeat( t = 600 ) :
    global heartbeat_last
    time.sleep( 0.01 )
    if( uptime( ) - heartbeat_last ) < t : return( False )
    s_log.write( "@" )
    heartbeat_last = uptime( )
    return( True )


def resetup_ifconfigchanged( ) :
    config = s_config.get_config( )
    if "/config/init/path_time" in config :
        cd = config[ "/config/cwd" ]
        cip = config[ "/config/init/path" ]
        cipt = config[ "/config/init/path_time" ]

        cfp = cip
        if not os.path.isabs( cip ) :
            cfp = cd + "/" + cip

        if os.path.isfile( cfp ) :

            cipt2 = os.path.getmtime( cfp )
            if( os.path.getmtime( cfp ) != cipt ) :
                s_config.setup( )
                s_db.setup( )
                s_log.write( "resetup_ifconfigchanged True" )
                #s_log.write( "CONFIG RELOADED " + cfp + str( cipt ) )


def ready( ) :

    resetup_ifconfigchanged( )

    if( not s_config.isready( ) ) :
        return( False )

    if( not s_net.check_connectivity( ) ) :
        return( False )

    return( True )



####################################################################

def gen_workingdirectory( ) :
    work_dir = wd = s_config.get_key( "sys/workspacedir" ) + "/" + uhash( "WOK" )
    return( work_dir )

####################################################################

def proc_setup( ) :

    app_dir = "/data/app"

    if( not os.path.isdir( app_dir ) ) :
        s_log.write( "app_dir " + app_dir + " does not exist!")
        return( False )


    work_dir = gen_workingdirectory( )

    # FIXME TODO should be coming from config
    shutil.copytree( app_dir , work_dir , ignore = shutil.ignore_patterns( ".git*" ) )

    os.chdir( work_dir )
    #print(os.getcwd())

    s_config.set_key( "sys/work_dir" , work_dir ) 

    # BEFORE WE ADD DEFAULT INPUT/OUTPUT FILE!!!
    proc_trackcurrentfiles( )

    ################
    #default_inputs =  s_db.meta_getdefault( )
    #s_db.files_set_defaultdata( default_inputs )
    s_db.files_defmeta_write( )
    ################

    #s_db.setup( ) 

    return( True )

def proc_trackcurrentfiles( ) :

    procfiles = { }
    for dirpath , dirs, files in os.walk( "." ) :  
        for filename in files :
            fname = os.path.join( dirpath , filename )
            #fname=os.path.abspath(fname)
            #print(fname)
            procfiles[ fname ] = True
            #if( not s_db.files_create( fname ) ) :
            #    s_log.write( "ERROR files_create " + fname )
            #with open(fname) as myfile:
            #print(myfile.read())

    s_config.set_key( "sys/procfiles" , procfiles ) 

def proc_run( ) :

    if not os.path.isfile( "_sapi.py" ) :
        s_log.write( "False isfile _sapi.py" )
        return( False )

    return( True )

def proc_storage( ) :

    procfiles = s_config.get_key( "sys/procfiles" ) 

    for dirpath , dirs, files in os.walk( "." ) :  
        for filename in files :
            fname = os.path.join( dirpath , filename )
            #fname=os.path.abspath(fname)
            #print(fname)
            if fname in procfiles : continue
            #print(fname)


            file_extension = Path( fname ).suffix

            # FIXME TODO extensions (list of) should be coming from config
            # anything starting with ".*"
            if( file_extension == ".pyc" ) : continue

            #s_log.write(fname)

            if( not s_db.files_update( fname ) ) :
                s_log.write( "ERROR files_update " + fname )
            #with open(fname) as myfile:
            #print(myfile.read())

def proc_teardown( ) :
    # FIXME TODO check a config/token flag to decide if to keep/delete work dir 
    shutil.rmtree( s_config.get_key( "sys/work_dir" )  )

    os.chdir( s_config.get_key( "/config/cwd" ) )

####################################################################

def compress( d ) :
    blob = gzip.compress( d )
    return( blob )

def decompress( d ) :
    blob = gzip.decompress( d )
    return( blob )

####################################################################

def parent_path( ) :

    # FIXME TODO this copy pasta should be cleaned up

    trc=None

    for teil in inspect.stack():
        # skip system calls
        if teil[1].startswith("<"):
            continue
        if teil[1].upper().startswith(sys.exec_prefix.upper()):
            continue
        trc = teil[1]
        
    # trc contains highest level calling script name
    # check if we have been compiled
    if getattr(sys, 'frozen', False):
        scriptdir, scriptname = os.path.split(sys.executable)
        return {"dir": scriptdir,
                "name": scriptname,
                "source": trc}


    if(trc==None):
        return(os.getcwd())

    # from here on, we are in the interpreted case
    scriptdir, trc = os.path.split(trc)
    # if trc did not contain directory information,
    # the current working directory is what we need
    if not scriptdir:
        scriptdir = os.getcwd()

    scr_dict ={"name": trc,
               "source": trc,
               "dir": scriptdir}

    #s_log.write(scr_dict)

    return scr_dict["dir"]

################

def environ_isdockerrunning( ) :
    return( "DOCKER_RUNNING" in os.environ )


def environ_getall( ) :
    return( dict( os.environ ) )

def environ_get( k ) :
    if k in os.environ :
        return( os.environ[ k ] )
    return( None )

def environ_set( k , v ) :
    os.environ[ k ] = v

def container_appenvstatic_get( ) :
    ENV_STATIC = { }
    if "_CONTAINER_LOCAL_APPENVSTATIC" in os.environ :
        ENV_STATIC = dict( urllib.parse.parse_qsl( os.environ[ "_CONTAINER_LOCAL_APPENVSTATIC" ] ) )
    return( ENV_STATIC )
  

def display_time( seconds , granularity = 2 ) :

    intervals = (
        ( 'weeks' , 604800 ) , 
        ( 'days' , 86400 ) ,  
        ( 'hours' , 3600 ) , 
        ( 'minutes' , 60 ) ,
        ( 'seconds' , 1 ) ,
    )

    result = [ ]

    for name, count in intervals :
        value = seconds // count
        if value :
            seconds -= value * count
            if value == 1 :
                name = name.rstrip( 's' )
            result.append( "{} {}".format( value , name ) )
    return ', '.join( result[ :granularity ] )


def datetimestr_to_unixtime( dt_str ) :
    if(dt_str.endswith("Z")):
        dt_str=dt_str[:-1]

    if(len(dt_str)==19):
        dt_str=dt_str+"+00:00"

    parsedDate = datetime.fromisoformat(dt_str)
    return( int( parsedDate.timestamp( ) ) )


def datetime_strtotimestampms( dtstr ) :
    return( datetime.strptime( dtstr , "%Y-%m-%dT%H:%M:%S" ).replace(tzinfo=timezone.utc).timestamp()*1000 )



def datetime_istype( v ) :
    return( type( v ) == datetime ) 


def datetime_utcfromtimestamp( ts ) :
    return( datetime.utcfromtimestamp( ts ).isoformat( ) )

def datetime_isofromtimestamp( ts ) :
    return(datetime.utcfromtimestamp( ts ).strftime( "%Y-%m-%dT%H:%M:%S" ))

def datetime_isofromtimestampms( ts ) :
    return(datetime.utcfromtimestamp( ts / 1000 ).strftime( "%Y-%m-%dT%H:%M:%S" ))

def datetime_iso( ) :
    return( datetime.now( datetime.now( ).astimezone( ).tzinfo ).isoformat( ) )



def time_now( ) :
    return( time.time( ) )

def time_nowms( ) :
    return( int( time.time( ) * 1000 ) )

def time_now_str( ) :
    return( str( round( time_now( ) ) ) )

def time_hexepoch_str( ) :
    return( hex( round( time_now( ) - 1666275269 ) )[ 2: ] )

def datetime_utcnow( ) :
    return( datetime.utcnow( ) )


def datetime_timestamp( ) :
    return( datetime.now( ).timestamp( ) )

def datetime_utctimestamp( ) :
    return( datetime.utcnow( ).timestamp( ) )

def url_parse( u ) :
    return( urllib.parse.urlparse( u ) )


def sleep( t = 1 ) :
    time.sleep( t ) 

def idle( ) :
    while True:
        s_log.write( "IDLE" )
        time.sleep( 86400 )

def datetime_add_timedelta( dt , sec ) :
    return( dt + timedelta( seconds = sec ) )

def datetime_nowutcstr( td = 0 ) :

    #d = datetime.now( timezone.utc) + timedelta( seconds = td )
    d = datetime.utcnow( ) + timedelta( seconds = td )
    return( d.strftime( "%Y-%m-%dT%H:%M:%S" ) )


def datetime_filestamp( td = 0 ) :

    d = datetime.utcnow( ) + timedelta( seconds = td)

    return( d.strftime( "%Y%m%d%H%M%S" ) )

def datetime_now_db( td = 0 ) :

    d = datetime.now( ) + timedelta( seconds = td)

    return( d.strftime( "%Y-%m-%dT%H:%M:%S" ) )

def datetime_timedelta_db( dbdtstr , td ) :
    d = datetime.strptime( dbdtstr , "%Y-%m-%dT%H:%M:%S" ) + timedelta( seconds = td )
    return( d.strftime( "%Y-%m-%dT%H:%M:%S" ) )

def datetime_inrange_db( dbdt1 , dbdt2 , td) :
    d1 = datetime.strptime( dbdt1 , '%Y-%m-%dT%H:%M:%S' )  
    d2 = datetime.strptime( dbdt2 , '%Y-%m-%dT%H:%M:%S' ) 

    dtdiff = d2 - d1
    dtdiff_seconds = int( dtdiff.total_seconds( ) )
    return( dtdiff_seconds <= td )

def datetime_diff( dt1 , dt2 ) :
        d1 = datetime.strptime( dt1 , "%Y-%m-%dT%H:%M:%S" )  
        d2 = datetime.strptime( dt2 , "%Y-%m-%dT%H:%M:%S" ) 
        dtdiff = d1 - d2 
        dt = int( dtdiff.total_seconds( ) )
        return( dt )


def datetime_diffnow( dt2 ) :
    dt1 = datetime_now_db( ) 
    return( datetime_diff( dt1 , dt2 ) )



def datetime_centerwindow( p , ec , ew ):
    a = datetime_timedelta_db( p[ ec ] , -0.5 * p[ ew ] )
    b = datetime_timedelta_db( p[ ec ] , 0.5 * p[ ew ] )
    return( [ a , b ] )


def datetime_initstartend( p , es , ee , ew ) :
    if( ( not es in p) and ( not ee in p ) ) :
        a = datetime_now_db( -1 * p[ ew ] )
        b = datetime_now_db( )
        return( [ a , b ] )
    elif( not ee in p) :
        b = datetime_timedelta_db( p[ es ] , p[ ew ] )
        return([p[es],b])
    elif( not es in p) :
        a = datetime_timedelta_db( p[ ee ] , -1 * p[ ew ] )
        return([a,p[ee]])
        
    return([p[es],p[ee]])
 


################


def path_ext( fp ) :

    file_extension = Path( fp ).suffix
    return( file_extension)

def path_mkdirs( dp ) :

    path = Path( dp )
    path.mkdir( parents = True , exist_ok = True )


def path_dirname( dp ) :
    return( os.path.dirname( dp ) )


def dir_exists( dp ) :
    if( not os.path.isdir( dp ) ) :
        return( False )
    return( True )

def dir_chdir( dp ) :
    os.chdir( dp )

def dir_make( dp ) :
    os.makedirs( dp , exist_ok = True )
# Return file getcontents given filename and parent script __FILE__
def file_getcontent( fn , scp ) :

    fd = os.path.dirname( os.path.realpath( scp ) )

    #s_log.write(fn +","+scp)

    with open( fd + "/" + fn , mode = "rb" ) as tfile : 
        contents = tfile.read( ).decode( )

    return( contents )


def file_readlines( fp ) :
    return( open( fp , "r" ).read( ).splitlines( ) )

def file_read( fp ) :
    return( open( fp , "r" ).read( ) )

def file_exists( fp ) :
    return( os.path.isfile( fp ) )


def prexit_fileexists( fp , pred = True ) :
    if file_exists( fp ) == pred :
        printexit( fp + " prexit_fileexists and PRED!")


def file_ctime( fp ) :
    if(not file_exists(fp)): return(False)
    return( os.path.getctime( fp ) )

def file_changed( fp , ctime ) :
    if(not file_exists(fp)): return(False)
    return( file_ctime(fp)!=ctime)

def file_rm( fp ) :
    if( not file_exists( fp ) ) : return( False )
    os.remove( fp )
    return( True )


def file_copy( fps , fpt ) :
    shutil.copyfile(fps,fpt)

def path_stem( p ) :
    fn = Path( p ).stem
    return( fn )


def sys_path_append_fp( fp ) :
    if( not file_exists(fp)): return(False)
    sys.path.append( os.path.dirname( fp ) )
    return(True)

def file_stat( fp ) :
    return( os.stat( fp ) )


def file_stat_dict(fp: str) -> dict:
    s_obj = os.stat(fp)
    return {k: getattr(s_obj, k) for k in dir(s_obj) if k.startswith('st_')}


def file_size( fp ) :
    return( os.path.getsize( fp ) )

def file_settimes( fp , t ) :
    os.utime( fp , ( t , t ) )


def file_replace( fp_source , fp_target ):
    os.replace( fp_source , fp_target )

def file_tmprandom(  ) :
    fp = "/tmp/sapitmp_" + uhash( ) + ".tmp"
    data = num_randomlist( 10000 )
    with open( fp, "w" ) as f :
        f.write( json_encode( data ) )
    return( fp )


def file_youngerthan( fp , ts ) :
    fstat = file_stat( fp )
    return( fstat.st_mtime > ts )


def dir_scan( dp ) :

    fps = [ ]
    
    if not dir_exists( dp ) :
        s_log.write("files_scan dir does not exist!")
        return( fps )

    for root , dirs , files in os.walk( dp ) :
        for f in files :
            fps.append( os.path.join( root , f ) )

    return( fps )


def matched_substring( haystack , needles ) :

    if( not needles ) : return( True )

    for needle in needles :
        if( needle in haystack ) :
            return( True )

    return( False )

################

def thread_get_id( ) :
    return( threading.get_ident( ) ) 
   
 
##################


def glob_files( dp , recursive=False ) :
    return( glob.glob( dp , recursive=recursive) )


def match_listindict( l , d ) :
    res = [ ]
    for dk in l :
        if dk in d :
            res.append( dk )

    return( list( dict.fromkeys( res ) ) )   


def math_dictkeylimit( d , k , l ) :
    if( not k in d ) :
        return( l )
    elif ( int( d[ k ] ) > l ) :
        return( l )
    return(d[k])

def dicts_merge( x , y ) :
    z = x.copy( )
    z.update( y )
    return( z )

def decode_redis(src):
    if isinstance(src, list):
        rv = list()
        for key in src:
            rv.append(decode_redis(key))
        return rv
    elif isinstance(src, dict):
        rv = dict()
        for key in src:
            rv[key.decode()] = decode_redis(src[key])
        return rv
    elif isinstance(src, bytes):
        return src.decode()
    else:
        raise Exception("type not handled: " +type(src))
