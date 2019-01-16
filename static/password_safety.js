function colorRectangles(color){
    let safeClass = document.getElementsByClassName('safe');
    for (let i = 0; i < safeClass.length; i++){
            safeClass[i].style.backgroundColor = color;
        }
}


function containsNumber(string){
    for (let i = 0; i < string.length; i++){
        if (Number(string[i])){
            return true
        }
    }
    return false
}


function containsSpecCharacter(string){
    const specCharacters = ".,;:?!'-_&@#/()*";
    for (let i = 0; i < string.length; i++){
        for (let j = 0; j < specCharacters.length; j++){
            if (string[i] === specCharacters[j]) {
                return true
            }
        }
    }
    return false
}


function containsLowerAndUpperCase(string){
    return string.toLowerCase() !== string && string.toUpperCase() !== string
}


function measureSafety(){
    let password = document.getElementById('password');
    let pswdString = password.value;
    console.log(pswdString.length);

    if (pswdString.length > 5 && containsLowerAndUpperCase(pswdString) && containsNumber(pswdString)
        && containsSpecCharacter(pswdString)){
        colorRectangles("green")
    }
    else if (pswdString.length > 5 && containsLowerAndUpperCase(pswdString) && containsNumber(pswdString) ||
             pswdString.length > 5 && containsLowerAndUpperCase(pswdString) && containsSpecCharacter(pswdString) ||
             pswdString.length > 5 && containsNumber(pswdString) && containsSpecCharacter(pswdString)){
        colorRectangles("yellowgreen")
    }
    else if (pswdString.length > 5 && containsLowerAndUpperCase(pswdString) ||
             pswdString.length > 5 && containsNumber(pswdString) ||
             pswdString.length > 5 && containsSpecCharacter(pswdString)) {
        colorRectangles("yellow")
    }
    else if (pswdString.length > 5){
        colorRectangles("darkorange")
    }
    else {
        colorRectangles("red")
    }

}