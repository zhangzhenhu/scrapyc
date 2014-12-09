function kill_job (task_id) {
    $.getJSON("/task_kill?task_id="+task_id,{},function(data,status){

            alert(data.msg);
  })
}
function stop_job (task_id) {
    $.getJSON("/task_stop?task_id="+task_id,{},function(data,status){

            alert(data.msg);
  })
}
function modify_cronjob (job_id) {
    $.getJSON("/cronjob_modify?job_id="+job_id,function(data,status){

            alert(data.msg);
  })
}
function pause_cronjob (job_id) {
    $.getJSON("/cronjob_pause?job_id="+job_id,{},function(data,status){

            alert(data.msg);
  })
}
function remove_cronjob (job_id) {
    $.getJSON("/cronjob_remove?job_id="+job_id,{},function(data,status){

            alert(data.msg);
  })
}

function load_run_list (ele_id) {
    // body...
    $.post("/run_list",{},function  (data,status) {
        if (status == "success"){
            $("#"+ele_id).html(data)
            
        }
        // body...
    })
}
function load_project_list (ele_id) {
    // body...
    $.post("/project_list",{},function  (data,status) {
        if (status == "success"){
            $("#"+ele_id).html(data)
            
        }
        // body...
    })
}
function load_history_list (ele_id) {
    // body...
    $.post("/history_list",{},function  (data,status) {
        if (status == "success"){
            $("#"+ele_id).html(data)
            
        }
        // body...
    })
}