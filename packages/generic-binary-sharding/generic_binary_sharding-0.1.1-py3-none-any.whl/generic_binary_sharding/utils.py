import os, sys, math
from pathlib import Path
import base64
import logging


def enumerate_files_in_paths(paths):
    files_to_serialize = []
    for path in paths:
        if os.path.isdir(path):
            logging.info(f"Found directory: {path} -- will now glob through directory")
            for _path in Path(path).rglob('*'):
                logging.debug(f"\tGLOB -- found file {_path}")
                files_to_serialize.append(_path.absolute().as_posix())
        elif os.path.isfile(path):
            logging.info(f"Found file: {path}")
            files_to_serialize.append(os.path.abspath(path))
        elif not os.path.exists( path ):
            logging.warn(f"Path does not exist: {path} -- skipped")
        else:
            logging.warn(f"Unknown path: {path} -- skipped")
    return files_to_serialize

def filter_paths_by_extensions(files, extensions):
    if extensions:
        candidate_files = []
        for path in files:
            if os.path.splitext(path)[1] in extensions:
                candidate_files.append(path)
        files = candidate_files
    return files

def fetch_files(files):
    data = {}
    for path in files:
        with open(path, 'rb') as f:
            b64_data = base64.b64encode( f.read() ).decode('utf-8')
            base_path = os.path.basename( path )
            if base_path in data.keys():
                logging.warn("Duplicate file names are being serialized. Beware! This is currently undefined behavior!")
            data[base_path] = {
                'b64': b64_data,
                'size' : math.ceil( len( b64_data ) / 1e6 )
            }
            logging.debug(f"Stored file {path} with b64 size: {data[base_path]['size']} megabytes.")
    return data


def write_shard( output_directory, shard_count, shard_size, data ):
    shard_output = os.path.join( output_directory, f"shard_{shard_count}.js" )
    current_size = 0
    to_write = {}

    while (current_size < shard_size) and (len(data.keys()) > 0):
        cur_key = list(data.keys())[0]
        cur_key_size = data[cur_key]['size']

        if current_size + cur_key_size < shard_size:
            to_write[cur_key] = data[cur_key]['b64']
            data.pop(cur_key, None)
            current_size += cur_key_size
        else:
            remainder = shard_size - current_size
            remainder_ind = int(remainder * 1e6)
            to_write[cur_key] = data[cur_key]['b64'][:remainder_ind]
            data[cur_key]['b64'] = data[cur_key]['b64'][remainder_ind:]
            data[cur_key]['size'] = math.ceil( len(data[cur_key]['b64']) / 1e6 )
            current_size += remainder

    with open(shard_output, 'w') as f:
        f.write("let data = {};\n")
        for key in to_write.keys():
            f.write(f"data[\"{key}\"] = `{to_write[key]}`;\n")
        f.write(f"exports.data = data;")
    return data

def get_network_patch():
    return """

/**
* Note that this atob implementation is based of the DCP implementation of atob which
* itself is a modification of the implementation from https://github.com/MaxArt2501/base64-js/blob/master/base64.js
**/
function _atob (string) {
  var b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
  string = String(string).replace(/[\\t\\n\\f\\r ]+/g, "");
  // Adding the padding if missing, for semplicity
  string += "==".slice(2 - (string.length & 3));
  var bitmap, result = "", r1, r2, i = 0;
  for (; i < string.length;) {
    bitmap = b64.indexOf(string.charAt(i++)) << 18 | b64.indexOf(string.charAt(i++)) << 12
            | (r1 = b64.indexOf(string.charAt(i++))) << 6 | (r2 = b64.indexOf(string.charAt(i++)));

    result += r1 === 64 ? String.fromCharCode(bitmap >> 16 & 255)
            : r2 === 64 ? String.fromCharCode(bitmap >> 16 & 255, bitmap >> 8 & 255)
            : String.fromCharCode(bitmap >> 16 & 255, bitmap >> 8 & 255, bitmap & 255);
  }
  return result;
};


/**
 * strtoab  Turns a string to an array buffer
 *          This function comes from the tfjs_utils model serializer project
 *          https://gitlab.com/dcp-aitf/utils/tfjs_utils
 *
 * @param {string} str - The string to serialize
 * @returns {ArrayBuffer} - The array buffer.
 */
function strtoab(str){
  let strin = _atob(str);
  var binaryArray = new Uint8Array(strin.length);
  for (let i = 0; i < strin.length; ++i){
    binaryArray[i] = strin.charCodeAt(i);
  };
  return binaryArray.buffer;
};

let oldFetch = globalThis.fetch;
globalThis.fetch = async function(...args){
    const URL = args[0];
    for (const [key, value] of Object.entries( data )){
        if ( URL.toLowerCase().includes( key.toLowerCase() )){
            return value;
        };
    };
    return oldFetch(...args);
};


let oldXMLHttpRequest = globalThis.XMLHttpRequest;
class PatchedXMLHttpRequest
{
    method;
    async;
    url;
    body;

    response;
    responseURL;
    responseType;
    onload;
    onerror;
    onprogress;

    constructor()
    {
        this.method = null;
        this.async = null;
        this.url = null;
        this.body = null;

        this.response = null;
        this.responseURL = null;
        this.responseType = null;
        this.onload = null;
        this.onerror = null;
        this.onprogress = null;

        this.status = null;
        this.statusText = null;
    };

    open(method, url, async = true, user = null, password = null)
    {
        this.method = method;
        this.url = url;
        this.async = async;
    }

    send(body = null)
    {
        for (const [key, value] of Object.entries( data )){
            if (this.url.toLowerCase().includes( key.toLowerCase() )){
                this.response = strtoab(value);
            };
        };

        if (this.response){
            this.status = 200;
            if (this.async)
            {
                setTimeout( ()=> {
                    if (typeof this.onload === 'function') {
                        this.onload();
                    }
                }, 500);
            }
        }else{
            throw("Missing file: " + this.url + " (xhr.open)");
        }
    }
};

globalThis.XMLHttpRequest = PatchedXMLHttpRequest;

"""
