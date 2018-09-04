var select = document.getElementById("selection");
select.focus();
var t = 'test';
var old_select=''

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
  taskName = btn.id;
  document.getElementById("selection").value = taskName;
  btn.style.background='white';
  console.log("New selection: " + taskName);
  console.log("Old selection: " + old_select);
  try{
    if(old_select){
    document.getElementById(old_select).style.background="#4170f4";
    }
  }
  catch(error){
    console.error(error);
  }
  task_text()
  populateForms(taskName);
  old_select = taskName;
}

function task_text() {
  // Declare variables
  var input, filter;
  input = document.getElementById('selection');
  filter = input.value.toUpperCase();

  var tasks = document.getElementsByClassName("inline button");
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
}

function hideTop(){
  var elements = document.getElementsByClassName('top');
    for (var i = 0; i < elements.length; i++){
        elements[i].style.display = 'none';
    }
}


function populateForms(taskName){
  var vForm = document.getElementById('variableForm');
  vForm.innerHTML='';
  var task = attr[taskName];
  for (var attribute in task){
    console.log(attribute);
    var label = document.getElementById("tempAttrLabel").cloneNode(true);
    label.id = "attrLabel"+attribute;
    var slider = document.getElementById("tempSlider").cloneNode(true);
    slider.id = "slider"+attribute;
    var numIn = document.getElementById("tempNumIn").cloneNode(true);
    numIn.id = "numIn"+attribute;
    numIn.name = attribute;
    slider.min = task[attribute]['min'];
    slider.max = task[attribute]['max'];
    slider.value = task[attribute]['default'];
    numIn.value = task[attribute]['default'];
    label.textContent = attribute;
    var submitBtn = document.getElementById("submitBtn").cloneNode(true);
    vForm.appendChild(label);
    vForm.appendChild(slider);
    vForm.appendChild(numIn);
    //Closure so slider function bind to right num input
    function makeFunc(numIn) {
      var numIn = numIn; 
      function func() {
        numIn.value = this.value;
      }
      return func;
    }
    var slide = makeFunc(numIn);
    slider.oninput = slide;
  }
  var notes = document.getElementById("tempNotes").cloneNode(true);
  notes
  vForm.appendChild(notes);
   vForm.appendChild(submitBtn);
}


