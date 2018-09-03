function task_text() {
    // Declare variables
    var input, filters;
    input = document.getElementById('selection');
    filters = input.value.toUpperCase();
    filters = filters.split(",");
  
  
    var tasks = document.getElementsByClassName("inline buttons");
    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < tasks.length; i++) {
      var task = tasks[i];
      var taskName = task.id.split('-')[0].toUpperCase()
      var hide=true;
      for (var x in filters){
        var filter = filters[x];
        if (taskName.indexOf(filter) > -1) {
            hide = false;
        } 
        
        }
        if(hide){
                task.style.display = "none";
        }
        else {
            task.style.display = "";
    }
  }
  }