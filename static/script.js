// Function to generate a new chat bubble for a given message and sender
function generateChatBubble(message, sender) {
    var chatBubble = '<div class="d-flex flex-row justify-content-' + sender + ' mb-4">';
    if (sender == 'start') {
        chatBubble += '<div class="p-3 ms-3 chat-bubble-left">';
      } else {
        chatBubble += '<div class="p-3 me-3 border chat-bubble-right">';
      }
    chatBubble += '<p class="small mb-0">' + message + '</p>';
    chatBubble += '</div>';
    chatBubble += '</div>';
    return chatBubble;
}


// Wait for the document to be fully loaded before executing the code inside the callback function
$(document).ready(function() {

    // Attach a submit event handler to the chat form
    $('#chat-form').submit(function(event) {
      // Prevent the form from submitting normally
      event.preventDefault();
  
      // Get the user's message from the input field and generate a chat bubble
      var userMessage = $('textarea[name="input"]').val();
      var chatBubble = generateChatBubble(userMessage, 'end');
  
      // Append the chat bubble to the chat history
      $('#chat-history').append(chatBubble);
  
      // Set the focus back to the input field and scroll to the bottom of the chat history
      var inputField = $('textarea[name="input"]');
      inputField.focus();
      var chatHistory = $('#chat-history');
      chatHistory.animate({
        scrollTop: chatHistory[0].scrollHeight - chatHistory.height()
      }, 500);
  
      // Send an AJAX request to the chatbot endpoint
      $.ajax({
        url: '/chatbot',
        type: 'POST',
        data: $(this).serialize(),
        success: function(response) {
          // Get the chatbot's response and generate a chat bubble
          var chatbotMessage = response.output;
          var chatBubble = generateChatBubble(chatbotMessage, 'start');
  
          // Append the chat bubble to the chat history and scroll to the bottom
          $('#chat-history').append(chatBubble);
          var chatHistory = $('#chat-history');
          chatHistory.animate({
            scrollTop: chatHistory[0].scrollHeight - chatHistory.height()
          }, 500);
  
          // Clear the input field
          inputField.val('');
        }
      });
    });
  });
  