
#####################################################################
#
# s_net.py
#
# Project   : SAPIADAPTER
# Author(s) : Zafar Iqbal < zaf@sparc.space >
# Copyright : (C) 2022 SPARC PC < https://sparc.space/ >
#
# All rights reserved. No warranty, explicit or implicit, provided.
# SPARC PC is and remains the owner of all titles, rights
# and interests in the Software.
#
#####################################################################

import time
import json
import requests
import gzip
import socket
import urllib3

urllib3.disable_warnings( urllib3.exceptions.InsecureRequestWarning )

#from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout 

from . import s_log , s_config , s_util , s_db

session = requests.Session( )

#####################################################################

check_connectivity_done = False

# FIXME TODO - when _CONTAINER_LOCAL_CONFIGENDPOINTKEY=_sapiserver_LOCAL_CONFIGENDPOINTKEY_
#  File "/usr/local/lib/python3.8/dist-packages/sapiadapter/s_net.py", line 96, in check_connectivity
#    s_log.write( endpoint_parseurl.hostname + "," + str( endpoint_url_port ) + "," + endpoint_host )
#TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'
#EXCEPTION job_get


def check_connectivity( ) :

    global check_connectivity_done

    if( check_connectivity_done ) : return( True )

    ################################################################

    flag_networkok = True

    ################################################################

    endpoint_url =  s_config.get_key( "endpoint/url" )
    if( not endpoint_url ):
        s_log.write( "False endpoint_url" )
        return( False )

    endpoint_parseurl = urllib3.util.parse_url( endpoint_url )

    if( endpoint_parseurl.scheme == None ) :
        s_log.write( "False endpoint_url scheme " + endpoint_url )
        return( False )

    ################################################################

    if( s_util.is_ip( endpoint_parseurl.hostname ) ) :
        s_config.set_key_alt( "endpoint/sslverify" , "no" )
    
    ################################################################

    endpoint_url_port = endpoint_parseurl.port
    if( endpoint_url_port == None ) :
        endpoint_url_port = 443

    ################################################################

    #if( s_config.get_key( "endpoint/skipnetworkcheck1" ) != "yes" ) : 

    #    try :

    #        host = socket.gethostbyname( endpoint_parseurl.hostname ) 
    #        s = socket.create_connection( ( host , endpoint_url_port ) , 10 )
    #        s.close( )

    #    except Exception as e :
    #        s_log.write( "False check_connectivity 1" )
    #        flag_networkok = False

    ################################################################

    s_config.set_key_alt( "endpoint/timeout" , 10 ) ;

    if( flag_networkok and get_request_response( { "X-Omni-Action": "check_connectivity" } ) == False ) :
        s_log.write( "False check_connectivity 2" )
        flag_networkok = False

    s_config.del_key_alt( "endpoint/timeout" ) ;

    ################################################################

    check_connectivity_done = flag_networkok

    if flag_networkok :
        return( True )

    endpoint_host =  s_config.get_key( "endpoint/host" , "HOST_NOT_SET")
    s_log.write( endpoint_parseurl.hostname + "," + str( endpoint_url_port ) + "," + endpoint_host )

    if( ( endpoint_url_port != 443 ) and ( endpoint_url_port != 10443 ) ) :
        s_log.write( "maybe endpoint_url_port smells fishy..." )

    return( False )

#####################################################################

def job_rping( jid_in = False ) :

    if( jid_in == False ) :
        s_log.write( "jid_in??" )
        return( False )



    headers =   {
                    "X-Omni-Action": "job_rping" ,
                    "X-Omni-Jid": jid_in ,
                }


    res = get_request_response( headers )

    if( res == False ) :
        s_log.write( "res??" )
        return( False )

    #s_log.write( str( res.headers ) )

    if( "X-Omni-Data" in res.headers ) :
        data=s_util.json_loads(res.headers["X-Omni-Data"])
        return( data)


    return( False )

#####################################################################



def job_request( params = { } ) :

    #if( not s_util.ready( ) ) :
    #    s_log.write( "NOT READY" )
    #    return( False )

    #####################################################################

    if s_db.fsize_limited( ) :
        s_log.write( "ERROR fsize_limited" )
        return( False )

    #####################################################################

    payload = s_db.blob_get( )

    #payload_len = len( payload )
    #if( payload_len > 0 ) : s_log.write( "PAYLOAD REQUEST " + str( payload_len ) )

    #####################################################################

    headers = { "X-Omni-Action": "job_request" }
    headers[ "X-Omni-Params" ] = s_util.json_encode( params )
    if( len( headers[ "X-Omni-Params" ] ) > 4096 ) :
        s_log.write( "ERROR Params TO BIG?? > 4096 bytes... " + str( len( headers[ "X-Omni-Params" ] ) ) )
        return( False )


    header_extra = s_config.get_key( "_header_extra" )
    if( header_extra ) :
        s_log.write( "FOUND _header_extra" )
        headers[ "X-Omni-Extra" ] = s_util.json_encode( header_extra )


    #s_log.write( headers )

    res = get_request_response( headers , payload )

    if( res == False ) :
        s_log.write( "res??" )
        return( False )

    #s_log.write( str( res.headers ))

    #####################################################################

    if( not "X-Omni-Jid" in res.headers ) :
        s_log.write( "Not found X-Omni-Jid" )
        return( False )

    if( len( res.headers[ "X-Omni-Jid" ] ) != 67 ) :
        s_log.write( "X-Omni-Jid!=67" )
        return( False )

    #####################################################################

    #s_log.write(str(res.headers))

    jid = res.headers[ "X-Omni-Jid" ]

    s_log.write( "job_request [" + jid + "]" )

    s_config.set_key( "jid" , jid )

    #s_db.meta_jid_create( jid )

    return( True )


def job_responsewait( jid , timeout = 60 ) :

    #if( not s_util.ready( ) ) :
    #    s_log.write( "NOT READY" )
    #    return( False )
        
    #####################################################################

    s_log.write( "job_wait " + str( timeout ) )
    
    time_start = time.time( )

    while True :
        jr = job_response( jid )
        if( jr == False ) : return( False )
        if( jr == True ) : return( True )
        if( time.time( ) - time_start ) > timeout : return( None )
        time.sleep( 1 )

def job_response( jid ) :

    #if( not s_util.ready( ) ) :
    #    s_log.write( "NOT READY" )
    #    return( False )
        
    #####################################################################

    headers =   {
                    "X-Omni-Action" : "job_response" ,
                    "X-Omni-Jid" : jid ,
                }

    res = get_request_response( headers )

    #####################################################################

    if( res == False ) :
        s_log.write( "res??" )
        return( False )

    #s_log.write( str(res.headers ) )

    if( not "X-Omni-State" in res.headers ) :
        s_log.write( "Not found X-Omni-State" )
        return( False )

    # FIXME TODO we must have this before AND after the DB SET
    s_db.meta_create( "_job_state" , res.headers[ "X-Omni-State" ] ) 

    if( res.headers[ "X-Omni-State" ].startswith( "error_" ) ) :
        # FIXME TODO should add more info here...
        s_log.write( "job_response STATE ERROR [" + jid + "]" )
        return( True )

    if( res.headers[ "X-Omni-State" ].startswith( "cancel" ) ) :
        # FIXME TODO should add more info here...
        s_log.write( "job_response CANCEL..LED [" + jid + "]" )
        return( True )

    if( res.headers[ "X-Omni-State" ] != "done" ) :
        s_log.write( "job_response !=Done [" + jid + "]" )
        return( None )

    if( len( res.content ) == 0) : 
        s_log.write( "ERROR EMPTY RES CONTENT" )
        return( False )

    #payload_len=len( res.content )
    #if(payload_len>0) : s_log.write( "PAYLOAD RESPONSE "+str(payload_len))
    
    s_db.blob_set( res.content )

    # FIXME TODO we must have this before AND after the DB SET
    s_db.meta_create( "_job_state" , res.headers[ "X-Omni-State" ] ) 

    return( True )

####################################################################

def job_get( queues_list = False ) :

    #if( not s_util.ready( ) ) :
    #    s_log.write( "NOT READY" )
    #    return( False )


    headers =   {
                    "X-Omni-Action": "job_get" ,
                }

    if(queues_list==False):
        env_queue=s_util.environ_get("_CONTAINER_LOCAL_APPQUEUE") ;
        if(env_queue):
            if not env_queue.endswith( "_LOCAL_APPQUEUE_" ) : 
                #s_log.write("FOUND _CONTAINER_LOCAL_APPQUEUE "+env_queue)
                headers["X-Omni-Queue"]=env_queue
        #else:
        #    s_log.write( "NOT FOUND _CONTAINER_LOCAL_APPQUEUE" )
    else:
        headers[ "X-Omni-Queue" ] = "," . join( queues_list )



    #####################################################################


    #s_log.write( headers )

    res = get_request_response( headers )

    if( res == False ) :
        s_log.write( "ERROR False res??" )
        return( False )

    #s_log.write( str(res.headers ) )

    if( not "X-Omni-Jid" in res.headers ) :
        #s_log.write( "Not found X-Omni-Jid" )
        return( None )

    payload = gzip.decompress( res.content )
    #s_log.write( payload )

    s_db.rewrite( payload )

    if( "X-Omni-Context" in res.headers ) :
        #s_log.write( "Found X-Omni-Context" )
        #s_log.write( res.headers[ "X-Omni-Context" ] )
        #s_log.write( "FIXME TODO context json to meta add" )
#        context_json = base64.b64decode( res.headers[ "X-Omni-Context" ] ).decode( "utf-8" )
        context_json = s_util.base64_decode( res.headers[ "X-Omni-Context" ] )
        context=json.loads(context_json)
        #s_db.meta_create( "_context" , context_json ) 
        s_config.set_key( "header_context" , context ) 

    job_id = res.headers[ "X-Omni-Jid" ]
    s_config.set_key( "jid" , job_id ) 
    s_log.write( "job_get [" + job_id + "]" )

    return( True )

def job_set( jid_in = False ) :

    #if( not s_util.ready( ) ) :
    #    s_log.write( "NOT READY" )
    #    return( False )

    #####################################################################

    if(jid_in!=False):
        jid = jid_in
    else:
        jid = s_config.get_key("jid")
    #s_db.meta_checkupdefault( )

    s_db.sys_rev_inc( )

    db_filecontents = s_db.file_contents( )

    payload = gzip.compress( db_filecontents  )
    #payload_size = len( payload )
    #s_log.write("YYY "+str(payload_size))

    #####################################################################

    headers =   {
                    "X-Omni-Action": "job_set" ,
                    "X-Omni-Jid": jid ,
                }

    #s_log.write( headers )

    res = get_request_response( headers , payload )

    #####################################################################

    if( res == False ) :
        # Remember res is false!
        s_log.write( "ERROR res??" )
        return( False )

    #s_log.write( str(res.headers ) )

    #s_log.write( "job_set [" + jid + "]" )

    return( True )

#####################################################################

def get_request_response( request_headers = { }  , payload = "" ) :

    time.sleep( 0.1 )

    if not "User-Agent" in request_headers :
        request_headers[ "User-Agent" ] = "sapiadapter"
    if not "X-Omni-Authorization" in request_headers :
        token=s_config.get_key( "endpoint/token" )
        if( token != False ) :
            request_headers[ "X-Omni-Authorization" ] = s_config.get_key( "endpoint/token" ) 

    endpoint_host = s_config.get_key( "endpoint/host" )
    if endpoint_host != None and endpoint_host != "" :
        request_headers[ "Host" ] = endpoint_host

    ################################################################ 

    token_session = s_config.get_key( "token_session" )
    if( token_session != None ) :
        # FIXME TODO why strip?
        request_headers[ "X-Omni-TokenSession" ] = token_session.strip( )

    request_headers[ "X-Omni-Traceid" ] = s_log.get_traceid( )   

    ################################################################ 

    endpoint_sslverify = s_config.get_key( "endpoint/sslverify" )

    if endpoint_sslverify == None :

        endpoint_sslverify = True
    else :        
        if endpoint_sslverify == "yes" :
            endpoint_sslverify = True
        else :
            endpoint_sslverify = False

    #s_log.write(endpoint_sslverify)

    ################################################################ 

    endpoint_timeout = s_config.get_key( "endpoint/timeout" )

    if( isinstance( endpoint_timeout , str ) ) :
        if endpoint_timeout == None or ( not endpoint_timeout.isdigit( ) ) :
            endpoint_timeout = 180
        else:
            endpoint_timeout = int( endpoint_timeout )

    endpoint_url = s_config.get_key( "endpoint/url" ) 
    if( not endpoint_url ) :
        s_log.write( "false endpoint_url" )
        return( False )

    if( not endpoint_url.endswith( "/" ) ) :
        endpoint_url = endpoint_url + "/"

    endpoint_version = s_config.get_key( "endpoint/version" ) 
    if( not endpoint_version ) :
        endpoint_version = "_sapi_1_"

    endpoint_url = endpoint_url + endpoint_version + "/"
    #s_log.write(endpoint_url)

    #####################################################################

    try :

        response = session.post( endpoint_url , data = payload , headers = request_headers ,timeout = ( endpoint_timeout , 60 ) , verify = endpoint_sslverify )

    except requests.exceptions.SSLError as e :
        s_log.write( endpoint_url )
        s_log.write( "ERROR requests.exceptions.SSLError:" + str( e ) )
        return( False )    
    except requests.exceptions.ReadTimeout as e :
        s_log.write( endpoint_url)
        s_log.write( "ERROR requests.exceptions.ReadTimeout:" + str( e ) )
        return( False )    
    except requests.exceptions.ConnectionError as e :
        s_log.write( "ERROR requests.exceptions.ConnectionError::" + str( e ) )
        s_log.write( "ERROR Maybe no omnibus..?" )
        s_log.write( endpoint_url )
        s_log.write( request_headers )
        s_config.set_key( "halt" , True ) 
        return( False )  
    except requests.exceptions.ReadTimeout as e :
        s_log.write( endpoint_url)
        s_log.write( "ERROR requests.exceptions.ReadTimeout:" + str( e ) )
        return( False )    

    #####################################################################

    if ( response.status_code == 200 ) :
        #X-Sapi-Tokensession
        if( "X-Sapi-Tokensession" in response.headers ) :
            token_session = response.headers[ "X-Sapi-Tokensession" ]
            s_config.set_key_fsoneshot( "token_session" , token_session )
            #s_log.write( token_session )
        return( response )

    #####################################################################

    s_log.write( "ERROR status_code" )
    s_log.write( endpoint_url )
    s_log.write( request_headers )
    s_log.write( response.status_code )
    if( response.status_code == 404 ) :
        s_log.write( "Check endpoint url" )
    if( response.status_code == 502 ) :
        s_log.write( "ERROR 502" )
    if( response.status_code == 418 ) :
        s_log.write( "ERROR 418" )
        s_log.write( "Sleep while tea is brewing" )
        s_util.sleep( 10 )

    time.sleep( 10 )

    return( False )
    