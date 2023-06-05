
const languageButtons = document.querySelectorAll('.language-btn');
const languageContainer = document.querySelector('.language__container')
const studiesContainer = document.querySelector('.cardlist__container')
const selectedLanguagesContainer = document.querySelector('.selected_languages__container');

languageButtons.forEach((button) => {
  button.addEventListener('click', async (e) => {
    button.classList.toggle('selected-btn');
    const selectedLangs = languageContainer.querySelectorAll('.selected-btn')
    const langs = Array.from(selectedLangs).map((v) => v.dataset.lang).join(',')

    try {
      const response = await fetch(`/studies/?lang=${langs}`);
      console.log(response);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const html = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const studies = doc.querySelector('.cardlist__container');
      studiesContainer.innerHTML = studies.innerHTML;
    } catch (error) {
      console.log(error);
    }
  });
});

selectedLanguagesContainer.addEventListener('click', async (e) => {
  const selectedLangs = languageContainer.querySelectorAll('.selected-btn')
  const langs = Array.from(selectedLangs).map((v) => v.dataset.lang).join(',')
  console.log(langs)

  try {
    const response = await fetch(`/studies/?lang=${langs}`);
    console.log(response);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const html = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const studies = doc.querySelector('.cardlist__container');
    studiesContainer.innerHTML = studies.innerHTML;
  } catch (error) {
    console.log(error);
  }
});
