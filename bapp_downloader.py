import requests
import shutil
from bs4 import BeautifulSoup
from pathlib import Path

BASE_URL = 'https://portswigger.net/bappstore/'
OUT_DIR = 'bapps'

BAPP_IDS = [
    ('Active Scan++', 'active_scan_plus_plus.bapp', '3123d5b5f25c4128894d97ea1acc4976'),
    ('Add Custom Header', 'add_custom_header.bapp', '807907f5380c4cb38748ef4fc1d8cdbc'),
    ('AuthMatrix', 'auth_matrix.bapp', '30d8ee9f40c041b0bfec67441aad158e'),
    ('Auth Analyzer', 'auth_analyzer.bapp', '7db49799266c4f85866f54d9eab82c89'),
    ('Autorize', 'autorize.bapp', 'f9bbac8c4acf4aefa4d7dc92a991af2f'),
    ('Blackslash Powered Scanner', 'backslash_powered_scanner.bapp', '9cff8c55432a45808432e26dbb2b41d8'),
    ('Collaborator Everywhere', 'collaborator_everywhere.bapp', '2495f6fb364d48c3b6c984e226c02968'),
    ('Content Type Converter', 'content_type_converter.bapp', 'db57ecbe2cb7446292a94aa6181c9278'),
    ('Copy Request Response', 'copy_request_response.bapp', '0d05f52c00a64cb2b2bea68744f6316c'),
    ('CORS*, Additional CORS Checks', 'cors.bapp', '420a28400bad4c9d85052f8d66d3bbd8'),
    ('Detect Dynamic JS', 'detect_dynamic_js.bapp', '4a657674ebe3410b92280613aa512304'),
    ('Error Message Checks', 'error_message_checks.bapp', '4f01db4b668c4126a68e4673df796f0f'),
    ('ExifTool Scanner', 'exiftool.bapp', '858352a27e6e4a6caa802e61fdeb7dd4'),
    ('Freddy, Deserialization Bug Finder', 'freddy.bapp','ae1cce0c6d6c47528b4af35faebc3ab3'),
    ('GraphQL Raider', 'graphql_raider.bapp', '4841f0d78a554ca381c65b26d48207e6'),
    ('Hackvertor', 'hackvertor.bapp', '65033cbd2c344fbabe57ac060b5dd100'),
    ('Headers Analyzer', 'headers_analyzer.bapp', '8b4fe2571ec54983b6d6c21fbfe17cb2'),
    ('Host Header Inchecktion', 'host_header_inchecktion.bapp', '3908768b9ae945d8adf583052ad2e3b3'),
    ('HTTP Request Smuggler', 'http_request_smuggler.bapp', 'aaaa60ef945341e8a450217a54a11646'),
    ('Java Deserialization Scanner', 'java_deserialization_scanner.bapp', '228336544ebe4e68824b5146dbbd93ae'),
    ('JSON Web Tokens', 'json_web_tokens.bapp', 'f923cbf91698420890354c1d8958fee6'),
    ('JS Link Finder', 'js_link_finder.bapp', '0e61c786db0c4ac787a08c4516d52ccf'),
    ('JS Miner', 'js_miner.bapp', '0ab7a94d8e11449daaf0fb387431225b'),
    ('Log4Shell Everywhere', 'log4shell_everywhere.bapp', '186be35f6e0d418eb1f6ecf1cc66a74d'),
    ('Log4Shell Scanner', 'log4shell_scanner.bapp', 'b011be53649346dd87276bca41ce8e8f'),
    ('OpenAPI Parser', 'open_api_parser.bapp', '6bf7574b632847faaaa4eb5e42f1757c'),
    ('Paramalyzer', 'paramalyzer.bapp', '0ac13c45adff4e31a3ca8dc76dd6286c'),
    ('Param Miner', 'param_miner.bapp', '17d2949a985c4b7ca092728dba871943'),
    ('Pentagrid Scan Controller', 'pentagrid_scan_controller.bapp', 'e3dde890bdce4ae4bcef0d97019f5d46'),
    ('Piper', 'piper.bapp', 'e4e0f6c4f0274754917dcb5f4937bb9e'),
    ('Proxy Auto Config', 'proxy_auto_config.bapp', '7b3eae07aa724196ab85a8b64cd095d1'),
    ('Reflected Parameters', 'reflected_parameters.bapp', '8e8f6bb313db46ba9e0a7539d3726651'),
    ('Request Minimizer', 'request_minimizer.bapp', 'cc16f37549ff416b990d4312490f5fd1'),
    ('Request Randomizer', 'request_randomizer.bapp', '36d6d7e35dac489b976c2f120ce34ae2'),
    ('Retire.js', 'retire_js.bapp', '36238b534a78494db9bf2d03f112265c'),
    ('SAML Raider', 'saml_raider.bapp', 'c61cfa893bb14db4b01775554f7b802e'),
    ('Software Vulnerability Scanner', 'software_vulnerability_scanner.bapp', 'c9fb79369b56407792a7104e3c4352fb'),
    ('Stepper', 'stepper.bapp', '065d156ecefd480fa3efa36e05d55f77'),
    ('Taborator', 'taborator.bapp', 'c9c37e424a744aa08866652f63ee9e0f'),
    ('Turbo Intruder', 'turbo_intruder.bapp', '9abaa233088242e8be252cd4ff534988'),
    ('Upload Scanner', 'upload_scanner.bapp', 'b2244cbb6953442cb3c82fa0a0d908fa'),
]


def extract_bapp_url(bapp_id):

    res = requests.get(BASE_URL + bapp_id)
    soup = BeautifulSoup(res.content, features='html.parser')

    return soup.find_all('a', id='DownloadedLink')[0]['href']


def download_bapp(bapp_name, bapp_url):

    with requests.get(bapp_url, stream=True) as r:
        with open(OUT_DIR + '/' + bapp_name, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def zip_bapps_dir(zip_file_name, bapps_dir):

    print('[*] Creating ZIP archive...')
    shutil.make_archive(zip_file_name, 'zip', base_dir=bapps_dir)
    print('[*] Creating GZTAR archive...')
    shutil.make_archive(zip_file_name, 'gztar', base_dir=bapps_dir)


if __name__ == '__main__':

    # Make sure that output dir exists
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

    # Download extensions
    for bapp_name, bapp_file_name, bapp_id in BAPP_IDS:


        try:
            print('[*] Downloading {}...'.format(bapp_name))

            bapp_href = extract_bapp_url(bapp_id)
            download_bapp(bapp_file_name, bapp_href)
        except:
            print('[!] Failed to download {}.'.format(bapp_name))

    # Create archive files
    zip_bapps_dir('bapps', OUT_DIR)


