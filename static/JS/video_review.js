// getFetch()

function getFetch() {
  const canvasBgContainer = document.querySelector('.canvas-bg-container')

  // fetch는 JS 적용 불가...
  // fetch(window.location.href + '/chat/2/problems/1/reviews/2/')
  // fetch(window.location.href + '/reviews/1/')
  .fetch()
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

const btnProblems = document.querySelectorAll('.problem-list')

btnProblems.forEach(btn => {
  btn.addEventListener('click', (e) => {
    const problemId = e.target.value
    const reviewList = document.getElementById(`review-list-${problemId}`)

    reviewList.hidden = !reviewList.hidden
  })
})

const btnReviews = document.querySelectorAll('.review-list')
btnReviews.forEach(btn => {
  btn.addEventListener('click', (e) => {
    const reviewId = e.target.getAttribute('value')

    // axios({
    //   method: 'GET',
    //   url: `/chat/review/${reviewId}/`,
    // })
    //   .then(response => {
    //     const { Editor } = toastui;
    //     const { codeSyntaxHighlight } = Editor.plugin;

    //     const content = response.data.content
    //     const reviewView = document.getElementById('reviewViewer')

    //     console.log(JSON.stringify(content))
    //     reviewView.textContent = JSON.stringify(content)

    //     const viewer = Editor.factory({
    //       el: reviewView,
    //       viewer: true,
    //       height: '100%',
    //       initialValue: JSON.parse(reviewView.textContent),
    //       plugins: [codeSyntaxHighlight]
    //     });
    //   })
    //   .catch(error => {
    //     console.error(error)
    //   })
  })
})