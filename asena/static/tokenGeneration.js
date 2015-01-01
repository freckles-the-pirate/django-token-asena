
// Default values

ASENA_TOKEN_GET_TOKEN_URL='/token/generate/'

function ajaxRequest(){
    // Thanks to http://tinyurl.com/5mmjcj for the boilerplate code!
    var activexmodes=["Msxml2.XMLHTTP", "Microsoft.XMLHTTP"]    //  activeX 
                                                                //  versions     
                                                                //  to check for
                                                                //  in IE
                                                                
    if (window.ActiveXObject){ //Test for support for ActiveXObject in IE first 
        (as XMLHttpRequest in IE7 is broken)
        for (var i=0; i<activexmodes.length; i++){
            try{
                return new ActiveXObject(activexmodes[i])
            }
            catch(e){
                //suppress error
            }
        }
    }
    else if (window.XMLHttpRequest) // if Mozilla, Safari etc
        return new XMLHttpRequest()
        else
            return false
}

//Sample call:
//var myajaxrequest=new ajaxRequest()

function generateAsenaToken(element_id){
    var mygetrequest=new ajaxRequest()
    
    // Set up a callback
    mygetrequest.onreadystatechange=function(){
        if (mygetrequest.readyState==4){
            if (mygetrequest.status==200 || 
                window.location.href.indexOf("http")==-1){
                // Do something
                }
            else{
                alert("An error has occured making the request");
            }
        }
    }
    // Open and send the request.
    mygetrequest.open("GET", "basicform.php?name="+namevalue+"&age="+agevalue, 
        true)
    mygetrequest.send(null)
}