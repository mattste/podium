jQuery(document).ready(function($) {

	//mobile

	var $links = $('#primary-navigation');
    
    $('#toggle-menu').on('click',function(e){
      e.preventDefault();
      
      $links.toggleClass('show');
      
    });

});