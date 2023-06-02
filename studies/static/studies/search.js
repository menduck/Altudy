const probSearchInput = document.querySelector('#prob-search-input')
const probSearchList = document.querySelector('#prob-search-list')

const displayResults = (results) => {
  // 기존의 검색 결과 제거
  probSearchList.innerHTML = ''
  const ulElement = document.createElement('ul')

  if (results.length === 0) {
    // 검색 결과가 없는 경우
    displayNoResults()
    return
  }

  // 결과를 화면에 표시
  results.forEach((result) => {
    const liElement = document.createElement('li')
    const problemLink = document.createElement('a')
    problemLink.href = `http://127.0.0.1:8000/reviews/${result.id}/`
    problemLink.textContent = result.title;
    liElement.appendChild(problemLink)
    ulElement.appendChild(liElement)
  })
  probSearchList.appendChild(ulElement)
}


// 검색 결과가 없을 경우
const displayNoResults = () => {
  // 기존의 검색 결과 제거
  probSearchList.innerHTML = ''

  // 검색 결과가 없는 문구 생성
  const noResultsMessage = document.createElement('p')
  noResultsMessage.textContent = '검색 결과가 없습니다.'
  probSearchList.appendChild(noResultsMessage)
};


// 초기 상태에서 모든 problems를 가져와서 표시
async function getInitialProblems() {
  try {
    const studyId = probSearchInput.dataset.studyId;
    const response = await axios.get(`/studies/${studyId}/mainboard/problem/search`)
    const results = response.data.problems
    displayResults(results)
  } catch (error) {
    console.error(error)
  }
}


probSearchInput.addEventListener('input', async (event) => {
  const query = probSearchInput.value.trim()
  const studyId = event.target.dataset.studyId

  if (query) {
    try {
      const response = await axios.get(`/studies/${studyId}/mainboard/problem/search`, {
        params: {
          query: query
        }
      })

      const results = response.data.problems  // 검색결과
      displayResults(results)


    } catch (error) {
      console.error(error)
    }
  } else {
    // 입력이 없는 경우 초기 상태로 복원
    getInitialProblems()
  }
})

// 초기 상태에서 모든 problems를 가져와서 표시
getInitialProblems()