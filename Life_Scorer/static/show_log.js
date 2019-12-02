function task_text() {
    // Declare variables
    var input, filters;
    input = document.getElementById('selection');
    filters = input.value.toUpperCase();
    filters = filters.split(",");
  
  
    var tasks = document.getElementsByClassName("log-item");
    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < tasks.length; i++) {
      var task = tasks[i];
      var taskName = task.id.split('-')[0].toUpperCase()
//      console.log(taskName);
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

  function clear_sel(){
    document.getElementById('selection').value = '';
    
    task_text();
  }

//Implement swipe action
//Taken from: https://stackoverflow.com/questions/45648886/swipe-left-right-for-a-webpage
 var start = null;
 window.addEventListener("touchstart",function(event){
   if(event.touches.length === 1){
      //just one finger touched
      start = event.touches.item(0).clientX;
    }else{
      //a second finger hit the screen, abort the touch
      start = null;
    }
  });

 window.addEventListener("touchend",function(event){
    var offset = 100;//at least 100px are a swipe
    if(start){
      //the only finger that hit the screen left it
      var end = event.changedTouches.item(0).clientX;

      if(end > start + offset){
              window.location.href="/create_log";
      }
      if(end < start - offset ){
              window.location.href="/create_log";
      }
    }
  });
//End swipe implementation
