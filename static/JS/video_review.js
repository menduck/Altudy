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

const btnProblems = document.querySelectorAll('.problem-list')

btnProblems.forEach(btn => {
  btn.addEventListener('click', (e) => {
    const problemId = e.target.value
    const reviewList = document.getElementById(`review-list-${problemId}`)

    reviewList.hidden = !reviewList.hidden
  })
})


// 참가자 리스트 액션
const userListContainer = document.querySelector('.user-list-container')
const btnOpenUser = document.querySelector('.user-list-open-btn')
const btnCloseUser = document.querySelector('.user-list-close-btn')

btnOpenUser.addEventListener('click', (e) => {
  userListContainer.hidden = !userListContainer.hidden
  btnCloseUser.disabled = false
  btnOpenUser.hidden = !btnOpenUser.hidden
  btnOpenUser.disabled = true
})
btnCloseUser.addEventListener('click', () => {
  userListContainer.hidden = !userListContainer.hidden
  btnCloseUser.disabled = true
  btnOpenUser.hidden = !btnOpenUser.hidden
  btnOpenUser.disabled = false
})