 var userInput = '{"name": "John", "age": 30}';
    var userObj;
    try {
        userObj = JSON.parse(userInput);  // Safely parse JSON without using eval
    } catch (e) {
        console.error("Invalid JSON input");
    }

    var userInput = "alert('Hello, world!')";
    eval(userInput);  // Unsafe
    var safe = 1243;
    document.getElementById('output').innerHTML = userInput;  // Unsafe
    document.write(userInput);  // Unsafe
