//Callback functions
var error = function (err, response, body) {
    console.log('ERROR [%s]', err);
};
var success = function (data) {
    console.log('Data [%s]', data);
};

var Twitter = require('twitter-node-client').Twitter;

var data = {
    "consumerKey": "EEokGGuHWjTlmDDptF4rvUaOZ",
    "consumerSecret": "Illo1cVRLsmGiX9XyJe8Q5EQNvtaAIzmgEhWGuFAPmjgUhcaWd",
    "accessToken": "2716892042-ak58Dv8xvos1W27rqhQ46BhibT5KDyFe3zXIPxs",
    "accessTokenSecret": "E7gCBMNFhGizpbXqO5h7tOQQuzCaXgnebaDeV8AJxr2ac",
};

var token = null;
var oauth2 = new OAuth2(data.consumerKey, data.consumerSecret, 'https://api.twitter.com/', null, 'oauth2/token', null);
oauth2.getOAuthAccessToken('', {
    'grant_type': 'client_credentials'
  }, function (e, access_token) {
        token = access_token;
});

// make a directory in the root folder of your project called data
// copy the node_modules/twitter-node-client/twitter_config file over into data/twitter_config`
// Open `data/twitter_config` and supply your applications `consumerKey`, 'consumerSecret', 'accessToken', 'accessTokenSecret', 'callBackUrl' to the appropriate fields in your data/twitter_config file

var twitter = new Twitter();
var parameters = {user_name: "meganspecia", count:5000}
twitter.getFollowersIds(parameters, error, success);
















