var slider = document.getElementById("myRange");
var output = document.getElementById("numIN");
output.value = slider.value;

slider.oninput = function() {
  output.value = this.value;
}

//Adds a datestamp to form before submitting.
//Needed because always want to use client local time instead of server
function submitForm() {
    console.log('Submitting form using script')

    var element1 = document.createElement("input");
    element1.type = "hidden";
    var dt = new Date()
    element1.value = dt.getTime(); //millisecond timestamp
    element1.name = "timestamp";
    document.getElementById("logForm").appendChild(element1);

    var element2 = document.createElement("input");
    element2.type = "hidden";
    var dt = new Date()
    element2.value = dt.getTimezoneOffset();
    element2.name = "tzoffset";
    document.getElementById("logForm").appendChild(element2);

    document.getElementById("logForm").submit();
}

function get_selection(btn) {
  var old_select = document.getElementById("selection").value;
  document.getElementById("selection").value = btn.id;
  btn.style.background='#000000';
  console.log("New selection: " + btn.id);
  console.log("Old selection: " + old_select);
  try{
    document.getElementById(old_select).style.background="#4170f4";
  }
  catch(error){
    console.error(error);
  }
  //window.scrollTo(0,document.body.scrollHeight);  //vanilla js (no animate scroll)
  //setTimeout(function(){ $('html,body').animate({ scrollTop: 9999 }, 'slow'); }, 250);
  task_text()
}

function task_text() {
  // Declare variables
  var input, filter;
  input = document.getElementById('selection');
  filter = input.value.toUpperCase();

  var tasks = document.getElementsByClassName("btn btn-primary btn-lg sel");
  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < tasks.length; i++) {
    task = tasks[i];

      if (task.value.toUpperCase().indexOf(filter) > -1) {
          task.style.display = "";
      } else {
          task.style.display = "none";
      }
  }
}

function clear_sel(){
  document.getElementById('selection').value = '';
  task_text();
}