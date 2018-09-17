// JavaScript Document

var ddData = [
    {
        value: 1,
        selected: false,
        imageSrc:"statusorange.png"
    },
    {
        value: 2,
		selected: false,
        imageSrc:"statusgray.png"
    },
    {
        value: 3,
        selected: true,
        imageSrc:"statusblue.png"
    }
];
$('.myDropdown').ddslick({
    data:ddData,
    width:50,
    selectText: "Select your preferred social network",
    imagePosition:"right",
    onSelected: function(selectedData){
        //callback function: do something with selectedData;
    }
   
}
);

$('.myDropdown2').ddslick({
    data:ddData,
    width:50,
    selectText: "Select your preferred social network",
    imagePosition:"right",
    onSelected: function(selectedData){
        //callback function: do something with selectedData;
    } });