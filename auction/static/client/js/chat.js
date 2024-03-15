document.addEventListener('DOMContentLoaded', function (event) {
  console.log('chat init');
  let location = window.location;
  let wsStart = 'ws://';

  if (location.protocol === 'https') {
    wsStart = 'wss://';
  }

  var currentUrl = location.href;
  var urlParts = currentUrl.split('/');
  var otherUserId = urlParts[urlParts.length - 2];
  console.log(otherUserId);
  const urlChat =
    wsStart + location.host + `/ws/chat/` + otherUserId + '/';

  const requestUser = JSON.parse(
    document.getElementById('request-user').textContent
  );

  const chatSocket = new WebSocket(urlChat);

  chatSocket.onopen = async function (e) {
    console.log('open', e);
  };

  // when data is received
  chatSocket.onmessage = async function (e) {
    console.log('message', e);

    const data = JSON.parse(e.data);
    const chat = document.getElementById('chat-messages');
    const dateOptions = { hour: 'numeric', minute: 'numeric', hour12: true };
    const datetime = new Date(data.datetime).toLocaleString('en', dateOptions);
    const isMe = data.sender === requestUser;
    const source = isMe ? 'chat-message-right' : ' chat-message-left';
    const name = isMe ? 'Me' : data.fullName;

    chat.innerHTML += `
      <div class="pb-4 ${source}">
            <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
              <div class="font-weight-bold mb-1">
              ${name}
              </div>
              ${data.message}
              <div class="text-muted small text-nowrap mt-2">
              ${datetime}
              </div>
            </div>
        </div>`;
    chat.scrollTop = chat.scrollHeight;
  };

  chatSocket.onerror = async function (e) {
    console.log('error', e);
  };

  chatSocket.onclose = async function (e) {
    console.error('Chat socket closed unexpectedly', e);
  };

  const messageInput = document.getElementById('chat-message-input');
  const loggedInUserId = document.getElementById('logged-in-userid');

  const messageSubmitButton = document.getElementById('chat-message-submit');
  messageSubmitButton.addEventListener('click', function (event) {
    const message = messageInput.value;
    if (message) {
      console.log(message);

      // send message in JSON format
      chatSocket.send(
        JSON.stringify({
          message: message,
          sender: requestUser,
        })
      );
      // clear messageInput
      console.log('message sent');
      messageInput.value = '';
      messageInput.focus();
    }
  });

  messageInput.addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
      // cancel the default action, if needed
      event.preventDefault();
      // trigger click event on button
      messageSubmitButton.click();
    }
  });

  messageInput.focus();
});
