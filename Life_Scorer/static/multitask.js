//Selection of task button sets up for selection of another task
var sel = document.getElementById("selection");

function multitask(btn){
    $(".picker.button").show()
    console.log("something");
    
    sel.value+='&';
    sel.focus();
  }
  

  function selectTask(btn){
      $('.picker.button').hide();
      document.getElementById(btn.id).style.display=''; //show
      
      var sels = sel.value.split('&');
      sels[sels.length-1] = btn.id;
      sel.value = sels.join('&');
  }

  function clear_sel(){
    document.getElementById('selection').value='';
    $(".picker.button").show()
    sel.focus();
  }