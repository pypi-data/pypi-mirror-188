import os, sys, math
from pathlib import Path
import logging
import base64

from .utils import enumerate_files_in_paths, filter_paths_by_extensions, fetch_files, \
    write_shard, get_network_patch

def bravojsify(files):
    prefix = "//This module was created by a bravojsify script from AITF\nmodule.declare([], function(require, exports, module) {\n"
    postfix = "\n});// this concludes the module definition"
    for file in files:
        with open(file, 'r') as f:
            content = f.readlines()
        content = [ "  " + line for line in content ]
        content.insert(0, prefix)
        content.append(postfix)
        content = "".join(content)
        with open(file, 'w') as f:
            f.write(content)
    return




def serialize_files(paths, extensions, output, shard_size, package_name, network_patch, **kwargs):
    logging.info("Beginning serialization process")

    logging.info(f"Paths found: {paths}")
    logging.info(f"Extensions to filter by: {extensions}" )

    files_to_serialize = enumerate_files_in_paths(paths)
    logging.info(f"Found a total of : {len(files_to_serialize)} candidates to serialize.")

    files_to_serialize = filter_paths_by_extensions(files_to_serialize, extensions)
    logging.info(f"After extension filtering, found a total of: {len(files_to_serialize)} candidates to serialize.")

    logging.debug(f"Serializing the following: {files_to_serialize}")
    data = fetch_files(files_to_serialize)
    logging.debug(f"Data read and stored in dictionary.")


    output = os.path.abspath(output)
    logging.info(f"Output directory is {output}")
    if not os.path.exists(output):
        mk_dir_bool = input(f"Output directory doesn't exist. Would you like me to make it ({output})? [y/n] ").lower()
        mk_dir_bool = mk_dir_bool in ['y','yes']
        if not mk_dir_bool:
            raise RuntimeError("Output directory doesn't exist. Please make it.")
    os.makedirs(output, exist_ok=True)

    logging.debug(f"Shard size is set to : {shard_size} megabytes.")

    shards = []
    shard_count = 0

    while len(data.keys()) > 0:
        shard_count += 1
        data = write_shard(output, shard_count, shard_size, data)
    del data

    with open(os.path.join( output, 'main.js' ), 'w') as f:
        f.write(f"const shardCount = {shard_count};\n")
        f.write(f"const packageName= \"{package_name}\";\n")
        f.write("let data = {};\n")
        f.write("""
/**
* Merge two objects into one object where any duplicate keys are resolved
* by merging the strings. This is done in a left to right way.
**/
function mergeData( left, right ){
    for (const key in right){
        if (key in left){
            left[key] = left[key] + right[key];
        }else {
            left[key] = right[key];
        };
    };
    return left;
};

async function providePackageFiles(packagePathArray) {
    return await new Promise((resolve, reject) => {
        try {
            module.provide(packagePathArray, () => {
                resolve();
            });
        } catch(myError) {
            reject(myError);
        };
    });
}

async function fetchData(){
    let shardPackagePaths = [];
    for (let i = 1; i < shardCount+1; i++){
        shardPackagePaths.push( packageName + '/shard_' + i + '.js' )
    };

    await providePackageFiles( shardPackagePaths );

    for (let i = 1; i < shardCount+1; i++){
        const shardExport = require('shard_' + i + '.js');
        data = mergeData( data, shardExport.data );
    };

    return data;
};

exports.data = data;
exports.fetchData = fetchData;
""")
        if network_patch:
            f.write( get_network_patch() )
    moduleFiles = Path(output).rglob('*.js')
    moduleFiles = [ _path.absolute().as_posix() for _path in moduleFiles ]
    bravojsify(moduleFiles)

    logging.info(f"Done writing to {output}.")
