$(document).ready(function () {
    // Setup - add a text input to each footer cell
    $('#example tfoot th').each(function () {
        var title = $(this).text();
        $(this).html('<input type="text" placeholder="Search ' + title + '" />');
    });
 
    // DataTable
    var table = $('#example').DataTable({
        initComplete: function () {
            // Apply the search
            this.api()
                .columns()
                .every(function () {
                    var that = this;
 
                    $('input', this.footer()).on('keyup change clear', function () {
                        if (that.search() !== this.value) {
                            that.search(this.value).draw();
                        }
                    });
                });
        },
    });
});

function myFunction() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("Patient");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }       
    }
  }

<script>
    $(document).ready(function(){
      $('#example thread tr')
        .clone(true)
        .addClass('filters')
        .appendTo('#example thread');

    var table = $('#example').DataTable({
      paging:true,
      pageLength:10,
      lengthChange:true,
      autoWidth:true,
      searching:true,
      bInfo:true,
      bSort:true,

      initComplete: function(){
        var api = this.api();

        api
            .columns([0,1,2,3,4,5])
            .eq(0)
            .each(function(colIdx)){
              var cell=$('.filters th').eq(
                $(api.column(colIdx).header()).index()
              );
              var title = $(cell).text();
              $(cell).html('<input type="text" placeholder="' + title + '"/>');

              $(
                'input',
                $('.filters th').eq($(api.column(colIdx).header()).index())
              )
              .off('keyip change')
              .on('keyup change', function(e)){
                e.stopPropagation();
                $(this).attr('title', $(this).val());
                var regxr = '({search})';

                var cursorPosition = this.selectionStart;

                api
                  .column(colIdx)
                  .search(
                        this.value !=''
                            ? regexr.replace('{search}','(((' + this.value + ')))')
                            :'',
                        this.value != '',
                        this.value ==''


                  )
                .draw();

              $(this)
                .focus()[0]
                .setSelectionRange(cursorPosition, cursorPosition);
              });
              .on('keyup', function (e) {
                e.stopPropagation();

                $(this).trigger('change');
                $(this)
                    .focus()[0]
                    .setSelectionRange(cursorPosition, cursorPosition);
            }
      }
    })
    })
  </script>