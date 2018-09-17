// JavaScript Document

var orange = [
    {
        value: 1,
        selected: true,
        imageSrc:'statics/images/statusorange.png'
    },
    {
        value: 2,
		selected: false,  
        imageSrc:'statics/images/statusgray.png'
    },
    {
        value: 3,
        selected: false,
        imageSrc:'statics/images/statusblue.png'
    }
];

var gray = [
    {
        value: 1,
        selected: false,
        imageSrc:'statics/images/statusorange.png'
    },
    {
        value: 2,
		selected: true,
        imageSrc:'statics/images/statusgray.png'
    },
    {
        value: 3,
        selected: false,
        imageSrc:'statics/images/statusblue.png'
    }
];

var blue = [
    {
        value: 1,
        selected: false,
        imageSrc:'statics/images/statusorange.png'
    },
    {
        value: 2,
		selected: false,
        imageSrc:'statics/images/statusgray.png'
    },
    {
        value: 3,
        selected: true,
        imageSrc:'statics/images/statusblue.png'
    }
];

$('.myDropdownorange').ddslick({
    data:orange,
    width:50,
    selectText: "Select your preferred social network",
    imagePosition:"right",
    onSelected: function(selectedData){
        //callback function: do something with selectedData;
    }   
});

$('.myDropdowngray').ddslick({
    data:gray,
    width:50,
    selectText: "Select your preferred social network",
    imagePosition:"right",
    onSelected: function(selectedData){
        //callback function: do something with selectedData;
    }   
});

$('.myDropdownblue').ddslick({
    data:blue,
    width:50,
    selectText: "Select your preferred social network",
    imagePosition:"right",
    onSelected: function(selectedData){
        //callback function: do something with selectedData;
    }   
});

/////////////////////////////this is where the pref box for availabilites is coded///////

var check = [
    {
        value: 1,
        selected:true,
        imageSrc:'statics/images/check.png'
    },
    {
        value: 2,
		selected: false,
        imageSrc:'statics/images/circle.png'
    },
    {
        value: 3,
        selected: false,
        imageSrc:'statics/images/warning.png',
		description: "Doesn't matter"
    }
];

var circle = [
    {
        value: 1,
        selected: false,
        imageSrc:'statics/images/check.png'
    },
    {
        value: 2,
		selected: true,
        imageSrc:'statics/images/circle.png'
    },
    {
        value: 3,
        selected: false,
        imageSrc:'statics/images/warning.png',
		description: "Doesn't matter"
    }
];

var warning = [
    {
        value: 1,
        selected: false,
        imageSrc:'statics/images/check.png'
    },
    {
        value: 2,
		selected: false,
        imageSrc:'statics/images/circle.png'
    },
    {
        value: 3,
        selected: true,
        imageSrc:'statics/images/warning.png',
		
		
    }
];

$('.myDropdowncheck').ddslick({
    data:check,
    width:50,
    selectText: "c",
    imagePosition:"right",
    onSelected: function(selectedData){
        //callback function: do something with selectedData;
    }   
});

$('.myDropdowncircle').ddslick({
    data:circle,
    width:50,
    selectText: "Select your preferred social network",
    imagePosition:"right",
    onSelected: function(selectedData){
        //callback function: do something with selectedData;
    }   
});

$('.myDropdownwarning').ddslick({
    data:warning,
    width:50,
    selectText: "Select your preferred social network",
    imagePosition:"right",
    onSelected: function(selectedData){
        //callback function: do something with selectedData;
    }   
});