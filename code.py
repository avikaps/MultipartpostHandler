import urllib2
import MultipartPostHandler

def handle_authentication(url):
    """handle_authentication description"""
    try:
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, USERNAME, PASSWORD)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
    except urllib2.HTTPError:
        print ERROR_300


def format_flash(option, opt_str, value, parser):
    """format_flash put a request to the web server to check the partition
    created on the SATA are correct or NOT. It also checks whether it requires
    INIT or REINIT functionality."""
    del option  # Resolving the pylint waring unused argument
    del opt_str  # Resolving the pylint waring unused argument
    del value  # Resolving the pylint waring unused argument
    try:
        host_ip = compute_ip(parser.values.serial, parser.values.channel)
    except TypeError:
        sys.exit(ERROR_224)
    except ValueError:
        sys.exit(ERROR_224)
    print "\nChecking Flash Memory . . ."
    url = 'http://' + host_ip + '/cgi-bin/SATA_Format.cgi'
    handle_authentication(url)
    try:
        response = urllib2.urlopen(url)
    except urllib2.URLError:
        sys.exit(ERROR_300)
    valid_response = check_response_received(response)
    if valid_response is not 'OK':
        sys.exit(ERROR_301)
    else:
        log_response = response.read()
        if "ERROR" in log_response:
            logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
            logging.debug(log_response)
            print ERROR_227
        else:
            print "\nFORMAT-FLASH : SUCCESS"

def write_config(option, opt_str, value, parser):
    """write_config checks the partition in the SATA and writes the
    configuration files in SATA. This function requires Input config file
    as a paramter and the same will get uploaded to the SCU by Web-Server"""
    del option  # Resolving the pylint waring unused argument
    del value  # Resolving the pylint waring unused argument
    check_paramters_required(opt_str,
                             parser.values.inputfilepath,
                             parser.values.outputfilepath)
    host_ip = compute_ip(parser.values.serial, parser.values.channel)
    url = 'http://' + host_ip + '/cgi-bin/SATA_Config.cgi'
    input_path = parser.values.inputfilepath
    board_type = parser.values.channel
    params = {'BoardType': board_type,
              'SataConfigFile': open(input_path, 'rb')}
    opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
    try:
        handle_authentication(url)
        response = opener.open(url, params)
    except urllib2.URLError:
        sys.exit(ERROR_300)
    valid_response = check_response_received(response)
    if valid_response is not 'OK':
        sys.exit(ERROR_301)
    else:
        log_response = response.read()
        if "ERROR" in log_response:
            logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
            logging.debug(log_response)
            print ERROR_228
        else:
            print "\nWRITE-CONFIG : SUCCESS"
