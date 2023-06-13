// getFetch()

function getFetch() {
  const canvasBgContainer = document.querySelector('.canvas-bg-container')

  // fetch는 JS 적용 불가...
  // fetch('http://127.0.0.1:8000/chat/2/problems/1/reviews/2/')
  fetch('http://127.0.0.1:8000/reviews/1/')
    .then(response => response.text())
    .then(content => {
      canvasBgContainer.innerHTML = content
    })
}

const btnChatClose = document.getElementById('chat-close-btn')
const btnChatOpen = document.getElementById('chat-open-btn')
const chatContainer = document.getElementById('chat-container')

btnChatClose.addEventListener('click', (e) => {
  chatContainer.hidden = true
  btnChatOpen.hidden = false

  const videoContainer = document.getElementById('video-container')
  const controllerContainer = document.querySelector('.room-controller-container')
  videoContainer.style.marginRight = 0
  controllerContainer.style.marginRight = 0
})
btnChatOpen.addEventListener('click', (e) => {
  chatContainer.hidden = false
  btnChatOpen.hidden = true

  const videoContainer = document.getElementById('video-container')
  const controllerContainer = document.querySelector('.room-controller-container')
  
  if (window.innerWidth > 1300) {
    videoContainer.style.marginRight = "20%"
    controllerContainer.style.marginRight = "20%"
  } else {
    videoContainer.style.marginRight = "30%"
    controllerContainer.style.marginRight = "30%"
  }
})

const btnReviewClose = document.querySelector('.review-controller-close-btn')
const btnReviewOpen = document.querySelector('.review-controller-open-btn')
const reviewContainer = document.querySelector('.review-controller-container')

btnReviewClose.addEventListener('click', (e) => {
  reviewContainer.hidden = true
  btnReviewClose.disabled = true
  btnReviewOpen.hidden = false
  btnReviewOpen.disabled = false
})
btnReviewOpen.addEventListener('click', (e) => {
  btnReviewOpen.hidden = true
  btnReviewOpen.disabled = true
  reviewContainer.hidden = false
  btnReviewClose.disabled = false
})