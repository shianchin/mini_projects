

extern const task_t tasks_table[] =
{
    /* taskname,    task_string,    stacksize,  stackaddr,  entryfunct*/
    {TN_ONE,        "FirstTsk",     2048,       NULL,       NULL},
    {TN_TWO,        "SecondTask",   4096,       NULL,       NULL},
    {LAST_TN,       "LastTask",     4096,       NULL,       NULL}
};
