var select = document.getElementById("selection");
select.focus();
var t = 'test';
var old_select=''


function task_text() {
  // Declare variables
  var input, filter;
  input = document.getElementById('selection');
  filter = input.value.toUpperCase();

  var tasks = document.getElementsByClassName("picker button");
  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < tasks.length; i++) {
    task = tasks[i];
      if (task.id.split('-')[0].toUpperCase().indexOf(filter) > -1) {
          task.style.display = "";
      } else {
          task.style.display = "none";
      }
  }
}



function clear_sel(){
  document.getElementById('selection').value = '';
  document.getElementById('variableForm').innerHTML='';
  task_text();
   var elements = document.getElementsByClassName('edit');
    for (var i = 0; i < elements.length; i++){
        elements[i].style.display = 'none';
    }
   
}

function hideTop(){
  var elements = document.getElementsByClassName('top');
    for (var i = 0; i < elements.length; i++){
        elements[i].style.display = 'none';
    }
}
