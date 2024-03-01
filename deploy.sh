#!/bin/bash
set -e

Help()
{
   # Display Help
   echo "Dynamic deploy api containers."
   echo
   echo "Syntax: bash build.sh [-h|r|d|e]"
   echo "options:"
   echo "h          display this help and exit"
   echo "r          path to routing table file"
   echo "e          environment name. Only services in routing table with this environment will be deployed. If not specified, all services will be deployed"
   echo "f          environment file"
}

while getopts "hr:e:f:" flag
do
    case "${flag}" in
        h)  Help && exit 1;;
        r)  routing_table=${OPTARG};;
        e)  env=${OPTARG};;
        f)  env_file=${OPTARG};;
    esac
done

# check if env file exists

if [[ -z $env_file ]]; then
    echo "-f argument is required. Help:" && Help && exit 1
    if ! [[ -f $env_file ]]; then
        echo "error: env file does not exists. Help:" && Help && exit 1
    fi
fi

# check if routing table file exists
if [[ -z $routing_table ]]; then
    echo "-r argument is required. Help:" && Help && exit 1
elif ! [[ -f $routing_table ]]; then
    echo "file specified with -r argument does not exists. Help:" && Help && exit 1
fi

for model in $(jq -r 'keys[]' $routing_table); do

    if ! [[ -z $env ]]; then
        model_env=$(jq -r '.["'$model'"] | .env' $routing_table)
        if [[ $model_env != "${env}" ]]; then
            echo "info: skipping $model because of env mismatch"
            continue
        fi
    fi

    api_port=$(jq -r '.["'$model'"] | .api_port' $routing_table)

    if [[ $api_port = "null" ]]; then
        echo "error: api_port is required for $model. Skipping api-v2 container" && exit 1
    fi

    if [[ -z $port_list ]]; then
        port_list=$api_port

    elif ! [[ $port_list =~ (^|[[:space:]])$api_port($|[[:space:]]) ]]; then
        port_list="$port_list $api_port"
    else
        continue
    fi

    for model in $(jq -r 'keys[]' $routing_table); do

        if ! [[ -z $env ]]; then
            model_env=$(jq -r '.["'$model'"] | .env' $routing_table)
            if [[ $model_env != "${env}" ]]; then
                continue
            fi
        fi

        model_port=$(jq -r '.["'$model'"] | .model_port' $routing_table)
        model_host=$(jq -r '.["'$model'"] | .model_host' $routing_table)
        hf_repo_id=$(jq -r '.["'$model'"] | .hf_repo_id' $routing_table)
        current_api_port=$(jq -r '.["'$model'"] | .api_port' $routing_table)

        if [[ $model_port = "null" ]] || [[ $model_host = "null" ]] || [[ $hf_repo_id = "null" ]]; then
            echo "error: model_port, model_host, hf_repo_id are required for $model. Skipping api-v2 container" && exit 1
        fi

        if [[ $api_port == $current_api_port ]]; then
            if [[ -z $model_list ]]; then
                model_list="(\"$hf_repo_id\", \"http://${model_host}:${model_port}\")"
            else
                model_list="$model_list, (\"$hf_repo_id\", \"http://${model_host}:${model_port}\")"
            fi
        else
            continue
        fi
        
    done
    
    model_list="[${model_list}]"
    api_table+=("($api_port, $model_list)")
    unset model_list

done

# for i in range length of api_table
for (( i=0; i<${#api_table[@]}; i++ ));do
    api_port=$(echo ${api_table[$i]} | cut -d',' -f1 | tr -d '()' | tr -d '[:space:]')
    echo "info: api_port: $api_port"
    # get index of the first "[" character in ${api_table[$i] and store it in a variable
    start_index=$(echo ${api_table[$i]} | grep -aob '\[' | head -n1 | cut -d: -f1)
    # get string from start_index to the end of the string
    model_list=$(echo ${api_table[$i]} | cut -c$(($start_index+1))- | rev | cut -c 2- | rev)

    export LLM_TABLE=$model_list
    export API_PORT=$api_port

    echo "info: deploying api container on ${API_PORT} port with LLM_TABLE: $LLM_TABLE"
    
    docker compose --env-file $env_file down
    #docker image rm ${CI_REGISTRY_IMAGE}/api:${CI_API_IMAGE_TAG} || true
    docker compose --env-file $env_file  up --detach  
done
