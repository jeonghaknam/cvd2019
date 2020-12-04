$(document).ready(function(){
  $('.data-table').dataTable({
    "searching": true,
    "paging": true,
    "iDisplayLength": 30,
    "lengthChange": false,
    "info": false,

    "columnDefs": [{
		"targets": 'nosort',
		"orderable": false
    }],
	"order": [[ 1, "desc" ]]
  });
});