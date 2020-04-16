# Elasticsearch, Logstash, Kibana, APM Server Python Logging Use Case Demo

The intent of this project is to enable developers to quickly scaffold an ELK logging eco system, locally.  The hope is that developers will leverage these tools to produce more meaningful and actionable logs.

## Getting Started
git clone 
install prerequisites (docker, docker-compose)
docker-compose up
verify deployment

### Prerequisites

docker 
https://docs.docker.com/docker-for-mac/install/

docker-compose
```
pip3 install docker-compose
```

tested with the following versions
```
~/dev » docker version
Client: Docker Engine - Community
 Version:           19.03.8
 API version:       1.40
 Go version:        go1.12.17
 Git commit:        afacb8b
 Built:             Wed Mar 11 01:21:11 2020
 OS/Arch:           darwin/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          19.03.8
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.12.17
  Git commit:       afacb8b
  Built:            Wed Mar 11 01:29:16 2020
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          v1.2.13
  GitCommit:        7ad184331fa3e55e52b890ea95e65ba581ae3429
 runc:
  Version:          1.0.0-rc10
  GitCommit:        dc9208a3303feef5b3839f4323d9beb36df0a9dd
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683
------------------------------------------------------------
~/dev » docker-compose version
docker-compose version 1.25.4, build 8d51620a
docker-py version: 4.1.0
CPython version: 3.7.5
OpenSSL version: OpenSSL 1.1.1d  10 Sep 2019
------------------------------------------------------------

```
### Deployment 

git clone the esdemo demo locally
```
git clone https://github.com/erok77/esdemo
```
change directory to the elk folder
```
cd ./esdemo/elk
```
edit ./esdemo/elk/.env and update the following env vars or set them via export, note the APPLOG_PATH will be your app log path
```
export ES_INDEX=applog
export APPLOG_PATH=/Users/eric77/dev/k72/logs
```

run docker-compose up
```
docker-compose up 
```

verify docker containers are running
```
docker ps
CONTAINER ID        IMAGE                                                 COMMAND                  CREATED             STATUS                    PORTS                              NAMES
14080a585055        docker.elastic.co/apm/apm-server:7.6.2                "/usr/local/bin/dock…"   56 minutes ago      Up 56 minutes (healthy)   0.0.0.0:8200->8200/tcp             elk_apm-server_1
db7b2cad3fc6        docker.elastic.co/kibana/kibana:7.6.2                 "/usr/local/bin/dumb…"   58 minutes ago      Up 58 minutes (healthy)   0.0.0.0:5601->5601/tcp             elk_kibana_1
da1ed08d2b7d        docker.elastic.co/logstash/logstash:7.6.2             "/usr/local/bin/dock…"   58 minutes ago      Up 58 minutes             5044/tcp, 9600/tcp                 elk_logstash_1
9698a939493f        docker.elastic.co/elasticsearch/elasticsearch:7.6.2   "/usr/local/bin/dock…"   58 minutes ago      Up 58 minutes (healthy)   0.0.0.0:9200->9200/tcp, 9300/tcp   elk_elasticsearch_1
```

curl/browse to elasticsearch and kibana endpoints to verify services are available
```
>> curl 127.0.0.1:9200
{
  "name" : "aleph77",
  "cluster_name" : "es_circusarcade",
  "cluster_uuid" : "WidG72wHRfSgGAOOw8OAoQ",
  "version" : {
    "number" : "7.6.1",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "aa751e09be0a5072e8570670309b1f12348f023b",
    "build_date" : "2020-02-29T00:15:25.529771Z",
    "build_snapshot" : false,
    "lucene_version" : "8.4.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}

>> curl 127.0.0.1:5601/api/status
{"name":"aleph77","uuid":"1da3e9dc-6a26-43d6-8918-b5b96ea7727b","version":{"number":"7.6.1","build_hash":"5ddabf8510131ebf173762b7405e5e18f2757c12","build_number":29118,"build_snapshot":false},"status":{"overall":{"state":"green","title":"Green","nickname":"Looking good","icon":"success","uiColor":"secondary","since":"2020-04-10T18:22:53.401Z"},"statuses":[{"id":"plugin:kibana@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.401Z"},{"id":"plugin:elasticsearch@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.576Z"},{"id":"plugin:xpack_main@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.382Z"},{"id":"plugin:graph@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.421Z"},{"id":"plugin:monitoring@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.429Z"},{"id":"plugin:spaces@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.668Z"},{"id":"plugin:security@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.399Z"},{"id":"plugin:searchprofiler@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.387Z"},{"id":"plugin:ml@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.387Z"},{"id":"plugin:tilemap@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.387Z"},{"id":"plugin:watcher@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.388Z"},{"id":"plugin:grokdebugger@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.388Z"},{"id":"plugin:dashboard_mode@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.503Z"},{"id":"plugin:logstash@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.388Z"},{"id":"plugin:beats_management@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.389Z"},{"id":"plugin:apm_oss@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.527Z"},{"id":"plugin:apm@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.535Z"},{"id":"plugin:maps@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.559Z"},{"id":"plugin:interpreter@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.561Z"},{"id":"plugin:canvas@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.568Z"},{"id":"plugin:license_management@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.570Z"},{"id":"plugin:index_management@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.389Z"},{"id":"plugin:console@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.585Z"},{"id":"plugin:console_extensions@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.587Z"},{"id":"plugin:index_lifecycle_management@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.390Z"},{"id":"plugin:kuery_autocomplete@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.601Z"},{"id":"plugin:metrics@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.608Z"},{"id":"plugin:infra@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.629Z"},{"id":"plugin:task_manager@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.632Z"},{"id":"plugin:rollup@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.390Z"},{"id":"plugin:transform@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.390Z"},{"id":"plugin:encryptedSavedObjects@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.650Z"},{"id":"plugin:actions@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.659Z"},{"id":"plugin:alerting@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.670Z"},{"id":"plugin:siem@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.716Z"},{"id":"plugin:remote_clusters@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.391Z"},{"id":"plugin:cross_cluster_replication@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.391Z"},{"id":"plugin:upgrade_assistant@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.735Z"},{"id":"plugin:uptime@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.753Z"},{"id":"plugin:oss_telemetry@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.756Z"},{"id":"plugin:file_upload@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.761Z"},{"id":"plugin:data@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.764Z"},{"id":"plugin:lens@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.770Z"},{"id":"plugin:snapshot_restore@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.392Z"},{"id":"plugin:input_control_vis@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.803Z"},{"id":"plugin:navigation@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.804Z"},{"id":"plugin:kibana_react@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.806Z"},{"id":"plugin:management@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.808Z"},{"id":"plugin:region_map@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.810Z"},{"id":"plugin:telemetry@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.816Z"},{"id":"plugin:ui_metric@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:53.824Z"},{"id":"plugin:timelion@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:54.153Z"},{"id":"plugin:markdown_vis@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:54.156Z"},{"id":"plugin:tagcloud@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:54.158Z"},{"id":"plugin:metric_vis@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:54.159Z"},{"id":"plugin:table_vis@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:54.161Z"},{"id":"plugin:vega@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-10T18:22:54.162Z"},{"id":"plugin:reporting@7.6.1","state":"green","icon":"success","message":"Ready","uiColor":"secondary","since":"2020-04-15T03:06:28.392Z"}]},"metrics":{"last_updated":"2020-04-15T20:48:43.718Z","collection_interval_in_millis":5000,"process":{"memory":{"heap":{"total_in_bytes":328585216,"used_in_bytes":246030280,"size_limit":1526909922},"resident_set_size_in_bytes":57622528},"event_loop_delay":0.13635900616645813,"pid":1228,"uptime_in_millis":140779292},"os":{"load":{"1m":2.60302734375,"5m":3.02734375,"15m":3.76611328125},"memory":{"total_in_bytes":17179869184,"free_in_bytes":1342935040,"used_in_bytes":15836934144},"uptime_in_millis":441123000,"platform":"darwin","platformRelease":"darwin-18.6.0"},"response_times":{"max_in_millis":0},"requests":{"disconnects":0,"statusCodes":{},"total":0,"status_codes":{}},"concurrent_connections":0}}%      
```


End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

> To test you can simply write a json log line to the ./esdemo/logs/app.json file
```
echo {"test":"test123"} > ./esdemo/logs/app.json
```

> Then browse to your local kibana instance, e.g. 
```
http://127.0.0.1:5601/app/kibana#/management/kibana/index_patterns?_g=()
```
> Create a Kibana Index Pattern for the index you established, (default is applog), select the time/date stamp if applicable
> Finally browse and select the index pattern you just created. 
```
http://127.0.0.1:5601/app/kibana#/discover 
```

## Authors

* **Eric Moss** - (https://github.com/erok77)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Noteworthy References

https://elastic.co

https://docs.python.org/3/howto/logging-cookbook.html

https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying
