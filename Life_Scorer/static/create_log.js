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
            document.getElementById(old_select+'-edit').style.display = 'none';
        }
    }
    catch(error){
        console.error(error);
    }
    task_text()
    populateForms(taskName);
    old_select = taskName;
    $('.picker').hide();
    document.getElementById(btn.id).style.display='inline';
    document.getElementById(btn.id+'-edit').style.display='inline';
    document.getElementById(btn.id+'-history').style.display='inline';
    document.getElementById(btn.id+'-graph').style.display='inline';
    document.getElementById(btn.id+'-edit').style.background='orange';
    document.getElementById(btn.id+'-history').style.background='orange';
    document.getElementById(btn.id+'-graph').style.background='orange';
    
    console.log(btn.id)
}

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

//Loop over and restyle elements. Better to just use css but leaving it for now in case I want it later
function re_style(){
    var tasks = document.getElementsByClassName("inline button");
    for (i = 0; i < tasks.length; i++) {
        task = tasks[i];
        if (task.id.split('_')[0] === "!"){
            task.style.background = "red";
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


function populateForms(taskName){
    var vForm = document.getElementById('variableForm');
    vForm.innerHTML='';
    var task = attr[taskName];
    for (var attribute in task){
        console.log(attribute);
        var label = document.getElementById("tempAttrLabel").cloneNode(true);
        label.id = "attrLabel"+attribute;
        var numIn = document.getElementById("tempNumIn").cloneNode(true);
        numIn.id = "numIn"+attribute;
        numIn.name = attribute;
        numIn.value = task[attribute]['default'];
        label.textContent = attribute.toUpperCase();
        var submitBtn = document.getElementById("submitBtn").cloneNode(true);
        //increment and decrement buttons
        var p = document.getElementById("p").cloneNode(true);
        var pp = document.getElementById("pp").cloneNode(true);
        var m = document.getElementById("m").cloneNode(true);
        var mm = document.getElementById("mm").cloneNode(true);
        //closure to bind button controls to right number input.
        function connect_button(numin,attribute,minmax,posneg){
            //var numin = numin; //apparrently unnecessary to bind variable
            function connect(){
                let newval=parseFloat(numin.value) + posneg * parseFloat(task[attribute][minmax]); 
                let prec=10000 //rounding precision
                newval = Math.round(newval*prec)/prec; //prevents num readin x.999999999 after a few pushes
                numin.value=newval;
            }
            return connect; 
        }        
        p.addEventListener('click', connect_button(numIn,attribute, 'min', 1));
        pp.addEventListener('click', connect_button(numIn,attribute,  'max', 1));
        m.addEventListener('click', connect_button(numIn,attribute, 'min', -1));
        mm.addEventListener('click', connect_button(numIn,attribute, 'max', -1));

        //Wrapping each form input in div to seperate.
        var div = document.createElement("div");
        vForm.appendChild(div);
        div.appendChild(label);
        div.appendChild(document.createElement('br'));
        div.appendChild(mm);
        div.appendChild(m);
        div.appendChild(numIn);
        div.appendChild(p);
        div.appendChild(pp);

    }
    var notes = document.getElementById("tempNotes").cloneNode(true);
    var submitBtn = document.getElementById("submitBtn").cloneNode(true);
    vForm.appendChild(notes);
    vForm.appendChild(document.createElement('br'));
    vForm.appendChild(submitBtn);
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
            window.location.href="show_log/50";
        }
        if(end < start - offset ){
            window.location.href="show_log/50";
        }
    }
});
//End swipe implementation


$(window).keydown(function(event) {
  if(event.altKey && event.keyCode == 13) {  //cntrl-enter
    console.log("Alt-enter caught, submitting form");
    event.preventDefault(); 
  	submitForm();
  }});

$(window).keydown(function(event) {
  if(event.altKey && event.keyCode == 49) {  //cntrl-enter
    console.log("Alt-1 caught, toggling");
    event.preventDefault(); 
    toggleTop();
}}); 

$(window).keydown(function(event) {
  if(event.altKey && event.keyCode == 50) {  //cntrl-enter
    console.log("Alt-2 caught, show log");
    event.preventDefault(); 
    window.location.href="show_log/50";
}}); 

$(window).keydown(function(event) {
  if(event.altKey && event.keyCode == 115) {  //cntrl-enter
    console.log("Alt-s caught, show log");
    event.preventDefault(); 
    event.stopPropagation();
    window.location.href="show_log/50";
}});

