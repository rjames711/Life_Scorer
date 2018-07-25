$( "#cat_select" ).click(function() {
    $( "#categories" ).toggle();
});

//Converts the point value with compound units to a single unit qty
document.getElementById("taskForm").onsubmit = setPoints;

function setPoints(){
    points = document.getElementById('points').value;
    defaults = document.getElementsByClassName('default');
    scored = document.getElementsByClassName('scored');
    var defaults = [].slice.call(defaults)
    var scored = [].slice.call(scored)
    defUnitQty = 1
    for(i =0;i < scored.length ; i++){
        if(scored[i].value ==="1" ){
        defUnitQty*=defaults[i].value;
        console.log(scored[i]);
        }
    }
    newPoints = (points / defUnitQty);
    document.getElementById('points').value =  newPoints;
    return [newPoints, defUnitQty];
}


function get_selection(btn) {
  var old_select = document.getElementById("selection").value;
  
  document.getElementById("selection").value = btn.id;
  btn.style.background='#000000';
  console.log("Selected task: " + old_select);
  try{
    document.getElementById(old_select).style.background="#4170f4";
  }
  catch(error){
    console.error(error);
  }
  //window.scrollTo(0,document.body.scrollHeight);  //vanilla js (no animate scroll)
  setTimeout(function(){ $('html,body').animate({ scrollTop: 9999 }, 'slow'); }, 250);
}
var attr_num = 0;
function addAttribute(){
    attr_num += 1;
    attr_string = '<label for="attribute_name-' + attr_num + '">Attribute-' + attr_num + ' Name </label><br>' +
                '<input name="attribute_name-' + attr_num + '" id="attribute_name-' + attr_num + '" required><br>'+
                '<label for="min-' + attr_num + '">Min Value</label><br>' +
                '<input type="number" name="min-' + attr_num + '" id="min-' + attr_num + '" required><br>'+
                '<label for="max-' + attr_num + '">Max Value</label><br>' +
                '<input type="number" name="max-' + attr_num + '" id="max-' + attr_num + '" required><br>'+
                '<label for="default-' + attr_num + '" >Default Value</label><br>' +
                '<input type="number" class="default" name="default-' + attr_num + '" id="default-' + attr_num + '" required onkeyup="updateLabel()"><br>'+
                '<label for="scored-' + attr_num + '">Scored?</label><br>' +
                '<input type="number" class="scored" name="scored-' + attr_num + '" id="scored-' + attr_num + '" required><br>'+
                '<br>';
    document.getElementById('attributes').insertAdjacentHTML('beforeend', attr_string);
    updateLabel();
}

function updateLabel(){
    console.log('label paren');
    l=document.getElementById('pointLabel');
    l.innerHTML = "Point Value (Score if you did all the default values)";
}