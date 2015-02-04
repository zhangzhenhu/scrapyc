
DATA_PATH="./data/yinni/`date +%Y%m%d`"
mkdir -p ${DATA_PATH}/

SAMPLE_COUNT_QUERY=3000

QUERY_PATH=./data/yinni/query
mkdir -p ${QUERY_PATH}/

HADOOP_BIN=${HOME}/hadoop-client-yq/hadoop/bin/hadoop

T=`date -d "2 days ago" +%Y%m%d-%Y%m%d`

function get_query
{
rm  ${QUERY_PATH}/query.$T
${HADOOP_BIN}  fs -get hdfs://szjjh-dbuild-hdfs.dmop.baidu.com:54310/user/score-int/zhangyi12/wise/round1/$T/ID/part-00000 ${QUERY_PATH}/query.$T

if [ $? -ne 0 ];then
exit 1
fi

#awk '{if(NR>1){print }}' ${DATA_PATH}/query.raw > ${DATA_PATH}/query.t
#mv ${DATA_PATH}/query.t ${DATA_PATH}/query.raw
}


#get_query


awk -F '\t'  '{if(NR>1){ for (i=0;i<$2;i++){ print $1} }}'  ${QUERY_PATH}/query.$T > ${DATA_PATH}/query.$T.ext
cat ${DATA_PATH}/query.$T.ext |  ~/share/common-tools/sample.sh ${SAMPLE_COUNT_QUERY} | awk -F '\t' '{print $1}' > ${DATA_PATH}/query.random.pre
sort -u ${DATA_PATH}/query.random.pre > ${DATA_PATH}/query.random 


rm ${QUERY_PATH}/query.`date -d "32 days ago" +%Y%m%d-%Y%m%d`

cat ${QUERY_PATH}/query.* | python hotquery.py >${DATA_PATH}/query.month
awk -F '\t'  '{if($2>=5 ){ for (i=0;i<$2;i++){  print $1}}}'  ${DATA_PATH}/query.month >${DATA_PATH}/query.hot.ext
cat ${DATA_PATH}/query.hot.ext  |  ~/share/common-tools/sample.sh ${SAMPLE_COUNT_QUERY}  > ${DATA_PATH}/query.hot.pre

sort -u ${DATA_PATH}/query.hot.pre > ${DATA_PATH}/query.hot


