<iframe
  sandbox="allow-scripts allow-same-origin allow-popups allow-downloads allow-top-navigation allow-top-navigation-by-user-activation"
  style="right: 0; position: fixed; bottom: 0; display: flex; align-self: flex-end; background-color: transparent; border-width: 0px; colorScheme: light;"
  id="adam-chat"
  title="chat live"
  src="https://app.startadam.com/adam-prd/adam-livechat-widget/index.html?channelKey=3G1SMG8SUG27I42Q2QF&integrationInteface=https://app.startadam.com/adam-prd/adam-integration-interface-prd&companyName=Web4app&transparent=0&linkChat=https://a.link/web4app&initialMessage=&imageUrl=&agentName=&userIcon=">
 </iframe>
<script>
window.onload = function () {
  const iframe = document.getElementById("adam-chat").contentWindow;
  const message = getChatStyles();

  iframe.postMessage(message, "*");
};

function getChatStyles() {
  return {
    color: {
      agentTextColor: "#f0fdff",
      agentTextBackground: "#2e0917",
      userTextColor: "#f7f7f7",
      userTextBackground: "#000000", // Initialize with a default color
      chatBackground: "#17170a",
      chatBoxForm: "#151824",
    },
  };
}

function notifyMe(noti) {
  if (Notification.permission === 'granted') {
    showNotification(noti);
  } else if (Notification.permission !== 'denied') {
    Notification.requestPermission().then(function(permission) {
      if (permission === 'granted') {
        showNotification(noti);
      }
    });
  }
}

function showNotification(message) {
  new Notification('Live chat - RODAAi', {
    body: message,
  });
}

window.onmessage = function(e) {
  e.preventDefault();
  if (e.data.message === 'chat') {
    updateIframeSize(e.data.class);
  } else if (e.data.message === 'notify') {
    notifyMe(e.data.notification);
  }
}

function updateIframeSize(displayClass) {
  const iframe = document.getElementById('adam-chat');
  if (displayClass === 'hidden') {
    iframe.style.maxWidth = '95px';
    iframe.style.width = '100%';
    iframe.style.height = '95px';
  } else {
    iframe.style.height = '95%';
    iframe.style.width = '100%';
    iframe.style.maxWidth = '469px';
  }
}
</script>
