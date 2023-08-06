//Declared variables
const btnEl = document.getElementById("btn");
const jokeEl = document.getElementById("joke");
const emailEl = document.getElementById("email");
const apiURL = "API_URL_FROM_API-NINJAS";
const apiKey = "API_KEY_FROM_API-NINJAS";
const functionURL = "LAMBDA_FUNCTION'S_URL/?"
const options = {
  method: "GET",
  headers: {
    "X-Api-Key": apiKey,
  },
};

//Asynchronous function
async function getJoke() {
  //If everything works
  try {
    //After click but before the joke appears
    jokeEl.innerText = "Updating...";
    btnEl.disabled = true;
    btnEl.innerText = "Loading...";
    const response = await fetch(apiURL, options);
    const data = await response.json();

    //Uncomment below to view the email data in the console
    //console.log(emailEl.value);

    //Reset page and display joke
    btnEl.disabled = false;
    btnEl.innerText = "Tell me a joke";
    const noPlusEmail = emailEl.value;          //Saved value before page reset
    emailEl.value = '';
    jokeEl.innerText = data[0].joke;
    const jokeLambda = jokeEl.innerText.replaceAll(' ', '$$$');         //Passed value
    const emailLambda = noPlusEmail.replaceAll('+', '$$$');             //Passed value


    //Uncomment below to view the joke, email, or URL version of the joke in the console
    //console.log(data[0].joke);
    //console.log(emailLambda);
    //console.log(jokeLambda);

    //Call the Lambda Function URL and pass variables
    sendToLambda = functionURL + 'emailLambda=' + emailLambda + '&jokeLambda=' + jokeLambda;
    //console.log(sendToLambda);
    fetch(sendToLambda);

  //If there are errors, reset page and console log
  } catch (error) {
    jokeEl.innerText = "An error happened, try again later";
    btnEl.disabled = false;
    btnEl.innerText = "Tell me a joke";
    emailEl.value = '';
    console.log(error);

  }
}

//Click action
btnEl.addEventListener("click", getJoke);