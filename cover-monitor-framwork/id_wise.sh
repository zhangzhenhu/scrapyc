
DATA_PATH="./data/yinni/`date +%Y%m%d`"
#DATA_PATH="./data/yinni/20150115"

mkdir -p ${DATA_PATH}/
HADOOP_BIN=${HOME}/hadoop-client-yq/hadoop/bin/hadoop

SAMPLE_COUNT_QUERY=3000
SAMPLE_COUNT_URL=1500

function crawl
{
local urlf=$1
local wait_time=$2
cd ./client
rm ./sendpack.log
rm -fr ./out_dir/317/0 
./cs_client -n  -c client_hk.conf -f ${urlf}
sleep ${wait_time} 
#${SAMPLE_COUNT_URL}+60
cd -
}


function hot
{

#head -n 300000 ${DATA_PATH}/query.raw |  ~/share/common-tools/sample.sh ${SAMPLE_COUNT_QUERY} | awk -F '\t' '{print $1}' > ${DATA_PATH}/query.hot 

cat ${DATA_PATH}/query.hot | python ./utils/mkgooglurl.py > ./client/url.hot

crawl url.hot 60
ls -l ./client/out_dir/317/0/ | grep -F 'html' | awk '{if ($9) print "./client/out_dir/317/0/"$9}' | python ./utils/parsegoogle.py > ${DATA_PATH}/url.hot.all

#cat ${DATA_PATH}/query.hot | python ./utils/google.py > ${DATA_PATH}/url.hot.all 2>${DATA_PATH}/hot.log


awk -F '\t'  '{if($2<5) print $1 }' ${DATA_PATH}/url.hot.all |  ~/share/common-tools/sample.sh ${SAMPLE_COUNT_URL}  > ${DATA_PATH}/url.hot.sample
 
}

function random
{
#cat ${DATA_PATH}/query.raw | ~/share/common-tools/sample.sh ${SAMPLE_COUNT_QUERY} | awk -F '\t' '{print $1}' > ${DATA_PATH}/query.random

#cat ${DATA_PATH}/query.random | python ./utils/google.py  >${DATA_PATH}/url.random.all 2>${DATA_PATH}/random.log

cat ${DATA_PATH}/query.random | python ./utils/mkgooglurl.py > ./client/url.random
crawl url.random 60
ls -l ./client/out_dir/317/0/ | grep -F 'html' | awk '{if ($9) print "./client/out_dir/317/0/"$9}' | python ./utils/parsegoogle.py > ${DATA_PATH}/url.random.all
awk -F '\t'  '{if($2<5) print $1 }' ${DATA_PATH}/url.random.all |  ~/share/common-tools/sample.sh ${SAMPLE_COUNT_URL} > ${DATA_PATH}/url.random.sample


}


sh -x ./get_query.sh

if [ $? -ne 0 ];then
exit 1;
fi

hot

python run.py -i ${DATA_PATH}/url.hot.sample  -u "印尼无线（热门）覆盖率监控"  -d ./history/id-id/`date +%Y%m%d`/hot/ 1>${DATA_PATH}/cover_hot.log  2>&1 &

#exit

random
python run.py -i ${DATA_PATH}/url.random.sample -u "印尼无线（随机）覆盖率监控"   -d ./history/id-id/`date +%Y%m%d`/random/ 1>${DATA_PATH}/cover_random.log  2>&1 &


function _scrapy
{
mkdir ./robot/data/`date +%Y%m%d`/
robot_input=robot/data/`date +%Y%m%d`/url.list
awk -F '\t'  '{print $1 }' ${DATA_PATH}/url.random.all  ${DATA_PATH}/url.hot.all | sort|uniq > ${robot_input}
cd ./robot/
scrapy crawl one -sJOBDIR=./data/`date +%Y%m%d`/job  -sinput=./data/`date +%Y%m%d`/url.list >./data/`date +%Y%m%d`/log.txt 2>&1 &
cd  -

mkdir -p ./intbogus/
cp ${robot_input} ./intbogus/`date +%Y%m%d`.google
cat robot/feeds/one/*.json  | python utils/parsejson.py | uniq >> ./intbogus/`date +%Y%m%d`.google
}

_scrapy
wait

