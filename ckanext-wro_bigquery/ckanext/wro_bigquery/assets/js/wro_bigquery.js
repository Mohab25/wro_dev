ckan.module("bigquery_dataset_view",function($){
    return{
        initialize:function(){
            let table = new DataTable('#bigquery_dataset_preview_table', function(){
                // options
            })            
        }
    }
})
