// Update this variable to point to your domain.
var apigatewayendpoint = 'https://1163a5ieh5.execute-api.us-east-1.amazonaws.com/search-bug-test';
var loadingdiv = $('#loading');
var noresults = $('#noresults');
var resultdiv = $('#results');
var searchbox = $('input#form-search');
var button = $('input#bug_search');
var table = $('#table_id');
var timer = 0;

// Executes the search function 250 milliseconds after user stops typing
searchbox.keyup(function (e) {
  // let query = searchbox.val();
  if(e.keyCode==13){
  clearTimeout(timer);
  timer = setTimeout(search, 250);    
  }
});
button.click(function(){
  search();
});

async function search() {
  // Clear results before searching
  noresults.hide();
  table.empty();
  resultdiv.empty();
  loadingdiv.show();
  // Get the query from the user
  let query = searchbox.val();
  // Only run a query if the string contains at least three characters
  if (query.length > 2) {
    // Make the HTTP request with the query as a parameter and wait for the JSON results
    let response = await $.get(apigatewayendpoint, { q: query, size: 25 }, 'json');
    // Get the part of the JSON response that we care about
    let results = response['aggregations']['combine_commit']['buckets'];
    // let results = response['hits']['hits'];
    if (results.length > 0) {
      loadingdiv.hide();
      // Iterate through the results and write them to HTML
      resultdiv.append('<a href="https://www.google.com/">Found ' + results.length + ' results.</a>');
      table.append('<thead><tr><th>Rank</th><th>Score</th><th>CommitId</th><th>CommitMessage</th><th>CommitDate</th></tr></thead><tbody>');

      for (var item in results) {
        let Score = results[item].top_hit.value;
        let commitid = results[item].key;
        let count = results[item].doc_count;
        // let fileName = results[item]._source.file_name;
        let fileDate = results[item].top_commits.hits.hits[0]._source.file_date;
        let commitmsg = results[item].top_commits.hits.hits[0]._source.commit_msg;
        let packageLink = results[item].top_commits.hits.hits[0]._source.package_link;
        var score = jQuery.trim(Score).substring(0, 8);
        var commitMessage;
        var commitId = jQuery.trim(commitid).substring(0, 7);
        if(commitmsg.length>200){
          commitMessage = jQuery.trim(commitmsg).substring(0, 200)
          .split(" ").slice(0, -1).join(" ") + "...";}
        else {commitMessage = commitmsg;}
        // Construct the full HTML string that we want to append to the div
        table.append( '<tr><td>'+(++item)+'</td><td>'+score+'</td><td><a href='+packageLink+'/commits/'+commitid+' target="_blank" >' + commitId+'('+count+')' + '</a></td><td> '+commitMessage+'</td><td>' + fileDate + ' </td></tr>' );
      }
      table.append('</tbody>');
      // table.hide();
      // resultdiv.append(table);
      // $(document).ready( function () { s
        // table.DataTable();
        // } );
      
    } else {
      noresults.show();
    }
  }
  loadingdiv.hide();
}
