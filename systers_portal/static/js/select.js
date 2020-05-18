$(document).ready(()=>{
    const optionlength = $('select > option').length;
    if(optionlength>1500){
      $('select').select2({
        minimumInputLength:1
      });
    }else{
      $('select').select2();
    }
});
