// Default values

console.log("Hello, world!");

ASENA_TOKEN_GET_TOKEN_URL='/token/generate';

function ajaxRequest(){
    // Thanks to http://tinyurl.com/5mmjcj for the boilerplate code!
    var activexmodes=["Msxml2.XMLHTTP", "Microsoft.XMLHTTP"]    //  activeX 
                                                                //  versions     
                                                                //  to check for
                                                                //  in IE
                                                                
    if (window.ActiveXObject){ //Test for support for ActiveXObject in IE first 
                                // (as XMLHttpRequest in IE7 is broken)
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

/**
 * Get the parent element of the element.
 * Recursively get the parent until either the parent or the "BODY" 
 * element is reached. See http://tinyurl.com/kngq4 for parentNode details and
 * http://tinyurl.com/kngq4 for nodeName details.
 * @name getParent
 * @param element The HTML DOM element
 * @param tag The tag name, e.g. "FORM". Must be in upper-case to comply with
 *            W3C standards.
 * @return The parent element, or ``null`` if not found.
 **/
function getParent(element, tag){
    parent = element.parentNode;
    if (parent.nodeName == "BODY") {
        console.warn("getParent(): Reached body. Tag %s not found", tag);
        return null;
    } else if (parent.nodeName == tag) {
        console.log("getParent(): `%s' found. Returning", tag);
        return parent;
    }
    console.log("Getting parent for %s", element.nodeName)
    return getParent(parent, tag);
}

function getChild(element, name){
//     nm = element.getAttribute("name");
    console.log("Checking if %s == %s", element.getAttribute("name"),
        name );
    if (element.getAttribute("name") == name)
        return element;
    for (var i = 0; i < element.children.length; ++i){
        c = getChild(element.children[i], name);
        if (c != null){
            console.log("Found child %s", c);
            return c;
        }
    }
    console.warn("Child %s not found from %s", name, element);
    return null;
}

function fillSelectList(field, stringResult){
    var results = stringResult.split(',');
    console.log("Filling with %d results", results.length);
    // First, clear the list.
    field.innerHTML = "";
    for (var i = 0; i < results.length; ++i){
        res = results[i];
        option = '<option value="' + res + '">' + res + '</option>\n';
        console.log("Appending %s to element.", option);
        field.innerHTML = field.innerHTML + option;
    }
}

function generateAsenaTokens(element_id){
    
    var button = document.getElementById(element_id);
    var parentForm = getParent(button, "FORM");
    
    var selectField = getChild(parentForm, "SELECT");
    
    if (selectField == null){
        console.error("selectField is null! Stopping...");
        return;
    }
    
    var mygetrequest=new ajaxRequest();
    
    // Set up a callback
    mygetrequest.onreadystatechange=function(){
        if (mygetrequest.readyState==4){
            if (mygetrequest.status==200 || 
                window.location.href.indexOf("http")==-1){
                    console.log("Got response: %s", mygetrequest.responseText);
                    fillSelectList(selectField, mygetrequest.responseText)
                }
            else{
                alert("An error has occured making the request");
            }
        }
    }
    
    // Get the values from the fields. This will require a bit of detective
    // work. We need to find the elements by id instead of name since the ID 
    // may change from form to form.
    
    var count = getChild(parentForm, "count").value;
    var length = getChild(parentForm, "length").value;
    
    if (count == null)
        count = '';
    if (length == null)
        length = '';
    
    console.log("Count is %d and length is %d", count, length);
    
    // Open and send the request.
    requestUrl = ASENA_TOKEN_GET_TOKEN_URL + "/" + count + "/" + length;
    console.log("Querying %s", requestUrl);
    mygetrequest.open("GET", requestUrl, true);
    mygetrequest.send(null);
}