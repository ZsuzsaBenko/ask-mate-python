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

    let score = 1;
    if (containsLowerAndUpperCase(pswdString)){
        score += 1;
    }
    if (containsSpecCharacter(pswdString)){
        score += 1;
    }
    if (containsNumber(pswdString)){
        score += 1;
    }

    const colors = {0: "red", 1: "darkorange", 2: "yellow", 3: "yellowgreen", 4: "green"};
    if (pswdString.length > 5) {
        colorRectangles(colors[score])
    } else {
        colorRectangles(colors[0])
    }
}