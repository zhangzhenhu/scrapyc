function kill_job (task_id) {
    $.get("/task_kill?task_id="+task_id)
}
function stop_job (task_id) {
    $.get("/task_stop?task_id="+task_id)
}