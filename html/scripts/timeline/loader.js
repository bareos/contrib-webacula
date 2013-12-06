
var tl;

function loadTimeline(data, date) {
	
	var jdate = date;
	var eventSource = new Timeline.DefaultEventSource();
	var jobtheme = Timeline.ClassicTheme.create();
  
	// Theme modification
	jobtheme.event.bubble.width = 350;
	jobtheme.event.bubble.height = 250;
	jobtheme.event.track.height = 30;
	jobtheme.event.tape.height = 16;
	jobtheme.autoWidth = true;

	var bandInfos = [
	
	  Timeline.createBandInfo({
	      eventSource:	eventSource,
	      date:		jdate,
	      theme:		jobtheme,
	      width:		"10%",
	      intervalUnit:	Timeline.DateTime.DAY,
	      intervalPixels:	100,
	      showEventText:	false,
	      overview:		true,
	      layout:		'overview'
	  }),
	  
	  Timeline.createBandInfo({
	      eventSource:	eventSource,
	      date:		jdate,
	      theme:		jobtheme,
	      layout:		'original', 			// original, detailed, overview
	      width:          	"80%", 
	      intervalUnit:   	Timeline.DateTime.HOUR, 
	      intervalPixels: 	200
	  }),
	  
	  Timeline.createBandInfo({
	      eventSource:	eventSource,
	      date:		jdate,
	      theme:		jobtheme,
	      width:		"10%",
	      intervalUnit:	Timeline.DateTime.MINUTE,
	      intervalPixels:	100,
	      showEventText:	true,
	      layout:		'original'
	  })
	  
	];
	
	bandInfos[0].syncWith = 1;
	bandInfos[0].highlight = true;
	bandInfos[1].syncWith = 2;
	bandInfos[1].highlight = true;
	
	tl = Timeline.create(document.getElementById("jobtimeline"), bandInfos);
	
   	tl.loadJSON(
	      
	      data, function(json, url) {
			    eventSource.loadJSON(json, url);
			}
	      );
	
	tl.finishedEventLoading(); // Automatically set new size of the div
	
}

var resizeTimerID = null;

function onResize() {

	if (resizeTimerID == null) {
         	resizeTimerID = window.setTimeout(function() {
             		resizeTimerID = null;
             		tl.layout();
         	}, 500);
     	}

}
