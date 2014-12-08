function kill_job (task_id) {
    $.post("/task_kill?task_id="+task_id,{},function(data,status){

            alert(data);
  })
}
function stop_job (task_id) {
    $.post("/task_stop?task_id="+task_id,{},function(data,status){

            alert(data);
  })
}
function modify_cronjob (job_id) {
    $.get("/cronjob_modify?job_id="+job_id,function(data,status){

            alert(data);
  })
}
function pause_cronjob (job_id) {
    $.post("/cronjob_pause?job_id="+job_id,{},function(data,status){

            alert(data);
  })
}
function remove_cronjob (job_id) {
    $.post("/cronjob_remove?job_id="+job_id,{},function(data,status){

            alert(data);
  })
}