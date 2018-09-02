function task_text() {
  // Declare variables
  var input, filter;
  input = document.getElementById('selection');
  filter = input.value.toUpperCase();

  var tasks = document.getElementsByClassName("inline buttons");
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