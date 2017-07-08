var i = 0;
var action_array=[];
var weburl_array=[];
var filename_array=[];
var startTime = "";

function printlist(weburl, action) {
  if (action == "Check Speed" || action == "Check Quota"){
    $('#list_of_actions').append('<li class="delete_action"><span class="fa fa-trash" aria-hidden="true"></span>' + " " + action + '</li>')
  }
  else {
    $('#list_of_actions').append('<li class="delete_action"><span class="fa fa-trash" aria-hidden="true"></span>' + " " + action + " " + weburl + '</li>')
  }
};

function printlog(date, weburl, action) {
  if (action == "Check Speed" || action == "Check Quota"){
    $('#logs').append('<li> Time Stamp: ' + date + ' - ' + action + '</li>')
  }
  else {
    $('#logs').append('<li> Time Stamp: ' + date + ' - ' + action + ' ' + weburl + '</li>')
  }
};

$('#add').on("click", function(e) {
  var weburl = $('#web_url').val();
  var action = $('#action').val();
  var filename = $('#filename').val();
  weburl_array[i] = weburl;
  action_array[i] = action;
  filename_array[i] = filename;
  i++;
  printlist(weburl,action);
});

$('#check_speed').on("click", function(e) {
  var weburl = "";
  var action = "Check Speed";
  var filename = "";
  weburl_array[i] = weburl;
  action_array[i] = action;
  filename_array[i] = filename;
  i++;
  printlist(weburl,action);
});

$('#check_quota').on("click", function(e) {
  var weburl = "";
  var action = "Check Quota";
  var filename = "";
  weburl_array[i] = weburl;
  action_array[i] = action;
  filename_array[i] = filename;
  i++;
  printlist(weburl,action);
});

$('#list_of_actions').on("click", "li.delete_action", function() {
  //console.log("hellos");
  var index = $(this).parent().children().index(this);
  weburl_array.splice(index,1);
  action_array.splice(index,1);
  filename_array.splice(index,1);
  if (weburl_array.length == 0){
    i = 0;
  };
  console.log(action_array);
  $('#list_of_actions').text("");
  for (var k=0; k < weburl_array.length; k++) {
    printlist(weburl_array[k], action_array[k]);
  };
});

$('#clear').on("click", function(e) {
  $('#list_of_actions').text("");
  action_array=[];
  weburl_array=[];
  filename_array=[];
  i=0;
});

function runCheckQuotaPyScript(msisdn){
  var jqXHR = $.ajax({
    type: "POST",
    url: "/check_quota",
    async: false,
    data: { param: msisdn }
  });

  return jqXHR.responseText;
}

function runDownloadSpeedPyScript(){
  var jqXHR = $.ajax({
    type: "POST",
    url: "/check_speed",
    async: false,
  });

  return jqXHR.responseText;
}

function runDownloadPyScript(url){
  var jqXHR = $.ajax({
    type: "POST",
    url: "/download",
    async: false,
    data: { param: url }
  });

  return jqXHR.responseText;
}

function runWatchPyScript(url){
  var jqXHR = $.ajax({
    type: "POST",
    url: "/watch",
    async: false,
    data: { param: url }
  });

  return jqXHR.responseText;
}

$("#start_test").on("click", function (e) {
  for(j = 0; j < weburl_array.length; j++) {
    startTime = new Date(Date.now()).toString();
    if(action_array[j] == "Download") {
      /*$('<a/>', {
         //"href": "http://digiretail.azurewebsites.net/video/twilight.mp4",
         http://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_30mb.mp4
         http://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_10mb.mp4
         "href": weburl_array[j],
         //"download": "twilight.mp4",
         "download": filename_array[j],
         id: "videoDownloadLink"
      }).appendTo(document.body);
      $('#videoDownloadLink').get(0).click();
      $('#videoDownloadLink').remove();*/
      console.log("Download File");
      download = runDownloadPyScript(weburl_array[j]);
      download = download.substring(12,download.length-1);
      download = download.replace(/\n/g, '<br />');
      $('#balance_quota').append(download);
    }
    if(action_array[j] == "Watch") {
      //https://www.youtube.com/watch?v=ZmvqTMyaCTo
      //https://www.youtube.com/watch?v=5HK3dwZj5BU&index=5&list=PLksfvoW6DFdPlvDxXQA5svF4ef9hGKXux
      //https://www.youtube.com/watch?v=bZazPMzBA0I
      console.log("Watch Video");
      watch = runWatchPyScript(weburl_array[j]);
      watch = watch.substring(12,watch.length-1);
      watch = watch.replace(/\n/g, '<br />');
      $('#balance_quota').append(watch);
    }
    else if(action_array[j] == "Check Speed") {
      console.log("Check Speed");
      speed = runDownloadSpeedPyScript();
      speed = speed.substring(12,speed.length-1);
      console.log('Got back ' + speed);
      speed = speed.replace(/\n/g, '<br />');
      $('#balance_quota').append(speed);
    }
    else if(action_array[j] == "Check Quota") {
      console.log("Check Quota");
      var msisdn = $('#msisdn').val();
      console.log(msisdn);
      quota_balance = runCheckQuotaPyScript(msisdn);
      quota_balance = quota_balance.substring(12,quota_balance.length-1);
      console.log('Got back ' + quota_balance);
      quota_balance = quota_balance.replace(/\n/g, '<br />');
      $('#balance_quota').append(quota_balance);
    }
    else {
      window.open(weburl_array[j], '_blank');
    }
    printlog(startTime, weburl_array[j], action_array[j])
  }
});
