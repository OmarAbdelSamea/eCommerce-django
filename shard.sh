#!/bin/bash

# Purpose: Create shard setup for mongoDB containers 
# Usage: ./shrad.sh
# --
# Input file format: None
# --
# Author: Omar AbdelSamea
# Last updated: 6/Dec/2021
# -----------------------------------------------------------------------------

echo "
 _______ _           _          ______       _____ _                   _ _             
|__   __| |         | |        |____  |     / ____| |                 | (_)            
   | |  | |__   __ _| |__   __ _   / /__   | (___ | |__   __ _ _ __ __| |_ _ __   __ _ 
   | |  |  _ \ / _  |  _ \ / _  | / / _ \   \___ \|  _ \ / _  |  __/ _  | |  _ \ / _  |
   | |  | | | | (_| | |_) | (_| |/ / (_) |  ____) | | | | (_| | | | (_| | | | | | (_| |
   |_|  |_| |_|\__ _|_ __/ \__ _/_/ \___/  |_____/|_| |_|\__ _|_|  \__ _|_|_| |_|\__  |
                                                                                  __/ |
                                                                                 |___/ 
"

if  [[ $1 = "-q" ]]; then
    REDIRECT=/dev/null
else
    REDIRECT=/dev/stdout
fi

# Setting config servers as master and slaves
echo '--------------- Initializing Config servers --------------- '
docker exec -it cfg1 bash -c "echo 'rs.initiate({_id: \"conf_replica\",configsvr: true, members: [{ _id : 0, host : \"cfg1\" },{ _id : 1, host : \"cfg2\" }, { _id : 2, host : \"cfg3\" }]})' | mongo" &> $REDIRECT
docker exec -it cfg1 bash -c "echo 'rs.status()' | mongo" &> $REDIRECT
echo -e "Config server Initialized succesfully \n"

sleep 2

# Setting shards as master and slaves
echo "--------------- Initializing Shard 1 ---------------"
docker exec -it shard1 bash -c "echo 'rs.initiate({_id : \"shard_replica\", members: [{ _id : 0, host : \"shard1\" },{ _id : 1, host : \"shard2\" },{ _id : 2, host : \"shard3\" }]})' | mongo" &> $REDIRECT
docker exec -it shard1 bash -c "echo 'rs.status()' | mongo" &> $REDIRECT
echo -e "Shard 1 Initialized succesfully \n"

sleep 2

# Setting shards as master and slaves
echo "--------------- Initializing Shard 2 --------------- "
docker exec -it shard4 bash -c "echo 'rs.initiate({_id : \"shard_replica2\", members: [{ _id : 0, host : \"shard4\" },{ _id : 1, host : \"shard5\" },{ _id : 2, host : \"shard6\" }]})' | mongo" &> $REDIRECT
docker exec -it shard4 bash -c "echo 'rs.status()' | mongo" &> $REDIRECT
echo -e "Shard 2 Initialized succesfully \n"

sleep 2

# Starting main router and setting shards and replicas
echo "--------------- Initializing Router  --------------- "
docker exec -it mongos bash -c "echo 'sh.addShard(\"shard_replica/shard1,shard2,shard3\")' | mongo " &> $REDIRECT
docker exec -it mongos bash -c "echo 'sh.status()' | mongo " &> $REDIRECT 

sleep 2

docker exec -it mongos bash -c "echo 'sh.addShard(\"shard_replica2/shard4,shard5,shard6\")' | mongo " &> $REDIRECT
docker exec -it mongos bash -c "echo 'sh.status()' | mongo " &> $REDIRECT
echo -e "Router Initialized succesfully \n"