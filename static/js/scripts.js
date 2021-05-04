$(document).ready( function () {
    $('#tableIndex')
        .addClass( 'nowrap' )
        .dataTable( {
            responsive: true,
            language: {
                url: 'https://cdn.datatables.net/plug-ins/1.10.24/i18n/Spanish.json'
            },
            columnDefs: [
                { targets: [-1, -3], className: 'dt-body-right' }
            ]
        } );
} );


