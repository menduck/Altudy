const reviewSearchInput = document.querySelector('.review-search-input')
const reviewSearchList = document.querySelector('.review-list')
const usernameContainer  = document.querySelector('.username-container')
const username = usernameContainer.getAttribute('data-username')

reviewSearchInput.addEventListener('input', debounce(async (e) => {
  const query = reviewSearchInput.value.trim();
  console.log(query)
  try {
    const response = await fetch(`/accounts/profile/${username}/?query=${query}`)
    console.log(response)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const html = await response.text()
    const parser = new DOMParser()
    const doc = parser.parseFromString(html, 'text/html')
    const reviews = doc.querySelector('.review-list')
    reviewSearchList.innerHTML = reviews.innerHTML;

  } catch (error) {
    console.log(error)
  }
}, 100))


// input 이벤트 지연을 위한 debonce 함수
// 한글 타이핑을 빠르게 쳤을 때 마지막 input 이벤트처리가 안 되는 경우가 있어서 추가
function debounce(func, delay) {
  let timeoutId;

  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
}