window.fbAsyncInit = function() {
    FB.init({
      appId      : '1051951819832687',  // app id
      cookie     : true,
      xfbml      : true,
      version    : 'v12.0'  // Replace with the API version you're using
    });
  
    FB.AppEvents.logPageView();   
  };
  
  (function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "https://connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));
  